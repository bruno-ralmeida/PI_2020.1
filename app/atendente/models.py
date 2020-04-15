from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Atendente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=20, unique=True)
    rg = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    foto = models.ImageField(upload_to='fotos/', blank=True)