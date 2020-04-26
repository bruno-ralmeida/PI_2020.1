from django.urls import path
from exames.views import *

urlpatterns = [
    path('', listar, name='exames'),
    path('detalhes/<int:paciente_id>', detalhes, name='det-exame'),
    path('importar/', importar_exame, name='importar')

] 