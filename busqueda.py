import email.Utils, re, string
#from django.core.management import setup_environ
#from pruebasTribus import settings
from apt import apt_pkg
#from paqueteria.models import Mantenedor, Paquete
#setup_environ(settings)
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

def pkg_solver(paquete, nombre_archivo):
    print "##########################################"
    print "RESOLVIENDO DEPENDENCIAS DE: ", paquete
    print "##########################################"
    seccion = buscar(paquete, nombre_archivo)
    #print "SECCION: "
    #print seccion
    #print "##########################################"
    dependencias = listar_dependencias(seccion)
    #print "##########################################"
    #print "DEPENDENCIAS LOCALIZADAS: "
    #print dependencias
    #print "##########################################"
    lista_dep_op = [string.strip(n, " ") for n in dependencias]
    #print "##########################################"
    for d in lista_dep_op:
        if re.findall("\|", d):
            d = string.splitfields(d, " | ", 1)
            print d
        elif re.findall("\s", d): 
            d = string.splitfields(d, " ", 1)
            print d
            for x in listar_dependencias(buscar(d[0], nombre_archivo)):
                pkg_solver(x, nombre_archivo)
        else:
            print d
            for x in listar_dependencias(buscar(d, nombre_archivo)):
                pkg_solver(x, nombre_archivo)
                 
def listar_dependencias(seccion): 
    if seccion == None:
        print "No se ha encontrado el paquete o no hay mas dependencias"
        return ""
    else:
        deps = seccion.get('Depends')
        if deps != None:    
            return string.splitfields(deps, ",")
        else:
            return ""

def buscar(paquete, nombre_archivo):
    nombre_archivo.jump(0)
    for section in nombre_archivo:
        if section.get('Package') == paquete:
            return section

pkg_solver("blender", paquetes)