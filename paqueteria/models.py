# -*- coding: utf-8 -*-
from django.db import models
import string
class Mantenedor(models.Model):
    nombre_completo = models.CharField("nombre del mantenedor", max_length = 100)
    correo = models.EmailField("correo electronico del mantenedor", max_length= 75)
    
    
    def __unicode__(self):
        return self.nombre_completo
    
    '''
    def fue_publicado_recientemente(self):
        return self.fecha_pub >= timezone.now() - datetime.timedelta(days=1)
    fue_publicado_recientemente.short_description = 'Publicación reciente?'

    def fue_publicado_hoy(self):
        return self.fecha_pub.date() == datetime.date.today()
    fue_publicado_hoy.spaquetes = models.ManyToManyField('self', null=True, symmetrical = False, blank=True)hort_description = "Publicado hoy?"
    '''
    
    class Meta:
        ordering = ["nombre_completo"]
        
class DependenciaSimple(models.Model):
    dep = models.ForeignKey('Paquete')

    def __unicode__(self):
         return self.dep.nombre

class DependenciaOR(models.Model):
    dep = models.ManyToManyField(DependenciaSimple, null=True, symmetrical = False, blank=True)
     
    def __unicode__(self): 
        x = ""
        for i in self.dep.only():
            x += i.dep.nombre + " | "
        return string.strip(x, "| ") 
    
class Paquete(models.Model):
    mantenedor = models.ForeignKey(Mantenedor, verbose_name = "nombre del mantenedor")
    nombre = models.CharField("nombre del paquete", max_length = 100)
    arquitectura = models.CharField("arquitectura del paquete", max_length = 10, choices = (
                     ('all', 'all'),
                     ('i386', 'i386'),
                     ('amd', 'amd'),
    ))
    dependenciaSimple = models.ManyToManyField(DependenciaSimple, null=True, symmetrical = False, blank=True)
    dependenciaOR = models.ManyToManyField(DependenciaOR, null=True, symmetrical = False, blank=True)
    
    class Meta:
        ordering = ["nombre"]
    
    def __unicode__(self):
        return self.nombre    