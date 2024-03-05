from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class User(AbstractUser):
    tel = models.CharField(max_length= 20) #Agregar el campo telefono a la tabla de usuario
    
    def es_encargado(self):
        return self.is_staff
    
#clase para formulario de agendar cita
class Cita(models.Model):
    carro = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    problema = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    
    def agendar(self):
        return self.cita