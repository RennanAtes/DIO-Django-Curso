from django.shortcuts import render, HttpResponse, redirect
from .models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def login_view(request):
    return render(request, 'login.html')


def submit_login(request):

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request,"Usuário ou senha inválido")
    
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')


def eventos_titulo(request,titulo_evento):
    Eventos = Evento.objects.get(titulo = titulo_evento)
    local_evento = Eventos.usuario
    return HttpResponse(f'{local_evento}')

@login_required(login_url='/login/')
def lista_eventos(request):

    usuario = request.user

    evento = Evento.objects.filter(usuario=usuario)
    context = { 
        'eventos': evento            
                }
    return render(request, 'agenda.html', context)

#def index(request):
#    return redirect('/agenda/')

@login_required(login_url='/login/')
def evento(request):
    if request.POST:

        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user

        Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              descricao=descricao,
                              usuario=usuario,
                              
                              )
        return redirect('/')
    return render(request,'evento.html')