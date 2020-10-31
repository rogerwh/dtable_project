# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.cache import cache

import random
import uuid
from django.utils import timezone

# Create your models here.
                    
def total_rand():
    return random.randint(800, 1000)

def rand_bool():
    b = [True, False]
    return b[random.randint(0,1)]

def rand_state():
    return random.randint(0, 4)

def rand_date():
    return timezone.now()

class Autor(models.Model):
    
    ESTADO_FACTURA = (
        (0, 'Pendiente de pago'),
        (1, 'Pagada'),
        (2, 'Cancelada'),
        (3, 'En Revision'),
        (4, 'Se Transfirio'),    
    )

    ESTADOS = (
        (0, 'Quintana Roo'),
        (1, 'CDMX'),
        (2, 'Guadalajara'),
        (3, 'Chihuahua'),
        (4, 'Oaxaca'),    
    )

    nombre = models.CharField(max_length=30, verbose_name="Nombre ")
    apellidos = models.CharField(max_length=40, verbose_name="Apellidos ", )
    email = models.EmailField(verbose_name="Email:")

    # Added for timing
    fecha_emision = models.DateField(default=rand_date)
    fecha_vencimiento = models.DateField(default=rand_date)
    fecha_pago = models.DateTimeField(default=rand_date)

    total = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)
    total2 = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)
    total3 = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)

    total_cobrado = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)
    impuestos = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)
    descuento = models.DecimalField(max_digits=15, decimal_places=2, default=total_rand)

    referencia = models.UUIDField(default=uuid.uuid4, verbose_name="Referencia")
    referencia2 = models.UUIDField(default=uuid.uuid4, verbose_name="Referencia")
    referencia3 = models.UUIDField(default=uuid.uuid4, verbose_name="Referencia")

    url = models.CharField(max_length=250)
    url2 = models.CharField(max_length=250)
    url3 = models.CharField(max_length=250)

    factura_generica = models.BooleanField(default=rand_bool)
    reconexion_aplicada = models.BooleanField(verbose_name="¿Ya se aplico reconexión?", default=rand_bool)
    mora_aplicada = models.BooleanField(verbose_name="¿Ya se aplico mora?",  default=rand_bool)

    estado = models.PositiveSmallIntegerField(choices=ESTADO_FACTURA, default=rand_state)

    # fk
    ciudad = models.ForeignKey('table.Ciudad', verbose_name="Ciudad", null=True, related_name='autor_ciudad')
    perfil = models.ForeignKey('table.Perfil', verbose_name='Autores', null=True)

    class Meta:
        ordering = ['nombre']
        verbose_name_plural = "Autores"

    def __unicode__(self):
        return '%s %s' %(self.nombre, self.apellidos)

    def save(self, *args, **kwargs):
        #Se elimina el cache cada vez que se actualize la notificacion
        cache.delete("Autores-")
        super(Autor, self).save(*args, **kwargs)


class Perfil(models.Model):

    telefono = models.CharField(max_length=20)
    direccion = models.TextField(blank=True)
    informacion = models.TextField(blank=True)
    
    # FK
    editorial = models.ForeignKey('table.Editorial', related_name='perfiles')


class Editorial(models.Model):

    nombre = models.CharField(max_length=250)
    direccion = models.TextField(blank=True)
    telefono = telefono = models.CharField(max_length=20)
    eslogan = models.CharField(max_length=250)
    rfc = models.CharField(max_length=100, default=uuid.uuid4)
    rfc2 = models.CharField(max_length=100, default=uuid.uuid4)

    #FK
    distribuidor = models.ForeignKey('table.Distribuidor', related_name='Editoriales')


class Distribuidor(models.Model):

    nombre = models.CharField(max_length=250)


class Ciudad(models.Model):

    nombre = models.CharField(max_length=250)
    personas = models.UUIDField(default=uuid.uuid4)
    personas2 = models.UUIDField(default=uuid.uuid4)

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