from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def saludo(request):
    return HttpResponse('hola mundo')

def registro(request):
    return HttpResponse('Registro')