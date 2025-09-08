from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Autor, Editorial, Libro, Miembro, Prestamo
from .serializers import (
    AutorSerializer, EditorialSerializer, LibroSerializer,
    MiembroSerializer, PrestamoSerializer
)


class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nombre', 'apellido']
    search_fields = ['nombre', 'apellido', 'biografia']
    ordering_fields = ['nombre', 'apellido']


class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nombre']
    search_fields = ['nombre', 'direccion', 'telefono']
    ordering_fields = ['nombre']


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.select_related('autor', 'editorial').all()
    serializer_class = LibroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtros basicos requeridos
    filterset_fields = {
        'autor': ['exact'],  # /api/libros/?autor=1
        'editorial': ['exact'],  # /api/libros/?editorial=2
        'anio_publicacion': ['exact', 'gte', 'lte']
    }

    # Busquedas de texto
    search_fields = ['titulo', 'resumen', 'autor__nombre', 'autor__apellido', 'editorial__nombre']

    # Ordenamiento
    ordering_fields = ['anio_publicacion', 'titulo', 'id']


class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.all()
    serializer_class = MiembroSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {'fecha_membresia': ['exact', 'gte', 'lte']}
    search_fields = ['nombre', 'apellido', 'email']
    ordering_fields = ['apellido', 'nombre', 'fecha_membresia']


class PrestamoViewSet(viewsets.ModelViewSet):
    queryset = Prestamo.objects.select_related('libro', 'miembro').all()
    serializer_class = PrestamoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Requeridos: filtrar por fecha de prestamo o por miembro
    filterset_fields = {
        'miembro': ['exact'],  # /api/prestamos/?miembro=3
        'fecha_prestamo': ['exact', 'gte', 'lte', 'range'],  # /api/prestamos/?fecha_prestamo__gte=2025-01-01
        'fecha_devolucion': ['isnull', 'exact', 'gte', 'lte']
    }

    search_fields = ['libro__titulo', 'miembro__nombre', 'miembro__apellido']
    ordering_fields = ['fecha_prestamo', 'fecha_devolucion', 'id']
