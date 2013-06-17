import email.Utils, re, string
from django.core.management import setup_environ
from pruebasTribus import settings
from apt import apt_pkg
from paqueteria.models import Mantenedor, Paquete

setup_environ(settings)
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

def resolvedor(paquete, nombre_archivo):
    seccion = buscar(paquete, nombre_archivo)
    if seccion == None: # Esto quiere decir que no encontro una seccion
        print "No he encontrado la ultima seccion"
    else:
        depends = seccion.get('Depends')
        if depends == None:
            print "Esta vacio"
        else:
            #expresion regular q saca los valores dentro de parentesis
            regexp1 = "\(\W*\D*\S*w*\d*\)"
            x = string.splitfields(depends, ",")
            for i in x:
                if re.findall("\|", i):
                    lista = string.splitfields(i, "|")
                    lista_dep_op = [string.strip(n, " ") for n in lista]
                    for dep_op in lista_dep_op:
                        resolvedor(dep_op, nombre_archivo) 
                    
                    # Aqui registraria dependencias opcionales
                    print "Esto es una dependencia opcional: ", i
                else:
                    # Aqui registraria las depencias simples
                    #print "Esto es una dependencia simple:", i
                    pass

def buscar(paquete, nombre_archivo):
    for section in nombre_archivo:
        if section.get('Package') == paquete:
            return section
    return None

resolvedor("0ad", paquetes)








        