from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pelicula/<int:id>/', views.detalle_pelicula, name='detalle_pelicula'),
    path('reservas/crear/', views.crear_reserva, name='crear_reserva'),
    path('reservas/', views.listar_reservas, name='listar_reservas'),
    path('reservas/pagar/<int:id>/', views.pagar_reserva, name='pagar_reserva'),
    path('reservas/pago/<int:reserva_id>/', views.portal_pago, name='pago'),
    path('gestionar_horarios/', views.gestionar_horarios, name='gestionar_horarios'),
    path('listar_horarios/', views.listar_horarios, name='listar_horarios'),  # Agrega esta línea


]


