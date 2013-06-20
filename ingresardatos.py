import email.Utils
from django.core.management import setup_environ
from pruebasTribus import settings
from apt import apt_pkg
from paqueteria.models import Mantenedor, Paquete, DependenciaSimple, DependenciaOR
import re, string

setup_environ(settings)
apt_pkg.init()

class dependencia_simple(object):
    def __init__(self, nombre, version = None):
        self.nombre = nombre
        self.version = version

def buscar_seccion(paquete, archivo):
    parar = True
    
    while parar != False:
        parar = archivo.step()
        if archivo.section.get('Package') == paquete:
            return archivo.section
    a1.jump(0)
        
def buscar_mantenedor(seccion):
    nombreMan, correoMan = email.Utils.parseaddr(seccion.get("Maintainer"))
    mantenedorActual = Mantenedor.objects.filter(nombre_completo = nombreMan, correo = correoMan)
    if len(mantenedorActual) == 1:
        return mantenedorActual[0]
    else:
        nMantenedor = Mantenedor(nombre_completo = nombreMan, correo = correoMan)
        nMantenedor.save()
    return nMantenedor

def buscar_paquete(seccion):
    if seccion == None:
        return
    nombre_paquete = seccion.get("Package")
    mantenedor_paquete = buscar_mantenedor(seccion)
    arqui_paquete = seccion.get("Architecture")
    md5_paquete = seccion.get("MD5sum")
    paquete_existe = Paquete.objects.filter(nombre = nombre_paquete, mantenedor = mantenedor_paquete,
                                            arquitectura = arqui_paquete, md5sum = md5_paquete)
    if len(paquete_existe):
        return paquete_existe[0]
    else:
        nPaquete = Paquete(nombre = nombre_paquete, mantenedor = mantenedor_paquete,
                           arquitectura = arqui_paquete)
        nPaquete.save()
        return nPaquete

def listar_dependencias(seccion):
    if seccion != None:
        if seccion.get('Depends') == None:
            return []
        lista_simple = []
        lista_or = []
        deps = string.splitfields(seccion.get('Depends'), ", ")
        for d in deps:
            if re.findall("\|", d):
                lista_or_raw = string.splitfields(d, " | ")
                tmpls = []
                for i in lista_or_raw:
                    if re.findall("\s", i):
                        obj = string.splitfields(i, " ", 1)
                        sp = dependencia_simple(obj[0], obj[1])
                        tmpls.append(sp)
                    else:
                        obj = string.splitfields(i, " ", 1)
                        sp = dependencia_simple(obj[0])
                        tmpls.append(sp)
                lista_or.append(tmpls)
                
            elif re.findall("\s", d):                
                obj = string.splitfields(d, " ", 1)
                sp = dependencia_simple(obj[0], obj[1])
                lista_simple.append(sp)

            else:
                sp = dependencia_simple(d)
                lista_simple.append(sp)
                
        #return lista_or, lista_simple
        return lista_simple
    else:
        return []
    
def buscar_dep_simple(seccion):
    paquete = buscar_paquete(seccion)
    if paquete == None:
        return
    dep_existe = DependenciaSimple.objects.filter(dep = paquete)
    if len(dep_existe) > 1:
        return dep_existe[0]
    else:
        dep_simple = DependenciaSimple(dep = paquete)
        dep_simple.save()
        return dep_simple
     
def registrar_dependencias(paquete, lista_dependencias, archivo):
    for dep in lista_dependencias:
        if dep in blacklist:
            continue
        d = dep.nombre
        sect = buscar_seccion(d, archivo)
        if sect != None:
            ds = buscar_dep_simple(sect)
            ds.save()
            paquete.dependenciaSimple.add(ds)
            
        else:
            blacklist.append(d)
            print "Probablemente", d, "sea un paquete virtual provisto por otro paquete, de momento no se registrara"

def registrar_paquetes(archivo):
    tmpoffset = 0
    parar = True
    while parar != False:
        archivo.jump(tmpoffset)
        parar = archivo.step()
        seccion_actual = a1.section
        tmpoffset = archivo.offset()
        paquete = buscar_paquete(seccion_actual)
        print paquete
        simple = listar_dependencias(seccion_actual)
        registrar_dependencias(paquete, simple, archivo)                

a1 = apt_pkg.TagFile(open('/home/fran/Packages'))

blacklist = []

#registrar_paquetes(a1)

sec = buscar_seccion("0ad", a1)
print sec
ceroad = buscar_paquete(sec)
print type(ceroad)
dep_ceroad = listar_dependencias(sec)
print dep_ceroad
registrar_dependencias(ceroad, dep_ceroad, a1)
