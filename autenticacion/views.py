from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .forms import RegistrarUsuario
from django.contrib.auth import login
from django.db import IntegrityError #Error de integridad en la base de datos, para manejar la excepción

# Create your views here.


def registro(request):
    
    if request.method == 'GET': #GET -> muestra el formulario
        
        return render(request,'registro.html',{
            'form': RegistrarUsuario
        })
        
    else: #POST -> obtiene datos del formulario
        print(request.POST)
        
        if request.POST['password1'] == request.POST['password2']: #válidar que sean las mismas contraseñas en el formulario
            # registrando usuario
            #Try except para evitar que se caiga el servidor si la consulta a la base de datos falla
            try:
                user = User.objects.create_user(first_name = request.POST['first_name'], last_name = request.POST['last_name'],
                                                email = request.POST['email'], tel = request.POST['tel'] ,username = request.POST['username'], password = request.POST['password1'])
                print(f"REGISTRO: {user}")
                user.save()
                login(request,user) #se crea una cookie 
                return redirect('login')
            
            except IntegrityError:
                
                return render(request,'registro.html',{
                        'form': RegistrarUsuario,
                        'error': 'El usuario ya existe'
                    })
        else:
            return render(request,'registro.html',{
                        'form': RegistrarUsuario,
                        'error': 'Las contraseñas no coinciden'
                    })


def inicio_sesion(request):
    return render(request,'login.html')
