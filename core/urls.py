from django.urls import path
from . import views

urlpatterns = [
    # --- ÁREA PÚBLICA ---
    path('', views.landing_page, name='landing'),

    # --- DASHBOARDS ---
    # Home Pessoal (Agenda, Meus Casos, Clima)
    path('app/', views.home, name='home'),
    # Visão Gerencial (Gráficos, KPIs do Escritório)
    path('app/visao-geral/', views.visao_geral, name='visao_geral'),

    # --- PROCESSOS (CRUD Completo) ---
    # Nota: Todas apontam para 'view_processos', que decide o que fazer baseada na URL
    path('app/processos/', views.view_processos, name='processos_list'),
    path('app/processos/novo/', views.view_processos, name='processo_create'),
    path('app/processos/<int:pk>/editar/', views.view_processos, name='processo_update'),
    path('app/processos/<int:pk>/deletar/', views.view_processos, name='processo_delete'),

    # --- CLIENTES (CRUD Completo) ---
    path('app/clientes/', views.view_clientes, name='clientes_list'),
    path('app/clientes/novo/', views.view_clientes, name='cliente_create'),
    path('app/clientes/<int:pk>/editar/', views.view_clientes, name='cliente_update'),
    path('app/clientes/<int:pk>/deletar/', views.view_clientes, name='cliente_delete'),

    # --- AGENDA E PRAZOS (CRUD Completo) ---
    path('app/agenda/', views.view_agenda, name='agenda'),
    path('app/agenda/novo/', views.view_agenda, name='evento_create'),
    path('app/agenda/<int:pk>/editar/', views.view_agenda, name='evento_update'),
    path('app/agenda/<int:pk>/deletar/', views.view_agenda, name='evento_delete'),

    # --- DOCUMENTOS (CRUD Completo) ---
    path('app/documentos/', views.view_documentos, name='docs_list'),
    path('app/documentos/novo/', views.view_documentos, name='doc_create'),
    path('app/documentos/<int:pk>/deletar/', views.view_documentos, name='doc_delete'),

    # --- CADASTROS AUXILIARES (Configurações Jurídicas) ---
    
    # Juízes
    path('app/juizes/', views.view_juizes, name='juizes_list'),
    path('app/juizes/novo/', views.view_juizes, name='juiz_create'),
    path('app/juizes/<int:pk>/editar/', views.view_juizes, name='juiz_update'),
    path('app/juizes/<int:pk>/deletar/', views.view_juizes, name='juiz_delete'),

    # Varas / Fóruns
    path('app/varas/', views.view_varas, name='varas_list'),
    path('app/varas/novo/', views.view_varas, name='vara_create'),
    path('app/varas/<int:pk>/editar/', views.view_varas, name='vara_update'),
    path('app/varas/<int:pk>/deletar/', views.view_varas, name='vara_delete'),

    # Promotores
    path('app/promotores/', views.view_promotores, name='promotores_list'),
    path('app/promotores/novo/', views.view_promotores, name='promotor_create'),
    path('app/promotores/<int:pk>/editar/', views.view_promotores, name='promotor_update'),
    path('app/promotores/<int:pk>/deletar/', views.view_promotores, name='promotor_delete'),

    # Advogados / Equipe (Placeholder ou Implementação Futura)
    path('app/equipe/', views.view_advogados, name='advogados_list'),
]