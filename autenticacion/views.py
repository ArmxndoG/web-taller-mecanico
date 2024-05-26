from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User
from .models import Servicio
from .forms import RegistrarUsuario,CitaForm, ServicioForm, ImagenForm
from .models import Cita,DetalleCita,Servicio,Fase, ImagenFase,Servicio
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError #Error de integridad en la base de datos, para manejar la excepción
from django.contrib.auth.decorators import login_required #Función decoradora para verificar que haya un usuario logeado (Protejer URL's)
from django.contrib import messages

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
                #return render(request, 'iniciar_sesion.html')
            
            except IntegrityError:
                
                return render(request,'registro.html',{
                        'form': RegistrarUsuario,
                        'error': 'El usuario ya existe, por favor inicie sesión'
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
                return redirect('panel_encargado')  
            else:
                # Usuario es un usuario regular
                login(request,user)
                return redirect('home')  
        else:
            return render(request, 'iniciar_sesion.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos',
            })

@login_required         
def agendarCita(request):
    if request.method == 'POST':
        cita_form = CitaForm(request.POST)
        if cita_form.is_valid():
            cita = cita_form.save(commit=False)
            cita.usuario = request.user
            cita.save()
            
            servicios_seleccionados = cita_form.cleaned_data['servicios']
            for servicio in servicios_seleccionados:
                DetalleCita.objects.create(cita=cita, servicio=servicio)

            # Mensaje de éxito
            messages.success(request, 'Tu cita se ha agendado con éxito.')

            # Detalles de la cita
            detalles_cita = {
                'modelo_carro': cita.modelo_carro,
                'color': cita.color,
                'placas': cita.placas,
                'fecha': cita.fecha,
                'hora': cita.hora,
                'servicios': [{'nombre': servicio.nombre, 'precio': servicio.precio} for servicio in cita.servicios.all()] 
            }

            return render(request, 'citas.html', {
                'form': CitaForm(),
                'exito': True,
                'detalles_cita': detalles_cita
            })
    else:
        cita_form = CitaForm()

    return render(request, 'citas.html', {
        'form': cita_form
        #'error': 'Algo salio mal, intente de nuevo'
    })
            
@login_required
def altaServicio(request):
    
    if request.method == 'GET':
        return render(request,'alta_servicio.html',{
            'form':ServicioForm
            
        })
    else:
        servicio_form = ServicioForm(request.POST)
        
        if servicio_form.is_valid():
            servicio = servicio_form.save(commit=False)
            servicio.save()#Guardando los datos en la cita
            
            return redirect('gestion_servicios')
        else:
            return render(request, 'citas.html',{
                'form': ServicioForm,
                'error': 'Algo salio mal, intente de nuevo'
            })
@login_required
def modificacion_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id = servicio_id)
    if request.method == 'GET':
        form = ServicioForm(instance = servicio)
        return render(request, 'modificacion_servicio.html',{
            'servicio': servicio,
            'form': form
        }) 
    else:
        try:
            form = ServicioForm(request.POST, instance = servicio)
            
            if form.is_valid():
                form.save()
                return redirect('gestion_servicios')

        except ValueError:
            return render(request, 'modificar_servicio',{
                'servicio': servicio,
                'form': form,
                'error': "Error al actualizar servicio",
                
            })
            
@login_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id = servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('gestion_servicios')
       

@login_required  
def detalle_cita_cliente(request,cita_id):
    cita = get_object_or_404(Cita, id = cita_id, usuario = request.user)
    detalles_cita = cita.detallecita_set.all()
    print(detalles_cita)
    if request.method == 'GET':
        form = CitaForm(instance = cita)
        return render(request,'detalle_cita_cliente.html',{
            'cita': cita,
            'form':form,
            'titulo': "Modificación de cita" 
        })
    else:
        try:
            form = CitaForm(request.POST, instance = cita)
            
            if form.is_valid():
                form.save()
                # Actualizar los servicios de la cita
                servicios_seleccionados = form.cleaned_data['servicios']
                print(f"Servicios seleccionados: {servicios_seleccionados}")
                cita.servicios.set(servicios_seleccionados)
                 # Actualizar los detalles de la cita
                for detalle in detalles_cita:
                    detalle.servicio = detalle.cita.servicios.first()  # Asignar el primer servicio seleccionado
                    print(cita.detallecita_set.all())
                return redirect('lista_citas_cliente')

        except ValueError:
            return render(request, 'detalle_cita_cliente',{
                'cita': cita,
                'form': form,
                'error': "Error al actualizar cita",
                'titulo': "Modificación de cita"
            })
