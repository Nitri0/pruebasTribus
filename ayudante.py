# /usr/bin/env python
# -*- coding: utf-8 -*-
from apt import apt_pkg
apt_pkg.init()

archivo = apt_pkg.TagFile(open('/home/fran/Packages'))

def paqueteVirtual(nombre, archivo):
    archivo.jump(0)
    for section in archivo:
        #if section.get('Provides') == nombre:
        if nombre in str(section.get('Provides')):
            return section.get('Package'), section.get('Provides') 
    return None, None
        
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
        proveedor, virtual = paqueteVirtual(paquete, archivo)
        if virtual != None:
            print virtual, " <--- provisto por ------> ", proveedor
        else:
            print "El paquete seleccionado no se encuentra en el repositorio y tampoco es un paquete virtual"