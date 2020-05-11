"""
@author Bruno Almeida
"""
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth, messages
from medico.models import Medico
from atendente.models import Atendente


def login(request):
    """Função para realizar o login"""
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=user).exists():
            user = auth.authenticate(request, username=user, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha inválida.')
        else:
            messages.error(request, 'Usuário/Senha inválidos.')
            return render(request, 'usuarios/login.html')

    return render(request, 'usuarios/login.html')


def logout(request):
    """Função para realizar o logout"""
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    """Função para o usuário de forma correta"""
    if request.user.is_authenticated:
        dados = get_dados(request)

    return render(request, 'usuarios/index.html', dados)

@login_required(login_url='login')
def usuarios(request):
    dados = get_dados(request)

    medicos = Medico.objects.all()
    atendentes = Atendente.objects.all()
    lst_usuarios = []

    for user in medicos:
        lst_usuarios.append(user)

    for user in atendentes:
        lst_usuarios.append(user)

    print(lst_usuarios)

    dados['lst_usuarios'] = lst_usuarios
    return render(request, 'usuarios/listar_usuarios.html', dados)

@login_required(login_url='login')
def editar(request, id):
    dados = get_dados(request)

    dados['useredit'] = medico = atendente = None
    usuario = get_object_or_404(User, id=id)

    if Medico.objects.filter(usuario=usuario):
        medico = get_object_or_404(Medico, usuario=usuario)
        dados['useredit'] = medico
        dados['usertipo'] = 1

    if Atendente.objects.filter(usuario=usuario):
        atendente = get_object_or_404(Atendente, usuario=usuario)
        dados['useredit'] = atendente
        dados['usertipo'] = 2

    return render(request, 'usuarios/editar_usuario.html', dados)

@login_required(login_url='login')
def salvar_usuario(request):
    dados = get_dados(request)
    if request.method == 'POST':
        usuario_id = request.POST['user_id']

        usuario = get_object_or_404(User, id=usuario_id)
        user_edit = None

        if Medico.objects.filter(usuario=usuario):
            user_edit = get_object_or_404(Medico, usuario=usuario)
            user_edit.crm = request.POST['crm']
            dados['usertipo'] = 1

        if Atendente.objects.filter(usuario=usuario):
            user_edit = get_object_or_404(Atendente, usuario=usuario)
            dados['usertipo'] = 2

        user_edit.nome = request.POST['nome']
        user_edit.email = request.POST['email']
        user_edit.sexo = request.POST['sexo']
        user_edit.data_nascimento =  datetime.strptime(request.POST['dt_nasc'],'%d/%m/%Y').date()
        user_edit.cpf = request.POST['cpf']
        user_edit.rg = request.POST['rg']

        if request.user.id == usuario.id:
            usuario_senha = request.POST['senha']
            usuario_csenha = request.POST['conf-senha']

        dados['useredit'] = user_edit
        user_edit.save()
        

    return render(request, 'usuarios/editar_usuario.html', dados)

#---------------------------------------------------------------
# UTILS
#---------------------------------------------------------------
def verifica_usuario(request):
    """Verifica o usuário do request e retorno se o tipo é médico ou atendente"""
    tipo_usuario = None
    if Medico.objects.filter(usuario=request.user):
        tipo_usuario = 1
    if Atendente.objects.filter(usuario=request.user):
        tipo_usuario = 2

    return tipo_usuario

def get_usuario(request):
    """Retorna o usuário de acrodo com request"""
    usuario = None
    if verifica_usuario(request) == 1:
        usuario = get_object_or_404(Medico, usuario=request.user)

    if verifica_usuario(request) == 2:
        usuario = get_object_or_404(Atendente, usuario=request.user)

    return usuario

def get_dados(request):
    """Pega as informações no contexto"""
    dados = {'usuario': get_usuario(request), 'tipo': verifica_usuario(request)}
    return dados
