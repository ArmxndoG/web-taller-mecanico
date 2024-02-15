from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def registro(request):
    
    if request.method == 'GET':
        return render(request,'registro.html',{
        'form': UserCreationForm
    })
    else:
        print(request)
        
    
    

def login(request):
    return render(request,'login.html')
