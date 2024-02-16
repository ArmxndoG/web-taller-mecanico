from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrarUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','tel','username','password1','password2']
    