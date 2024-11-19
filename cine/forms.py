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

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['pelicula', 'sala', 'fecha', 'hora_inicio']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
        }
