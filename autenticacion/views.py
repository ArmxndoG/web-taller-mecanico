from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from .forms import RegistrarUsuario,CitaForm
from .models import Cita,DetalleCita
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
         
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
    
            # Verifica el valor de is_staff
            if user.is_staff:
                # Usuario es un encargado
                login(request,user)
                return redirect('panel_encargado')  # Cambia 'vista_encargado' con la URL de la vista de encargado
            else:
                # Usuario es un usuario regular
                login(request,user)
                return redirect('home')  # Cambia 'home' con la URL de la página principal del usuario
        else:
            return render(request, 'iniciar_sesion.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos',
            })

            
def agendarCita(request):
    
    if request.method == 'GET':
        return render(request,'citas.html',{
            'form':CitaForm
            
        })
    else:
        cita_form = CitaForm(request.POST)
        
        if cita_form.is_valid():
            cita = cita_form.save(commit=False)
            cita.usuario = request.user #agregando el campo id_usuario con la sesión iniciada
            cita.save()#Guardando los datos en la cita
            
             # Obtener el servicio seleccionado en el checkbox
            servicios_seleccionados = cita_form.cleaned_data['servicios']

            for servicio in servicios_seleccionados:
                DetalleCita.objects.create(cita=cita, servicio=servicio, total=servicio.precio)#Damos de alta los datos en detalle_cita
            
            #form.save_m2m() #Guarda la relación muchos a muchos
            return redirect('home')
        else:
            return render(request, 'citas.html',{
                'form': CitaForm,
                'error': 'Algo salio mal, intente de nuevo'
            })
    
  

