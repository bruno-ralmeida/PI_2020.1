from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados
from consulta.models import *
from exames.models import *
from paciente.models import *
from paciente.views import calculo_idade

def listar(request):
    dados = get_dados(request)
    lst_consultas = Consulta.objects.all()
    dados['lst_consultas'] = lst_consultas

    return render(request, 'exames/exames.html', dados)

def detalhes(request, paciente_id):
    dados = get_dados(request)
    paciente = get_object_or_404(Paciente, id=paciente_id)
    start_age = 0
    end_age = calculo_idade(paciente.data_nascimento)
    exame_ref = Exame_Referencia.objects.filter(idade__range=(start_age,end_age))
    dados['paciente'] = paciente
    dados['exame_referencia'] = exame_ref
    return render(request, 'exames/exames.html', dados)