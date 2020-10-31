# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from django.utils import formats

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
                json_autores.append({
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
                    "estado": autor.estado,
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
        return obj.ciudad.nombre
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
        return Autor.objects.select_related("perfil").prefetch_related("perfil__editorial").all()