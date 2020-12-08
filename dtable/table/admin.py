# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from table.models import Autor, Libro, FacturaCached, Ciudad, Empresa
# Register your models here.


class AutorAdmin(admin.ModelAdmin):
	list_display= ('nombre', 'apellidos', 'email')
	search_fields=('nombre', 'apellidos')
	list_select_related = ["ciudad", "perfil"]
	raw_id_fields = list_select_related


class LibroAdmin(admin.ModelAdmin):
	list_display= ('titulo', 'fecha_publicacion')
	list_filter=('fecha_publicacion',)
	date_hierarchy ='fecha_publicacion'
	ordering = ('fecha_publicacion',)
	filter_horizontal = ('autor',)


class FacturaCachedAdmin(admin.ModelAdmin):
	list_display= ('key',)
	list_filter=('key',)


class CiudadAdmin(admin.ModelAdmin):
	list_display= ('nombre', 'personas')


class EmpresaAdmin(admin.ModelAdmin):
	list_display= ('nombre',)


admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(FacturaCached, FacturaCachedAdmin)
admin.site.register(Ciudad, CiudadAdmin)
admin.site.register(Empresa, EmpresaAdmin)
