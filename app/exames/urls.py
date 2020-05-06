"""
@author Bruno Almeida
"""
from django.urls import path
from exames.views import cad_exame, detalhes, excluir_exame, importar_exame

urlpatterns = [
    path('detalhes/<int:paciente_id>', detalhes, name='det-exame'),
    path('cadastro/', cad_exame, name='cadastro'),
    path('excluir/<int:exame_id>', excluir_exame, name='del-exame'),
    path('importar/', importar_exame, name='importar')

]
