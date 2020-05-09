from django.contrib import admin
from consulta.models import Consulta

class lista_consulta(admin.ModelAdmin):
    list_display = ('id','data', 'hora', 'medico', 'atendente', 'paciente')
    list_display_links = ('medico', 'atendente', 'paciente')    

admin.site.register(Consulta, lista_consulta)