import email.Utils, re, string
from apt import apt_pkg, cache
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

lista_registro = []

def pkg_solver(paquete, nombre_archivo):
    seccion = buscar(paquete, nombre_archivo)
    dependencias = listar_dependencias(seccion)
    if dependencias != None:
        lista_dep_op = [string.strip(n, " ") for n in dependencias]
        for dep in lista_dep_op:
            if dep not in lista_registro:
                if re.findall("\|", dep):
                    dep = string.splitfields(dep, " | ")
                    for d in dep:
                        if re.findall("\s", d):
                            d = string.splitfields(d, " ", 1)[0]       
                        if d not in lista_registro:
                            print "registrando", d, "como dependencia de: ", paquete
                            lista_registro.append(d)
                            pkg_solver(d, nombre_archivo)
                        else:
                            print "Ya se ha registrado: ", d
                        
                elif re.findall("\s", dep):
                    dep = string.splitfields(dep, " ", 1)[0]
                    if dep not in lista_registro:
                        print "registrando", dep, "como dependencia de: ", paquete
                        lista_registro.append(dep)
                        pkg_solver(dep, nombre_archivo)
                    else: 
                        print "Ya se ha registrado: ", dep
                else:
                    if dep not in lista_registro:
                        print "registrando", dep, "como dependencia de: ", paquete
                        lista_registro.append(dep)
                        pkg_solver(dep, nombre_archivo)
                    else: 
                        print "Ya se ha registrado: ", dep
                                                    
def listar_dependencias(seccion):
    if seccion != None:
        deps = seccion.get('Depends')
        if deps != None:    
            return string.splitfields(deps, ", ")
        else:
            return None
                
def buscar(paquete, nombre_archivo):
    for section in nombre_archivo:
        if section.get('Package') == paquete:
            return section
    nombre_archivo.jump(0)
    
pkg_solver("gnome", paquetes)
print len(lista_registro), lista_registro