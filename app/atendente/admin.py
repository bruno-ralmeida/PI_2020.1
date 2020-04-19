from django.contrib import admin
from atendente.models import *

class lista_atendente(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'foto')
    list_display_links = ('id', 'nome')

admin.site.register(Atendente,lista_atendente)