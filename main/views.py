from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def saludo(request):
    return HttpResponse('hola mundo')
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def servicios(request):
    return render(request,'servicios.html')

def contacto(request):
    return render(request,'contacto.html')

def acerca(request):
    return render(request,'acerca.html')

def preguntasfrec(request):
    return render(request,'preguntasfrec.html')

def panelEncargado(request):
    return render(request, 'panelEncargado.html')