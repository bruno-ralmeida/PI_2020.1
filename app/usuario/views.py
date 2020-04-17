from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from medico.models import Medico
from atendente.models import Atendente


def login(request):
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        
        if User.objects.filter(username=user).exists():
            user = auth.authenticate(request, username=user, password=password)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso.')
                return redirect('dashboard')

    return render(request, 'usuarios/login.html')

def logout(request):
    auth.logout(request.user)   
    return redirect('login')

def dashboard(request):
    if request.user.is_authenticated:
      dados =  get_dados(request)
    return render(request, 'usuarios/index.html', dados)



#---------------------------------------------------------------
# UTILS 
#---------------------------------------------------------------
def verifica_usuario(request):
    tipo_usuario = None
    if Medico.objects.filter(usuario=request.user):
        tipo_usuario = 1   
    if Atendente.objects.filter(usuario=request.user):
        tipo_usuario = 2

    return tipo_usuario

def get_usuario(request):
    usuario = None
    if verifica_usuario(request) == 1:
        usuario = get_object_or_404(Medico, usuario=request.user)

    if verifica_usuario(request) == 2:  
        usuario = get_object_or_404(Atendente, usuario=request.user)

    return usuario

def get_dados(request):
    dados = {'usuario': get_usuario(request),'tipo': verifica_usuario(request)}   
    return dados