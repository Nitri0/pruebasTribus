# /usr/bin/env python
# -*- coding: utf-8 -*-
from apt import apt_pkg
apt_pkg.init()

archivo = apt_pkg.TagFile(open('/home/fran/Packages'))

def paqueteVirtual(nombre, archivo):
    archivo.jump(0)
    for section in archivo:
        if section.get('Provides') == nombre:
            return section.get('Package')
    return None
        
def paqueteExiste(nombre, archivo):
    for section in archivo:
        if section.get('Package') == nombre:         
            return section.get('Package')
    return None

salir = False

while salir == False:
    archivo.jump(0)
    paquete = raw_input("Ingrese el nombre del paquete: ")
    resultado = paqueteExiste(str(paquete), archivo)
    if paquete == "salir":
        salir = True
    if resultado:
        print resultado
    else:
        virtual = paqueteVirtual(paquete, archivo)
        if virtual != None:
            print "El paquete seleccionado es un paquete virtual provisto por: "
            print virtual
        else:
            print "El paquete seleccionado no se encuentra en el repositorio y tampoco es un paquete virtual"