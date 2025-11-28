from django.db import models
from django.contrib.auth.models import AbstractUser

# Usuário customizado
class User(AbstractUser):
    pontos = models.IntegerField(default=0)

# Pontos de coleta
class DropOffPoint(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.nome

# Recompensas
class Reward(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    points_required = models.PositiveIntegerField()
    image = models.ImageField(upload_to="rewards/", blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.points_required} pontos)"

# Tipos de materiais e pontos
MATERIAL_CHOICES = [
    ("papel", "Papel/Papelão"),
    ("plastico", "Plástico"),
    ("vidro", "Vidro"),
    ("metal", "Metal"),
    ("eletronico", "Eletrônicos"),
    ("organico", "Orgânico"),
]

MATERIAL_POINTS = {
    "papel": 10,
    "plastico": 15,
    "vidro": 8,
    "metal": 12,
    "eletronico": 25,
    "organico": 5,
}

# Submissão de materiais recicláveis
class Submission(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("approved", "Aprovado"),
        ("rejected", "Rejeitado"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="submissions/")
    description = models.TextField(blank=True)
    material_type = models.CharField(
        max_length=20, choices=MATERIAL_CHOICES, default="papel"
    )
    quantity = models.DecimalField(max_digits=6, decimal_places=2)  # em kg
    points = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_points(self):
        """Calcula os pontos com base na quantidade e no tipo de material."""
        return int(self.quantity * MATERIAL_POINTS.get(self.material_type, 0))

    def save(self, *args, **kwargs):
        """Calcula pontos automaticamente ao salvar."""
        self.points = self.calculate_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.material_type} ({self.quantity} kg)"
