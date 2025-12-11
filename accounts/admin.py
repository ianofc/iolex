# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Escritorio, Cargo

# Registra o Escritório (simples)
admin.site.register(Escritorio)

# Registra o Cargo (simples)
admin.site.register(Cargo)

# Customiza o Usuário para mostrar os campos extras (Escritório, OAB, etc)
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    
    # Adiciona nossos campos personalizados na tela de edição
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Profissionais', {'fields': ('escritorio', 'role', 'oab', 'telefone', 'foto_perfil')}),
    )
    
    # Adiciona campos na tela de criação
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Profissionais', {'fields': ('escritorio', 'role', 'email')}),
    )

    list_display = ['username', 'email', 'escritorio', 'role', 'is_staff']
    search_fields = ['username', 'email', 'escritorio__nome']