from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

#  ViewSets de la app biblioteca
from biblioteca_app.views import (
    AutorViewSet, EditorialViewSet, LibroViewSet,
    MiembroViewSet, PrestamoViewSet
)

#  router  rutas CRUD
router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'editoriales', EditorialViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'miembros', MiembroViewSet)
router.register(r'prestamos', PrestamoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),  # Panel de administracion
    path('api/', include(router.urls)),  # Todas las rutas CRUD bajo /api/
]
