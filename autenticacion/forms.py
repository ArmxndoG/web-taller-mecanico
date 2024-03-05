from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from .models import Cita

class RegistrarUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','tel','username','password1','password2']
    
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['carro', 'color', 'problema', 'fecha', 'hora']