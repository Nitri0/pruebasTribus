'''
V1 de ingreso de datos
'''

import email.Utils, re, string
from django.core.management import setup_environ
from pruebasTribus import settings
from apt import apt_pkg
from paqueteria.models import Mantenedor, Paquete, DependenciaSimple, DependenciaOR 

setup_environ(settings)
apt_pkg.init()

class dependencia_simple(object):
    def __init__(self, nombre, version = None):
        self.nombre = nombre
        self.version = version
    
def buscar_seccion(paquete, archivo):
    archivo.jump(0)
    for section in archivo:   
        if section.get('Package') == paquete:
            return section

def buscar_mantenedor(seccion):
    nombreMan, correoMan = email.Utils.parseaddr(seccion.get("Maintainer"))
    mantenedorActual = Mantenedor.objects.filter(nombre_completo = nombreMan, correo = correoMan)
    if len(mantenedorActual) == 1:
        return mantenedorActual[0]
    else:
        nMantenedor = Mantenedor(nombre_completo = nombreMan, correo = correoMan)
        nMantenedor.save()
    return nMantenedor

def buscar_paquete(seccion, npaquete = None):
    if seccion != None:
        nombre_pq = seccion.get("Package")
        instsize_pq = seccion.get("Installed-Size")
        version_pq = seccion.get("Version")
        mantenedor_paquete = buscar_mantenedor(seccion)
        arquitectura_pq = seccion.get("Architecture")
        size_pq = seccion.get("Size")
        sha256_pq =  seccion.get("SHA256") 
        sha1_pq = seccion.get("SHA1")
        md5sum_pq = seccion.get("MD5sum")
        descripcion_pq = seccion.get("Description")
        pagina_pq = seccion.get("Homepage")
        desmd5_pq = seccion.get("Description-md5")
        sec_pq = seccion.get("Section")
        prioridad_pq = seccion.get("Priority")
        nombrearchivo_pq = seccion.get("Filename")
        paquete_existe = Paquete.objects.filter(nombre = nombre_pq, md5sum = md5sum_pq)
        if len(paquete_existe):
            return paquete_existe[0]
        else:
            nPaquete = Paquete(nombre = nombre_pq, version = version_pq, size = size_pq,
                               instsize = instsize_pq, sha256 = sha256_pq, sha1 = sha1_pq,
                               mantenedor = mantenedor_paquete, desmd5 = desmd5_pq,
                               descripcion = descripcion_pq, pagina = pagina_pq, seccion = sec_pq,
                               prioridad = prioridad_pq, nombrearchivo = nombrearchivo_pq,
                               arquitectura = arquitectura_pq, md5sum = md5sum_pq)
            nPaquete.save()
            return nPaquete
    else:
        if npaquete:
            # Registro de paquete virtual
            nPaquete = Paquete(nombre = npaquete)
            nPaquete.save()
            return nPaquete
     
def listar_dependencias(seccion):
    dependencias = {}
    dependencias["simples"] = []
    dependencias["comp"] = []
    if seccion == None or seccion.get('Depends') == None:
        return dependencias
    else:
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
                dependencias["comp"].append(tmpls)
            
            elif re.findall("\s", d):                
                obj = string.splitfields(d, " ", 1)
                sp = dependencia_simple(obj[0], obj[1])
                dependencias["simples"].append(sp)
            else:
                sp = dependencia_simple(d)
                dependencias["simples"].append(sp)
        return dependencias
    
def buscar_dep_simple(seccion, npaq = None):
    paquete = buscar_paquete(seccion, npaq)
    dep_existe = DependenciaSimple.objects.filter(dep = paquete)
    if len(dep_existe):
        return dep_existe[0]
    else:
        dep_simple = DependenciaSimple(dep = paquete)
        dep_simple.save()
        return dep_simple

def buscar_dep_comp(seccion, dep):
    paquete = buscar_paquete(seccion)
    dep_existe = DependenciaOR.objects.filter(dep__dep__nombre = dep[0].nombre)
    if len(dep_existe):
        return dep_existe[0]
    else:
        depcomp = DependenciaOR()
        depcomp.save()
        paquete.dependenciaOR.add(depcomp)
        return depcomp
    
def registrar_dependencias_simples(paquete, lista_dependencias, archivo):
    for dep in lista_dependencias:
        d = dep.nombre
        sect = buscar_seccion(d, archivo)
        if sect != None:
            depsim = buscar_dep_simple(sect)
            depsim.save()
            paquete.dependenciaSimple.add(depsim)
        
def registrar_dependencias_comp(npaquete, lista_dependencias, archivo):
    if lista_dependencias:
        for dep in lista_dependencias:
            sec = buscar_seccion(npaquete, archivo)
            depcomp = buscar_dep_comp(sec, dep)
            if not depcomp.dep.all():
                for d in dep:
                    n = d.nombre
                    sect = buscar_seccion(n, archivo)
                    ds = buscar_dep_simple(sect, n)
                    ds.save()
                    depcomp.dep.add(ds)
                    
def comparar_con_archivo2(archivo):
    lista_diff = []
    archivo.jump(0)
    archivo.jump(0)
    #lista_paquetes = Paquete.objects.all()
    for section in archivo:
        pq = Paquete.objects.filter(nombre = section.get('Package'))  
        if pq:
            if section.get('MD5sum') == pq[0].md5sum:
                print "El paquete", section.get('Package'), "no ha sufrido modificaciones"
            else:
                lista_diff.append(section)
    return lista_diff
    
def registrar_paquetes(archivo):
    tmpoffset = 0
    seccionvalida = True
    archivo.step()
    while seccionvalida:
        seccion_actual = a1.section
        print seccion_actual.get("Package")
        tmpoffset = archivo.offset()
        paquete = buscar_paquete(seccion_actual)
        dict_dep = listar_dependencias(seccion_actual)
        registrar_dependencias_simples(paquete, dict_dep["simples"], archivo)
        registrar_dependencias_comp(paquete.nombre, dict_dep["comp"], archivo)
        archivo.jump(tmpoffset)
        archivo.jump(tmpoffset) #Misterios de la ciencia, puede ser un bug del apt_pkg
        seccionvalida = archivo.step()
        
a1 = apt_pkg.TagFile(open('/home/fran/Packages'))
#registrar_paquetes(a1)

#lista = comparar_con_archivo(a1)
lista = comparar_con_archivo2(a1)
print lista