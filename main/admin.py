from django.contrib import admin
from autenticacion.models import User,Cita,Servicio,Fase,DetalleCita,ImagenFase
# Register your models here.

admin.site.register(User)
admin.site.register(Cita)
admin.site.register(Servicio)
admin.site.register(Fase)
admin.site.register(DetalleCita)
admin.site.register(ImagenFase)



