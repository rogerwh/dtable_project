# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import formats
from django.core.urlresolvers import reverse

from .models import Autor, Libro, Ciudad

import json
import timeit

# Rest Framework
from rest_framework import serializers
from rest_framework import generics
from rest_framework.renderers import JSONRenderer


class CodeTimer:

    def __init__(self, name=None):
        self.name = " '"  + name + "'" if name else ''

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (timeit.default_timer() - self.start) * 1000.0
        print('Code block' + self.name + ' time: ' + str(self.took) + ' ms')

# Create Users for Table Autores
# from djipsum.faker import FakerModel
# faker = FakerModel(app='table', model='Autor')
# ##Creando autores ES RAPIDO
# for _ in range(8000):
#     fields = {
#         'nombre': faker.fake.name(),
#         'apellidos': faker.fake.word()+" "+faker.fake.word(),
#         'email': faker.fake.email(),
#     }
#     faker.create(fields)

def lista_autores_json_cached(request):
    # Mostrar 8 mil registros con cache para datatables usando el modelo Autor con poco campos y sin relaciones 
        
    # Tiempo desde la vista que genera el json
    # Code block 'for autor in autores: generando cache' time: 128.698825836 ms 
    # Code block 'mostrando cache: 16-24.13ms'    
    # Tiempo desde la vista donde esta la tabla: 99/105 ms

    # Tiempo desde la vista obteniendo la info desde Mysql: 119 ms

    # Tiempo con Mysql agregando mas columnas(14): +190 ms
    # Tiempo con Mysql agregando mas columnas(24): +422 ms

    Autores="Autores-"
    cache_autores = cache.get(Autores)
    json_autores = []
    if cache_autores is None:
        autores = Autor.objects.all()
        with CodeTimer("for autor in autores: cached"):
            for autor in autores:
                json_autores.append({   # 14 / 23
                "nombre_completo":autor.nombre+" "+autor.apellidos,
                "nombre": autor.nombre,
                "apellidos": autor.apellidos,
                "email": autor.email,
                "fecha_emision": formats.date_format(autor.fecha_emision, "SHORT_DATE_FORMAT"),
                "fecha_vencimiento": formats.date_format(autor.fecha_vencimiento, "SHORT_DATE_FORMAT"),
                "fecha_pago": formats.date_format(autor.fecha_pago, "SHORT_DATE_FORMAT"),
                "total": float(autor.total),
                "total_cobrado": float(autor.total_cobrado),
                "referencia": str(autor.referencia),
                "factura_generica": autor.factura_generica,
                "reconexion_aplicada": autor.reconexion_aplicada,
                "mora_aplicada": autor.mora_aplicada,
                "total2": float(autor.total2),
                "total3": float(autor.total3),
                "impuestos": float(autor.impuestos),
                "subtotal": float(autor.subtotal),
                "descuento": float(autor.descuento),
                "referencia2": str(autor.referencia2),
                "referencia3": str(autor.referencia3),
                "url": autor.url,
                "url2": autor.url2,
                "url3": autor.url3,
                "estado": autor.get_estado_display(),

                # FK 6
                "ciudad__nombre": autor.ciudad.nombre,
                "ciudad__personas": str(autor.ciudad.personas),
                "ciudad__personas2": str(autor.ciudad.personas2),
                "perfil__telefono": autor.perfil.telefono, 
                "perfil__direccion": autor.perfil.direccion,
                "perfil__informacion": autor.perfil.informacion,
                
                "perfil__editorial__nombre": autor.perfil.editorial.nombre,
                "perfil__editorial__direccion": autor.perfil.editorial.direccion,
                "perfil__editorial__telefono": autor.perfil.editorial.telefono,
                "perfil__editorial__eslogan": autor.perfil.editorial.eslogan,
                "perfil__editorial__rfc": autor.perfil.editorial.rfc,
                "perfil__editorial__rfc2": autor.perfil.editorial.rfc2,

                "perfil__editorial__distribuidor__nombre": autor.perfil.editorial.nombre,
                # "cliente__user_cliente__estado",
                # "cliente__user_cliente__ip",
            })
        cache_autores = json.dumps(json_autores)
        cache.set(Autores, cache_autores, timeout=21600)
    return HttpResponse(cache_autores, content_type='application/json')


