#!
# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import lista_autores_json_cached, lista_autores_json_no_cached, AutorListView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^autores/json/cached/$', lista_autores_json_cached, name="lista_autores_json_cached"), 
    url(r'^autores/json/no-cached/$', lista_autores_json_no_cached, name="lista_autores_json_no_cached"),
    
    url(r'^autores/api/$', TemplateView.as_view(template_name="lado_cliente/lista_autores_api.html"), name="lista_autores_cliente_api"),
    url(r'^autores/json/serialize/$', AutorListView.as_view(), name="lista_autores_json_serialize"),
]