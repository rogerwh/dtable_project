# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse
from table.models import Autor, Libro
from django.core.cache import cache
from django.db.models.functions import Concat
from django.db.models import Q, Count, Sum, Value as V
from django.db.models import Q
import time
import json
# Create your views here.
def limpiar_cache(request):
    otro_cache = cache
    list_keys = cache.keys("*")
    resultado = "Se limpio el cache {0} \nKeys: {1}".format(otro_cache, list_keys)
    cache.clear()

    return  HttpResponse(resultado, content_type="text/plain")

def index(request):
	return render(request, 'index.html')

def lista_autores_cliente(request):
	return render(request, 'lado_cliente/lista_autores.html')

def lista_libros_cliente(request):
	return render(request, 'lado_cliente/lista_libros.html')

def lista_autores_json(request):
	Autores="Autores-"
	cache_autores = cache.get(Autores)
	json_autores = []
	if cache_autores is None:
		time.sleep(3)
		autores = Autor.objects.all()
		for autor in autores:
			json_autores.append({
				"nombre_completo":autor.nombre+" "+autor.apellidos,
	            "nombre": autor.nombre,
	            "apellidos": autor.apellidos,
	            "email": autor.email,
	        })
		cache_autores = json.dumps(json_autores)
	cache.set(Autores, cache_autores, timeout=21600)
	return HttpResponse(cache_autores, content_type='application/json')

def lista_libros_json(request):
	Libros="Libros-"
	cache_libros = cache.get(Libros)
	json_libros = []
	if cache_libros is None:
		time.sleep(3)
		libros = Libro.objects.all()
		for libro in libros:
			json_libros.append({
	            "titulo": libro.titulo,
	            "fecha_publicacion": str(libro.fecha_publicacion),
	            "portada": str(libro.portada),
	        })
		cache_libros = json.dumps(json_libros)
	cache.set(Libros, cache_libros, timeout=21600)
	return HttpResponse(cache_libros, content_type='application/json')


def lista_autores_server(request):
	return render(request, 'lado_servidor/lista_autores_server.html')

def lista_libros_server(request):
	return render(request, 'lado_servidor/lista_libros_server.html')

def lista_autores_server_json(request):
	json_autores = []
	draw = request.POST['draw']
	start = int(request.POST['start'])
	length = int(request.POST['length'])
	order_by = request.POST.get('orden_columna')
	tipo_orden = request.POST.get('tipo_orden')
	global_search = request.POST['search[value]']
	busqueda_individual = request.POST.get('busqueda_individual', "{}")
	busqueda_individual = json.loads(busqueda_individual)
	
	kwargs_autores={}
	kwargs_annotate = {}
	if busqueda_individual:
		for columna_dic in busqueda_individual:
			columna_name = str(columna_dic.get("columna"))
			valor_busqueda = columna_dic.get("valor_busqueda")
			if columna_name in ["nombre_completo"]:
				kwargs_annotate["full_name"] = Concat('nombre', V(' '),
                                                        'apellidos')
				kwargs_autores["full_name__icontains"] = valor_busqueda
			else:
				kwargs_autores["{0}__icontains".format(columna_name)] = valor_busqueda
	autores=Autor.objects.annotate(**kwargs_annotate).filter(**kwargs_autores)

	if global_search:
		autores = autores.annotate(full_name=Concat('nombre', V(' '), 'apellidos')).filter(Q(nombre__icontains=global_search)|
																						Q(apellidos__icontains=global_search)|
																						Q(email__icontains=global_search)|
																						Q(full_name__icontains=global_search))
	if order_by:
		if order_by=="nombre_completo":
			order_by="nombre"
		autores = autores.order_by(tipo_orden + order_by)
	total_count = autores.count()
	filtered_count = total_count    
	try:
		autores = autores[start:start + length]
	except AssertionError:
		pass
	for autor in autores:
		json_autores.append({
			"nombre_completo":autor.nombre+" "+autor.apellidos,
            "nombre": autor.nombre,
            "apellidos": autor.apellidos,
            "email": autor.email,
        })
	json_data = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": json_autores,
    }
   	json_data = json.dumps(json_data) 
   	return HttpResponse(json_data, content_type='application/json')

def lista_libros_server_json(request):
	json_libros = []
	draw = request.POST['draw']
	start = int(request.POST['start'])
	length = int(request.POST['length'])
	order_by = request.POST.get('orden_columna')
	tipo_orden = request.POST.get('tipo_orden')
	global_search = request.POST['search[value]']
	busqueda_individual = request.POST.get('busqueda_individual', "{}")
	busqueda_individual = json.loads(busqueda_individual)
	
	kwargs_libros={}
	if busqueda_individual:
		for columna_dic in busqueda_individual:
			columna_name = str(columna_dic.get("columna"))
			valor_busqueda = columna_dic.get("valor_busqueda")
			kwargs_libros["{0}__icontains".format(columna_name)] = valor_busqueda
			
   	libros=Libro.objects.filter(**kwargs_libros)
   	if global_search:
   		libros = libros.filter(Q(titulo__icontains=global_search)|Q(fecha_publicacion__icontains=global_search)|Q(portada__icontains=global_search))

	if order_by:
		libros = libros.order_by(tipo_orden + order_by)   
	total_count = libros.count()
	filtered_count = total_count    
	try:
		libros = libros[start:start + length]
	except AssertionError:
		pass

	for libro in libros:
		json_libros.append({
            "titulo": libro.titulo,
            "fecha_publicacion": str(libro.fecha_publicacion),
            "portada": str(libro.portada),
        })
	json_data = {
        "draw": draw,
        "recordsTotal": total_count,
        "recordsFiltered": filtered_count,
        "data": json_libros,
    }
   	json_data = json.dumps(json_data) 
   	return HttpResponse(json_data, content_type='application/json')
