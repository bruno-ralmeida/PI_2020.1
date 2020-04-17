from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages, sessions
from usuario.views import get_dados
from paciente.models import Paciente
from datetime import date

def listar_paciente(request):
    dados =  get_dados(request)
    lst_pacientes = Paciente.objects.all()
    for paciente in lst_pacientes:
       
        imc = calculo_imc(paciente.peso, paciente.altura)
        paciente.imc = imc
        
        idade = calculo_idade(paciente.data_nascimento)
        paciente.idade = idade

    dados['lst_pacientes'] = lst_pacientes
    
    return render(request, 'paciente/lista_pacientes.html', dados)




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