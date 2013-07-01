# Create your views here.

# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, render_to_response
from paqueteria.models import Paquete,Mantenedor,DependenciaSimple,DependenciaOR
from django.core.context_processors import request
#from form import *




def index(request):
    pqt = Paquete.objects.all()
    contexto = {"pqt":pqt}
    return render(request,'encuestas/paquetes.html', contexto)

# def search (request):
#     query = request.Get.get('q', '')
#     if query:
#         qset =(
#               Q(Mantenedor__nombre__icontains = query) |
#               Q(Paquete__nombre__icontains = query) |
#               Q(Paquete__descripcion__icontains = query)
#               )
#         result = Paquete.objects.filter(qset).distinct()
#     else:
#         result = []
#     return render_to_response ("encuentas/search.html",{
#                                         "request" : request,
#                                         "query" : query} 
#                                )
        


def contacto (request):
    pass

def inicio (request):
    return render(request, 'encuestas/inicio.html')


def busqueda(request,pqt):
    print pqt
    x = Paquete.objects.all().get(nombre = pqt)
    contexto = {"i":x}
    return render(request,'encuestas/detalles.html', contexto)
    
# 
# def busqueda(request,paquete):
#     print paquete
#     pqt = Paquete.objects.all().filter(nombre = paquete)
#     contexto = {"i":pqt}
#     return render (request,'encuestas/detalles.html', contexto)
    


#def busqueda (request, valor):
    

'''
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