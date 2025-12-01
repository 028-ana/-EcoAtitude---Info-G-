# coletas/views_admin.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Coleta

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_coletas_pendentes(request):
    coletas = Coleta.objects.filter(status='pendente').order_by('data_solicitacao')
    return render(request, 'admin/coletas_pendentes.html', {'coletas': coletas})

@user_passes_test(is_admin)
def admin_aprovar_coleta(request, coleta_id):
    coleta = get_object_or_404(Coleta, id=coleta_id)
    coleta.aprovar()
    messages.success(request, f'Coleta #{coleta.id} aprovada! {coleta.pontos_ganhos} pontos concedidos.')
    return redirect('admin_coletas_pendentes')

@user_passes_test(is_admin)
def admin_rejeitar_coleta(request, coleta_id):
    coleta = get_object_or_404(Coleta, id=coleta_id)
    coleta.status = 'rejeitado'
    coleta.save()
    messages.success(request, f'Coleta #{coleta.id} rejeitada.')
    return redirect('admin_coletas_pendentes')