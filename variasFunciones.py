from apt import apt_pkg
apt_pkg.init()

#paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

def tieneDependencias(paquete, archivo):
    archivo.jump(0)
    for section in archivo:
        if section.get('Package') == paquete:
            if section.get('Depends'):
                print "Dependencias de: ", paquete
                print section.get('Depends')
            else:
                print "No tiene dependencias"
    