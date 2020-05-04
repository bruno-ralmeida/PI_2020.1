import os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib import auth, messages
from usuario.views import get_dados
from consulta.models import *
from exames.models import *
from exames.leitor_pdf import *
from paciente.models import *
from paciente.views import calculo_idade, calculo_imc
from datetime import datetime, date

#CRUD 
@login_required(login_url='login')
def detalhes(request, paciente_id):
    dados = get_dados(request)
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.idade = calculo_idade(paciente.data_nascimento)
    paciente.imc = calculo_imc(paciente.peso, paciente.altura)
    
    #Paginação
    exames = Exame_Resultado.objects.filter(paciente=paciente).order_by('data_exame').reverse()
    paginator = Paginator(exames,6)  
    page = request.GET.get('page')
    exames_por_pagina = paginator.get_page(page)

    estimativa(paciente)

    print(paciente.id)

    dados['paciente'] = paciente
    dados['exames'] = exames_por_pagina
    dados['exame_referencia'] = exame_referencia(paciente.idade)
    dados['exames_grafico'] = converte_grafico(exames_periodo(paciente))
    return render(request, 'exames/exames.html', dados)

@login_required(login_url='login')
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

@login_required(login_url='login')
def excluir_exame(request, exame_id):
    exame =  get_object_or_404(Exame_Resultado, id= exame_id)
    exame.delete()
    return redirect(reverse('det-exame', kwargs={'paciente_id': exame.paciente.id}))

#IMPORTAÇÃO DE PDF


@login_required(login_url='login')
def importar_exame(request):
    """
    Função para importar exames no formato de arquivo PDF.
    """
    if request.method == 'POST':
        paciente_id = request.POST['paciente']
        arquivo = request.FILES['pdf']
        paciente = get_object_or_404(Paciente, id=paciente_id)
        exame = Exame_Resultado.objects.create(paciente=paciente, data_exame=datetime.now(), glicose=0, ldl=0, hdl=0, triglicerides=0, colesterol=0, vldl=0,pdf=arquivo)
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
    vldl = int(re.sub(regex_syntax, '', dado_aux[21]))
    #Atualizando os dados no banco
    exame.data_exame = datetime.strptime(data_exame, "%d/%m/%Y")
    exame.glicose = glicose
    exame.ldl = ldl
    exame.hdl = hdl
    exame.triglicerides = triglicerides
    exame.colesterol = colesterol
    exame.vldl = vldl
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
    
    return  get_object_or_404(Exame_Referencia, idade_min=range_idade[0] , idade_max=range_idade[1]) #Exame_Referencia.objects.filter(idade_min=range_idade[0], idade_max=range_idade[1])

def exames_periodo(paciente):
    """Função para realizar a busca de exames pelo periodo de 6 meses"""
    data_atual = datetime.now()
    data_inicial = data_atual
    data_inicial = data_inicial + relativedelta(months=-6)

    lst_exames = Exame_Resultado.objects.filter(paciente=paciente, data_exame__range=(data_inicial, data_atual)).order_by('data_exame')

    return lst_exames

def converte_grafico(lst_exames):
    """
    Função para conversão dos valores do grafico
    """
    for exame in lst_exames:
        exame.glicose = int(exame.glicose)
        exame.ldl = int(exame.ldl)
        exame.hdl = int(exame.hdl)
        exame.triglicerides = int(exame.triglicerides)
        exame.colesterol = int(exame.colesterol)

    return lst_exames

