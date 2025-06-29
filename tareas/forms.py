from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tarea

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario para registrar nuevos usuarios usando el modelo de usuario de Django,
    utiliza los campos básicos: username, password1 y password2
    """
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class TareaForm(forms.ModelForm):
    """
    Formulario para crear o editar tareas,
    utiliza el modelo Tarea y especifica los campos relevantes para el formulario
    """
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion', 'completo', 'fecha_limite']
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
        }

