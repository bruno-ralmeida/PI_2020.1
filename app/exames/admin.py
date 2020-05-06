"""
@author Bruno Almeida
"""
from django.contrib import admin
from exames.models import Exame_Referencia, Exame_Resultado

class ListaExamesResult(admin.ModelAdmin):
    """Lista de exibição Django"""
    list_display = ('paciente', 'data_exame', 'glicose', 'ldl', 'hdl', 'triglicerides',
                    'colesterol')
    list_display_links = ('data_exame', 'paciente')

class ListaExamesRef(admin.ModelAdmin):
    """Lista de exibição Django"""
    list_display = ('id', 'glicose_min', 'glicose_max', 'ldl_min', 'ldl_max', 'hdl_min',
                    'hdl_max', 'triglicerides_min', 'triglicerides_max', 'colesterol_min',
                    'colesterol_max', 'vldl_min', 'vldl_max', 'idade_min', 'idade_max')

admin.site.register(Exame_Resultado, ListaExamesResult)

admin.site.register(Exame_Referencia, ListaExamesRef)
