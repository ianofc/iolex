from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta

# Import Models
from accounts.models import Usuario, Escritorio
from .models import (
    Processo, Cliente, Vara, Juiz, Promotor, Documento, EventoAgenda
)
# Import Forms
from .forms import (
    ProcessoForm, ClienteForm, VaraForm, JuizForm, PromotorForm, 
    DocumentoForm, AgendaForm
)

# --- DASHBOARDS & HOME ---

def landing_page(request):
    """Site Institucional (Público)"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'core/public/landing.html')

@login_required
def home(request):
    """Home Pessoal do Advogado (Painel Diário)"""
    escritorio = getattr(request.user, 'escritorio', None)
    
    # SEU ERRO ESTAVA AQUI: Agora aponta para o caminho padronizado na pasta 'app'
    if not escritorio: 
        return render(request, 'core/app/sem_acesso.html')

    # Dados para os Widgets Pessoais
    prazos_hoje = EventoAgenda.objects.filter(
        escritorio=escritorio,
        responsavel=request.user,
        data_inicio__date=timezone.now().date(),
        concluido=False
    ).count()

    # Meus Processos Recentes
    meus_processos = Processo.objects.filter(escritorio=escritorio)
    if hasattr(Processo, 'advogado_responsavel'):
        meus_processos = meus_processos.filter(advogado_responsavel=request.user)
    
    context = {
        'prazos_hoje': prazos_hoje,
        'processos': meus_processos.order_by('-ultima_atualizacao')[:6],
        'novos_clientes': Cliente.objects.filter(escritorio=escritorio, criado_em__gte=timezone.now()-timedelta(days=30)).count(),
        'lembretes': []
    }
    return render(request, 'core/app/home.html', context)

@login_required
def visao_geral(request):
    """Dashboard Gerencial (Visão Macro)"""
    escritorio = getattr(request.user, 'escritorio', None)
    if not escritorio: return redirect('home')

    context = {
        'total_processos': Processo.objects.filter(escritorio=escritorio).count(),
        'processos_ativos': Processo.objects.filter(escritorio=escritorio, status='ATIVO').count(),
        'total_clientes': Cliente.objects.filter(escritorio=escritorio).count(),
        'processos_recentes': Processo.objects.filter(escritorio=escritorio).order_by('-ultima_atualizacao')[:10]
    }
    return render(request, 'core/app/visao_geral.html', context)

# --- SISTEMA DE CRUD GENÉRICO (Inteligente) ---

def crud_view(request, model_class, form_class, template_list, template_form, redirect_list):
    """
    Controlador Mestre: Gerencia Listar, Criar, Editar e Deletar para qualquer model.
    """
    escritorio = request.user.escritorio
    pk = request.resolver_match.kwargs.get('pk')
    
    # 1. DELETE
    if 'deletar' in request.path and pk:
        obj = get_object_or_404(model_class, pk=pk, escritorio=escritorio)
        if request.method == 'POST':
            obj.delete()
            messages.success(request, 'Registro removido.')
            return redirect(redirect_list)
        return redirect(redirect_list)

    # 2. CREATE / UPDATE
    if 'novo' in request.path or 'editar' in request.path:
        obj = get_object_or_404(model_class, pk=pk, escritorio=escritorio) if pk else None
        
        if request.method == 'POST':
            try:
                form = form_class(request.POST, request.FILES, instance=obj, escritorio=escritorio)
            except TypeError:
                form = form_class(request.POST, request.FILES, instance=obj)

            if form.is_valid():
                item = form.save(commit=False)
                item.escritorio = escritorio
                item.save()
                messages.success(request, 'Salvo com sucesso!')
                return redirect(redirect_list)
        else:
            try:
                form = form_class(instance=obj, escritorio=escritorio)
            except TypeError:
                form = form_class(instance=obj)

        return render(request, template_form, {'form': form, 'titulo': 'Editar' if obj else 'Novo'})

    # 3. LIST (Padrão)
    items = model_class.objects.filter(escritorio=escritorio)
    q = request.GET.get('q')
    if q:
        if hasattr(model_class, 'nome'): items = items.filter(nome__icontains=q)
        elif hasattr(model_class, 'titulo'): items = items.filter(titulo__icontains=q)
    
    return render(request, template_list, {'items': items})

# --- VIEWS ESPECÍFICAS ---

@login_required
def view_processos(request, pk=None):
    if 'novo' in request.path or 'editar' in request.path or 'deletar' in request.path:
        return crud_view(
            request, Processo, ProcessoForm, 
            'core/app/processos_list.html', 
            'core/app/add/add_process.html', # Template customizado
            'processos_list'
        )
    
    # Listagem Customizada
    escritorio = request.user.escritorio
    processos = Processo.objects.filter(escritorio=escritorio).select_related('cliente').order_by('-ultima_atualizacao')
    q = request.GET.get('q')
    if q:
        processos = processos.filter(Q(titulo__icontains=q) | Q(numero__icontains=q))
        
    return render(request, 'core/app/processos_list.html', {'processos': processos})

@login_required
def view_clientes(request, pk=None):
    return crud_view(
        request, Cliente, ClienteForm, 
        'core/app/clientes_list.html', 
        'core/app/add/add_clientes.html', # Template customizado
        'clientes_list'
    )

@login_required
def view_agenda(request, pk=None):
    # Se ainda não criou agenda_list.html, usa o genérico ou cria um simples
    return crud_view(request, EventoAgenda, AgendaForm, 'core/app/agenda_list.html', 'core/app/add/form_generico.html', 'agenda')

@login_required
def view_documentos(request, pk=None):
    return crud_view(request, Documento, DocumentoForm, 'core/app/docs_list.html', 'core/app/add/form_generico.html', 'docs_list')

# --- CADASTROS AUXILIARES (Usam form_generico.html) ---

@login_required
def view_juizes(request, pk=None):
    return crud_view(request, Juiz, JuizForm, 'core/app/auxiliar_list.html', 'core/app/add/form_generico.html', 'juizes_list')

@login_required
def view_varas(request, pk=None):
    return crud_view(request, Vara, VaraForm, 'core/app/auxiliar_list.html', 'core/app/add/form_generico.html', 'varas_list')

@login_required
def view_promotores(request, pk=None):
    return crud_view(request, Promotor, PromotorForm, 'core/app/auxiliar_list.html', 'core/app/add/form_generico.html', 'promotores_list')

@login_required
def view_advogados(request, pk=None):
    # Listagem de usuários do escritório
    escritorio = request.user.escritorio
    usuarios = Usuario.objects.filter(escritorio=escritorio)
    return render(request, 'core/app/advogados_list.html', {'usuarios': usuarios})