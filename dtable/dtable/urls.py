"""dtable URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from dtable.views import index, lista_autores_cliente,lista_libros_cliente, lista_autores_json, lista_libros_json, lista_autores_server, lista_libros_server, lista_autores_server_json, lista_libros_server_json, limpiar_cache

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^autores/$', lista_autores_cliente, name="lista_autores_cliente"),
    url(r'^libros/$', lista_libros_cliente, name="lista_libros_cliente"),

    url(r'^autores/server$', lista_autores_server, name="lista_autores_server"),
    url(r'^libros/server$', lista_libros_server, name="lista_libros_server"),

    url(r'^autores/json$', lista_autores_json, name="lista_autores_json"), 
    url(r'^libros/json$', lista_libros_json, name="lista_libros_json"),
    url(r'^autores/server/json$', lista_autores_server_json, name="lista_autores_server_json"),
    url(r'^libros/server/json$', lista_libros_server_json, name="lista_libros_server_json"),
    url(r'^limpiar-cache/$', limpiar_cache, name="limpiar_cache"),
    
    url(r'^', include('table.urls')),

]
