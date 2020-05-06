"""
@author Bruno Almeida
"""
from django.db import models
from medico.models import Medico
from atendente.models import Atendente
from paciente.models import Paciente

class Consulta(models.Model):
    """Classe de modelo consulta."""
    data = models.DateTimeField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    atendente = models.ForeignKey(Atendente, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
