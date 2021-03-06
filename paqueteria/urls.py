from django.conf.urls import patterns, url
from paqueteria import views



urlpatterns = patterns('',
                       
                
    url(r'^$', views.inicio, name='inicio'),
    url(r'^/index$', views.index, name='index'),
    #url(r'^/contact$', views.contacto, name='contacto'),
    #url(r'^/admin$')
    #url(r'^(?P<pqt>\w*-?\w*)', views.busqueda, name='busqueda'),
    #url(r'^(?P<pqt>\w*\.*?-*\w*)', views.busqueda, name='busqueda'),
    #url(r'^(?P<pqt>(\w*-?\w*:-*?\w*)', views.busqueda, name='busqueda'),
    url(r'^(?P<pqt>(\w*\W*)*)', views.busqueda, name='busqueda'),
    )
'''    
    url(r'^(?P<encuesta_id>\d+)/$', views.detalles, name='detalles'), 
    
    # la url de la expresion regular puede modificarse a su gusto, mientras q los otros parametros
    # tienen q coincidir con los metodos httprequest
    
    url(r'^(?P<encuesta_id>\d+)/resultados/$', views.resultados, name='resultados'),
    
    url(r'^(?P<encuesta_id>\d+)/votar/$', views.votar, name='votar'),
)

'''