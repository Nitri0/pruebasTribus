# Create your views here.
'''
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from encuestas.models import Encuesta

def index(request):
    ultima_lista_encuestas = Encuesta.objects.order_by('-fecha_pub')[:5]
    contexto = {'ultima_lista_encuestas': ultima_lista_encuestas}    
    return render(request, 'encuestas/index.html', contexto)

def detalles(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, pk=encuesta_id)
    return render(request, 'encuestas/detalles.html', {'encuesta': encuesta})
    
def resultados(request, encuesta_id):
    return HttpResponse("You're looking at the results of poll %s." % encuesta_id)

def votar(request, encuesta_id):
    return HttpResponse("You're voting on poll %s." % encuesta_id)
'''