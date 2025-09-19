from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pontos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username

class DropOffPoint(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.nome

class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    image = models.ImageField(upload_to="submissions/")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    points_awarded = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%d/%m/%Y')}"

class Reward(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    points_required = models.PositiveIntegerField()
    image = models.ImageField(upload_to="rewards/", blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.points_required} pontos)"
class Submission(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    image = models.ImageField(upload_to="submissions/")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    points_awarded = models.PositiveIntegerField(default=0)
    validation_message = models.TextField(blank=True, null=True)  # NOVO CAMPO

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%d/%m/%Y')}"