@login_required
def gestion_servicios(request):
    servicios = Servicio.objects.all()
    print(servicios)
    
    return render(request, "gestionServicios.html",{
        "servicios": servicios
    })

         
@login_required             
def lista_citas_cliente(request):
    #citas_cliente = Cita.objects.filter(usuario = request.user)
    citas_en_espera = Cita.objects.filter(usuario = request.user, estado = "pendiente")
    citas_en_proceso = Cita.objects.filter(usuario = request.user, estado = "en proceso")
    citas_finalizadas = Cita.objects.filter(usuario = request.user, estado = "finalizada")
    print(citas_finalizadas)
    titulo = "Citas del cliente"
    return render(request, "lista_citas_cliente.html",{
        'titulo': titulo,
        'citas_en_espera' : citas_en_espera,
        'citas_en_proceso' : citas_en_proceso,
        'citas_finalizadas' : citas_finalizadas,
    })
    
@login_required 
def eliminar_cita_cliente(request, cita_id):
    cita = get_object_or_404(Cita, id = cita_id, usuario = request.user)
    if request.method == 'POST':
        cita.delete()
        return redirect('lista_citas_cliente')
  
            
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
    

'''def estatus_cita(request, cita_id):
    # Obtener la cita
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Obtener todas las imágenes asociadas a la cita
    imagenes_fase = ImagenFase.objects.filter(cita_id=cita_id)
    
    # Obtener todos los servicios asociados a la cita
    servicios = cita.servicios.all()
    
    # Crear un diccionario para almacenar el progreso de cada servicio
    progreso_servicios = {}

    for servicio in servicios:
        # Obtener todas las fases para el servicio actual
        fases = Fase.objects.filter(servicio=servicio)
        total_fases = fases.count()
        
        # Contar cuántas fases tienen imágenes
        fases_con_imagen = imagenes_fase.filter(servicio=servicio).values('fase').distinct().count()
        
        # Calcular el porcentaje de progreso
        if total_fases > 0:
            porcentaje_progreso = (fases_con_imagen / total_fases) * 100
        else:
            porcentaje_progreso = 0
        
        # Guardar el progreso en el diccionario
        progreso_servicios[servicio.id] = {
            'total_fases': total_fases,
            'fases_con_imagen': fases_con_imagen,
            'porcentaje_progreso': porcentaje_progreso
        }
        print(progreso_servicios)

    return render(request, 'estatus_cita.html', {
        'cita': cita,
        'servicios': servicios,
        'progreso_servicios': progreso_servicios,
    })'''
@login_required
def estatus_cita(request, cita_id):
    # Obtener la cita
    cita = get_object_or_404(Cita, id=cita_id)
    # Obtener todas las imágenes asociadas a la cita
    imagenes_fase = ImagenFase.objects.filter(cita_id=cita_id)
    
    servicios = cita.servicios.all()
    print(servicios)
    
    

    # Lista para almacenar información adicional sobre las imágenes de la fase
    info_imagenes_fase = []

    # Iterar sobre las imágenes de la fase
    for imagen_fase in imagenes_fase:
        # Obtener el servicio y la fase asociados a la imagen de la fase actual
        servicio_id = imagen_fase.servicio_id
        fase_id = imagen_fase.fase_id
        # Agregar la información de la imagen, el servicio y la fase a la lista
        info_imagenes_fase.append({'imagen_fase': imagen_fase, 'servicio_id': servicio_id, 'fase_id': fase_id})

    return render(request, 'estatus_cita.html', {
        
        'cita': cita,
        'info_imagenes_fase': info_imagenes_fase,
        'servicios': servicios
    })
    
