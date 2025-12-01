# recompensas/models.py
from django.db import models
from usuarios.models import Usuario

class Recompensa(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    pontos_necessarios = models.IntegerField()
    quantidade_disponivel = models.IntegerField()
    ativo = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='recompensas/', blank=True, null=True)
    
    def __str__(self):
        return self.nome

class Resgate(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    recompensa = models.ForeignKey(Recompensa, on_delete=models.CASCADE)
    data_resgate = models.DateTimeField(auto_now_add=True)
    codigo_resgate = models.CharField(max_length=20, unique=True)
    utilizado = models.BooleanField(default=False)
    
    def gerar_codigo(self):
        import uuid
        return str(uuid.uuid4())[:8].upper()
    
    def save(self, *args, **kwargs):
        if not self.codigo_resgate:
            self.codigo_resgate = self.gerar_codigo()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Resgate {self.codigo_resgate} - {self.usuario.username}"