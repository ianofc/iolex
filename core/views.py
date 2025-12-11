from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Processo, Cliente

def landing_page(request):
    """
    Site Institucional (Público).
    Caminho: templates/core/public/landing.html
    """
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/public/landing.html')

@login_required
def home(request):
    """
    Painel Pessoal do Advogado (Home).
    Caminho: templates/core/app/home.html
    """
    escritorio = getattr(request.user, 'escritorio', None)
    
    context = {
        'prazos_hoje': 0,
        'novos_clientes': 0,
        'processos': [],
        'lembretes': [],
    }

    if escritorio:
        # Prazos (Simulação - futuramente filtrar por data)
        context['prazos_hoje'] = 0 
        
        # Novos Clientes (Últimos 30 dias)
        data_inicio_mes = timezone.now() - timedelta(days=30)
        context['novos_clientes'] = Cliente.objects.filter(
            escritorio=escritorio, 
            criado_em__gte=data_inicio_mes
        ).count()

        # Meus Processos Recentes (Top 6 para os cards)
        context['processos'] = Processo.objects.filter(
            escritorio=escritorio
        ).select_related('cliente').order_by('-ultima_atualizacao')[:6]

    return render(request, 'core/app/home.html', context)

@login_required
def visao_geral(request):
    """
    Dashboard Gerencial do Escritório.
    Caminho: templates/core/app/visao_geral.html
    """
    escritorio = getattr(request.user, 'escritorio', None)
    
    context = {
        'total_processos': 0,
        'processos_ativos': 0,
        'novos_clientes': 0,
        'processos_recentes': [],
    }

    if escritorio:
        context['total_processos'] = Processo.objects.filter(escritorio=escritorio).count()
        context['processos_ativos'] = Processo.objects.filter(escritorio=escritorio, status='ATIVO').count()
        
        data_inicio_mes = timezone.now() - timedelta(days=30)
        context['novos_clientes'] = Cliente.objects.filter(
            escritorio=escritorio, 
            criado_em__gte=data_inicio_mes
        ).count()

        context['processos_recentes'] = Processo.objects.filter(
            escritorio=escritorio
        ).select_related('cliente').order_by('-ultima_atualizacao')[:10]

    return render(request, 'core/app/visao_geral.html', context)

# --- Placeholders ---

@login_required
def listar_processos(request):
    return render(request, 'core/app/em_breve.html', {'titulo': 'Gestão de Processos'})

@login_required
def listar_clientes(request):
    return render(request, 'core/app/em_breve.html', {'titulo': 'Carteira de Clientes'})

@login_required
def agenda(request):
    return render(request, 'core/app/em_breve.html', {'titulo': 'Agenda e Prazos'})