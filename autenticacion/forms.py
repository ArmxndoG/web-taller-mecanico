from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User,Cita,Servicio,DetalleCita, ImagenFase

class RegistrarUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','tel','username','password1','password2']

    
   
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['modelo_carro', 'color', 'placas', 'fecha', 'hora','servicios']
        
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            
        }
        
    servicios = forms.ModelMultipleChoiceField(
            queryset=None,
            widget=forms.CheckboxSelectMultiple
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar queryset para el campo de servicios
        self.fields['servicios'].queryset = Servicio.objects.all()
    

class ImagenForm(forms.ModelForm):
    class Meta:
        model = ImagenFase
        fields = ['fase', 'cita','servicio','imagen']
        
