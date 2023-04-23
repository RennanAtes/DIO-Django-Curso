from django.shortcuts import render, HttpResponse
from .models import Evento
# Create your views here.
def eventos_titulo(request,titulo_evento):
    Eventos = Evento.objects.get(titulo = titulo_evento)
    local_evento = Eventos.usuario
    return HttpResponse(f'{local_evento}')