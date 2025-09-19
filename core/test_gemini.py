import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoatitude.settings')
django.setup()

from core.gemini_client import GeminiClient

def test_gemini():
    gemini = GeminiClient()
    print(f"API Key: {gemini.api_key}")
    
    # Teste simples - substitua pelo caminho de uma imagem real
    is_valid, message = gemini.validate_submission_image(
        "caminho/para/sua/imagem.jpg",  # Substitua por uma imagem real
        "Descrição de teste para reciclagem"
    )
    
    print(f"Resultado: {is_valid}")
    print(f"Mensagem: {message}")

if __name__ == "__main__":
    test_gemini()