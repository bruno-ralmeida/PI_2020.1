"""
@author Bruno Almeida
"""
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from usuario.views import get_dados
from exames.models import Exame_Referencia, Exame_Resultado
from exames.leitor_pdf import ler_pdf
from paciente.models import Paciente
from paciente.views import calculo_idade, calculo_imc


@login_required(login_url='login')
def detalhes(request, paciente_id):
    """Função para mostrar os detalhes do paciente e exames."""
    dados = get_dados(request)
    paciente = get_object_or_404(Paciente, id=paciente_id)
    paciente.idade = calculo_idade(paciente.data_nascimento)
    paciente.imc = calculo_imc(paciente.peso, paciente.altura)
    #Paginação
    exames = Exame_Resultado.objects.filter(paciente=paciente).order_by('data_exame').reverse()
    paginator = Paginator(exames, 6)
    page = request.GET.get('page')
    exames_por_pagina = paginator.get_page(page)
    dados['paciente'] = paciente
    dados['exames'] = exames_por_pagina
    dados['lst_estimativa'] = estimativa(paciente)
    dados['exame_referencia'] = exame_referencia(paciente.idade)
    dados['exames_grafico'] = converte_grafico(exames)

    return render(request, 'exames/exames.html', dados)

@login_required(login_url='login')
def cad_exame(request):
    """Função para cadastro de exames"""
    try:
        if request.method == 'POST':
            paciente_id = request.POST['paciente']
            paciente = get_object_or_404(Paciente, id=paciente_id)
            exame = Exame_Resultado.objects.create(paciente=paciente, data_exame=request.POST['data'],
                                                   glicose=request.POST['glicose'], ldl=request.POST['ldl'],
                                                   hdl=request.POST['hdl'], triglicerides=request.POST['triglicerides'],
                                                   colesterol=request.POST['colesterol'], vldl=request.POST['vldl'], pdf=None)
            exame.save()
            messages.success(request, 'Dados cadastrados com sucesso.')
    except:
        messages.error(request, 'Erro ao cadastrar exame.')

    return redirect(reverse('det-exame', kwargs={'paciente_id': paciente_id}))

@login_required(login_url='login')
def excluir_exame(request, exame_id):
    """Função para exclusão de exames"""
    exame = get_object_or_404(Exame_Resultado, id=exame_id)
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
        exame = Exame_Resultado.objects.create(paciente=paciente, data_exame=datetime.now(),
                                               glicose=0, ldl=0, hdl=0, triglicerides=0,
                                               colesterol=0, vldl=0, pdf=arquivo)
        exame.save()
        salvar_pdf(request, exame.id)


    return redirect(reverse('det-exame', kwargs={'paciente_id': paciente_id}))

def salvar_pdf(request, exame_id):
    """
    Função para salvar informações corretas após leitura do arquivo PDF.
    """
    exame = get_object_or_404(Exame_Resultado, id=exame_id)
    texto_conv = str(exame.pdf)
    texto = ler_pdf(texto_conv)
    linha = []
    #Tratamento de informações
    for letra in texto:
        if letra != '\n':
            linha.append(letra)
    aux = str(''.join(linha))

    dado_aux = aux.split(':')
    regex_syntax = r'\D'

    try:
       
        cpf = dado_aux[5].strip()
        glicose = int(re.sub(regex_syntax, '', dado_aux[9]))
        ldl = int(re.sub(regex_syntax, '', dado_aux[11]))
        hdl = int(re.sub(regex_syntax, '', dado_aux[13]))
        triglicerides = int(re.sub(regex_syntax, '', dado_aux[15]))
        colesterol = int(re.sub(regex_syntax, '', dado_aux[17]))
        vldl = int(re.sub(regex_syntax, '', dado_aux[19]))
        data_exame = dado_aux[21].strip()

        if cpf != exame.paciente.cpf:
            messages.warning(request, f'Exame não importado! Verifique o exame importado. O CPF está divergente da '+
                             f'nossa base de dados. \nPDF {cpf} \nCadastro: {exame.paciente.cpf}')
            exame.delete()
        else:
            exame.data_exame = datetime.strptime(data_exame, "%d/%m/%Y")
            exame.glicose = glicose
            exame.ldl = ldl
            exame.hdl = hdl
            exame.triglicerides = triglicerides
            exame.colesterol = colesterol
            exame.vldl = vldl
            exame.pdf = exame.pdf
            exame.save()
            messages.success(request, 'Dados importados com sucesso.')
    except:
        exame.delete()
        messages.error(request, 'Erro ao Salvar. Modelo fora do padrão.')

#EXAME REFERENCIA E GRAFICO
def exame_referencia(idade_paciente):
    """
    Função para buscar os exames de referencia de acordo com a idade do paciente.
    """
    i_ref = []

    if idade_paciente <= 9:
        i_ref.append(0)
        i_ref.append(9)

    if idade_paciente > 9 and idade_paciente <= 19:
        i_ref.append(10)
        i_ref.append(19)

    if idade_paciente >= 20:
        i_ref.append(20)
        i_ref.append(150)

    return  get_object_or_404(Exame_Referencia, idade_min=i_ref[0], idade_max=i_ref[1])

