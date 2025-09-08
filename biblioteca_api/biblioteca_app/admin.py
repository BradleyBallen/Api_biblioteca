from django.contrib import admin
from .models import Autor, Editorial, Libro, Miembro, Prestamo

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Libro)
admin.site.register(Miembro)
admin.site.register(Prestamo)
