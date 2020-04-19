from django.contrib import admin
from medico.models import *

class lista_medicos(admin.ModelAdmin):
    list_display = ('id', 'nome', 'crm', 'email', 'foto')
    list_display_links = ('id', 'nome', 'crm') 
 
admin.site.register(Medico, lista_medicos)