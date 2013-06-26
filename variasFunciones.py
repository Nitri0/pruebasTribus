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
            
            
            
    