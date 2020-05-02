import os
import re
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados
from media.pdf.leitor_pdf import *
from consulta.models import *
from exames.models import *
from paciente.models import *
from paciente.views import calculo_idade, calculo_imc
from datetime import datetime, date

#CRUD 
def detalhes(request, paciente_id):
    dados = get_dados(request)
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.idade = calculo_idade(paciente.data_nascimento)
    paciente.imc  = calculo_imc(paciente.peso, paciente.altura)

    
    #Paginação
    exames = Exame_Resultado.objects.filter(paciente=paciente).order_by('data_exame')
    paginator = Paginator(exames.reverse(),6)  
    page = request.GET.get('page')
    exames_por_pagina = paginator.get_page(page)

    dados['paciente'] = paciente
    dados['exames'] = exames_por_pagina
    dados['exame_referencia'] = exame_referencia(paciente.idade)
    dados['exames_grafico'] = grafico(paciente)
    return render(request, 'exames/exames.html', dados)

def cad_exame(request):
    if request.method == 'POST':
        paciente_id = request.POST['paciente']
        data = request.POST['data']
        glicose = request.POST['glicose']
        ldl = request.POST['ldl']
        hdl = request.POST['hdl']
        triglicerides = request.POST['triglicerides']
        colesterol = request.POST['colesterol']

    paciente = get_object_or_404(Paciente, id=paciente_id)
    messages.success(request, 'Dados cadastrados com sucesso.')

    exame = Exame_Resultado.objects.create(paciente=paciente, data_exame=data, glicose=glicose, ldl=ldl, hdl=hdl, triglicerides=triglicerides, colesterol=colesterol, pdf=None)
    exame.save()

    return redirect(reverse('det-exame', kwargs={'paciente_id': paciente_id}))

def excluir_exame(request, exame_id):
    exame =  get_object_or_404(Exame_Resultado, id= exame_id)
    exame.delete()
    return redirect(reverse('det-exame', kwargs={'paciente_id': exame.paciente.id}))

#IMPORTAÇÃO DE PDF
def importar_exame(request):
    """
    Função para importar exames no formato de arquivo PDF.
    """
    if request.method == 'POST':
        paciente_id = request.POST['paciente']
        arquivo = request.FILES['pdf']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        exame = Exame_Resultado.objects.create(paciente=paciente, data_exame=datetime.now(), glicose=0, ldl=0, hdl=0, triglicerides=0, colesterol=0, pdf=arquivo)
        exame.save()
        salvar_pdf(exame.id)
        messages.success(request, 'Dados importados com sucesso.')

    return redirect(reverse('det-exame', kwargs={'paciente_id': paciente_id}))

def salvar_pdf(exame_id):
    """
    Função para salvar informações corretas após leitura do arquivo PDF.
    """
    exame = get_object_or_404(Exame_Resultado, id=exame_id)
    texto_conv = str(exame.pdf)
    
    texto = ler_pdf(texto_conv)
    linha = []
    #Tratamento de informações
    for letra in texto:   
        if(letra != '\n'):
            linha.append(letra)
    aux = str(''.join(linha))  

    dado_aux = aux.split(':')
    regex_syntax = r'\D'
    #Informações do PDF
    nome = dado_aux[1].strip()
    data_nasc = dado_aux[3].strip()
    convenio = dado_aux[5].strip()
    idade = dado_aux[7].strip()
    data_exame = dado_aux[9].strip()
    glicose = int(re.sub(regex_syntax, '', dado_aux[11]))
    ldl = int(re.sub(regex_syntax, '', dado_aux[13]))
    hdl = int(re.sub(regex_syntax, '', dado_aux[15]))
    triglicerides = int(re.sub(regex_syntax, '', dado_aux[17]))
    colesterol = int(re.sub(regex_syntax, '', dado_aux[19]))
    #Atualizando os dados no banco
    exame.data_exame = datetime.strptime(data_exame, "%d/%m/%Y")
    exame.glicose = glicose
    exame.ldl = ldl
    exame.hdl = hdl
    exame.triglicerides = triglicerides
    exame.colesterol = colesterol
    exame.pdf = exame.pdf
    exame.save()

#EXAME REFERENCIA E GRAFICO
def exame_referencia(idade_paciente):
    """
    Função para buscar os exames de referencia de acordo com a idade do paciente.
    """
    range_idade = []

    if idade_paciente <= 9:
        range_idade.append(0)
        range_idade.append(9)

    if idade_paciente > 9 and idade_paciente <= 19:
        range_idade.append(10)
        range_idade.append(19)

    if idade_paciente >= 20:
        range_idade.append(20)
        range_idade.append(150)
    
    return  Exame_Referencia.objects.filter(idade_min=range_idade[0], idade_max=range_idade[1])

def grafico(paciente):
    """Para inserir as informações no gráfico é necessário que sejam tipos inteiros"""
    data_atual = datetime.now()
    data_inicial = data_atual
    data_inicial = data_inicial + relativedelta(months=-6)

    lst_exames = Exame_Resultado.objects.filter(paciente=paciente, data_exame__range=(data_inicial, data_atual)).order_by('data_exame')

    for exame in lst_exames:
        exame.glicose = int(exame.glicose)
        exame.ldl = int(exame.ldl)
        exame.hdl = int(exame.hdl)
        exame.triglicerides = int(exame.triglicerides)
        exame.colesterol = int(exame.colesterol)

    return lst_exames
