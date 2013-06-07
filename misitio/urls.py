from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^encuestas/', include('encuestas.urls', namespace="encuestas")),
    url(r'^admin/', include(admin.site.urls)),
)