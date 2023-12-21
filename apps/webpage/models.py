import os, re
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator, MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator

# Validaciones
# IMAGEN
def validar_tamano_imagen(value):
    limite = 20 * 1024 * 1024  # 20 MB
    if value.size > limite:
        raise ValidationError('El tamaño del archivo no puede exceder los 20 MB.')
def validar_formato_imagen(value):
    if not value.name.endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('El formato del archivo debe ser PNG, JPEG o JPG.')
#TELEFONO
def validar_telefono(value):
    if not re.match(r'^\d{8}$', value):
        raise ValidationError('El número de teléfono debe tener exactamente 8 dígitos y contener solo números.')
#MENSAJE
PALABRAS_INAPROPIADAS = ['Mierda', 'Puta', 'Conchetumare', 'conchetumare', 'Ctm', 'ctm', 'maricon', 'marica']
def validar_mensaje(value):
    # Verifica si contiene palabras inapropiadas
    if any(palabra in value.lower() for palabra in PALABRAS_INAPROPIADAS):
        raise ValidationError('El mensaje contiene lenguaje inapropiado.')

    # Verifica si contiene URLs
    if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value):
        raise ValidationError('El mensaje no debe contener URLs.')
#CORREO
DOMINIOS_PERMITIDOS = ['gmail.com', 'primeracbpa.cl', 'icloud.com', 'cbpa.cl', 'duocuc.cl', 'outlook.es', 'outlook.com', 'outlook.cl']
def validar_dominio_correo(value):
    dominio_email = value.split('@')[-1]
    if dominio_email not in DOMINIOS_PERMITIDOS:
        raise ValidationError('El dominio del correo electrónico no está permitido.')
#PDFS
def validar_formato_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('El archivo debe ser un PDF.')
def validar_tamano_pdf(value):
    limite = 20 * 1024 * 1024  # 20 MB
    if value.size > limite:
        raise ValidationError('El tamaño del pdf no puede exceder los 20 MB.')
# Validaciones

class CategoriaNoticia(models.Model):
    CategoriaNoticia = models.CharField(max_length=50, null=True, blank=True, editable=True, verbose_name="Categoría")
    def __str__(self):
        return self.CategoriaNoticia
    class Meta:
        verbose_name = "Noticia - categoría"
        verbose_name_plural = "Noticias - categorías"

class Noticia(models.Model):
    titulo          = models.CharField(max_length=50, null=False, blank=False, default="Título genérico", editable=True, verbose_name="Título")
    fecha_pub       = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    imagen_noticia  = models.ImageField(max_length=50, null=True, verbose_name="Imagen", validators=[validar_tamano_imagen,validar_formato_imagen])
    categoria       = models.ForeignKey(CategoriaNoticia, on_delete=models.PROTECT, verbose_name="Categoría")
    def __str__(self):
        return str(self.fecha_pub) + " " + self.titulo
    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"

class Contenido(models.Model):
    contenido   = models.TextField(null=True, blank=True, editable=True,validators=[MaxLengthValidator(1000),validar_mensaje])
    noticia     = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    def __str__(self):
        return self.contenido
    class Meta:
        verbose_name = "Noticia - contenido"
        verbose_name_plural = "Noticias - contenidos"

class EspecialidadCarro(models.Model):
    especialidad    = models.CharField(max_length=50, null=False, blank=False, editable=True)
    descripcion     = models.CharField(max_length=50, null=True, blank=True, editable=True, default="Ingrese una descripción", verbose_name="Descripción")
    icono           = models.ImageField(max_length=50, null=True, upload_to="Iconos", validators=[validar_formato_imagen,validar_tamano_imagen])
    def __str__(self):
        return self.especialidad
    class Meta:
        verbose_name = "Carro - especialidad"
        verbose_name_plural = "Carros - especialidades"

