from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pelicula, Sala, Reserva
from .forms import ReservaForm
from .models import ProductoConfiteria


def home(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'cine/home.html', {'peliculas': peliculas})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Pelicula, Horario
from .forms import ReservaForm

def detalle_pelicula(request, id):
    pelicula = get_object_or_404(Pelicula, id=id)  # Obtiene la película
    horarios = Horario.objects.filter(pelicula=pelicula)  # Filtra los horarios de la película

    if request.method == 'POST':
        form = ReservaForm(request.POST, pelicula=pelicula)  # Pasa la película al formulario
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.pelicula = pelicula  # Asigna la película a la reserva
            reserva.save()
            return redirect('pago', reserva_id=reserva.id)  # Redirige al portal de pago
    else:
        form = ReservaForm(pelicula=pelicula)  # Inicializa el formulario con los horarios de la película

    return render(
        request,
        'cine/detalle.html',
        {'pelicula': pelicula, 'horarios': horarios, 'form': form}
    )



def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_reservas')
    else:
        form = ReservaForm()
    return render(request, 'cine/crear_reserva.html', {'form': form})

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def listar_reservas(request):
    reservas = Reserva.objects.all()
    return render(request, 'cine/listar_reservas.html', {'reservas': reservas})


def pagar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.pagado = True
    reserva.save()
    return redirect('listar_reservas')

from decimal import Decimal, ROUND_DOWN
from django.shortcuts import render, get_object_or_404
from .models import Reserva, ProductoConfiteria, CodigoPromocional
from .forms import ConfiteriaForm, CodigoPromocionalForm

PRECIO_ENTRADA = 5000  # Precio fijo por entrada

def portal_pago(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    horario = reserva.horario  # Obtiene el horario relacionado con la reserva
    sala = horario.sala  # Obtiene la sala asociada al horario

    confiteria_form = ConfiteriaForm(request.POST or None)
    codigo_form = CodigoPromocionalForm(request.POST or None)

    descuento_aplicado = Decimal('0.00')  # Inicializamos el descuento
    codigo_usado = None  # Para mostrar el código en el resumen

    # Calcular total por entradas
    total_reserva = Decimal(reserva.cantidad_boletos) * Decimal(PRECIO_ENTRADA)

    if request.method == 'POST' and confiteria_form.is_valid() and codigo_form.is_valid():
        productos_seleccionados = confiteria_form.cleaned_data['productos']
        total_confiteria = sum(producto.precio for producto in productos_seleccionados)

        # Validar código promocional
        codigo = codigo_form.cleaned_data['codigo']
        if codigo:
            try:
                codigo_promocional = CodigoPromocional.objects.get(codigo=codigo)
                descuento_aplicado = (total_reserva + total_confiteria) * (codigo_promocional.descuento / Decimal('100'))
                codigo_usado = codigo_promocional.codigo
            except CodigoPromocional.DoesNotExist:
                descuento_aplicado = Decimal('0.00')

        total_final = (total_reserva + total_confiteria - descuento_aplicado).quantize(Decimal('1'), rounding=ROUND_DOWN)

        return render(
            request,
            'cine/resumen_pago.html',
            {
                'reserva': reserva,
                'productos': productos_seleccionados,
                'total_reserva': total_reserva,
                'total_confiteria': total_confiteria,
                'descuento_aplicado': descuento_aplicado,
                'total_final': total_final,
                'codigo_usado': codigo_usado,
                'sala': sala,  # Incluye la sala en el contexto
            }
        )

    return render(
        request,
        'cine/portal_pago.html',
        {
            'reserva': reserva,
            'confiteria_form': confiteria_form,
            'codigo_form': codigo_form,
            'total_reserva': total_reserva,
            'sala': sala,  # Incluye la sala en el contexto
        }
    )


from django.shortcuts import render, redirect
from .forms import HorarioForm
from .models import Horario

from django.shortcuts import render, redirect, get_object_or_404
from .models import Horario
from .forms import HorarioForm

def gestionar_horarios(request):
    if request.method == 'POST':
        form = HorarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el horario si es válido
            return redirect('gestionar_horarios')
    else:
        form = HorarioForm()

    horarios = Horario.objects.all()
    return render(request, 'cine/gestionar_horarios.html', {'form': form, 'horarios': horarios})



def listar_horarios(request):
    horarios = Horario.objects.all()
    return render(request, 'cine/listar_horarios.html', {'horarios': horarios})