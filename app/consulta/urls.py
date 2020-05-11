"""
@author Bruno Almeida
"""
from django.urls import path
from consulta.views import listar, nova_consulta, cadastro, editar, salvar_alteracao, buscar_medico, buscar_cpf

urlpatterns = [
    path('', listar, name='consultas'),
    path('novaConsulta', nova_consulta, name='nova_consulta'),
    path('cadstro', cadastro, name='minha_consulta'),
    path('editar/<int:consulta_id>', editar, name='consulta-edit'),
    path('salvar', salvar_alteracao, name='salvar_alteracao'),
    path('medicos', buscar_medico, name='buscar_medico'),
    path('pacientes', buscar_cpf, name='buscar_paciente'),

]
