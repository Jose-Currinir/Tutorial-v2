from django.contrib import admin
from .models import *
# Imports para crear pdfs
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# Register your models here.

class ContenidoInline(admin.StackedInline):
    model = Contenido
    extra = 1
    
@admin.register(CategoriaNoticia)
class CategoriaNoticiaAdmin(admin.ModelAdmin):
    list_per_page = 10
    
@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    inlines = [ContenidoInline]
    list_display = ('titulo', 'fecha_pub', 'categoria', 'imagen_noticia')
    ordering = ('fecha_pub',)
    search_fields = ('fecha_pub','titulo','categoria')
    list_display_links = ('titulo', 'fecha_pub', 'categoria', 'imagen_noticia')
    list_filter = ('titulo', 'fecha_pub', 'categoria',)
    list_per_page = 10

@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ('contenido', 'noticia',)
    ordering = ('noticia',)
    search_fields = ('contenido', 'noticia',)
    list_display_links = ('contenido', 'noticia',)
    list_filter = ('contenido', 'noticia',)
    list_per_page = 5

@admin.register(EspecialidadCarro)
class EspecialidadCarroAdmin(admin.ModelAdmin):
    list_display = ('especialidad', 'descripcion', 'icono')
    search_fields = ('especialidad', 'descripcion', 'icono')
    list_filter = ('especialidad', 'descripcion', 'icono')
    list_per_page = 10

@admin.register(CarroBomba)
class CarroBombaAdmin(admin.ModelAdmin):
    list_display = ('modelo', 'origen', 'anio_fabricacion', 'reliquia')
    search_fields = ('modelo', 'origen', 'anio_fabricacion', 'reliquia')
    list_filter = ('modelo', 'origen', 'anio_fabricacion', 'reliquia')
    list_per_page = 10

#Funcionalidad extra
def exportar_miembros_pdf(modeladmin, request, queryset):
    html_string = render_to_string('miembros_pdf_template.html', {'miembros': queryset})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="miembros.pdf"'
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Ocurrieron errores al generar el PDF')
    return response
exportar_miembros_pdf.short_description = "Exportar a PDF"


admin.site.register(CargoMiembro)

@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cargo', 'foto', 'numero_cargo')
    search_fields = ('nombre', 'apellido', 'cargo', 'numero_cargo')
    list_filter = ('nombre', 'apellido', 'cargo', 'numero_cargo')
    actions = [exportar_miembros_pdf]


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre','correo', 'asunto', 'mensaje')
    search_fields = ('nombre','correo', 'asunto', 'mensaje')

@admin.register(Postulacion)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'telefono', 'formulario')
    search_fields = ('nombre', 'correo', 'telefono', 'formulario')

@admin.register(Galeria)
class ContactoAdmin(admin.ModelAdmin):
    list_display    = ('titulo', 'descripcion', 'imagen')
    search_fields   = ('titulo', 'descripcion', 'imagen')
    list_per_page = 10