def lista_autores_json_no_cached(request):
    # Mostrar 8 mil registros sin cache para datatable  usando el modelo Autor con poco campos y sin relaciones 
        
    # Tiempo desde la vista obteniendo la vista desde sqlite: 288 ms
    # Code block 'for autor in autores: no cached' time: 130.93495369 ms 
    
    # Tiempo desde la vista obteniendo la info desde Mysql: 316 ms
    # Code block 'for autor in autores: no cached' time: 254.454851151 m ms

    # Tiempo con Mysql agregando mas columnas (14): 1.86 Seg
    # Code block 'for autor in autores: no cached' time: 1720.08013725 ms

    # Tiempo con Mysql agregando mas columnas (24): 3.26 Seg
    # Code block 'for autor in autores: no cached' time: 3021.81100845 ms

    # Tiempo con Mysql agregando mas columnas (37): +13.65 Seg
    # Code block 'for autor in autores: no cached' time: 13215.321064 ms
    json_autores = []
    autores = Autor.objects.select_related("perfil").prefetch_related("perfil__editorial").all()
    with CodeTimer("for autor in autores: no cached"):
        for autor in autores:
            json_autores.append({   # 14 / 23
                "nombre_completo":autor.nombre+" "+autor.apellidos,
                "nombre": autor.nombre,
                "apellidos": autor.apellidos,
                "email": autor.email,
                "fecha_emision": formats.date_format(autor.fecha_emision, "SHORT_DATE_FORMAT"),
                "fecha_vencimiento": formats.date_format(autor.fecha_vencimiento, "SHORT_DATE_FORMAT"),
                "fecha_pago": formats.date_format(autor.fecha_pago, "SHORT_DATE_FORMAT"),
                "total": float(autor.total),
                "total_cobrado": float(autor.total_cobrado),
                "referencia": str(autor.referencia),
                "factura_generica": autor.factura_generica,
                "reconexion_aplicada": autor.reconexion_aplicada,
                "mora_aplicada": autor.mora_aplicada,
                "total2": float(autor.total2),
                "total3": float(autor.total3),
                "impuestos": float(autor.impuestos),
                "subtotal": float(autor.subtotal),
                "descuento": float(autor.descuento),
                "referencia2": str(autor.referencia2),
                "referencia3": str(autor.referencia3),
                "url": autor.url,
                "url2": autor.url2,
                "url3": autor.url3,
                "estado": autor.get_estado_display(),

                # FK 6
                "ciudad__nombre": autor.ciudad.nombre,
                "ciudad__personas": str(autor.ciudad.personas),
                "ciudad__personas2": str(autor.ciudad.personas2),
                "perfil__telefono": autor.perfil.telefono, 
                "perfil__direccion": autor.perfil.direccion,
                "perfil__informacion": autor.perfil.informacion,
                
                "perfil__editorial__nombre": autor.perfil.editorial.nombre,
                "perfil__editorial__direccion": autor.perfil.editorial.direccion,
                "perfil__editorial__telefono": autor.perfil.editorial.telefono,
                "perfil__editorial__eslogan": autor.perfil.editorial.eslogan,
                "perfil__editorial__rfc": autor.perfil.editorial.rfc,
                "perfil__editorial__rfc2": autor.perfil.editorial.rfc2,

                "perfil__editorial__distribuidor__nombre": autor.perfil.editorial.nombre,
                # "cliente__user_cliente__estado",
                # "cliente__user_cliente__ip",
            })
    cache_autores = json.dumps(json_autores)
    return HttpResponse(cache_autores, content_type='application/json')


# Django Serializer Views
class ModelCiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'


class AutorModelSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField('get_full_name')
    ciudad = ModelCiudadSerializer()
    # nombre_ciudad = serializers.SerializerMethodField('ciudad_nombre')
    
    def get_full_name(self, obj):
        return obj.nombre + " " + obj.apellidos

    # def ciudad_nombre(self, obj):
    #    return obj.ciudad.nombre

    class Meta:
        model = Autor
        fields = [
            "id",
            "nombre_completo",
            "nombre",
            "apellidos",
            "email",
            "fecha_emision",
            "fecha_vencimiento",
            "fecha_pago",
            "total",
            "total_cobrado",
            "referencia",
            "factura_generica",
            "reconexion_aplicada",
            "mora_aplicada",
            "total2",
            "total3",
            "impuestos",
            "subtotal",
            "descuento",
            "referencia2",
            "referencia3",
            "url",
            "url2",
            "url3",
            "estado",
            "ciudad",
        ]
        read_only_fields = fields


