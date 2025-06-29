from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (ListaTareas, DetalleTarea, CrearTarea, EditarTarea, EliminarTarea, RegistroUsuario, ToggleCompleto,
                    EliminarUsuario)

urlpatterns = [
    path('', ListaTareas.as_view(), name='lista_tareas'),
    path('tarea/<int:pk>/', DetalleTarea.as_view(), name='detalle_tarea'),
    path('tarea/crear/', CrearTarea.as_view(), name='crear_tarea'),
    path('tarea/editar/<int:pk>/', EditarTarea.as_view(), name='editar_tarea'),
    path('tarea/eliminar/<int:pk>/', EliminarTarea.as_view(), name='eliminar_tarea'),
    path('registro/', RegistroUsuario.as_view(), name='registro'),
    path('toggle_completo/<int:pk>/', ToggleCompleto.as_view(), name='toggle_completo'),
    path('eliminar_usuario/', EliminarUsuario.as_view(), name='eliminar_usuario'),
]