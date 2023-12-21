from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("historia/", views.historia, name="historia"),
    path("material_mayor/", views.material_mayor, name="material_mayor"),
    path("voluntarios/", views.voluntarios, name="voluntarios"),
    path("brigada_juvenil/", views.brigada_juvenil, name="brigada_juvenil"),
    path("noticias/", views.noticias, name="noticias"),
    path("contacto/", views.contacto, name="contacto"),
    path("postulacion/", views.postulacion, name="postulacion"),
    path("usuarios/logout", views.login, name="logout" ),
    path('ruta-a-tu-vista-detalle-noticia/<int:noticia_id>/', views.detalle_noticia, name='detalle_noticia'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]

if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)