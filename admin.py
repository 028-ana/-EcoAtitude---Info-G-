# recompensas/admin.py
from django.contrib import admin
from .models import Recompensa, Resgate

@admin.register(Recompensa)
class RecompensaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'pontos_necessarios', 'quantidade_disponivel', 'ativo']
    list_filter = ['ativo']
    search_fields = ['nome']

@admin.register(Resgate)
class ResgateAdmin(admin.ModelAdmin):
    list_display = ['codigo_resgate', 'usuario', 'recompensa', 'data_resgate', 'utilizado']
    list_filter = ['utilizado', 'data_resgate']
    search_fields = ['codigo_resgate', 'usuario__username']