#ESTIMATIVA 
def estimativa(paciente):
    ultimo_exame = Exame_Resultado.objects.filter(paciente=paciente).latest('data_exame')
    exame_ref = exame_referencia(paciente.idade)
    
    lst_glicose = []
    lst_ldl = []
    lst_hdl = []
    lst_triglicerides = []
    lst_colesterol = []
    lst_vldl = []
    lst_data = []

    for exame in exames_periodo(paciente):
        lst_data.append(exame.data_exame)
        lst_glicose.append(exame.glicose)
        lst_ldl.append(exame.ldl)
        lst_hdl.append(exame.hdl)
        lst_triglicerides.append((exame.triglicerides))
        lst_colesterol.append(exame.colesterol)
        lst_vldl.append(exame.vldl)

    periodo = calculo_periodo_exames(lst_data)

    var_glicose = calculo_variacao(lst_glicose)
    var_ldl = calculo_variacao(lst_ldl)
    var_hdl = calculo_variacao(lst_hdl)
    var_triglicerides = calculo_variacao(lst_triglicerides)
    var_colesterol = calculo_variacao(lst_colesterol)
    var_vldl = calculo_variacao(lst_vldl)


    print(calculo_estimativa('glicose', ultimo_exame.glicose, exame_ref.glicose_min , exame_ref.glicose_max, periodo, var_glicose))
    
    print(calculo_estimativa('ldl', ultimo_exame.ldl, exame_ref.ldl_min, exame_ref.ldl_max, periodo, var_ldl))

    print(calculo_estimativa('hdl', ultimo_exame.hdl, exame_ref.hdl_min, exame_ref.hdl_min, periodo, var_hdl))

    print(calculo_estimativa('triglicerides', ultimo_exame.triglicerides, exame_ref.triglicerides_min,exame_ref.triglicerides_max, periodo, var_triglicerides))

    print(calculo_estimativa('colesterol', ultimo_exame.colesterol, exame_ref.colesterol_min, exame_ref.colesterol_max, periodo, var_colesterol))

    print(calculo_estimativa('vldl', ultimo_exame.vldl, exame_ref.vldl_min ,exame_ref.vldl_max, periodo, var_vldl))


def calculo_estimativa(tipo_exame, ultimo_exame, exame_ref_min ,exame_ref_max, periodo_ref, variacao):
    """
    Função para realizar o calculo da estimativa.
    @Params tipo_exame, ultimo_exame, exame_ref_min,exame_ref_max, periodo_ref, variacao
    @return dicionario com as informações do tipo de exame da simulação, o periodo para atigir o limite e valor limite no periodo.
    """
    exame_result = ultimo_exame 
    calc_periodo = 0
    print(f'ultimo exame: {ultimo_exame}')
    if(variacao < 0):
        while(ultimo_exame < exame_ref_max):
            if(exame_result <= exame_ref_max):
                exame_result += abs(variacao)
                calc_periodo += periodo_ref
            else:
                break
    if(variacao > 0):
        
        while(ultimo_exame > exame_ref_min):
            if(exame_result >= exame_ref_min):
                exame_result -= variacao
                calc_periodo += periodo_ref
            else:
                break


    resultado = {
        'tipo_exame' : tipo_exame,
        'periodo' : calc_periodo,
        'resultado_simulação' : exame_result
    }

    return resultado

def calculo_variacao(lst):
    
    lst_aux = []
    #Negativo == subindo  //  Positivo == caindo
    #Pegando os ultimos 6 exames
    max_ind = 0
    if(len(lst) < 6):
        max_ind = len(lst)
    else:
        max_ind = 6

    for i in range(1, max_ind):
        
        diferenca = (lst[i-1] - lst[i]) 
        
        lst_aux.append(diferenca)    
    
    
    return (sum(lst_aux)/len(lst_aux))

def calculo_periodo_exames(lst):
    """
    Função para realizar o cálculo de média do periodo entre os exames realizados.
    """
    lst.reverse()
    lst_aux = []
    max_ind = 0
    
    if(len(lst) < 6): #Filtro de até 6 exames.
        max_ind = len(lst)
    else:
        max_ind = 6

    for i in range(1, max_ind):
        aux = (lst[i-1] - lst[i]) #Data ini / fim.
       
        diferenca = int(aux.days) 
        lst_aux.append(diferenca)   
    
    return int(sum(lst_aux)/len(lst_aux))
    
    