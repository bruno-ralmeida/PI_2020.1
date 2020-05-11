from django.urls import path
from usuario.views import login, logout, dashboard, usuarios, editar, salvar_usuario

urlpatterns = [
    path('', login, name='login'),
    path('logout', logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('usuarios/', usuarios, name='usuarios'),
    path('editar-usuario/<id>', editar, name='edit-user'),
    path('salvar-usuario/', salvar_usuario, name='salvar-usario'),
] 