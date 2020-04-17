from django.contrib import admin
from paciente.models import *


class lista_pacientes(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sexo', 'data_nascimento', 'cpf', 'rg', 'carteira_convenio', 'peso', 'altura')
    list_display_links = ('id', 'nome') 
    
admin.site.register(Paciente, lista_pacientes)