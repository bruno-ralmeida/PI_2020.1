"""
@author Bruno Almeida
"""
from django.urls import path
from consulta.views import listar, nova_consulta, cadastro, buscar_medico, buscar_cpf

urlpatterns = [
    path('', listar, name='conusultas'),
    path('novaConsulta', nova_consulta, name='nova_consulta'),
    path('cadstro', cadastro, name='minha_consulta'),
    path('medicos', buscar_medico, name='buscar_medico'),
    path('pacientes', buscar_cpf, name='buscar_paciente'),

]
