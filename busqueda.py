import email.Utils, re, string
#from django.core.management import setup_environ
#from pruebasTribus import settings
from apt import apt_pkg
#from paqueteria.models import Mantenedor, Paquete

#setup_environ(settings)
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

def pkg_solver(paquete, nombre_archivo):
    seccion = buscar(paquete, nombre_archivo)
    dependencias = listar_dependencias(seccion)
    lista_dep_op = [string.strip(n, " ") for n in dependencias]
    for d in lista_dep_op:
        if re.findall("\|", d):
            pass
        elif re.findall("\s", d): 
            pass
        else:
            print d, listar_dependencias(buscar(d, nombre_archivo))
            
def listar_dependencias(seccion): 
    if seccion == None:
        print "Aparentemente el paquete no tiene mas dependencias"
        return ""
    else:
        deps = seccion.get('Depends')
        if deps != None:    
            return string.splitfields(deps, ",")
        else:
            return deps

def buscar(paquete, nombre_archivo):
    nombre_archivo.jump(0)
    for section in nombre_archivo:
        if section.get('Package') == paquete:
            return section

pkg_solver("banshee", paquetes)