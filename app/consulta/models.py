from django.db import models
from medico.models import Medico
from atendente.models import Atendente
from paciente.models import Paciente

# Create your models here.
class Consulta(models.Model):
    data = models.DateTimeField()
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    atendente = models.ForeignKey(Atendente, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)