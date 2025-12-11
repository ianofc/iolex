# core/models.py
from django.db import models
from accounts.models import Escritorio, Usuario

class Vara(models.Model):
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200) # Ex: 1ª Vara Cível
    comarca = models.CharField(max_length=200) # Ex: São Paulo - Capital
    
    def __str__(self): return f"{self.nome} - {self.comarca}"

class Juiz(models.Model):
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    titular = models.BooleanField(default=True)
    
    def __str__(self): return self.nome

class Promotor(models.Model):
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    
    def __str__(self): return self.nome

class Cliente(models.Model):
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='clientes')
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self): return self.nome

class Processo(models.Model):
    STATUS_CHOICES = (('ATIVO', 'Ativo'), ('SUSPENSO', 'Suspenso'), ('ARQUIVADO', 'Arquivado'), ('FINALIZADO', 'Finalizado'))
    
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='processos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='processos')
    advogado_responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Novos relacionamentos
    vara = models.ForeignKey(Vara, on_delete=models.SET_NULL, null=True, blank=True)
    juiz = models.ForeignKey(Juiz, on_delete=models.SET_NULL, null=True, blank=True)
    
    numero = models.CharField("Número do Processo", max_length=50, unique=True)
    titulo = models.CharField("Título/Ação", max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    data_abertura = models.DateField(blank=True, null=True)
    valor_causa = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self): return f"{self.numero} - {self.titulo}"

class Documento(models.Model):
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE)
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='documentos')
    titulo = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to='documentos/%Y/%m/')
    data_upload = models.DateTimeField(auto_now_add=True)

class EventoAgenda(models.Model):
    TIPO_CHOICES = (('AUDIENCIA', 'Audiência'), ('PRAZO', 'Prazo Fatal'), ('REUNIAO', 'Reunião'), ('OUTRO', 'Outro'))
    
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField(blank=True, null=True)
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, null=True, blank=True)
    responsavel = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    concluido = models.BooleanField(default=False)