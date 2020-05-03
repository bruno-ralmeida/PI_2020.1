from django.db import models
from paciente.models import Paciente
# Create your models here.
class Exame_Resultado(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    data_exame = models.DateField()
    glicose = models.FloatField(max_length=15)
    ldl = models.FloatField(max_length=15)
    hdl = models.FloatField(max_length=15)
    triglicerides = models.FloatField(max_length=15)
    colesterol = models.FloatField(max_length=15)
    vldl = models.FloatField(max_length=15)
    pdf = models.FileField(upload_to=f'pdf/', blank=True)


class Exame_Referencia(models.Model):
    glicose_min = models.IntegerField()
    glicose_max = models.IntegerField()
    ldl_min = models.IntegerField()
    ldl_max = models.IntegerField()
    hdl_min = models.IntegerField()
    hdl_max = models.IntegerField()
    triglicerides_min = models.IntegerField()
    triglicerides_max = models.IntegerField()
    colesterol_min = models.IntegerField()
    colesterol_max = models.IntegerField()
    vldl_min = models.IntegerField()
    vldl_max = models.IntegerField()
    idade_min = models.IntegerField()
    idade_max = models.IntegerField()