from django.db import models  # type: ignore
from django.utils import timezone  # type: ignore


class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['apellido', 'nombre']

        def __str__(self):
            return f"{self.apellido}, {self.nombre}"


class Editorial(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    resumen = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    anio_publicacion = models.PositiveIntegerField()

    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT, related_name='libros')

    class Meta:
        ordering = ['titulo']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['anio_publicacion']),
        ]

    def __str__(self):
        return f"{self.titulo} ({self.anio_publicacion})"


class Miembro(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # se acepta fecha y hora actual como valor por defecto
    fecha_membresia = models.DateField(default=timezone.now)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Prestamo(models.Model):
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(blank=True, null=True)

    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='prestamos')
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, related_name='prestamos')

    class Meta:
        ordering = ['-fecha_prestamo', '-id']
        constraints = [
            # Un mismo miembro no puede tener un mismo libro prestado mas de una vez al mismo tiempo
            models.UniqueConstraint(
                fields=['libro', 'miembro'],
                condition=models.Q(fecha_devolucion__isnull=True),
                name='unique_prestamo_abierto_por_libro_y_miembro',
            )
        ]

    def __str__(self):
        return f"Préstamo #{self.id} — Libro: {self.libro} — Miembro: {self.miembro}"
