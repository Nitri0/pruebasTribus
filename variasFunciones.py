from apt import apt_pkg
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

def tieneDependencias(paquete, archivo):
    archivo.jump(0)
    for section in archivo:
        if section.get('Package') == paquete:
            if section.get('Depends'):
                print "Dependencias de: ", paquete
                print section.get('Depends')
            else:
                print "No tiene dependencias"
                
def paqueteVirtual(nombre, archivo):
    archivo.jump(0)
    for section in archivo:
        if section.get('Provides') == nombre:
            print "Es un paquete virtual provisto por el paquete: ", section.get('Package') 
                
def paqueteExiste(nombre, archivo):
    archivo.jump(0)
    for section in archivo:
        if section.get('Package') == nombre:
            print "El paquete existe"
        else:
            paqueteVirtual(nombre, archivo)
            
def generar_dict_paquetes(tagFile):
    dic = {}
    for seccion in tagFile:
        dic[seccion.get('Package')] = seccion
    return dic

def comparar_archivos(nuevos, anteriores, debug = False):
    dic_ant = generar_dict_paquetes(anteriores)
    dic_nue = generar_dict_paquetes(nuevos)
    nuevos_paquetes = []
    actualizar_paquetes = []
    for paquete in dic_nue.keys():
        if paquete in dic_ant.keys():
            if debug:
                print paquete, "ya esta incluido"
            if dic_nue[paquete].get('MD5sum') == dic_ant[paquete].get('MD5sum'):
                if debug:
                    print  paquete, "no tiene cambios"
            else: 
                if debug:
                    print  paquete, "tiene nueva informacion o es una nueva version"
                actualizar_paquetes.append(dic_nue[paquete])
        else:
            if debug: 
                print paquete, "no esta incluido"
            nuevos_paquetes.append(dic_nue[paquete])
            
    return actualizar_paquetes, nuevos_paquetes
            
paqueteExiste("libjpeg-dev", paquetes)   
    