import email.Utils, re, string
from apt import apt_pkg, cache
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

lista_registro = []
base = []

# Metodo 'simple'

#def reg_paquete(seccion):
    

def pkg_solver(paquete, nombre_archivo):
    seccion = buscar(paquete, nombre_archivo)
    dependencias = listar_dependencias(seccion)
    if dependencias != None:
        dependencias = [string.strip(n, " ") for n in dependencias]
        for dep in dependencias:
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
    else:
        base.append(paquete)
    
    
# Metodo Extendido

def pkg_solver_ext(paquete, nombre_archivo):
    seccion = buscar(paquete, nombre_archivo)
    dependencias = listar_dependencias(seccion)
    if dependencias != None:
        dependencias = [string.strip(n, " ") for n in dependencias]
        for dep in dependencias:
            if dep not in lista_registro:
                if re.findall("\|", dep):
                    dep = string.splitfields(dep, " | ")
                    for d in dep:
                        if re.findall("\s", d):
                            par = string.splitfields(d, " ", 1)
                            d = par[0]
                            if len(par) > 1:
                                v = par[1]
                            if d not in lista_registro:
                                print "registrando", d, v, "como dependencia de: ", paquete
                                lista_registro.append(d)
                                pkg_solver(d, nombre_archivo)
                            else:
                                print "Ya se ha registrado: ", d
                        else:
                            if d not in lista_registro:
                                print "registrando", d, "sin una version especifica como dependencia de: ", paquete
                                lista_registro.append(d)
                                pkg_solver(d, nombre_archivo)
                            else:
                                print "Ya se ha registrado: ", d
                        
                elif re.findall("\s", dep):
                    par = string.splitfields(dep, " ", 1)
                    dep = par[0]
                    if len(par) > 1:
                        v = par[1]
                        if dep not in lista_registro:
                            print "registrando", dep, v, "como dependencia de: ", paquete
                            lista_registro.append(dep)
                            pkg_solver(dep, nombre_archivo)
                        else: 
                            print "Ya se ha registrado: ", dep
                        
                    else:
                        if dep not in lista_registro:
                            print "registrando", dep, "sin una version especifica como dependencia de: ", paquete
                            lista_registro.append(dep)
                            pkg_solver(dep, nombre_archivo)
                        else: 
                            print "Ya se ha registrado: ", dep
                else:
                    if dep not in lista_registro:
                        print "registrando", dep, "sin una version especifica como dependencia de: ", paquete
                        lista_registro.append(dep)
                        pkg_solver(dep, nombre_archivo)
                    else:
                        print "Ya se ha registrado: ", dep
    else:
        base.append(paquete)
                                                     
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
    
pkg_solver("0ad", paquetes)
print len(lista_registro), lista_registro
print base