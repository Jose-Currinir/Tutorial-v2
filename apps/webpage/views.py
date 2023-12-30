from email.message import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import login as lg, logout as lt, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
#Imports para generar pdf
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from datetime import date, timedelta
from .forms import *
from django.core.exceptions import ValidationError
import logging
from django.contrib.auth import logout
from django.urls import reverse


@cache_page(60 * 2)
def index(request):
    template_name = 'webpage/index.html'
    name_hero = 'Inicio'
    # Obtener imágenes para el carrusel
    imagenes_carrusel = Galeria.objects.all()[:3]
    # Obtener imágenes para la galeria
    imagenes_galeria = Galeria.objects.all()[:6]
    # Obtener especialidades
    especialidades = EspecialidadCarro.objects.all()[:3]
    return render(request, template_name, {
        'name_hero': name_hero,
        'imagenes_carrusel': imagenes_carrusel,
        'imagenes_galeria': imagenes_galeria,
        'especialidades' : especialidades,
    })

@cache_page(60 * 2)
def historia(request):
    page = 'webpage/historia.html'
    name_hero = 'Historia'
    description_hero = 'Descripción (30 a 40 palabras)'
    return render(request, page, {
         'name_hero' : name_hero,
         'description_hero' : description_hero
    })

@cache_page(60 * 2)
def material_mayor(request):
    page                =   'webpage/material-mayor.html'
    name_hero           =   'Material Mayor'
    description_hero    =   'Descripción (30 a 40 palabras)'
    carros_operativo    =   CarroBomba.objects.filter(reliquia=False)
    carros_reliquia     =   CarroBomba.objects.filter(reliquia=True)
    especialidades      =   EspecialidadCarro.objects.all()[:3]
    return render(request, page, {
            'name_hero': name_hero,
            'description_hero': description_hero,
            'carros_operativo': carros_operativo,
            'carros_reliquia':  carros_reliquia,
            'especialidades':   especialidades,
    })

@cache_page(60 * 2)
def voluntarios(request):
    page = 'webpage/voluntarios.html'
    name_hero = 'Voluntarios'
    description_hero = 'Descripción (30 a 40 palabras)'
    # Of. Administrativos
    LIST_ADMINISTRATIVOS = ['Director', 'Secretario', 'Tesorero', 'Intendente']
    administrativos = Miembro.objects.filter(cargo__cargo__in=LIST_ADMINISTRATIVOS).order_by('numero_cargo')
    # Of. Operativos
    LIST_OPERATIVOS = ['Capitán', 'Teniente primero', 'Teniente primero', 'Teniente tercero', 'Ayudante', 'Ayudante segundo', 'Ayudante tercero', 'Maquinista']
    operativos = Miembro.objects.filter(cargo__cargo__in=LIST_OPERATIVOS).order_by('numero_cargo')
    # Voluntarios Honorarios
    LIST_HONORARIOS = ['Vol. honorario']
    honorarios = Miembro.objects.filter(cargo__cargo__in=LIST_HONORARIOS).order_by('numero_cargo')
    # Voluntarios Activos
    LIST_ACTIVOS = ['Vol. activo']
    activos = Miembro.objects.filter(cargo__cargo__in=LIST_ACTIVOS).order_by('numero_cargo')
    return render(request, page, {
        'name_hero': name_hero,
        'description_hero': description_hero,
        'administrativos': administrativos,
        'operativos': operativos,
        'honorarios':honorarios,
        'activos': activos
    })

@cache_page(60 * 2)
def brigada_juvenil(request):
    page = 'webpage/brigada-juvenil.html'
    name_hero = 'Brigada Juvenil'
    description_hero = 'A'
    return render(request, page, {
        'name_hero' : name_hero,
        'description_hero' : description_hero
        })

