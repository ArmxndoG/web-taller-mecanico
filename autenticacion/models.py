from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class User(AbstractUser):
    tel = models.CharField(max_length= 20) #Agregar el campo telefono a la tabla de usuario
    
    def es_encargado(self):
        return self.is_staff
    
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return self.nombre
    
#clase para formulario de agendar cita
class Cita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    modelo_carro = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    placas = models.CharField(max_length=20)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=50, default='pendiente')
    retroalimentacion = models.TextField(null=True, blank=True)
    
    servicios = models.ManyToManyField(Servicio, through='DetalleCita')
    
    def __str__(self):
        return f"Cita {self.id} - {self.modelo_carro}"
    

class DetalleCita(models.Model):
    cita = models.ForeignKey('Cita', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    total = models.FloatField()

    def __str__(self):
        return f"DetalleCita #{self.id} - Cita #{self.cita.id} - Servicio #{self.servicio.id}"
    
class Fase(models.Model):
    nombre = models.CharField(max_length=255)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class ImagenFase(models.Model):
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE)
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete = models.CASCADE, default=0)
    imagen_path = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ImagenFase #{self.id} - Fase #{self.fase.id} - Cita #{self.cita.id}"