def exames_periodo(paciente):
    """Função para realizar a busca de exames pelo periodo de 6 meses"""
    fim = datetime.now()
    ini = fim + relativedelta(months=-6)

    lst_exames = Exame_Resultado.objects.filter(paciente=paciente,
                                                data_exame__range=(ini, fim)).order_by('data_exame')

    return lst_exames

def converte_grafico(lst_exames):
    """
    Função para conversão dos valores do grafico
    """
    for exame in lst_exames:
        exame.glicose = f'{exame.glicose:.2f}'
        exame.ldl = f'{exame.ldl:.2f}'
        exame.hdl = f'{exame.hdl:.2f}'
        exame.triglicerides = f'{exame.triglicerides:.2f}'
        exame.colesterol = f'{exame.colesterol:.2f}'

    lst_fmt = []
    for i, exame in enumerate(lst_exames):
        if i < 6:
            lst_fmt.append(exame)
    lst_fmt.reverse()

    return lst_fmt

#ESTIMATIVA
def estimativa(paciente):
    """
    Função que realiza a estimativa em dias do periodo para
    que o paciente atinja o limite de referencia dos exames.
    """
    ult_exame = Exame_Resultado.objects.filter(paciente=paciente).latest('data_exame')
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

    periodo = calc_periodo_exames(lst_data)

    var_glicose = calc_variacao(lst_glicose)
    var_ldl = calc_variacao(lst_ldl)
    var_hdl = calc_variacao(lst_hdl)
    var_triglicerides = calc_variacao(lst_triglicerides)
    var_colesterol = calc_variacao(lst_colesterol)
    var_vldl = calc_variacao(lst_vldl)

    lst_dados = []
    lst_dados.append(calc_esitmativa('glicose', ult_exame.glicose, exame_ref.glicose_min,
                                     exame_ref.glicose_max, periodo, var_glicose))

    lst_dados.append(calc_esitmativa('ldl', ult_exame.ldl, exame_ref.ldl_min,
                                     exame_ref.ldl_max, periodo, var_ldl))

    lst_dados.append(calc_esitmativa('hdl', ult_exame.hdl, exame_ref.hdl_min,
                                     exame_ref.hdl_min, periodo, var_hdl))

    lst_dados.append(calc_esitmativa('triglicerides', ult_exame.triglicerides,
                                     exame_ref.triglicerides_min, exame_ref.triglicerides_max,
                                     periodo, var_triglicerides))

    lst_dados.append(calc_esitmativa('colesterol', ult_exame.colesterol, exame_ref.colesterol_min,
                                     exame_ref.colesterol_max, periodo, var_colesterol))

    lst_dados.append(calc_esitmativa('vldl', ult_exame.vldl, exame_ref.vldl_min, exame_ref.vldl_max,
                                     periodo, var_vldl))

    return lst_dados

def calc_esitmativa(tipo_exame, ultimo_exame, exame_ref_min, exame_ref_max, periodo_ref, variacao):
    """
    Função para realizar o calculo da estimativa.
    @Params tipo_exame, ultimo_exame, exame_ref_min,exame_ref_max, periodo_ref, variacao
    @return dicionario com as informações do tipo de exame da simulação,
    o periodo para atigir o limite e valor limite no periodo.
    """
    exame_result = ultimo_exame
    calc_periodo = 0
    if variacao < 0:
        while ultimo_exame < exame_ref_max:
            if exame_result <= exame_ref_max:
                exame_result += abs(variacao)
                calc_periodo += periodo_ref
            else:
                break
    if variacao > 0:

        while ultimo_exame > exame_ref_min:
            if exame_result >= exame_ref_min:
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

def calc_variacao(lst):
    """Função para realizar o calculo de variação de acordo com uma lista de resultados,
    o retorno será com nos ultimos 6 exames (- ==  ↑ //  + == ↓).
    """
    try:
        if len(lst) > 0:
            lst_aux = []
            max_ind = 0
            if len(lst) < 6:
                max_ind = len(lst)
            else:
                max_ind = 6

            for i in range(1, max_ind):
                diferenca = (lst[i-1] - lst[i])
                lst_aux.append(diferenca)

            variacao = sum(lst_aux)/len(lst_aux)
        else:
            variacao = 0
        return variacao
    except ZeroDivisionError:
        return 0

def calc_periodo_exames(lst):
    """
    Função para realizar o cálculo de média do periodo entre os exames realizados.
    """
    try:
        if len(lst) > 0:
            lst.reverse()
            lst_aux = []
            max_ind = 0

            if len(lst) < 6: #Filtro de até 6 exames.
                max_ind = len(lst)
            else:
                max_ind = 6

            for i in range(1, max_ind):
                aux = (lst[i-1] - lst[i]) #Data ini / fim.
                diferenca = int(aux.days)
                lst_aux.append(diferenca)

            valor_periodo = int(sum(lst_aux)/len(lst_aux))

        else:
            valor_periodo = 0

        return valor_periodo
    except ZeroDivisionError:
        return 0
