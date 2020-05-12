from django.urls import path
from paciente.views import *

urlpatterns = [
    path('', listar, name='pacientes'),
    path('<int:paciente_id>', detalhe, name='det_paciente'),
    path('alterar/<int:paciente_id>', alterar, name='altera_paciente'),
    path('atualiza_paciente', atualiza_paciente, name='atualiza_paciente'),
    path('adicionar', adicionar, name='adicionar'),
    path('adiciona_paciente', adiciona_paciente, name='adiciona_paciente'),
] 