class AutorListView(generics.ListAPIView):
    # Serializa la informacion de la base de datos para el datatables 
    # Tiempo desde la vista donde esta la tabla: 762.86 ms 
    
    # Tiempo desde la vista obteniendo la info desde Mysql: 980 ms
    # Tiempo con Mysql agregando mas columnas (14): 4.62 Seg
    # Tiempo con Mysql agregando mas columnas (24): 11.39 Seg
    # Tiempo con mysql agregando una columna relacionada y actualizando el query: 23 Segundos
    # Tiempo con mysql agregando una columna relacionada y serializada: 44 Segundos

    queryset = Autor.objects.all()
    serializer_class = AutorModelSerializer
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        return Autor.objects.select_related("perfil", "ciudad").prefetch_related("perfil__editorial").all()


def table_api(request):
    title_page = "Lista Autores - API con Django Rest Framework"
    info_page = """
        <p>La problematica al mostrar 9k registros con Rest Framework posiblemente sea lo de n+1, puesto que las tablas se relacionan. La solución es usar 
        un serializer para el modelo que esta relacionado pero, aun con el modelo serializado y modificando el queryset para agregar el select_related y el prefetch_related, 
        sigue siendo demasiado lento para mostrar los datos de tantas columnas!</p>

        <ul>
            <li>Tiempo con Mysql agregando mas columnas (14): <strong>4.62 Seg</strong></li>
            <li>Tiempo con Mysql agregando mas columnas (24): <strong>11.39 Seg</strong></li>
            <li>Tiempo con mysql agregando una columna relacionada y actualizando el query: <strong>23 Segundos</strong></li>
            <li>Tiempo con mysql agregando una columna relacionada y serializada: <strong>44 Segundos</strong></li>
        </ul>

        <p></p>
    """
    return render(request, 'lado_cliente/lista_autores_api.html', {"title_page": title_page, "info_page": info_page})


def table_no_cached(request):
    url_json = reverse("lista_autores_json_no_cached")
    title_page = "Lista Autores - Json creado con Queryset Recorrido"
    info_page = """
        <p>La problematica al mostrar 9k registros con recorriendo una query y creando el diccionario es el tiempo que tarda la vista en devolver la informacion
        en formato json. El tiempo tambien aumento con validaciones (validando si un campo es null para poner que este vacio), o creando variables que 
        crean html desde la vista (Botones de accion). </p>

        <ul>
            <li>Tiempo desde la vista obteniendo la vista desde sqlite (4 columas): <strong>288 ms</strong></li>
            <li>Tiempo desde la vista obteniendo la info desde Mysql (4 columnas): <strong>316 ms</strong></li>
            <li>Tiempo con Mysql agregando mas columnas (14): <strong>1.86 Seg</strong></li>
            <li>Tiempo con Mysql agregando mas columnas (24): <strong>3.26 Seg</strong></li>
            <li>Tiempo con Mysql agregando mas columnas (37): <strong>+13.65-17 Seg</strong></li>
        </ul>

        <p></p>
    """
    return render(request, 'lado_cliente/lista_autores.html', {"title_page": title_page, "info_page": info_page, "url_json": url_json})


def table_cached(request):
    url_json = reverse("lista_autores_json_cached")
    title_page = "Lista Autores - Utilizando informacón en cache"
    info_page = """
        <p> Esta es la forma mas rapida de pasar la información a la tabla. Sin embargo, no todos los registros de todos los clientes pueden estar guardados.
        Teniendo en cuenta que aproximadamente 100 clientes cuenten con mas de 8k registros, la informacion en cache se ve afectada?
        
        Tambien puede guardarse en un campo de base de datos y consultarse. </p>
        <p></p>
    """
    return render(request, 'lado_cliente/lista_autores.html', {"title_page": title_page, "info_page": info_page, "url_json": url_json})