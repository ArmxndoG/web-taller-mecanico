from django.contrib import admin
from autenticacion.models import User,Cita,Servicio,Fase
# Register your models here.

admin.site.register(Cita)
admin.site.register(Servicio)
admin.site.register(Fase)


