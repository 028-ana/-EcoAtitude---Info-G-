import os
import requests
import base64
from django.conf import settings

class GeminiClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
    
    def validate_submission_image(self, image_path, description=""):
        """Valida se a imagem mostra uma ação sustentável"""
        try:
            # Modo de desenvolvimento - simula validação se não houver API key
            if not self.api_key or self.api_key == "sua_chave_gemini_aqui":
                print("Modo de desenvolvimento: Simulando validação Gemini")
                return True, "Imagem validada (modo desenvolvimento - API key não configurada)"
            
            # Lê a imagem e converte para base64
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepara o payload para a API Gemini
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"""
                                Analise esta imagem e determine se ela mostra uma ação sustentável genuína.

                                TIPOS DE AÇÕES VÁLIDAS:
                                - Reciclagem: separação de materiais, uso de lixeiras coloridas, descarte em locais adequados
                                - Compostagem: resíduos orgânicos, composteiras, hortas
                                - Limpeza ambiental: coleta de lixo em praias, parques, ruas
                                - Descarte correto: pilhas, eletrônicos, óleo, medicamentos
                                - Reutilização: uso criativo de materiais, upcycling

                                DESCRIÇÃO FORNECIDA: "{description}"

                                CRITÉRIOS DE VALIDAÇÃO:
                                1. A imagem deve mostrar uma ação real de sustentabilidade
                                2. Não pode ser uma imagem genérica ou de stock
                                3. Deve corresponder à descrição fornecida
                                4. Não pode conter conteúdo inadequado ou ofensivo

                                Responda APENAS com uma das seguintes opções:
                                - APPROVED: se a imagem for válida
                                - REJECTED: se a imagem for inválida
                                - UNCERTAIN: se não for possível determinar com certeza

                                Justifique brevemente sua decisão após a palavra chave.
                                """
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 100,
                }
            }
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Faz a requisição para a API
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Extrai a resposta
            if 'candidates' in result and result['candidates']:
                text_response = result['candidates'][0]['content']['parts'][0]['text']
                print(f"Resposta Gemini: {text_response}")
                
                if 'APPROVED' in text_response:
                    return True, text_response
                elif 'REJECTED' in text_response:
                    return False, text_response
                else:
                    return False, "Resposta não determinística da API"
            else:
                return False, "Nenhuma resposta válida da API Gemini"
                
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição Gemini: {e}")
            return False, f"Erro de conexão com a API: {str(e)}"
        except Exception as e:
            print(f"Erro inesperado no Gemini Client: {e}")
            return False, f"Erro inesperado: {str(e)}"