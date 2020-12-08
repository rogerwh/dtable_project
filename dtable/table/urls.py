#!
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (
    lista_autores_json_cached, lista_autores_json_no_cached, AutorListView, lista_autores_json_db_cached,
    table_api, table_cached, table_no_cached, table_db_cached, update_author)
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^autores/json/serialize/$', AutorListView.as_view(), name="lista_autores_json_serialize"),
    url(r'^autores/json/no-cached/$', lista_autores_json_no_cached, name="lista_autores_json_no_cached"),
    url(r'^autores/json/cached/$', lista_autores_json_cached, name="lista_autores_json_cached"),
    url(r'^autores/json/db-cached/$', lista_autores_json_db_cached, name="lista_autores_json_db_cached"),

    url(r'^autores/api/$', table_api, name="lista_autores_cliente_api"),
    url(r'^autores/no-cached/$', table_no_cached, name="lista_autores_no_cached"),
    url(r'^autores/cached/$', table_cached, name="lista_autores_cached"),
    url(r'^autores/db-cached/$', table_db_cached, name="lista_autores_db_cached"),

    url(r'^autores/update/(?P<author_id>[\d{1,4}]+)/$', update_author, name="update_author"),
]