from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['horario', 'nombre_cliente', 'cantidad_boletos']
        widgets = {
            'horario': forms.Select(attrs={'class': 'form-control'}),  # Campo de selección
        }

    def __init__(self, *args, **kwargs):
        pelicula = kwargs.pop('pelicula', None)  # Pasar película desde la vista
        super().__init__(*args, **kwargs)
        if pelicula:
            self.fields['horario'].queryset = Horario.objects.filter(pelicula=pelicula)


from .models import ProductoConfiteria

class ConfiteriaForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(
        queryset=ProductoConfiteria.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

class CodigoPromocionalForm(forms.Form):
    codigo = forms.CharField(max_length=20, required=False, label="Código Promocional")


from django import forms
from .models import Horario
from datetime import datetime, time

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['pelicula', 'sala', 'fecha', 'hora_inicio']

        widgets = {
            'pelicula': forms.Select(attrs={'class': 'form-select'}),
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < datetime.now().date():
            raise forms.ValidationError("La fecha no puede ser anterior a la fecha actual.")
        return fecha

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if hora_inicio and time(0, 0) <= hora_inicio <= time(10, 0):
            raise forms.ValidationError("El horario no puede estar entre las 00:00 (12 AM) y las 10:00 AM.")
        return hora_inicio