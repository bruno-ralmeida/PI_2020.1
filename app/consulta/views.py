from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados, separa_data_hr
from consulta.models import *

def listar(request):
    dados = get_dados(request)
    if dados['tipo'] == 1:
        lst_consultas = Consulta.objects.filter(medico=dados['usuario'])
        lst_consultas = separa_data_hr(lst_consultas)
        dados['lst_consultas'] = lst_consultas
        return render(request, 'consulta/consultas_medico.html', dados)
    else:
        lst_consultas = Consulta.objects.order_by('medico')
        lst_consultas = separa_data_hr(lst_consultas)
        dados['lst_consultas'] = lst_consultas
        for i in lst_consultas:
            print(i)
        return render(request, 'consulta/consultas_atendente.html', dados)
    