from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados
from consulta.models import *

def listar(request):
    dados = get_dados(request)
    lst_consultas = Consulta.objects.all()
    dados['lst_consultas'] = lst_consultas

    return render(request, 'consulta/consultas.html', dados)