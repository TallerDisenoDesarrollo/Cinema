from django.db import models

class Pelicula(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.PositiveIntegerField()  # Duración en minutos
    idioma = models.CharField(max_length=50)
    subtitulos = models.BooleanField(default=False)
    imagen = models.URLField(max_length=200, blank=True, null=True)  # Campo para la URL de la imagen

    def __str__(self):
        return f"{self.titulo} ({self.idioma})"


    def __str__(self):
        return f"{self.titulo} ({self.idioma})"


class Reserva(models.Model):
    pelicula = models.ForeignKey('Pelicula', on_delete=models.CASCADE)  # Esto puede mantenerse para referencias cruzadas
    horario = models.ForeignKey('Horario', on_delete=models.CASCADE, related_name='reservas')  # Relación con el horario
    nombre_cliente = models.CharField(max_length=100)
    fecha_reserva = models.DateTimeField(auto_now_add=True)  # Fecha de la reserva
    cantidad_boletos = models.PositiveIntegerField()
    pagado = models.BooleanField(default=False)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.horario.pelicula.titulo} - {self.horario.fecha} {self.horario.hora_inicio}"



class ProductoConfiteria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class CodigoPromocional(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    descuento = models.DecimalField(max_digits=4, decimal_places=2)  # Ejemplo: 20.00 para 20%

    def __str__(self):
        return f"{self.codigo} - {self.descuento}% de descuento"



class Sala(models.Model):
    numero = models.IntegerField()  # Número identificador de la sala
    capacidad = models.IntegerField()  # Capacidad de la sala

    def __str__(self):
        return f"Sala {self.numero}"

from django.utils.timezone import now
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from datetime import datetime, time

class Horario(models.Model):
    pelicula = models.ForeignKey('Pelicula', on_delete=models.CASCADE, related_name='horarios')
    sala = models.ForeignKey('Sala', on_delete=models.CASCADE, related_name='horarios')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField(blank=True, null=True)

    def clean(self):
        # Validar que la fecha no sea None
        if not self.fecha:
            raise ValidationError("La fecha es un campo obligatorio.")

        # Validar que la hora de inicio no sea None
        if not self.hora_inicio:
            raise ValidationError("La hora de inicio es un campo obligatorio.")

        # Validar que la fecha no sea anterior a hoy
        if self.fecha < datetime.now().date():
            raise ValidationError("La fecha no puede ser anterior a la fecha actual.")

        # Validar que la hora de inicio no esté entre las 00:00 (12 AM) y las 10:00 AM (hasta 10:00:59)
        if time(0, 0) <= self.hora_inicio <= time(10, 0):
            raise ValidationError("El horario no puede estar entre las 00:00 (12 AM) y las 10:00 AM.")

        # Validar superposición de horarios
        if self.hora_fin:
            overlapping_horarios = Horario.objects.filter(
                sala=self.sala,
                fecha=self.fecha,
                hora_inicio__lt=self.hora_fin,
                hora_fin__gt=self.hora_inicio
            ).exclude(id=self.id)

            if overlapping_horarios.exists():
                raise ValidationError("Ya existe un horario que se superpone en esta sala.")

    def save(self, *args, **kwargs):
        # Cálculo automático de hora_fin antes de guardar
        if not self.hora_fin and self.hora_inicio and self.pelicula.duracion:
            hora_inicio_datetime = datetime.combine(self.fecha, self.hora_inicio)
            duracion = timedelta(minutes=self.pelicula.duracion)
            self.hora_fin = (hora_inicio_datetime + duracion).time()
        super().save(*args, **kwargs)
import logging

logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

def clean(self):
    import logging
    logger = logging.getLogger(__name__)
    logger.debug(f"sala={self.sala}, fecha={self.fecha}, hora_inicio={self.hora_inicio}, hora_fin={self.hora_fin}")

    if not self.sala or not self.fecha or not self.hora_inicio or not self.hora_fin:
        raise ValidationError("Todos los campos deben estar llenos antes de validar.")

    overlapping_horarios = Horario.objects.filter(
        sala=self.sala,
        fecha=self.fecha,
        hora_inicio__lt=self.hora_fin,
        hora_fin__gt=self.hora_inicio
    ).exclude(id=self.id)
    if overlapping_horarios.exists():
        raise ValidationError("Ya existe un horario que se superpone en esta sala.")


def save(self, *args, **kwargs):
    if self.hora_inicio and self.pelicula and self.pelicula.duracion:
        hora_inicio_datetime = datetime.combine(self.fecha, self.hora_inicio)
        duracion = timedelta(minutes=self.pelicula.duracion)
        self.hora_fin = (hora_inicio_datetime + duracion).time()
    super().save(*args, **kwargs)