'''@login_required
def estatus_cita(request, cita_id):
    print(cita_id)
    cita = get_object_or_404(Cita, id = cita_id)
    servicios_cita = cita.detallecita_set.all()
    servicios = [detalle_cita.servicio for detalle_cita in servicios_cita]
    
    # Lista para almacenar la información de cada servicio
    info_servicios = []

    # Iterar sobre cada servicio
    for servicio in servicios:
        # Obtener las fases asociadas al servicio
        fases_servicio = servicio.fase_set.all()

        # Lista para almacenar la información de cada fase
        info_fases = []

        # Iterar sobre cada fase
        for fase in fases_servicio:
            # Obtener las imágenes asociadas a la fase
            imagenes_fase = fase.imagenfase_set.all()

            # Agregar la información de la fase a la lista
            info_fases.append({
                'fase': fase,
                'imagenes': imagenes_fase
            })

        # Agregar la información del servicio y sus fases a la lista de servicios
        info_servicios.append({
            'servicio': servicio,
            'fases': info_fases
        })

    # Pasar los datos a la plantilla
    return render(request, 'estatus_cita.html', {
        'cita': cita,
        'servicios': info_servicios
    })'''
 
    
    
    
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
    servicio = get_object_or_404(Servicio, id=servicio_id)
    fases_servicio = servicio.fase_set.all()
    fase_imagen_asociada = []  # Lista de listas para almacenar información

    for fase in fases_servicio:
        if ImagenFase.objects.filter(cita=cita, servicio=servicio, fase=fase).exists():
            imagen_fase = ImagenFase.objects.get(cita=cita, servicio=servicio, fase=fase)
            fase_imagen_asociada.append([fase, True, imagen_fase])
        else:
            fase_imagen_asociada.append([fase, False, None])

    return render(request, 'detalle_servicio.html', {
        'cita': cita,
        'servicio': servicio,
        'fase_imagen_asociada': fase_imagen_asociada,
    })
    
'''@login_required
def detalle_servicio(request, cita_id, servicio_id):
    cita = get_object_or_404(Cita, id=cita_id, estado="en proceso")
    servicio = get_object_or_404(Servicio, id=servicio_id)
    fases_servicio = servicio.fase_set.all()
    #fases_asociadas = get_object_or_404(ImagenFase, cita = cita_id, servicio = servicio_id)
    #print(fases_asociadas)
    imagen_asociada_fase = {}  # Diccionario para almacenar imagen por ID de fase
    fase_imagen_asociada = []  # Lista de listas para almacenar información
    
    for fase in fases_servicio:
        if ImagenFase.objects.filter(cita=cita.id, servicio=servicio.id, fase=fase.id).exists():
            imagen_asociada_fase[fase.id] = True
            imagen_asociada = imagen_asociada_fase[fase.id]
            fase_imagen_asociada.append([cita.id,servicio.id,fase.id, imagen_asociada])
        else:
            imagen_asociada_fase[fase.id] = False
            
    
    print(f"Fases - tiene imagen: {imagen_asociada_fase}")

    
        
    print(f"fase imagen asociada {fase_imagen_asociada}")
    
    for fase, imagen_asociada in fase_imagen_asociada:
        if imagen_asociada:
            print("img/url\t Subir imagen")
        elif imagen_asociada is None:
            print("Subir imagen")
    
    return render(request, 'detalle_servicio.html', {
        'cita': cita,
        'servicio': servicio,
        'fases_servicio': fases_servicio,
        'fase_imagen_asociada': fase_imagen_asociada,
        #'fases_asociadas': fases_asociadas
    })'''
    
'''@login_required
def detalle_servicio(request, cita_id, servicio_id):
    cita = get_object_or_404(Cita, id=cita_id, estado="en proceso")
    servicio = get_object_or_404(Servicio,id = servicio_id)
    fases_servicio = servicio.fase_set.all()#Me devuelve las fases de ese servicio 
    
    #imagen_asociada_fase = []
    imagen_asociada_fase = {}
    print(f"Cita: {cita.id}")
    print(f"Servicio: {servicio.id}")
    print(f"Fases asociadas: {fases_servicio}")
    
    #Lista que devuelve True si hay un registro en la tabla ImagenFase y false si no hay un registro     
    for fase in fases_servicio:
        print(fase.id, fase.nombre)
        if ImagenFase.objects.filter(cita = cita.id, servicio = servicio.id, fase=fase.id).exists():
            #imagen_asociada_fase.append(True)
            imagen_asociada_fase[fase.id] = True
        else:
            #imagen_asociada_fase.append(False)
            imagen_asociada_fase[fase.id] = False
                
   
    print(f"tiene imagenes {imagen_asociada_fase}")

  
    return render(request, 'detalle_servicio.html',{
        'cita': cita,
        'servicio':servicio,
        'fases_servicio': fases_servicio,
        'imagen_asociada_fase':imagen_asociada_fase
        
    })'''
    
   
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
@login_required
def modificar_estado_cita_finalizada(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    # Modificar el estado de la cita de "en espera" a "en proceso"
    cita.estado = 'finalizada'
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




