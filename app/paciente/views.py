from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages, sessions
from usuario.views import get_dados
from paciente.models import Paciente
from exames.models import Exame_Resultado
from datetime import date, datetime


@login_required(login_url='login')
def listar(request):
    dados =  get_dados(request)
    lst_pacientes = Paciente.objects.all()
    
    
    paginator = Paginator(lst_pacientes,5)  
    page = request.GET.get('page')
    pacientes_por_pagina = paginator.get_page(page)    
    dados['lst_pacientes'] = pacientes_por_pagina
    


    return render(request, 'paciente/lista_pacientes.html', dados)

@login_required(login_url='login')
def detalhe(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    imc = calculo_imc(paciente.peso, paciente.altura)
    paciente.imc = imc
    exames = get_list_or_404(Exame_Resultado, paciente=paciente)
    dados =  get_dados(request)
    exames.reverse()
    paginator = Paginator(exames,5)  
    page = request.GET.get('page')
    exames_por_pagina = paginator.get_page(page)    

    dados['paciente'] = paciente
    dados['exames'] = exames_por_pagina
    return render(request, 'paciente/det_paciente.html', dados)


@login_required(login_url='login')
def alterar(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    dados =  get_dados(request)
    dados['paciente'] = paciente
    return render(request, 'paciente/altera_paciente.html', dados)

@login_required(login_url='login')
def atualiza_paciente(request):
    if request.method == 'POST':
        paciente_id = request.POST['paciente_id']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        paciente.nome = request.POST['nome']
        paciente.cpf = request.POST['cpf']
        paciente.rg = request.POST['rg']
        paciente.carteira_convenio = request.POST['carteira_convenio']
        paciente.sexo = request.POST['sexo']
        paciente.peso = float(request.POST['peso'].replace(',','.')) 
        paciente.altura = float(request.POST['altura'].replace(',','.'))
        paciente.data_nascimento = datetime.strptime(request.POST['data_nascimento'], '%d/%m/%Y').date()
        
        paciente.save() #Em django para atualizar os dados utilizamos o método save()
    return redirect('pacientes')

def busca(request, paciente_nome):
    pass
#---------------------------------------------------------------
# UTILS 
#---------------------------------------------------------------
def calculo_idade(data_nascimento):
    """
    @params DATA_NASCIMENTO
    Função para calcular a idade.
    """
    data_atual = date.today()
    return data_atual.year - data_nascimento.year - ((data_atual.month, data_atual.day) < (data_nascimento.month, data_nascimento.day))

def calculo_imc(peso, altura):
    """
    @params PESO, ALTURA
    @return (PESO*2) / ALTURA e status do peso.
    Função para realizar o calulo de IMC
    """
    imc =  peso / (altura*2)
    resultado = ''
    if imc < 18.5:
        resultado = 'Abaixo do peso'
    elif imc >= 18.5 and imc < 24.90:
        resultado = 'Peso Normal'
    elif imc >= 25 and imc < 29.90:
        resultado = 'Sobrepeso'
    elif imc >= 30 and imc < 34.90:
        resultado = 'Obesidade grau 1'
    elif imc >= 35 and imc < 39.90: 
        resultado = 'Obesidade grau 2'
    else:
        resultado = 'Obesidade grau 3'
    return (f'{imc:.2f} - {resultado}')