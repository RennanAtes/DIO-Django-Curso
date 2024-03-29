from django.shortcuts import render, HttpResponse, redirect
from .models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.contrib.auth.models import User
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
    print('passou por aqui')
    return HttpResponse(f'{local_evento}')

@login_required(login_url='/login/')
def lista_eventos(request):

    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)

    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt = data_atual)
    context = { 
        'eventos': evento            
                }
    return render(request, 'agenda.html', context)

#def index(request):
#    return redirect('/agenda/')

@login_required(login_url='/login/')
def evento(request):

    id_evento = request.GET.get('id')
    usuario = request.user
    dados ={ }
    if not id_evento is None:
        evento = Evento.objects.get(id=id_evento)
    #Verificando se o usuario e dono daquela agenda
    if id_evento and evento.usuario == usuario :
        dados['evento'] = Evento.objects.get(id = id_evento)
    # Se não for, verifica e redireciona ele para a página inicial
    elif id_evento and not evento.usuario == usuario:
        return redirect('/')
    
    # method='POST' para criar ou editar uma agenda.
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        id_evento = request.POST.get('id_evento')

        #Se o id_evento for verdadeiro, quer dizer que é para editar.
        if id_evento:

            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()


            #Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                       #data_evento = data_evento,
                                                       #descricao = descricao)
        else: 
            Evento.objects.create(titulo=titulo,
                                data_evento=data_evento,
                                descricao=descricao,
                                usuario=usuario,
                                )
        return redirect('/')
    return render(request,'evento.html', dados)


@login_required(login_url='/login/')
def delete_evento(request, id_evento):

    user = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    if user == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento), safe=False)