from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados, separa_data_hr
from consulta.models import *

def listar(request):
    dados = get_dados(request)
    url = ''
    if dados['tipo'] == 1:
        lst_consultas = Consulta.objects.filter(medico=dados['usuario']).reverse()
        lst_consultas = separa_data_hr(lst_consultas)
        url = 'consulta/consultas_medico.html'
    else:
        lst_consultas = Consulta.objects.order_by('medico').reverse()
        lst_consultas = separa_data_hr(lst_consultas)
        url = 'consulta/consultas_atendente.html'
            
    
    paginator = Paginator(lst_consultas, 5)  
    page = request.GET.get('page')
    consulta_por_pagina = paginator.get_page(page)
    dados['consultas'] = consulta_por_pagina

    return render(request, url , dados)
    