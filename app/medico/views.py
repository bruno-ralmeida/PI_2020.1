"""
@author Bruno Almeida
"""
from django.shortcuts import get_list_or_404
from medico.models import Medico

def listar_medico():
    """Função para retornar um dicionário com id e nome de todos os médicos para opções do formulario de consulta"""
    lst_medico = get_list_or_404(Medico)
    aux = {}
    for medico in lst_medico:
        aux[medico.id] = medico.nome

    lst_op = aux.items()

    return lst_op