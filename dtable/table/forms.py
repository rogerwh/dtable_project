from django import forms
from table.models import Libro, Autor

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
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('nombre', 'apellidos', 'email',)
	
		