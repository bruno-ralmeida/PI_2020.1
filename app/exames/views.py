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
    data_atual = datetime.now()
    data_inicial = data_atual
    data_inicial = data_inicial + relativedelta(months=-12)

    paciente = get_object_or_404(Paciente, id=paciente_id)
    pac_idade = calculo_idade(paciente.data_nascimento)
    imc = calculo_imc(paciente.peso, paciente.altura)
    paciente.imc = imc
    paciente.idade = pac_idade

    if pac_idade <= 9:
        start_age = 0
        end_age = 9
    if pac_idade > 9 and pac_idade <= 19:
        start_age = 10
        end_age = 19
    if pac_idade >= 20:
        start_age = 20
        end_age = 150

    exame_ref = Exame_Referencia.objects.filter(idade_min=start_age, idade_max=end_age)
    exames = Exame_Resultado.objects.filter(paciente=paciente, data_exame__range=(data_inicial, data_atual)).order_by('data_exame')

    paginator = Paginator(exames.reverse(),6)  
    page = request.GET.get('page')
    exames_por_pagina = paginator.get_page(page)

  


    dados = get_dados(request)
    dados['paciente'] = paciente
    dados['exames'] = exames_por_pagina
    dados['exame_referencia'] = exame_ref  
    dados['exames_grafico'] = tratamento_grafico( exames)
    return render(request, 'exames/exames.html', dados)

def tratamento_grafico(lst_exames):
    for exame in lst_exames:
        exame.glicose = int(exame.glicose)
        exame.ldl = int(exame.ldl)
        exame.hdl = int(exame.hdl)
        exame.triglicerides = int(exame.triglicerides)
        exame.colesterol = int(exame.colesterol)



    return lst_exames

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

    
