"""
@author Bruno Almeida
"""
from django.shortcuts import render
from django.core.paginator import Paginator
from usuario.views import get_dados, separa_data_hr
from consulta.models import Consulta

def listar(request):
    """Função para listar as consultas"""
    dados = get_dados(request)

    if dados['tipo'] == 1:
        lst_consultas = Consulta.objects.filter(medico=dados['usuario']).reverse()
        lst_consultas = separa_data_hr(lst_consultas)

    else:
        lst_consultas = Consulta.objects.order_by('medico').reverse()
        lst_consultas = separa_data_hr(lst_consultas)

    paginator = Paginator(lst_consultas, 5)
    page = request.GET.get('page')
    consulta_por_pagina = paginator.get_page(page)
    dados['consultas'] = consulta_por_pagina

    return render(request, 'consulta/consultas.html', dados)
