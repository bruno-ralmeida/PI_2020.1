from django.urls import path
from paciente.views import *

urlpatterns = [
    path('', listar_paciente, name='pacientes'),
    path('paciente/<int:paciente_id>', detalhe_paciente, name='det_paciente')
] 