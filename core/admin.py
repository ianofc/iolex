from django.contrib import admin
from .models import Cliente, Processo

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'escritorio')
    search_fields = ('nome', 'cpf_cnpj')
    list_filter = ('escritorio',)

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'titulo', 'cliente', 'status', 'escritorio')
    search_fields = ('numero', 'titulo', 'cliente__nome')
    list_filter = ('status', 'escritorio')