@cache_page(60 * 2)
def noticias(request):
    page = 'webpage/noticias.html'
    name_hero = 'Artículos'
    description_hero = 'Espacio actualizado con las últimas noticias y eventos relacionados con la Primera Compañía, incluyendo intervenciones y actividades comunitarias.'
    # Noticias de historia
    noticias_historia = Noticia.objects.filter(categoria__CategoriaNoticia="Historia")
    # Noticias para la comunidad
    noticias_comunidad = Noticia.objects.filter(categoria__CategoriaNoticia='Comunidad')    
    # Todas las noticias
    noticias = Noticia.objects.all()
    # Obtener filtro de fecha
    fecha_filtro = request.GET.get('fecha_filtro')
    # Filtrar por fecha si se selecciona un filtro
    if fecha_filtro == 'hoy':
        noticias = noticias.filter(fecha_pub__date=date.today())
    elif fecha_filtro == 'semana':
        noticias = noticias.filter(fecha_pub__date__gte=date.today() - timedelta(days=7))
    # Pasa los datos de las noticias a la plantilla HTML
    return render(request, page, {
        'name_hero': name_hero,
        'description_hero': description_hero,
        'noticias': noticias,
        'noticias_historia':noticias_historia,
        'noticias_comunidad': noticias_comunidad,
        'fecha_filtro': fecha_filtro,
    })

@cache_page(60 * 2)
def detalle_noticia(request, noticia_id):
    noticia = get_object_or_404(Noticia, pk=noticia_id)
    return render(request, 'webpage_fun/detalle_noticia.html', {'noticia': noticia})

@cache_page(60 * 2)
def contacto(request):
    page = 'webpage/contacto.html'
    name_hero = 'Contacto'
    description_hero = 'Descripción (30 a 40 palabras)'
    
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Datos del formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            correo_comaud = 'comisionaudiovisual.primera@gmail.com'

            # Renderizar la plantilla HTML con los datos
            cuerpo_correo = render_to_string('correo_contacto.html', {
                'nombre': nombre,
                'correo': correo,
                'asunto': asunto,
                'mensaje': mensaje
            })

            # Enviar el correo electrónico
            send_mail(
                'Nueva respuesta al formulario de contacto',
                cuerpo_correo,
                correo_comaud,
                [correo_comaud],
                html_message=cuerpo_correo  # Versión HTML del mensaje
            )

            messages.success(request, 'Tu mensaje ha sido enviado con éxito.')
            return redirect('contacto')  # Asegúrate de que 'contacto' sea el nombre correcto de la URL

    else:
        form = ContactoForm()

    return render(request, page, {
        'name_hero': name_hero,
        'description_hero': description_hero,
        'form': form,  # Pasa el formulario a la plantilla
    })

@cache_page(60 * 2)
def postulacion(request):
    page = 'webpage/postulaciones.html'
    name_hero = 'Postulación'
    description_hero = 'Descripción (30 a 40 palabras)'
    if request.method == 'POST':
        # Asegúrate de pasar request.FILES para manejar la subida de archivos
        form = PostulacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Aquí puedes agregar más lógica, como enviar un correo de confirmación
            messages.success(request, 'Tu postulación ha sido enviada con éxito.')
            return redirect(reverse('postulacion'))  # Reemplaza con la URL a la que deseas redirigir
        else:
            # Manejo de errores en el formulario
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = PostulacionForm()  # Crear un formulario vacío para solicitudes GET
        
    return render(request, page, {
        'name_hero': name_hero,
        'description_hero': description_hero,
        'form': form,
    })

@cache_page(60 * 2)
def login (request):
    page = 'users/login.html'
    name_hero = 'Inicio Sesión'
    description_hero = 'Descripción (30 a 40 palabras)'
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        usuarios = authenticate(username=username, password=password)
        if usuarios:
            lg(request,usuarios)
            return redirect('/admin/')
    return render(request, page, {
        'name_hero' : name_hero,
        'description_hero' : description_hero
        })

#Exportar pdfs
#def exportar_miembros_pdf(request):
    # Renderiza una plantilla HTML como string
    html_string = render_to_string('miembros_pdf_template.html', {'miembros': Miembro.objects.all()})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="miembros.pdf"'
    # Convierte el HTML a PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    if pisa_status.err:
        return HttpResponse('Ocurrieron errores <pre>' + html_string + '</pre>')
    return response

def cerrar_sesion(request):
    logout(request)
    return redirect('index') 