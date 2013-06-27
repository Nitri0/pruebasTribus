import email.Utils, re, string
from django.core.management import setup_environ
from pruebasTribus import settings
#from apt import apt_pkg
from paqueteria.models import Mantenedor, Paquete, DependenciaSimple, DependenciaOR 
from debian import deb822

a1 = file('/home/fran/Packages')

def buscar_mantenedor(str_mant):
    nombreMan, correoMan = email.Utils.parseaddr(str_mant)
    mantenedorActual = Mantenedor.objects.filter(nombre_completo = nombreMan, correo = correoMan)
    if len(mantenedorActual) == 1:
        return mantenedorActual[0]
    else:
        nMantenedor = Mantenedor(nombre_completo = nombreMan, correo = correoMan)
        nMantenedor.save()
    return nMantenedor

def buscar_paquete_virtual(nombre_pq):
    paquete_existe = Paquete.objects.filter(nombre = nombre_pq)
    if len(paquete_existe):
        return paquete_existe[0]
    else:
        print "Registrando paquete virtual %s" % nombre_pq
        nPaquete = Paquete(nombre = nombre_pq)
        nPaquete.save()
        return nPaquete

def buscar_paquete(paquete):
    if paquete != None:
        nombre_pq = paquete['Package'] if paquete.has_key('Package') else None
        instsize_pq = paquete['Installed-Size'] if paquete.has_key('Installed-Size') else None
        version_pq = paquete["Version"] if paquete.has_key("Version") else None
        mantenedor_paquete = buscar_mantenedor(paquete['Maintainer']) if paquete.has_key('Maintainer') else None
        arquitectura_pq = paquete["Architecture"] if paquete.has_key("Architecture") else None
        size_pq = paquete["Size"] if paquete.has_key("Size") else None 
        sha256_pq =  paquete["SHA256"] if paquete.has_key("SHA256") else None
        sha1_pq = paquete["SHA1"] if paquete.has_key("SHA1") else None
        md5sum_pq = paquete["MD5sum"] if paquete.has_key("MD5sum") else None
        descripcion_pq = paquete["Description"] if paquete.has_key("Description") else None
        pagina_pq =  paquete["Homepage"] if paquete.has_key("Homepage") else None
        desmd5_pq = paquete["Description-md5"] if paquete.has_key("Description-md5") else None
        sec_pq = paquete["Section"] if paquete.has_key("Section") else None
        prioridad_pq = paquete["Priority"] if paquete.has_key("Priority") else None
        nombrearchivo_pq = paquete["Filename"] if paquete.has_key("Filename") else None
        paquete_existe = Paquete.objects.filter(nombre = nombre_pq, md5sum = md5sum_pq)
        if len(paquete_existe):
            return paquete_existe[0]
        else:
            print "Registrando %s" % nombre_pq
            nPaquete = Paquete(nombre = nombre_pq, version = version_pq, size = size_pq,
                               instsize = instsize_pq, sha256 = sha256_pq, sha1 = sha1_pq,
                               mantenedor = mantenedor_paquete, desmd5 = desmd5_pq,
                               descripcion = descripcion_pq, pagina = pagina_pq, seccion = sec_pq,
                               prioridad = prioridad_pq, nombrearchivo = nombrearchivo_pq,
                               arquitectura = arquitectura_pq, md5sum = md5sum_pq)
            nPaquete.save()
            return nPaquete
    
def buscar_pq_bd(nombre):
    pq_existe = Paquete.objects.filter(nombre = nombre)
    if len(pq_existe):
        return pq_existe[0]
    
def buscar_ds_bd(pq):
    ds_existe = DependenciaSimple.objects.filter(dep = pq)
    if len(ds_existe):
        return ds_existe[0]
    else:
        dep_simple = DependenciaSimple(dep = pq)
        dep_simple.save()
        return dep_simple
    
def ubicar_dependencias(paquete, dic_dep):
    dependencias = paquete.relations['Depends']
    lista_tmp = []
    for dep in dependencias:
        if len(dep) == 1:
            lista_tmp.append(dep[0]['name']) # Para cada elemento de las dependencias guardare solo el nombre de momento
    dic_dep[paquete['Package']] = lista_tmp

def ubicar_paquetes_virtuales(paquete, dic_vir):
    if paquete.has_key('Provides'):
        dic_vir[paquete['Package']] = paquete.relations['Provides']

def registrar_dependencias(dic_dep):
    for dep in dic_dep.items():
        if len(dep[1]):
            pq = Paquete.objects.get(nombre = dep[0])
            for d in dep[1]:
                print "Registrando dependencia %s" % d
                pq_ds = buscar_pq_bd(d)
                if pq_ds == None: # Hasta ahora esto me indica que es un paquete virtual
                    continue
                ds = buscar_ds_bd(pq_ds)
                pq.dependenciaSimple.add(ds)

def registrar_paquetes_virtuales(dic_vir):
    for vir in dic_vir.items():
        #print "Dupla virtual:", vir
        if len(vir[1]) > 1:
            for v in vir[1]:
                if len(v) > 1:
                    # En este caso no estoy claro que pasa y por eso lo comento
                    # Este debe ser para paquetes virtuales opcionales
                    pass
                else:
                    buscar_paquete_virtual(v[0]['name'])
        else:
            buscar_paquete_virtual(vir[1][0][0]['name'])
            
def registrar_paquetes(archivo):
    dic_dep = {}
    dic_vir = {}
    for paquete in deb822.Packages.iter_paragraphs(a1):
        buscar_paquete(paquete) # 1) Registrar los paquetes
        ubicar_paquetes_virtuales(paquete, dic_vir) # 2) Ubicar paquetes virtuales
        #ubicar_dependencias(paquete, dic_dep)
    registrar_paquetes_virtuales(dic_vir) # 3) Registrar paquetes virtuales
    #print "Ubicacion de dependencias finalizada"    
    #registrar_dependencias(dic_dep)
    #print len(dic_vir)
    
registrar_paquetes(a1)
print "Finalizado"


