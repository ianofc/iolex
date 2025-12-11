from django import forms
from .models import Processo, Cliente, Vara, Juiz, Promotor, Documento, EventoAgenda
from accounts.models import Usuario

# --- Estilos CSS (Tailwind Glass Aurora) ---
STYLE_INPUT = (
    "w-full pl-4 pr-4 py-3 bg-white/50 dark:bg-slate-800/50 border border-gray-200 "
    "dark:border-gray-700 rounded-xl text-sm focus:ring-2 focus:ring-brand-purple "
    "focus:border-transparent dark:text-white transition-all shadow-sm"
)
STYLE_SELECT = (
    "w-full pl-4 pr-10 py-3 bg-white/50 dark:bg-slate-800/50 border border-gray-200 "
    "dark:border-gray-700 rounded-xl text-sm focus:ring-2 focus:ring-brand-purple "
    "focus:border-transparent dark:text-white transition-all shadow-sm appearance-none"
)
STYLE_TEXTAREA = (
    "w-full p-4 bg-white/50 dark:bg-slate-800/50 border border-gray-200 "
    "dark:border-gray-700 rounded-xl text-sm focus:ring-2 focus:ring-brand-purple "
    "focus:border-transparent dark:text-white transition-all shadow-sm resize-none"
)

# --- Classe Base (DRY Principle) ---
class BaseForm(forms.ModelForm):
    """
    Classe pai para todos os forms. 
    1. Recebe 'escritorio' no __init__.
    2. Aplica estilos CSS automaticamente em todos os campos.
    """
    def __init__(self, *args, **kwargs):
        self.escritorio = kwargs.pop('escritorio', None)
        super(BaseForm, self).__init__(*args, **kwargs)
        
        # Aplica estilos automaticamente baseado no tipo do widget
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Textarea)):
                field.widget.attrs['class'] = STYLE_TEXTAREA
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = STYLE_SELECT
            else:
                field.widget.attrs['class'] = STYLE_INPUT

# --- Formulários Principais ---

class ProcessoForm(BaseForm):
    class Meta:
        model = Processo
        # Excluímos campos automáticos ou de controle interno
        exclude = ['escritorio', 'ultima_atualizacao']
        widgets = {
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'titulo': forms.TextInput(attrs={'placeholder': 'Ex: Ação Trabalhista vs Empresa X'}),
            'numero': forms.TextInput(attrs={'placeholder': '0000000-00.0000.0.00.0000'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se um escritório foi passado, filtra TODOS os relacionamentos para segurança
        if self.escritorio:
            self.fields['cliente'].queryset = Cliente.objects.filter(escritorio=self.escritorio)
            self.fields['vara'].queryset = Vara.objects.filter(escritorio=self.escritorio)
            self.fields['juiz'].queryset = Juiz.objects.filter(escritorio=self.escritorio)
            self.fields['advogado_responsavel'].queryset = Usuario.objects.filter(escritorio=self.escritorio)

class ClienteForm(BaseForm):
    class Meta:
        model = Cliente
        exclude = ['escritorio', 'criado_em']
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo ou Razão Social'}),
            'cpf_cnpj': forms.TextInput(attrs={'placeholder': 'Apenas números'}),
        }

class AgendaForm(BaseForm):
    class Meta: 
        model = EventoAgenda
        exclude = ['escritorio', 'concluido']
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.escritorio:
            self.fields['processo'].queryset = Processo.objects.filter(escritorio=self.escritorio)
            self.fields['responsavel'].queryset = Usuario.objects.filter(escritorio=self.escritorio)

class DocumentoForm(BaseForm):
    class Meta: 
        model = Documento
        exclude = ['escritorio', 'data_upload']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.escritorio:
            self.fields['processo'].queryset = Processo.objects.filter(escritorio=self.escritorio)

# --- Formulários Auxiliares (Cadastros Simples) ---

class VaraForm(BaseForm):
    class Meta: 
        model = Vara
        exclude = ['escritorio']

class JuizForm(BaseForm):
    class Meta: 
        model = Juiz
        exclude = ['escritorio']

class PromotorForm(BaseForm):
    class Meta: 
        model = Promotor
        exclude = ['escritorio']