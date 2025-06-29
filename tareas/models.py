from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tarea(models.Model):
    """
    Modelo que representa una tarea individual en la lista de tareas de un usuario
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(null=True, blank=True)
    completo = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['completo']

