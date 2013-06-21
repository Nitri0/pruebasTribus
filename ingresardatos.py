import email.Utils
#from django.core.management import setup_environ
#from pruebasTribus import settings
from apt import apt_pkg
from paqueteria.models import Mantenedor, Paquete, DependenciaSimple, DependenciaOR
import re, string

#setup_environ(settings)
apt_pkg.init()

class dependencia_simple(object):
    def __init__(self, nombre, version = None):
        self.nombre = nombre
        self.version = version

def buscar_seccion(paquete, archivo):
    seccionvalida = True
    archivo.step()
    print "Este es el nombre que estoy buscando", paquete
    while seccionvalida:
        seccionvalida = archivo.step()
        if archivo.section.get('Package') == paquete:
            return archivo.section
    a1.jump(0)
    
def buscar_seccion_for(paquete, archivo):
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

def buscar_paquete(seccion):
    if seccion != None:
        nombre = seccion.get("Package")
        instsize = seccion.get("Installed-Size")
        version = seccion.get("Version")
        mantenedor_paquete = buscar_mantenedor(seccion)
        arquitectura = seccion.get("Architecture")
        size = seccion.get("Size")
        sha256 =  seccion.get("SHA256") 
        sha1 = seccion.get("SHA1")
        md5sum = seccion.get("MD5sum")
        descripcion = seccion.get("Description")
        pagina = seccion.get("Homepage")
        desmd5 = seccion.get("Description-md5")
        sec = seccion.get("Section")
        prioridad = seccion.get("Priority")
        nombrearchivo = seccion.get("Filename")
        paquete_existe = Paquete.objects.filter(nombre = nombre, md5sum = md5sum)
        if len(paquete_existe):
            return paquete_existe[0]
        else:
            nPaquete = Paquete(nombre = nombre, version = version, size = size,
                               instsize = instsize, sha256 = sha256, sha1 = sha1,
                               mantenedor = mantenedor_paquete, desmd5 = desmd5,
                               descripcion = descripcion, pagina = pagina, seccion = sec,
                               prioridad = prioridad, nombrearchivo = nombrearchivo,
                               arquitectura = arquitectura, md5sum = md5sum)
            nPaquete.save()
            return nPaquete
    else:
        return
        
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
    
def buscar_dep_simple(seccion):
    paquete = buscar_paquete(seccion)
    dep_existe = DependenciaSimple.objects.filter(dep = paquete)
    if len(dep_existe):
        return dep_existe[0]
    else:
        dep_simple = DependenciaSimple(dep = paquete)
        dep_simple.save()
        return dep_simple
     
def registrar_dependencias_simples(paquete, lista_dependencias, archivo):
    for dep in lista_dependencias:
        if dep in blacklist:
            continue
        d = dep.nombre
        #sect = buscar_seccion(d, archivo)
        sect = buscar_seccion_for(d, archivo)
        if sect != None:
            depsim = buscar_dep_simple(sect)
            depsim.save()
            paquete.dependenciaSimple.add(depsim)
        else:
            blacklist.append(d)
            
def registrar_dependencias_comp(paquete, lista_dependencias, archivo):
    if lista_dependencias:
        for dep in lista_dependencias:
            depcomp = DependenciaOR()
            depcomp.save()
            paquete.dependenciaOR.add(depcomp) # Hasta aqui se que esta bien porque esta creando 3 instancias de dependenciasOR
            for d in dep:
                n = d.nombre
                print "##########"
                sect = buscar_seccion_for(n, archivo)
                #print n
                #print sect
                print "##########"
                if sect != None:
                    ds = buscar_dep_simple(sect)
                    ds.save()
                    depcomp.dep.add(ds)
                    
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
        registrar_dependencias_comp(paquete, dict_dep["comp"], archivo)
        archivo.jump(tmpoffset)
        archivo.jump(tmpoffset) #Misterios de la ciencia, puede ser un bug del apt_pkg
        seccionvalida = archivo.step()
        
a1 = apt_pkg.TagFile(open('/home/fran/Packages'))
blacklist = []
registrar_paquetes(a1)