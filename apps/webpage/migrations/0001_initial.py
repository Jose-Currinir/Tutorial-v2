# Generated by Django 4.2.7 on 2023-12-21 19:50

import apps.webpage.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CargoMiembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=50, unique=True, validators=[apps.webpage.models.validar_mensaje])),
            ],
            options={
                'verbose_name': 'Voluntario - cargo',
                'verbose_name_plural': 'Voluntarios - cargos',
            },
        ),
        migrations.CreateModel(
            name='CategoriaNoticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoriaNoticia', models.CharField(blank=True, max_length=50, null=True, verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Noticia - categoría',
                'verbose_name_plural': 'Noticias - categorías',
            },
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingresa tu nombre completo', max_length=75, validators=[apps.webpage.models.validar_mensaje])),
                ('correo', models.EmailField(help_text='Ingresa tu correo electrónico', max_length=50, validators=[apps.webpage.models.validar_dominio_correo])),
                ('asunto', models.CharField(help_text='Ingresa el motivo por el cual nos contacta', max_length=50, validators=[apps.webpage.models.validar_mensaje])),
                ('mensaje', models.CharField(help_text='Coméntanos en que te podemos ayudar (máximo de 500 caracteres)', max_length=500, validators=[apps.webpage.models.validar_mensaje])),
            ],
            options={
                'verbose_name': 'Recepción - contacto',
                'verbose_name_plural': 'Recepción - contactos',
            },
        ),
        migrations.CreateModel(
            name='EspecialidadCarro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, default='Ingrese una descripción', max_length=50, null=True, verbose_name='Descripción')),
                ('icono', models.ImageField(max_length=50, null=True, upload_to='Iconos', validators=[apps.webpage.models.validar_formato_imagen, apps.webpage.models.validar_tamano_imagen])),
            ],
            options={
                'verbose_name': 'Carro - especialidad',
                'verbose_name_plural': 'Carros - especialidades',
            },
        ),
        migrations.CreateModel(
            name='Galeria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, help_text='Suba la imagen', max_length=50, null=True, validators=[apps.webpage.models.validar_mensaje], verbose_name='Título')),
                ('descripcion', models.CharField(blank=True, help_text='Ingresa una descripcion', max_length=60, null=True, validators=[apps.webpage.models.validar_mensaje], verbose_name='Descripción')),
                ('imagen', models.ImageField(max_length=50, null=True, upload_to='Galeria', validators=[apps.webpage.models.validar_formato_imagen, apps.webpage.models.validar_tamano_imagen])),
            ],
            options={
                'verbose_name': 'Galería - imagen',
                'verbose_name_plural': 'Galería - imágenes',
            },
        ),
        migrations.CreateModel(
            name='Postulacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingresa tu nombre completo', max_length=50, validators=[apps.webpage.models.validar_mensaje])),
                ('correo', models.EmailField(help_text='Ingresa tu correo electrónico', max_length=50, validators=[apps.webpage.models.validar_dominio_correo])),
                ('telefono', models.CharField(help_text='Ingresa tu número de teléfono. No ingresar +56 9', max_length=8, validators=[apps.webpage.models.validar_telefono], verbose_name='Teléfono')),
                ('formulario', models.FileField(help_text='Sube tu formulario en formato PDF', upload_to='postulaciones', validators=[apps.webpage.models.validar_formato_pdf, apps.webpage.models.validar_tamano_pdf])),
            ],
            options={
                'verbose_name': 'Postulación',
                'verbose_name_plural': 'Postulaciones',
            },
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='Título genérico', max_length=50, verbose_name='Título')),
                ('fecha_pub', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
                ('imagen_noticia', models.ImageField(max_length=50, null=True, upload_to='', validators=[apps.webpage.models.validar_tamano_imagen, apps.webpage.models.validar_formato_imagen], verbose_name='Imagen')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webpage.categorianoticia', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
            },
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25, validators=[apps.webpage.models.validar_mensaje])),
                ('apellido', models.CharField(max_length=25, validators=[apps.webpage.models.validar_mensaje])),
                ('foto', models.ImageField(blank=True, max_length=50, null=True, upload_to='Voluntarios', validators=[apps.webpage.models.validar_formato_imagen, apps.webpage.models.validar_tamano_imagen])),
                ('numero_cargo', models.IntegerField(blank=True, default=100, null=True, validators=[django.core.validators.MinValueValidator(41), django.core.validators.MaxValueValidator(1000)], verbose_name='N° Registro')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webpage.cargomiembro')),
            ],
            options={
                'verbose_name': 'Voluntario',
                'verbose_name_plural': 'Voluntarios',
            },
        ),
        migrations.CreateModel(
            name='Contenido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(1000), apps.webpage.models.validar_mensaje])),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.noticia')),
            ],
            options={
                'verbose_name': 'Noticia - contenido',
                'verbose_name_plural': 'Noticias - contenidos',
            },
        ),
        migrations.CreateModel(
            name='CarroBomba',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelo', models.CharField(default='Carro ...', max_length=50)),
                ('origen', models.CharField(default='Nacional', max_length=50)),
                ('anio_fabricacion', models.IntegerField(default=2000, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2200)], verbose_name='Año de fabricación')),
                ('caracteristicas', models.CharField(blank=True, default='Ingrese una característica', max_length=150, null=True, validators=[apps.webpage.models.validar_mensaje], verbose_name='Características')),
                ('foto', models.ImageField(max_length=50, upload_to='Carros', validators=[apps.webpage.models.validar_formato_imagen, apps.webpage.models.validar_tamano_imagen])),
                ('reliquia', models.BooleanField()),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webpage.especialidadcarro')),
            ],
            options={
                'verbose_name': 'Carro',
                'verbose_name_plural': 'Carros',
            },
        ),
    ]
