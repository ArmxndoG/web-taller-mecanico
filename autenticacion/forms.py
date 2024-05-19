from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User,Cita,Servicio,DetalleCita, ImagenFase
from django.forms.widgets import SelectDateWidget
from datetime import date
from django.utils.html import format_html
from django.db import models  # Agrega esta importación
from django.utils import timezone

class RegistrarUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','tel','username','password1','password2']

class CustomDateInput(forms.DateInput):
    def __init__(self, attrs=None):
        today = date.today()
        super().__init__(attrs={'type': 'date', 'min': today.strftime('%Y-%m-%d')})

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio']
    
    
class CustomDateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'min': timezone.now().strftime('%Y-%m-%d')}
        super().__init__(*args, **kwargs)

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['modelo_carro', 'color', 'placas', 'fecha', 'hora', 'servicios']
        
        widgets = {
            'fecha': CustomDateInput(),
            'hora': forms.Select(choices=[('09:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00')]),
        }

    servicios = forms.ModelMultipleChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha < timezone.now().date():
            raise forms.ValidationError("La fecha no puede ser en el pasado.")
        citas_del_dia = Cita.objects.filter(fecha=fecha).count()
        if citas_del_dia >= 5:
            raise forms.ValidationError("Dia lleno, seleccione otra fecha.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get("fecha")
        hora = cleaned_data.get("hora")
        if fecha:
            citas_del_dia = Cita.objects.filter(fecha=fecha).count()
            if citas_del_dia >= 5:
                self.add_error('fecha', "Dia lleno, seleccione otra fecha.")
        return cleaned_data
        
class ImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenFase
        fields = ['fase', 'cita','servicio','imagen']
        
