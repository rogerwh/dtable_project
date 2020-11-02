#!
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (
    lista_autores_json_cached, lista_autores_json_no_cached, AutorListView,
    table_api, table_cached, table_no_cached)
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^autores/json/cached/$', lista_autores_json_cached, name="lista_autores_json_cached"), 
    url(r'^autores/json/no-cached/$', lista_autores_json_no_cached, name="lista_autores_json_no_cached"),
    url(r'^autores/json/serialize/$', AutorListView.as_view(), name="lista_autores_json_serialize"),

    url(r'^autores/api/$', table_api, name="lista_autores_cliente_api"),
    url(r'^autores/cached/$', table_cached, name="lista_autores_cached"),
    url(r'^autores/no-cached/$', table_no_cached, name="lista_autores_no_cached"),
]