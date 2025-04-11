from django.db import models
from django.contrib.auth.models import User

class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='fotos_perros/')
    contacto = models.CharField(max_length=100, help_text="Teléfono, correo o red social")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.autor.username}'
