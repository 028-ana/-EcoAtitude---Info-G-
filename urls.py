# recompensas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_recompensas, name='listar_recompensas'),
    path('resgatar/<int:recompensa_id>/', views.resgatar_recompensa, name='resgatar_recompensa'),
    path('pdf/<int:resgate_id>/', views.gerar_pdf_resgate, name='gerar_pdf_resgate'),
]