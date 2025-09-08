from rest_framework import serializers
from .models import Autor, Editorial, Libro, Miembro, Prestamo


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'


class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = '__all__'


class LibroSerializer(serializers.ModelSerializer):
    autor_nombre_completo = serializers.SerializerMethodField(read_only=True)
    editorial_nombre = serializers.CharField(source='editorial.nombre', read_only=True)

    class Meta:
        model = Libro
        fields = [
            'id', 'titulo', 'resumen', 'isbn', 'anio_publicacion',
            'autor', 'editorial', 'autor_nombre_completo', 'editorial_nombre'
        ]

    def get_autor_nombre_completo(self, obj):
        return f"{obj.autor.nombre} {obj.autor.apellido}"


class MiembroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = '__all__'


class PrestamoSerializer(serializers.ModelSerializer):
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)
    miembro_nombre = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            'id', 'fecha_prestamo', 'fecha_devolucion',
            'libro', 'miembro', 'libro_titulo', 'miembro_nombre'
        ]

    def get_miembro_nombre(self, obj):
        return f"{obj.miembro.nombre} {obj.miembro.apellido}"
