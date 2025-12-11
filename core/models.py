from django.db import models
# Importamos o modelo de Escritório que criamos no passo anterior
from accounts.models import Escritorio 

class Cliente(models.Model):
    # Vínculo Obrigatório: Este cliente pertence a qual escritório?
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='clientes')
    
    nome = models.CharField(max_length=255)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Processo(models.Model):
    STATUS_CHOICES = (
        ('ATIVO', 'Ativo'),
        ('SUSPENSO', 'Suspenso'),
        ('ARQUIVADO', 'Arquivado'),
        ('FINALIZADO', 'Finalizado'),
    )

    # Vínculo: Processo pertence a um escritório
    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='processos')
    
    # Vínculo: Processo pertence a um Cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='processos')
    
    numero = models.CharField("Número do Processo", max_length=50, unique=True)
    titulo = models.CharField("Título/Ação", max_length=255, help_text="Ex: Ação Trabalhista vs Empresa X")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ATIVO')
    
    data_abertura = models.DateField(blank=True, null=True)
    valor_causa = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.numero} - {self.cliente.nome}"