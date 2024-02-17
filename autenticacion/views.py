from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from .forms import RegistrarUsuario
from django.contrib.auth import login,logout,authenticate
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
                #login(request,user) #se crea una cookie (sesión) 
                return redirect('iniciar_sesion')
            
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
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def inicio_sesion(request):
    if request.method == 'GET':
         return render(request,'iniciar_sesion.html',{
            'form': AuthenticationForm
        }) 
    else:
        print(request.POST)
        #autenticar que el usuario y contraseña se enecuentren en la base de datos
        user = authenticate(request, username=request.POST['username'], password=request.POST['password']) 

        if user is None: #Si no se encuentra el usuario y contraseña
            return render(request, 'iniciar_sesion.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos',
            })
        else:
            login(request,user) #guardar su sesión
            return redirect('home')
    
