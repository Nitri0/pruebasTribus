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
            # si la seccion es nula, es probable que se trate de un paquete virtual
            # por lo tanto creamos aqui un paquete solo con el nombre
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
        if dep in blacklist:
            print "En algun momento paso por aqui de verdad?"
            continue
        d = dep.nombre
        sect = buscar_seccion(d, archivo)
        if sect != None:
            depsim = buscar_dep_simple(sect)
            depsim.save()
            paquete.dependenciaSimple.add(depsim)
        else:
            blacklist.append(d)
            
def registrar_dependencias_comp(npaquete, lista_dependencias, archivo):
    if lista_dependencias:
        for dep in lista_dependencias:
            sec = buscar_seccion(npaquete, archivo)
            depcomp = buscar_dep_comp(sec, dep)
            if depcomp.dep.all():
                print "No hago nada porque ya estan registradas las dependencias"
            else:
                for d in dep:
                    n = d.nombre
                    sect = buscar_seccion(n, archivo)
                    #if sect != None:
                    ds = buscar_dep_simple(sect, n)
                    ds.save()
                    depcomp.dep.add(ds)
                    #else:
                    #    print "Probablemente se trate de un paquete virtual: ", n
                        # Como puedo crear una dependencia hacia un paquete virtual?
                        # el paquete virtual no saldra en la lista y necesito informacion
                        # para registrarlo debidamente.
                        # Conceptualmente hay un fallo aqui porque el modelo planteado 
                        # solo permite el registro de depencias que esten en la lista
                        # mientras que las dependencias virtuales no son tomadas en cuenta
                        # esto puede resolverse agregando un modelo para representar las
                        # dependencias virtuales.
                        # Lo ideal seria que pudiera registrar juntas dependencias reales y dependencias
                        # virtuales, pero algo me dice que no podre =/ por restricciones de la clave 
                        # foranea que me pedira un mismo tipo de objeto al cual referenciar.
                        # La unica solucion que se me ocurre por el momento es modificar el modelo 
                        # paquete para que acepte valores nulos y vacios en todos sus campos, menos en el nombre
                        # de modo que pueda registrar paquetes solo con su nombre, lo cual representaria 
                        # los paquetes virtuales. En teoria esta solucion mantendria el concepto original 
                        # y resuelve el conflicto de los paquetes virtuales sin muchas consecuencias.
                        # Seria util agregar unas consultas para demostrar la utilidad de este concepto, 
                        # es decir consultas que soliciten todos los paquetes que dependen de X dependencia
                        # simple o compuesta
                       
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
        
a1 = apt_pkg.TagFile(open('/home/usuario/Packages'))
blacklist = []
registrar_paquetes(a1)