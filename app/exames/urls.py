from django.urls import path
from exames.views import *

urlpatterns = [
    path('detalhes/<int:paciente_id>', detalhes, name='det-exame'),
    path('excluir/<int:exame_id>', excluir_exame, name='del-exame'),
    path('importar/', importar_exame, name='importar')

] 