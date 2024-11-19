from django.contrib import admin
from .models import Pelicula, Sala, Reserva, ProductoConfiteria
from .models import CodigoPromocional


admin.site.register(Pelicula)
admin.site.register(Sala)
admin.site.register(Reserva)
admin.site.register(ProductoConfiteria)  # Registro del modelo ProductoConfiteria

@admin.register(CodigoPromocional)
class CodigoPromocionalAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descuento')  # Mostrar código y descuento en la lista
    search_fields = ('codigo',)  # Habilitar búsqueda por código
    list_filter = ('descuento',)  # Filtro por porcentaje de descuento