class CarroBomba(models.Model):
    modelo              = models.CharField(max_length=50, null=False, blank=False, editable=True, default="Carro ...")
    origen              = models.CharField(max_length=50, null=False, blank=False, editable=True, default="Nacional")
    anio_fabricacion    = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1800), MaxValueValidator(2200)], default=2000, verbose_name="Año de fabricación")
    caracteristicas     = models.CharField(max_length=150, null=True, blank=True, editable=True, default="Ingrese una característica", verbose_name="Características", validators=[validar_mensaje])
    especialidad        = models.ForeignKey(EspecialidadCarro, on_delete=models.PROTECT)
    foto                = models.ImageField(max_length=50, null=False, upload_to="Carros",validators=[validar_formato_imagen,validar_tamano_imagen])
    reliquia            = models.BooleanField(blank=False, null=False)
    def __str__(self):
        return self.modelo
    class Meta:
        verbose_name = "Carro"
        verbose_name_plural = "Carros"

class CargoMiembro(models.Model):
    cargo = models.CharField(max_length=50, unique=True, editable=True, validators=[validar_mensaje])
    def __str__(self):
        return self.cargo
    class Meta:
        verbose_name = "Voluntario - cargo"
        verbose_name_plural = "Voluntarios - cargos"
    
class Miembro(models.Model):
    nombre          = models.CharField(max_length=25, null=False, blank=False, editable=True, validators=[validar_mensaje])
    apellido        = models.CharField(max_length=25, null=False, blank=False, editable=True, validators=[validar_mensaje])
    cargo           = models.ForeignKey(CargoMiembro, on_delete=models.PROTECT)
    foto            = models.ImageField(max_length=50, null=True, blank=True, upload_to="Voluntarios", validators=[validar_formato_imagen,validar_tamano_imagen])
    numero_cargo    = models.IntegerField(null=True, blank=True, default=100, validators=[MinValueValidator(41), MaxValueValidator(1000)], verbose_name="N° Registro")
    def __str__(self):
        return self.nombre + " " + self.apellido
    class Meta:
        verbose_name = "Voluntario"
        verbose_name_plural = "Voluntarios"

class Contacto(models.Model):
    nombre  = models.CharField(max_length=75, null=False, blank=False, help_text="Ingresa tu nombre completo", validators=[validar_mensaje])
    correo  = models.EmailField(max_length=50, null=False, blank=False, help_text="Ingresa tu correo electrónico", validators=[validar_dominio_correo])
    asunto  = models.CharField(max_length=50, null=False, blank=False, help_text="Ingresa el motivo por el cual nos contacta", validators=[validar_mensaje])
    mensaje = models.CharField(max_length=500, null=False, blank=False, help_text="Coméntanos en que te podemos ayudar (máximo de 500 caracteres)", validators=[validar_mensaje])
    def __str__(self):
        return "Mensaje de" + self.nombre
    class Meta:
        verbose_name = "Recepción - contacto"
        verbose_name_plural = "Recepción - contactos"

class Postulacion(models.Model):
    nombre = models.CharField(max_length=50, null=False, blank=False, help_text="Ingresa tu nombre completo", validators=[validar_mensaje])
    correo = models.EmailField(max_length=50, null=False, blank=False, help_text="Ingresa tu correo electrónico", validators=[validar_dominio_correo])
    telefono = models.CharField(max_length=8, null=False, blank=False, help_text="Ingresa tu número de teléfono. No ingresar +56 9", verbose_name="Teléfono", validators=[validar_telefono])
    formulario = models.FileField(max_length=100, null=False, upload_to="postulaciones", help_text="Sube tu formulario en formato PDF", validators=[validar_formato_pdf, validar_tamano_pdf])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Postulación"
        verbose_name_plural = "Postulaciones"
       
class Galeria(models.Model):
    titulo      = models.CharField(max_length=50, null=True, blank=True, help_text="Suba la imagen", verbose_name="Título", validators=[validar_mensaje])
    descripcion = models.CharField(max_length=60, null=True, blank=True, help_text="Ingresa una descripcion", verbose_name="Descripción", validators=[validar_mensaje])
    imagen      = models.ImageField(max_length=50, null=True, upload_to="Galeria", validators=[validar_formato_imagen,validar_tamano_imagen])
    def __str__(self):
        return self.titulo
    class Meta:
        verbose_name = "Galería - imagen"
        verbose_name_plural = "Galería - imágenes"
    
