import os
import requests
from django.conf import settings

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def validate_submission_image(self, image_path, description=""):
        """Valida se a imagem mostra uma ação sustentável"""
        try:
            # Para desenvolvimento, simula validação
            # Remova este bloco de simulação quando tiver a API key real
            if not self.api_key or self.api_key == "sua_chave_gemini_aqui":
                # Simulação para desenvolvimento
                return True, "Imagem validada (modo simulação)"
            
            # Lê a imagem
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Prepara o prompt
            prompt = f"""
            Analise esta imagem e determine se ela mostra uma ação sustentável como:
            - Reciclagem (separação de lixo, descarte em locais adequados)
            - Compostagem (resíduos orgânicos, composteira)
            - Limpeza de áreas públicas
            - Descarte correto de resíduos
            
            A descrição fornecida é: "{description}"
            
            Responda apenas com 'APPROVED' se for válida ou 'REJECTED' se não for válida.
            """
            
            headers = {'Content-Type': 'application/json'}
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }, {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_data.decode('latin-1')
                        }
                    }]
                }]
            }
            
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            text_response = result['candidates'][0]['content']['parts'][0]['text']
            
            if 'APPROVED' in text_response:
                return True, "Imagem validada com sucesso"
            else:
                return False, "Imagem não corresponde a uma ação sustentável"
                
        except Exception as e:
            return False, f"Erro na validação: {str(e)}"