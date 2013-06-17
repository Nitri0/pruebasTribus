import email.Utils
from django.core.management import setup_environ
from pruebasTribus import settings
from apt import apt_pkg
from paqueteria.models import Mantenedor, Paquete

setup_environ(settings)
apt_pkg.init()

paquetes = apt_pkg.TagFile(open('/home/fran/Packages'))

for seccion in paquetes:
    nombreMan, correoMan = email.Utils.parseaddr(paquetes.section.get("Maintainer"))
    mantenedorActual = Mantenedor.objects.filter(nombre_completo = nombreMan, correo = correoMan)
    # En teoria solo debe tener un mantenedor
    if len(mantenedorActual) == 1:
        nPaquete = Paquete(mantenedor = mantenedorActual[0],
                           nombre = seccion.get('Package'),
                           arquitectura = seccion.get('Architecture'))
        nPaquete.save()
        
    else:
        nMantenedor = Mantenedor(nombre_completo = nombreMan, correo = correoMan)
        nMantenedor.save()
        nPaquete = Paquete(mantenedor = nMantenedor,
                           nombre = seccion.get('Package'),
                           arquitectura = seccion.get('Architecture'))
        nPaquete.save()
    print "Guardando datos del paquete: ", seccion.get('Package')
print "Volcado de datos finalizado"