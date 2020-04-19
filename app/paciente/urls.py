from django.urls import path
from paciente.views import *

urlpatterns = [
    path('', listar, name='pacientes'),
    path('paciente/<int:paciente_id>', detalhe, name='det_paciente')
    path('paciente/<char:paciente_nome>,', busca, name='busca')
] 