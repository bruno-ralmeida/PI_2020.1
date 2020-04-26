from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados
from consulta.models import *
from exames.models import *
from paciente.models import *
from paciente.views import calculo_idade
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from media.pdf.leitor_pdf import *
import os

def listar(request):
    dados = get_dados(request)
    lst_consultas = Consulta.objects.all()
    dados['lst_consultas'] = lst_consultas

    return render(request, 'exames/exames.html', dados)

def detalhes(request, paciente_id):
    dados = get_dados(request)

    data_atual = datetime.now()
    data_inicial = data_atual
    data_inicial = data_inicial + relativedelta(months=-12)

    paciente = get_object_or_404(Paciente, id=paciente_id)
    pac_idade = calculo_idade(paciente.data_nascimento)
    if pac_idade <= 9:
        start_age = 0
        end_age = 9
    if pac_idade > 9 and pac_idade <= 19:
        start_age = 10
        end_age = 19
    if pac_idade >= 20:
        start_age = 20
        end_age = 150

    exames = Exame_Resultado.objects.filter(paciente=paciente, data_exame__range=(data_inicial, data_atual))
    exame_ref = Exame_Referencia.objects.filter(idade_min=start_age, idade_max=end_age)
    
    dados['paciente'] = paciente
    dados['exames'] = exames
    dados['exame_referencia'] = exame_ref


    

    return render(request, 'exames/exames.html', dados)

def importar_exame(request):
    if request.method == 'POST':
        paciente_id = request.POST['paciente']
        arquivo = request.FILES['pdf']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        exame = Exame_Resultado.objects.create(paciente=paciente, data_exame=datetime.now(), glicose=0, ldl=0, hdl=0, triglicerides=0, colesterol=0, pdf=arquivo)
        exame.save()
        salvar_pdf(exame.id)
    return redirect('dashboard')


def salvar_pdf(exame_id):
    exame = get_object_or_404(Exame_Resultado, id=exame_id)
    print(exame.pdf)
    teste = str(exame.pdf)
    

    dados = ler_pdf(teste)
   
    print(f'Dados1: {dados[1]}')
