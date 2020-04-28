from django.db import models

# Create your models here.
class Paciente(models.Model):
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=20, unique=True)
    rg = models.CharField(max_length=20, unique=True)
    carteira_convenio = models.CharField(max_length=30, unique=True)
    peso = models.FloatField()
    altura = models.FloatField()
    endereco = models.CharField(max_length=250)
    end_num = models.IntegerField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50)
    telefone = models.CharField(max_length=14)    
    celular = models.CharField(max_length=15)    