# recompensas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Recompensa, Resgate
from .utils import gerar_pdf_resgate

@login_required
def listar_recompensas(request):
    recompensas = Recompensa.objects.filter(ativo=True, quantidade_disponivel__gt=0)
    return render(request, 'recompensas/listar.html', {'recompensas': recompensas})

@login_required
def resgatar_recompensa(request, recompensa_id):
    recompensa = get_object_or_404(Recompensa, id=recompensa_id, ativo=True)
    
    if request.user.pontos < recompensa.pontos_necessarios:
        messages.error(request, 'Pontos insuficientes para resgatar esta recompensa.')
        return redirect('listar_recompensas')
    
    if recompensa.quantidade_disponivel <= 0:
        messages.error(request, 'Esta recompensa está esgotada.')
        return redirect('listar_recompensas')
    
    # Criar resgate
    resgate = Resgate.objects.create(
        usuario=request.user,
        recompensa=recompensa
    )
    
    # Deduzir pontos
    request.user.usar_pontos(recompensa.pontos_necessarios)
    
    # Atualizar quantidade disponível
    recompensa.quantidade_disponivel -= 1
    recompensa.save()
    
    messages.success(request, f'Recompensa "{recompensa.nome}" resgatada com sucesso!')
    return redirect('listar_recompensas')

@login_required
def gerar_pdf_resgate(request, resgate_id):
    resgate = get_object_or_404(Resgate, id=resgate_id, usuario=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resgate_{resgate.codigo_resgate}.pdf"'
    
    pdf = gerar_pdf_resgate(resgate)
    response.write(pdf)
    return response