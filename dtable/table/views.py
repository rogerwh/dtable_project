# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import timeit
from datetime import datetime

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import formats

# Rest Framework
from rest_framework import serializers
from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from .models import Autor, Empresa, Ciudad, FacturaCached, Perfil
from .forms import AuthorForm, Filter

class CodeTimer:

    def __init__(self, name=None):
        self.name = " '"  + name + "'" if name else ''

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (timeit.default_timer() - self.start) * 1000.0
        print('Code block' + self.name + ' time: ' + str(self.took) + ' ms')


class Columns:
    # Para replicar la seleccion de columnas
    keys = [
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
        "ciudad__nombre",
        "ciudad__personas",
        "ciudad__personas2",
        "perfil__telefono",
        "perfil__direccion",
        "perfil__informacion",
        "perfil__editorial__nombre",
        "perfil__editorial__direccion",
        "perfil__editorial__telefono",
        "perfil__editorial__eslogan",
        "perfil__editorial__rfc",
        "perfil__editorial__rfc2",
        "perfil__editorial__distribuidor__nombre",
    ]
    
    cached_keys = [
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
        "ciudad__nombre",
        "ciudad__personas",
        "ciudad__personas2",
        "perfil__telefono",
        "perfil__direccion",
        "perfil__informacion",
        "perfil__editorial__nombre",
        "perfil__editorial__direccion",
        "perfil__editorial__telefono",
        "perfil__editorial__eslogan",
        "perfil__editorial__rfc",
        "perfil__editorial__rfc2",
        "perfil__editorial__distribuidor__nombre",
    ]

    no_cached_keys = [
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
        "ciudad__nombre",
        "ciudad__personas",
        "ciudad__personas2",
        "perfil__telefono",
        "perfil__direccion",
        "perfil__informacion",
        "perfil__editorial__nombre",
        "perfil__editorial__direccion",
        "perfil__editorial__telefono",
        "perfil__editorial__eslogan",
        "perfil__editorial__rfc",
        "perfil__editorial__rfc2",
        "perfil__editorial__distribuidor__nombre",
    ]

    db_keys = [
        "id",
        "empresa",
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
        "ciudad__nombre",
        "ciudad__personas",
        "ciudad__personas2",
        "perfil__telefono",
        "perfil__direccion",
        "perfil__informacion",
        "perfil__editorial__nombre",
        "perfil__editorial__direccion",
        "perfil__editorial__telefono",
        "perfil__editorial__eslogan",
        "perfil__editorial__rfc",
        "perfil__editorial__rfc2",
        "perfil__editorial__distribuidor__nombre",
    ]

# autores/cached/ | Lista Autores - Utilizando informacón en cache
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
    if cache_autores is None:
        autores = Autor.objects.select_related("ciudad", "perfil").prefetch_related(
            "perfil__editorial", "perfil__editorial__distribuidor").all()
        json_autores = []
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
        cache.set(Autores, cache_autores, timeout=180)
    return HttpResponse(cache_autores, content_type='application/json')


# autores/no-cached/ | Lista Autores - Json creado con Queryset Recorrido
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
    autores = Autor.objects.select_related("ciudad", "perfil").prefetch_related(
        "perfil__editorial", "perfil__editorial__distribuidor").all()

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


