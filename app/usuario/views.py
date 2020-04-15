from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from medico.models import Medico
from atendente.models import Atendente

# Create your views here.
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

def dashboard(request):
    if request.user.is_authenticated:
        tipo = {}
        if Medico.objects.filter(usuario=request.user):
           tipo_usuario = {'tipo':1}
        if Atendente.objects.filter(usuario=request.user):
            tipo_usuario = {'tipo':2}
        
    return render(request, 'usuarios/index.html', tipo_usuario)
    



#Utils