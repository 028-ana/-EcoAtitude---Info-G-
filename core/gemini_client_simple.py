import os
import random
from django.conf import settings

class SimpleGeminiClient:
    """Cliente simplificado para desenvolvimento sem API real"""
    
    def validate_submission_image(self, image_path, description=""):
        """Simulação de validação para desenvolvimento"""
        
        # Lista de palavras-chave que indicam ações sustentáveis
        sustainable_keywords = [
            'reciclagem', 'reciclar', 'lixo', 'resíduos', 'descarte', 
            'compostagem', 'compostar', 'orgânico', 'horta', 'plantio',
            'limpeza', 'coleta', 'meio ambiente', 'sustentável', 'ecológico',
            'reutilizar', 'reuso', 'upcycling', 'energia solar', 'hortaliças'
        ]
        
        # Verifica se a descrição contém palavras-chave sustentáveis
        description_lower = description.lower()
        has_sustainable_keyword = any(keyword in description_lower for keyword in sustainable_keywords)
        
        # Simula análise baseada na descrição (80% de aprovação se tiver palavras-chave)
        if has_sustainable_keyword:
            is_approved = random.random() < 0.8  # 80% de chance de aprovação
            if is_approved:
                points = random.randint(40, 100)
                return True, f"Simulação: Ação sustentável detectada! +{points} pontos"
            else:
                return False, "Simulação: Imagem não atende aos critérios de sustentabilidade"
        else:
            # Sem palavras-chave, 20% de chance de aprovação
            is_approved = random.random() < 0.2
            if is_approved:
                points = random.randint(20, 50)
                return True, f"Simulação: Ação básica validada! +{points} pontos"
            else:
                return False, "Simulação: Descrição muito genérica ou não relacionada à sustentabilidade"