# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.db import models

class Encuesta(models.Model):
    pregunta = models.CharField(max_length=100)
    fecha_pub = models.DateTimeField('Fecha de publicación')
    
    def __unicode__(self):
        return self.pregunta
    
    def fue_publicado_recientemente(self):
        return self.fecha_pub >= timezone.now() - datetime.timedelta(days=1)
    fue_publicado_recientemente.short_description = 'Publicación reciente?'

    def fue_publicado_hoy(self):
        return self.fecha_pub.date() == datetime.date.today()
    fue_publicado_hoy.short_description = 'Publicado hoy?'

class Eleccion(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    eleccion = models.CharField(max_length=100)
    votos = models.IntegerField()

    def __unicode__(self):
        return self.eleccion
