# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.cache import cache

# Create your models here.
					

class Autor(models.Model):
	nombre=models.CharField(max_length=30, verbose_name="Nombre ")
	apellidos=models.CharField(max_length=40, verbose_name="Apellidos ", )
	email=models.EmailField(verbose_name="Email:")

	class Meta:
		ordering = ['nombre']
		verbose_name_plural = "Autores"

	def __unicode__(self):
		return '%s %s' %(self.nombre, self.apellidos)

	def save(self, *args, **kwargs):
		#Se elimina el cache cada vez que se actualize la notificacion
		cache.delete("Autores-")
		super(Autor, self).save(*args, **kwargs)

			
	
class Libro(models.Model):
	titulo=models.CharField(max_length=100)
	autor=models.ManyToManyField(Autor)
	fecha_publicacion=models.DateField()
	portada=models.ImageField(upload_to='portadas')

	def __unicode__(self):
		return self.titulo

	def save(self, *args, **kwargs):
		cache.delete("Libros-")
		super(Libro, self).save(*args, **kwargs)