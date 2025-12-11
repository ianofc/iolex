# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Escritorio(models.Model):
    nome = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Cargo(models.Model):
    """
    Representa o 'Role' do usuário (Ex: Advogado, Juiz, Cliente, Promotor).
    Isso permite usar user.role.name no template.
    """
    name = models.CharField("Nome do Cargo", max_length=50, unique=True) # Ex: 'admin', 'advogado', 'juiz'
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Usuario(AbstractUser):
    GENEROS = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
        ('Outro', 'Outro'),
    )

    escritorio = models.ForeignKey(Escritorio, on_delete=models.CASCADE, related_name='usuarios', null=True, blank=True)
    
    # Novo campo para suportar a lógica de cores (isFeminino)
    genero = models.CharField("Gênero", max_length=20, choices=GENEROS, default='Masculino')
    
    # Substituindo o antigo 'tipo' por uma ForeignKey para Cargo (Role)
    role = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    oab = models.CharField("Número da OAB", max_length=20, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True) # Adicionei suporte a foto

    def __str__(self):
        cargo_nome = self.role.name if self.role else "Sem Cargo"
        return f"{self.username} - {cargo_nome}"