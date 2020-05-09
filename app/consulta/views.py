"""
@author Bruno Almeida
"""
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from usuario.views import get_dados
from consulta.models import Consulta
from consulta.forms import CadConsulta
from medico.models import Medico
from paciente.models import Paciente
from atendente.models import Atendente

def listar(request):
    """Função para listar as consultas"""
    dados = get_dados(request)

    if dados['tipo'] == 1:
        lst_consultas = Consulta.objects.filter(medico=dados['usuario']).reverse()
    else:
        lst_consultas = Consulta.objects.order_by('medico').reverse()

    paginator = Paginator(lst_consultas, 5)
    page = request.GET.get('page')
    consulta_por_pagina = paginator.get_page(page)
    dados['consultas'] = consulta_por_pagina

    return render(request, 'consulta/consultas.html', dados)

def nova_consulta(request):
    """
    Função para redirecionar para o cadastro de novas consultas
    """
    dados = get_dados(request)
    dados['form'] = CadConsulta()

    return render(request, 'consulta/nova_consulta.html', dados)

@csrf_exempt
def cadastro(request):
    """
    Função de cadastro para novas consultas.
    """
    paciente_id = request.POST['paciente']
    medico_id = request.POST['medico']
    dt_consulta = request.POST['data']
    hr_consulta = request.POST['hora']
    data_hora = fmt_data_hora(dt_consulta, hr_consulta)

    try:
        medico = get_object_or_404(Medico, id=medico_id)
        paciente = get_object_or_404(Paciente, id=paciente_id)
        atendente = get_object_or_404(Atendente, usuario=request.user)
        Consulta.objects.create(data=data_hora['data'], hora=data_hora['hora'], medico=medico,
                                atendente=atendente, paciente=paciente)
        messages.success(request, 'Consulta cadastrada com sucesso.')
    except:
        messages.error(request, 'Desculpe, ocorreu um erro ao tentar cadastrar a consulta.')

    return redirect('nova_consulta')

@csrf_exempt
def buscar_cpf(request):
    """Função para buscar o paciente de acordo com o CPF"""
    cpf = request.POST.get('cpf', '')

    if cpf is not None:
        lst_pacientes = Paciente.objects.filter(cpf__icontains=cpf)
    else:
        lst_pacientes = Paciente.objects.all()

    print(lst_pacientes)
    lst_dados = [
        dict(id=obj.id, nome=obj.nome)
        for obj in lst_pacientes
        ]

    return JsonResponse(lst_dados, safe=False)

@csrf_exempt
def buscar_medico(request):
    """
    Função para realizar a busca de médicos disponiveis na data e horario preenchidos no formulário.
    """
    dt_consulta = request.POST.get('data', '01/01/2020')
    hr_consulta = request.POST.get('hora', '00:00')
    lst_dados = []
    if datetime.strptime(hr_consulta, '%H:%M') <= datetime.strptime('17:30', '%H:%M'):
        data_hora = fmt_data_hora(dt_consulta, hr_consulta)
        consultas = Consulta.objects.filter(data=data_hora['data'],
                                            hora__istartswith=data_hora['hora'])
        lst_medico = []

        for consulta in consultas:
            lst_medico.append(consulta.medico.id)

        med_disp = Medico.objects.exclude(id__in=lst_medico)

        lst_dados = [
            dict(id=obj.id, nome=obj.nome)
            for obj in med_disp
        ]

    return JsonResponse(lst_dados, safe=False)

#UTILS
def fmt_data_hora(data, hora):
    """Função para formatar data e hora."""
    fmt_dt = datetime.strptime(data, '%d/%m/%Y')
    fmt_hr = datetime.strptime(hora, '%H:%M')

    dict_data_hora = {'data' : fmt_dt.strftime('%Y-%m-%d'), 'hora' : fmt_hr.strftime('%H:%M')}
    return dict_data_hora
