from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def saludo(request):
    return HttpResponse('hola mundo')
def home(request):
    return render(request,'home.html')

def registro(request):
    return render(request,'registro.html')

def login(request):
    return render(request,'login.html')


def servicios(request):
    return render(request,'servicios.html')