# autores/db-cached/ | Lista Autores - Información Consultada de un Json en la Base de Datos
def lista_autores_json_db_cached(request):
    # Generar el Json por primera vez y guardarlo es igual de tardado que los demas metodos, pues la query debe
    # recorrerse y crear el diccionario con la informacion

    # Una vez guardada la informacion, el tiempo de Descarga del json en la vista de 9k registros es de +-1 segundo.
    # Code block 'Query Facturacached' time: 229.119062424 ms
    # Code block 'Conversion a JSON del String de FacturaCached' time: 540.380001068 ms

    # Lo demas depende del navegador y la computadora : Finish: 2.45 s | DOMContentLoaded: 1.29 s | Load: 1.51 s
    data = request.GET
    kwargs = {}
    ignore = ['_', 'amp', 'csrfmiddlewaretoken']
    for key in data.keys():
        if not key in ignore:
            if data.get(key):
                kwargs.update({key: data.get(key)})
                if key == "fecha_emision":
                    date = datetime.strptime(data.get(key), '%Y-%m-%d')
                    kwargs.update({key: date})

    key = "autores_"
    with CodeTimer("Query Facturacached"):
        factura_cached = FacturaCached.objects.filter(key=key).first() # ToDo -> Cambiar Nombre del modelo
    
    if factura_cached:
        if kwargs:
            id_list = list(Autor.objects.select_related("ciudad", "perfil", "empresa").prefetch_related(
                "perfil__editorial", "perfil__editorial__distribuidor").filter(**kwargs).values_list("id", flat=True))
            data = factura_cached.get_json_data(id_list)
        else:
            data = factura_cached.get_json_data()
    else:
        json_autores = {}
        autores = Autor.objects.select_related("ciudad", "perfil", "empresa").prefetch_related(
            "perfil__editorial", "perfil__editorial__distribuidor").filter(**kwargs)
        
        for autor in autores:
            autor_id = autor.id
            json_autores[autor_id] = {
                "id": "<a href={0} target='_blank'>{1}</a>".format(reverse(update_author, kwargs={"author_id":autor_id}), autor_id),
                "empresa": autor.empresa.nombre,
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
            }

        data = json.dumps(json_autores)
        FacturaCached.objects.create(
            key=key,
            data=data
        )
    
    return HttpResponse(data, content_type='application/json')


# Django Serializer Views
class ModelCiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'


class ModelPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = '__all__'


class AutorModelSerializer(serializers.ModelSerializer):
    # nombre_completo = serializers.SerializerMethodField('get_full_name')
    ciudad = ModelCiudadSerializer()
    perfil = ModelPerfilSerializer()
    # nombre_ciudad = serializers.SerializerMethodField('ciudad_nombre')
    
    # def get_full_name(self, obj):
    #     return obj.nombre + " " + obj.apellidos

    # def ciudad_nombre(self, obj):
    #    return obj.ciudad.nombre

    class Meta:
        model = Autor
        fields = [
            "id",
            # "nombre_completo",
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
            "perfil",
        ]
        read_only_fields = fields


# autores/api/ | Lista Autores - API con Django Rest Framework
class AutorListView(generics.ListAPIView):
    # Serializa la informacion de la base de datos para el datatables 
    # Tiempo desde la vista donde esta la tabla: 762.86 ms 
    
    # 3000 Usuarios | Antes de resolver el problema de query lenta (sin prefetch y select_related)
    # Tiempo desde la vista obteniendo la info desde Mysql: 980 ms
    # Tiempo con Mysql agregando mas columnas (14): 4.62 Seg
    # Tiempo con Mysql agregando mas columnas (24): 11.39 Seg
    # Tiempo con mysql agregando una columna relacionada y actualizando el query: 23 Segundos
    # Tiempo con mysql agregando una columna relacionada y serializada: 44 Segundos

    # 9000 Usuarios
    # Tiempo con mysql 16 Segundos

    # Nota: Se ha probado con python 3.6 y es mas rapido.

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


def table_cached(request):
    url_json = reverse("lista_autores_json_cached")
    title_page = "Lista Autores - Utilizando informacón en cache"
    keys = Columns.cached_keys
    info_page = """
        <p> Esta es la forma mas rapida de pasar la información a la tabla. Sin embargo, no todos los registros de todos los clientes pueden estar guardados.
        Teniendo en cuenta que aproximadamente 100 clientes cuenten con mas de 8k registros, la informacion en cache se ve afectada?
        
        Tambien puede guardarse en un campo de base de datos y consultarse. </p>
        <p></p>
    """
    return render(request, 'lado_cliente/lista_autores_test.html', {
        "title_page": title_page, "info_page": info_page, "url_json": url_json, "keys": keys})


def table_no_cached(request):
    url_json = reverse("lista_autores_json_no_cached")
    title_page = "Lista Autores - Json creado con Queryset Recorrido"
    keys = Columns.no_cached_keys
    info_page = """
        <p>La problematica al mostrar 9k registros con recorriendo una query y creando el diccionario es el tiempo que tarda la vista en devolver la informacion
        en formato json. El tiempo tambien aumento con validaciones (validando si un campo es null para poner que este vacio), o creando variables que 
        crean html desde la vista (Botones de accion). </p>

        <ul>
            <li>Tiempo con Mysql agregando mas columnas (37): <strong>+4 Seg</strong></li>
        </ul>

        <p>No se agregan validaciones ni html</p>
    """
    return render(request, 'lado_cliente/lista_autores_test.html', {
        "title_page": title_page, "info_page": info_page, "url_json": url_json, "keys": keys})


