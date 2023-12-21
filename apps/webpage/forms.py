from multiprocessing import Value
from django import forms
from django.core.exceptions import ValidationError
from .models import (CategoriaNoticia, Noticia, Contenido, EspecialidadCarro, CarroBomba, 
                     CargoMiembro, Miembro, Contacto, Postulacion, Galeria)
from django.core.exceptions import ValidationError
import re 

# Formulario para CategoriaNoticia
class CategoriaNoticiaForm(forms.ModelForm):
    class Meta:
        model = CategoriaNoticia
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data

# Formulario para Noticia
class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data

# Formulario para Contenido
class ContenidoForm(forms.ModelForm):
    class Meta:
        model = Contenido
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data

# Formulario para especialidad del carro
class EspecialidadCarroForm(forms.ModelForm):
    class Meta:
        model = EspecialidadCarro
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data

# Formulario para el carro
class CarroBombaForm(forms.ModelForm):
    class Meta:
        model = CarroBomba
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data
        
# Formulario para el cargo del miembro
class CargoMiembroForm(forms.ModelForm):
    class Meta:
        model = CargoMiembro
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data

# Formulario para el miembro
class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data

# Formulario para el contacto
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    #NOMBRE
    def validar_mensaje(value):
    # Verifica si contiene palabras inapropiadas
        PALABRAS_INAPROPIADAS = ['Mierda', 'Puta', 'Conchetumare', 'conchetumare', 'Ctm', 'ctm', 'maricon', 'marica']
        if any(palabra in value.lower() for palabra in PALABRAS_INAPROPIADAS):
            raise ValidationError('El mensaje contiene lenguaje inapropiado.')
    # Mensaje
    def clean_mensaje(self):
        mensaje = self.cleaned_data['mensaje']
        palabras_inapropiadas = ['Mierda', 'Puta', 'Conchetumare', 'conchetumare', 'Ctm', 'ctm', 'maricon', 'marica']
        
        if any(palabra in mensaje.lower() for palabra in palabras_inapropiadas):
            raise ValidationError('El mensaje contiene lenguaje inapropiado.')

        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mensaje):
            raise ValidationError('El mensaje no debe contener URLs.')
        return mensaje

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        dominios_permitidos = ['gmail.com', 'primeracbpa.cl', 'icloud.com', 'cbpa.cl', 'duocuc.cl', 'outlook.es', 'outlook.com', 'outlook.cl']
        dominio_email = correo.split('@')[-1]

        if dominio_email not in dominios_permitidos:
            raise ValidationError('El dominio del correo electrónico no está permitido.')
        return correo

# Formulario para la postulacion
class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        formulario = self.cleaned_data.get('formulario')

        # Validación del tamaño del archivo
        max_size = 10 * 1024 * 1024  # 10 MB
        if formulario.size > max_size:
            raise ValidationError('El tamaño del archivo no puede exceder los 10 MB.')

        # Validación de la extensión del archivo
        if not formulario.name.endswith('.pdf'):
            raise ValidationError('El archivo debe ser un PDF.')
        return cleaned_data

# Formulario para el contacto
class GaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        fields = '__all__'
    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar validaciones que involucren varios campos
        return cleaned_data