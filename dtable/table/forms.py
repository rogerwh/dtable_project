from django import forms
from table.models import Libro, Autor, Empresa, Ciudad

class LibroForm(forms.ModelForm):

    class Meta:
        model = Libro
        fields= [
            'titulo',
            'autor',
            'fecha_publicacion',
            'portada',
        ]
        
        labels= {
            'titulo': 'Titulo',
            'autor': 'Autor',
            'editor': 'Editor',
            'fecha_publicacion':' Fecha de publicacion',
            'portada':'Portada',
        }

        widgets= {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_publicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'portada': forms.Select(attrs={'class': 'form-control'}),

        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = [
            'nombre', 
            'apellidos', 
            'email',
            'total',
            'total2',
            'total3',
            'referencia',
            'referencia2',
            'referencia3',
            'factura_generica',
            'reconexion_aplicada',
            'mora_aplicada',
            'estado',
            'ciudad',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.TextInput(attrs={'class': 'form-control'}),
            'total2': forms.TextInput(attrs={'class': 'form-control'}),
            'total3': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia2': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia3': forms.TextInput(attrs={'class': 'form-control'}),
            'factura_generica': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'reconexion_aplicada': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'mora_aplicada': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class Filter(forms.Form):

    ESTADO_FACTURA = (
        ("", 'Todos los estados'),
        (0, 'Pendiente de pago'),
        (1, 'Pagada'),
        (2, 'Cancelada'),
        (3, 'En Revision'),
        (4, 'Se Transfirio'),
    )

    empresa__id = forms.ModelChoiceField(queryset=Empresa.objects.all(), required=False, label="Empresa")
    fecha_emision = forms.DateField(initial="2020-10-31", required=False)
    estado = forms.ChoiceField(choices=ESTADO_FACTURA, required=False)
    ciudad__id = forms.ModelChoiceField(queryset=Ciudad.objects.all(), required=False, label="Ciudad")
