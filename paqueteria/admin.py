# -*- coding: utf-8 -*-

from django.contrib import admin
from paqueteria.models import Paquete, Mantenedor

admin.site.register(Mantenedor)
admin.site.register(Paquete)


'''class EleccionAlineada(admin.TabularInline):
    model = Eleccion
    extra = 2

class AdminEncuesta(admin.ModelAdmin):
    fieldsets = (
        ('Nombre de la pregunta', {
        'classes': ('wide', 'extrapretty', 'collapse'),
            'fields': ('pregunta',)
        }),

        ('Información sobre la fecha', {
        'classes': ('wide', 'extrapretty', 'collapse'),
            'fields': ('fecha_pub',)
        }),
    )

    inlines = [EleccionAlineada]
    list_display = ('pregunta', 'fecha_pub', 'fue_publicado_hoy', 'fue_publicado_recientemente')
    list_filter = ['fecha_pub']
    search_fields = ['pregunta']
    date_hierarchy = "fecha_pub"'''

