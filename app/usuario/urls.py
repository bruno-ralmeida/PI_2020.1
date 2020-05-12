from django.urls import path
from usuario.views import login, logout, dashboard, usuarios, cadastrar, criar, editar, salvar_usuario

urlpatterns = [
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('usuarios/', usuarios, name='usuarios'),
    path('usuarios/cadastrar', cadastrar, name='cadastrar'),
    path('usuarios/criar', criar, name='criar'),
    path('editar-usuario/<id_user>', editar, name='edit-user'),
    path('salvar-usuario/', salvar_usuario, name='salvar-usario'),
] 