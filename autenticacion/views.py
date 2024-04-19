from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from .models import Servicio
from .forms import RegistrarUsuario,CitaForm, ImagenForm
from .models import Cita,DetalleCita,Servicio,Fase, ImagenFase,Servicio
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError #Error de integridad en la base de datos, para manejar la excepción
from django.contrib.auth.decorators import login_required #Función decoradora para verificar que haya un usuario logeado (Protejer URL's)

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
@login_required 
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

@login_required         
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
            
@login_required             
def lista_citas_cliente(request):
    citas_cliente = Cita.objects.filter(usuario = request.user)
    titulo = "Citas del cliente"
    return render(request, "lista_citas_cliente.html",{
        'titulo': titulo,
        'citas' : citas_cliente,
    })
    
    

'''def estatus_cita(request,cita_id):
    cita = get_object_or_404(Cita, id = cita_id, usuario = request.user)
    print(cita)
    # Renderizar el template de estatus de cita con la información de la cita
    return render(request, 'estatus_cita.html', {'cita': cita})'''

    
@login_required
def panel_encargado(request):
    citas_pendientes = Cita.objects.filter(estado='pendiente')
    citas_en_proceso = Cita.objects.filter(estado='en proceso')
    citas_finalizadas = Cita.objects.filter(estado='finalizada')
    
    print("Citas en espera: ",citas_pendientes.count())
    for cita1 in citas_pendientes:
        print(cita1)
    
    print("Citas en proceso: ", citas_en_proceso.count())
    for cita2 in citas_en_proceso:
        print(cita2)
        
  
    print("Citas finalizadas: " , citas_en_proceso.count())
    for cita3 in citas_en_proceso:
        print(cita3)
    
    return render(request, 'panelEncargado.html', {
        'citas_en_espera': citas_pendientes,
        'citas_en_proceso': citas_en_proceso,
        'citas_finalizadas': citas_finalizadas
    })
    
@login_required
def detalle_cita_enProceso(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, estado="en proceso")
    servicios_cita = cita.detallecita_set.all()
    servicios = [detalle_cita.servicio for detalle_cita in servicios_cita]
    print(servicios)
    return render(request, 'detalle_cita_enProceso.html', {
        'cita': cita,
        'servicios': servicios,
    })
    
@login_required
def detalle_servicio(request, cita_id, servicio_id):
    cita = get_object_or_404(Cita, id=cita_id, estado="en proceso")
    servicio = get_object_or_404(Servicio,id = servicio_id)
    fases_servicio = servicio.fase_set.all()
    
    
    print(f"Servicio: {servicio}")
    print(f"Fases asociadas: {fases_servicio}")
    return render(request, 'detalle_servicio.html',{
        'cita': cita,
        'servicio':servicio,
        'fases_servicio': fases_servicio,
    })
    
@login_required  
def subir_imagen(request, fase_id):
    if request.method == 'POST':
        cita_id = request.POST.get('cita_id')
        fase_id = request.POST.get('fase_id')
        servicio_id = request.POST.get('servicio_id')
        imagen=request.FILES['imagen']
        
        fase = get_object_or_404(Fase,id=fase_id)
        cita = get_object_or_404(Cita, id=cita_id)
        servicio = get_object_or_404(Servicio, id=servicio_id)
        
        print(f"id cita: {cita_id}, servicio: {servicio_id}, fase: {fase_id}")
      
        # Guardar la imagen en la tabla ImagenFase
        imagen_fase = ImagenFase(cita = cita, servicio = servicio, fase = fase, imagen = imagen)
        imagen_fase.save()
        return redirect('detalle_servicio', cita_id = cita_id, servicio_id = servicio_id)

    else:
        return redirect('detalle_servicio', cita_id = cita_id, servicio_id = servicio_id)
    
@login_required
def eliminar_imagen(request, fase_id):
    cita_id = request.POST.get('cita_id')
    fase_id = request.POST.get('fase_id')
    servicio_id = request.POST.get('servicio_id')
    
    imagen_fase = get_object_or_404(ImagenFase, fase = fase_id)
    imagen_fase.delete()
    return redirect('detalle_servicio', cita_id = cita_id, servicio_id = servicio_id)

    
@login_required
def modificar_estado_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    # Modificar el estado de la cita de "en espera" a "en proceso"
    cita.estado = 'en proceso'
    cita.save()
    return redirect('panel_encargado')

def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    # Eliminar la cita de la base de datos
    cita.delete()
    return redirect('panel_encargado')

#tomar los servicios de la base de datos y mostrarlos en servicios.html
def lista_de_servicios(request):
    print("Servicios")
    print("La vista lista_de_servicios se está ejecutando.")  # Agregar este mensaje de prueba
    servicios = Servicio.objects.all()
    print(servicios)  # Agregar esta línea para verificar si se están recuperando los servicios correctamente
    return render(request, 'servicios.html', {'servicios': servicios})




