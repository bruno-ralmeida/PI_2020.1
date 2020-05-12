"""
@author Bruno Almeida, Ana
"""
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from usuario.views import get_dados
from paciente.models import Paciente
from exames.models import Exame_Resultado



@login_required(login_url='login')
def listar(request):
    """Função para listagem de pacientes"""
    dados = get_dados(request)
    filtro = request.GET.get('filtro', '')
    if filtro is not None:
        lst_pacientes = Paciente.objects.filter(Q(nome__icontains=filtro) |
                                                Q(carteira_convenio__icontains=filtro))
    else:
        lst_pacientes = Paciente.objects.all()

    paginator = Paginator(lst_pacientes, 5)
    page = request.GET.get('page')
    pacientes_por_pagina = paginator.get_page(page)
    dados['lst_pacientes'] = pacientes_por_pagina

    return render(request, 'paciente/lista_pacientes.html', dados)


@login_required(login_url='login')
def detalhe(request, paciente_id):
    """Função para detalhes de pacientes"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    imc = calculo_imc(paciente.peso, paciente.altura)
    paciente.imc = imc
    dados = get_dados(request)
    exames = Exame_Resultado.objects.filter(paciente=paciente).order_by('data_exame').reverse()

    if len(exames) > 0:
        paginator = Paginator(exames, 5)
        page = request.GET.get('page')
        exames_por_pagina = paginator.get_page(page)
        dados['exames'] = exames_por_pagina

    dados['paciente'] = paciente
    return render(request, 'paciente/det_paciente.html', dados)


@login_required(login_url='login')
def alterar(request, paciente_id):
    """Função para redirecionar para a pagina de alteração de pacientes"""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    dados = get_dados(request)
    dados['paciente'] = paciente
    return render(request, 'paciente/altera_paciente.html', dados)

@login_required(login_url='login')
def atualiza_paciente(request):
    """Função para atualização de pacientes"""
    dados = get_dados(request)
    if request.method == 'POST':
        paciente_id = request.POST['paciente_id']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        paciente.nome = request.POST['nome']
        paciente.sexo = request.POST['sexo']
        paciente.data_nascimento = datetime.strptime(request.POST['dt_nasc'], '%d/%m/%Y').date()
        paciente.carteira_convenio = request.POST['convenio']
        paciente.cpf = request.POST['cpf']
        paciente.rg = request.POST['rg']
        paciente.email = request.POST['email']
        paciente.telefone = request.POST['telefone']
        paciente.celular = request.POST['celular']
        if dados['tipo'] == 1:
            paciente.peso = request.POST['peso']
            paciente.altura = request.POST['altura']
        if dados['tipo'] == 2:
            paciente.endereco = request.POST['endereco']
            paciente.end_num = request.POST['end_num']
            paciente.complemento = request.POST['complemento']
        paciente.save()

    return redirect('pacientes')


@login_required(login_url='login')
def adicionar(request):
    """Função para redirecionar para pagina de cadastro de pacientes"""
    dados = get_dados(request)
    paciente = Paciente()
    dados['paciente'] = paciente
    return render(request, 'paciente/adiciona_paciente.html', dados)

@login_required(login_url='login')
def adiciona_paciente(request):
    """Função para adicionar pacientes"""
    if request.method == 'POST':
        paciente = Paciente()
        paciente.nome = request.POST['nome']
        paciente.sexo = request.POST['sexo']
        paciente.data_nascimento = datetime.strptime(request.POST['dt_nasc'], '%d/%m/%Y').date()
        paciente.carteira_convenio = request.POST['convenio']
        paciente.cpf = request.POST['cpf']
        paciente.rg = request.POST['rg']
        paciente.email = request.POST['email']
        paciente.telefone = request.POST['telefone']
        paciente.celular = request.POST['celular']
        paciente.endereco = request.POST['endereco']
        paciente.end_num = request.POST['end_num']
        paciente.complemento = request.POST['complemento']
        paciente.peso = 0
        paciente.altura = 0

        paciente.save()
    return redirect('pacientes')

#---------------------------------------------------------------
# UTILS
#---------------------------------------------------------------
def calculo_idade(nasc):
    """
    @params DATA_NASCIMENTO
    Função para calcular a idade.
    """
    dt_atual = date.today()
    return dt_atual.year - nasc.year - ((dt_atual.month, dt_atual.day) < (nasc.month, nasc.day))

def calculo_imc(peso, altura):
    """
    @params PESO, ALTURA
    @return (PESO*2) / ALTURA e status do peso.
    Função para realizar o calulo de IMC
    """
    try:
        imc = peso / (altura*2)
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
    except ZeroDivisionError: 
            imc = 0
            resultado = 'Atualize os dados do paciente.'
    return f'{imc:.2f} - {resultado}'

def listar_paciente():
    """Função para retornar um dicionário com id e nome de todos os pacientes para opções do formulario de consulta"""
    lst_paciente = get_list_or_404(Paciente)
    aux = {}
    for paciente in lst_paciente:
        aux[paciente.id] = paciente.nome

    lst_op = aux.items()
    
    return lst_op
