from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Processo, Cliente

def landing_page(request):
    """
    Página inicial do site (Público).
    Se o usuário já estiver logado, redireciona para o sistema (app).
    """
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/landing.html')

@login_required
def home(request):
    """
    Home do Sistema / Painel Pessoal (Antiga 'index' do Cortex).
    Focada no dia a dia do advogado: Agenda, Clima, Meus Casos Recentes.
    """
    # Garante que o usuário tem um escritório vinculado para evitar erros
    escritorio = getattr(request.user, 'escritorio', None)
    
    # Contexto padrão
    context = {
        'prazos_hoje': 0,
        'novos_clientes': 0,
        'processos': [],
        'lembretes': [], # Placeholder para futuro sistema de lembretes
    }

    if escritorio:
        # 1. Estatísticas Rápidas (Para os Widgets)
        # (Futuramente você pode criar um Model 'Prazo' para filtrar por data=hoje)
        context['prazos_hoje'] = 0 
        
        data_inicio_mes = timezone.now() - timedelta(days=30)
        context['novos_clientes'] = Cliente.objects.filter(
            escritorio=escritorio, 
            criado_em__gte=data_inicio_mes
        ).count()

        # 2. "Meus Casos Recentes" (Limitado a 6 para os cards grandes)
        # Idealmente filtraríamos por 'responsavel=request.user', mas por enquanto pegamos do escritório
        context['processos'] = Processo.objects.filter(
            escritorio=escritorio
        ).select_related('cliente').order_by('-ultima_atualizacao')[:6]

    return render(request, 'core/home.html', context)

@login_required
def visao_geral(request):
    """
    Dashboard Gerencial (Antiga 'dashboard.html').
    Visão macro do escritório: Todos os números e tabela completa recente.
    """
    escritorio = getattr(request.user, 'escritorio', None)
    
    context = {
        'total_processos': 0,
        'processos_ativos': 0,
        'novos_clientes': 0,
        'prazos_hoje': 0,
        'processos_recentes': [],
    }

    if escritorio:
        # Estatísticas Gerais
        context['total_processos'] = Processo.objects.filter(escritorio=escritorio).count()
        context['processos_ativos'] = Processo.objects.filter(escritorio=escritorio, status='ATIVO').count()
        
        # Novos Clientes (30 dias)
        data_inicio_mes = timezone.now() - timedelta(days=30)
        context['novos_clientes'] = Cliente.objects.filter(
            escritorio=escritorio, 
            criado_em__gte=data_inicio_mes
        ).count()

        # Tabela de Movimentações (Limitada a 10 para não poluir)
        context['processos_recentes'] = Processo.objects.filter(
            escritorio=escritorio
        ).select_related('cliente').order_by('-ultima_atualizacao')[:10]

    return render(request, 'core/visao_geral.html', context)

# --- Placeholders para Funcionalidades Futuras ---
# Isso evita o erro de "NoReverseMatch" nos links do menu

@login_required
def listar_processos(request):
    # Futuro: Lista completa com filtros, busca avançada e paginação
    return render(request, 'core/em_breve.html', {'titulo': 'Gestão de Processos'})

@login_required
def listar_clientes(request):
    # Futuro: CRM completo
    return render(request, 'core/em_breve.html', {'titulo': 'Carteira de Clientes'})

@login_required
def agenda(request):
    # Futuro: Calendário interativo (FullCalendar)
    return render(request, 'core/em_breve.html', {'titulo': 'Agenda e Prazos'})