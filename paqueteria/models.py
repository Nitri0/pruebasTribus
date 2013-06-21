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
    '''
    
    class Meta:
        ordering = ["nombre_completo"]
        
class DependenciaSimple(models.Model):
    dep = models.ForeignKey('Paquete')

    def __unicode__(self):
        return self.dep.nombre
    
    class Meta:
        ordering = ["dep"]

class DependenciaOR(models.Model):
    dep = models.ManyToManyField(DependenciaSimple, null=True, symmetrical = False, blank=True)
    
    def __unicode__(self): 
        x = ""
        for i in self.dep.only():
            x += i.dep.nombre + " | "
        return string.strip(x, "| ")
    
class Paquete(models.Model):
    nombre = models.CharField("nombre del paquete", max_length = 150)
    version = models.CharField("version del paquete", max_length = 50)
    size = models.IntegerField("tamaño del paquete")
    instsize = models.IntegerField("tamaño una vez instalado")
    sha256 = models.CharField("SHA256 del paquete", max_length = 100)
    sha1 = models.CharField("SHA1", max_length = 100)
    md5sum = models.CharField("llave md5 del paquete", max_length = 75)
    descripcion = models.TextField("descripcion del paquete", max_length = 200)
    pagina = models.URLField("pagina web del paquete", max_length = 100, null = True)
    desmd5 = models.CharField("descripcion md5", max_length = 75, null = True)
    mantenedor = models.ForeignKey(Mantenedor, verbose_name = "nombre del mantenedor")
    seccion = models.CharField("seccion del paquete", max_length = 20)
    prioridad = models.CharField("prioridad del paquete", max_length = 20)
    nombrearchivo = models.CharField("nombre del archivo del paquete", max_length = 150)
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
    
    def show_data(self):
        print self.nombre
        print self.arquitectura
        print self.mantenedor
        print self.dependenciaSimple