def table_db_cached(request):
    url_json = reverse("lista_autores_json_db_cached")+"?"
    title_page = "Lista Autores - Información Consultada de un Json en la Base de Datos"
    keys = Columns.db_keys
    form = Filter(request.POST or None)

    if request.POST:
        data = request.POST
        for key in data:
            if data.get(key):
                url_json = url_json + "&" + key + "=" + data.get(key)

    info_page = """
        <p>
            Que se genere el view una vez que se obtenga de base de datos no es tardado, esto debido a que se guarda
            de la forma en la que datatables necesita. Y esto es un problema al querer actualizar el json/campo
            cuando sucede una actualizacion en la factura.
        </p>

        <p>
        Como lo necesita datatables: <br><br>
            [ <br>
             &nbsp;&nbsp;&nbsp;&nbsp;{"id_autor": "10", "nombre": "Van", "apellido": "Hoenheim"}, <br>
             &nbsp;&nbsp;&nbsp;&nbsp;{"id_autor": "11", "nombre": "Edward", "apellido": "Elric"}, <br>
             &nbsp;&nbsp;&nbsp;&nbsp;{"id_autor": "12", "nombre": "Alphonse", "apellido": "Elric"}, <br>
            ]
        </p>

        <p>
            Como seria mas facil obtener la ifnormacion de las facturas para actualizar. Sin embargo no es lo ideal <br>
            Para que datatables funcione.<br><br>
            { <br>
             &nbsp;&nbsp;&nbsp;&nbsp;"1": {"sub_total": "10.00", "cliente": "wisp1"}, <br>
             &nbsp;&nbsp;&nbsp;&nbsp;"2": {"sub_total": "10.00", "cliente": "wisp1"}, <br>
             &nbsp;&nbsp;&nbsp;&nbsp;"3": {"sub_total": "10.00", "cliente": "wisp1"}, <br>
            }
        </p>
        
        <p></p>
    """
    return render(request, 'lado_cliente/lista_autores_db.html', {
        "title_page": title_page, "url_json": url_json, "keys": keys, "form": form})


# Edit Views
def update_author(request, author_id):
    author = Autor.objects.filter(id=author_id).first()
    title_page = "Update Author - Form"
    form = AuthorForm(request.POST or None, instance=author)
    if request.POST:
        if form.is_valid():
            _author = form.save()
            update_db_cached(author, author_id, form.changed_data)

    return render(request, 'forms/update_author.html', {'form': form, 'title_page': title_page})


def serialize_autor(autor):
    return {
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
        #
        "perfil__editorial__nombre": autor.perfil.editorial.nombre,
        "perfil__editorial__direccion": autor.perfil.editorial.direccion,
        "perfil__editorial__telefono": autor.perfil.editorial.telefono,
        "perfil__editorial__eslogan": autor.perfil.editorial.eslogan,
        "perfil__editorial__rfc": autor.perfil.editorial.rfc,
        "perfil__editorial__rfc2": autor.perfil.editorial.rfc2,
        ##
        "perfil__editorial__distribuidor__nombre": autor.perfil.editorial.nombre,
    }


def update_db_cached(author, author_id, changed_keys):
    key = "autores_"
    factura_cached = FacturaCached.objects.filter(key=key).first()
    
    if factura_cached:
        # Opcion 1.- Obtener los campos que se cambiaron y actualizarlos en el json usando .__dict___
        # Opcion 2.- Actualizar cada uno de los campos debido a los foreign_key

        # convertmos el campo en diccionario
        data = factura_cached.get_dict_data()

        # Obtenemos la llave del diccionario
        author_dict = data.get(author_id)

        # Serializamos el autor
        s_author = serialize_autor(author)

        # Actualizamos ...
        data[author_id].update(s_author)
        data = json.dumps(data)
        factura_cached.data = data
        factura_cached.save()

    else:
        "Se ejecuta el metodo que calcula el json"
        pass
