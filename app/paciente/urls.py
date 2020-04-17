from django.urls import path
from paciente.views import *

urlpatterns = [
    path('', listar_paciente, name='pacientes')
] 