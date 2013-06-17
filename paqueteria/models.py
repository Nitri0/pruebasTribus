# -*- coding: utf-8 -*-
from django.db import models

class Mantenedor(models.Model):
    nombre_completo = models.CharField("nombre del mantenedor", max_length = 100)
    correo = models.EmailField("correo electronico del mantenedor", max_length= 75)
    paquetes = models.ManyToManyField('self', null=True, symmetrical = False, blank=True)
    
    
    def __unicode__(self):
        return self.nombre_completo
    
    '''
    def fue_publicado_recientemente(self):
        return self.fecha_pub >= timezone.now() - datetime.timedelta(days=1)
    fue_publicado_recientemente.short_description = 'Publicación reciente?'

    def fue_publicado_hoy(self):
        return self.fecha_pub.date() == datetime.date.today()
    fue_publicado_hoy.short_description = "Publicado hoy?"
    '''
    
    class Meta:
        ordering = ["nombre_completo"]

class Paquete(models.Model):
    mantenedor = models.ForeignKey(Mantenedor, verbose_name = "nombre del mantenedor")
    # Deberia ser un text field
    nombre = models.CharField("nombre del paquete", max_length = 100)
    arquitectura = models.CharField("arquitectura del paquete", max_length = 10, choices = (
                     ('all', 'all'),
                     ('i386', 'i386'),
                     ('amd', 'amd'),
    ))
    dependencias = models.ManyToManyField('self', null=True, symmetrical = False, blank=True)
    
    class Meta:
        ordering = ["nombre"]
    
    def __unicode__(self):
        return self.nombre
    
