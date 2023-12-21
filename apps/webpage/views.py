from django.shortcuts import render

# Create your views here.
def index(request):
    template_name = 'webpage/index.html'
    name_hero = 'Inicio'
    # Obtener imágenes para el carrusel
    #imagenes_carrusel = Galeria.objects.all()[:3]
    # Obtener imágenes para la galeria
    #imagenes_galeria = Galeria.objects.all()[:6]
    # Obtener especialidades
    #especialidades = EspecialidadCarro.objects.all()[:3]
    return render(request, template_name, {
        'name_hero': name_hero,
        #'imagenes_carrusel': imagenes_carrusel,
        #'imagenes_galeria': imagenes_galeria,
        #'especialidades' : especialidades,
    })