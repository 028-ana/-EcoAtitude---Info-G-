@api_view(['POST'])
def create_submission(request):
    serializer = SubmissionCreateSerializer(data=request.data)
    if serializer.is_valid():
        submission = serializer.save(user=request.user)
        
        # Tenta usar o Gemini real, se não funcionar usa o simulador
        try:
            gemini = GeminiClient()
            is_valid, message = gemini.validate_submission_image(
                submission.image.path,
                submission.description or ""
            )
        except Exception as e:
            print(f"Erro no Gemini Client, usando simulador: {e}")
            from .gemini_client_simple import SimpleGeminiClient
            simple_gemini = SimpleGeminiClient()
            is_valid, message = simple_gemini.validate_submission_image(
                submission.image.path,
                submission.description or ""
            )
        
        if is_valid:
            submission.status = 'approved'
            # Atribui pontos de forma inteligente baseado na mensagem
            if "pontos" in message:
                # Extrai pontos da mensagem
                import re
                points_match = re.search(r'\+(\d+)', message)
                if points_match:
                    submission.points_awarded = int(points_match.group(1))
                else:
                    submission.points_awarded = 50
            else:
                submission.points_awarded = 50
            
            # Atualiza pontos do usuário
            request.user.pontos += submission.points_awarded
            request.user.save()
            
            submission.validation_message = message
        else:
            submission.status = 'rejected'
            submission.validation_message = message
        
        submission.save()
        
        response_data = SubmissionSerializer(submission).data
        response_data['validation_message'] = message
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)