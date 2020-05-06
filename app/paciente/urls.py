from django.urls import path
from paciente.views import *

urlpatterns = [
    path('', listar, name='pacientes'),
    path('paciente/<int:paciente_id>', detalhe, name='det_paciente'),
    path('paciente/alterar/<int:paciente_id>', alterar, name='altera_paciente'),
    path('paciente/atualiza_paciente', atualiza_paciente, name='atualiza_paciente'),
    path('paciente/adicionar', adicionar, name='adicionar'),
    path('paciente/adiciona_paciente', adiciona_paciente, name='adiciona_paciente'),
] 