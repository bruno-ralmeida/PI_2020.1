from django.urls import path
from consulta.views import *

urlpatterns = [
    path('', listar, name='conusultas')
] 