# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 1. Landing Page (Pública)
    path('', views.landing_page, name='landing'),
    
    # 2. Painel Pessoal (Home do Advogado) - Onde o login redireciona
    path('app/', views.home, name='home'),
    
    # 3. Painel Gerencial (Visão Geral do Escritório)
    path('app/visao-geral/', views.visao_geral, name='visao_geral'),
    
    # 4. Funcionalidades (Placeholders)
    path('app/processos/', views.listar_processos, name='processos_list'),
    path('app/clientes/', views.listar_clientes, name='clientes_list'),
    path('app/agenda/', views.agenda, name='agenda'),
]