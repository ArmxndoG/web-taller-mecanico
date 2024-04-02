"""
URL configuration for django_taller_mecanico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from autenticacion import views as v_auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registro/', v_auth.registro,name='registro'),
    path('iniciar_sesion/', v_auth.inicio_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', v_auth.cerrar_sesion, name='cerrar_sesion'),
    #path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('preguntasfrec/', views.preguntasfrec, name='preguntasfrec'),
    path('acerca/', views.acerca, name='acerca'),
    path('citas/',v_auth.agendarCita, name='citas'),
    path('panel_encargado/', v_auth.panel_encargado, name='panel_encargado'),
    path('modificar_estado/<int:cita_id>', v_auth.modificar_estado_cita, name='modificar_estado_cita'),
    path('eliminar_cita/<int:cita_id>', v_auth.eliminar_cita, name='eliminar_cita'),
    path('detalle_cita_en_proceso/<int:cita_id>', v_auth.detalle_cita_enProceso, name='detalle_cita_en_proceso'),
    path('detalle_cita_en_proceso/<int:cita_id>/detalle_servicio/<int:servicio_id>/', v_auth.detalle_servicio, name='detalle_servicio'),
    path('subir_imagen/<int:fase_id>/', v_auth.subir_imagen, name='subir_imagen'),
    path('eliminar_imagen/<int:fase_id>/', v_auth.eliminar_imagen, name='eliminar_imagen'),
    path('servicios/', v_auth.lista_de_servicios, name='lista_de_servicios'),
    
    
    
    #path('detalle_cita_en_proceso/<int:cita_id>/detalle_servicio/<int:servicio_id>/', v_auth.detalle_servicio, name='detalle_servicio'),
    #path('detalle_servicio/<int:servicio_id>', v_auth.detalle_servicio, name='detalle_servicio'),
    #path('estatus_cita/<int:cita_id>', v_auth.estatus_cita, name='estatus_cita'),
]
#Si se encuentra en desarrollo, en producción se tiene que configurar otra cosa
if settings.DEBUG:#Si está en producción...
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    


