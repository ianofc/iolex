from django.urls import path
from . import views

urlpatterns = [
    # Site Público
    path('', views.landing_page, name='landing'),
    
    # Sistema Interno (Pós-login)
    path('app/', views.home, name='home'),               # A nova Home Pessoal (estilo Cortex)
    path('app/visao-geral/', views.visao_geral, name='visao_geral'), # A antiga Dashboard
    
    # Placeholders
    path('app/processos/', views.listar_processos, name='processos_list'),
    path('app/clientes/', views.listar_clientes, name='clientes_list'),
    path('app/agenda/', views.agenda, name='agenda'),
]