from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, TareaForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea

# Create your views here.

class ListaTareas(LoginRequiredMixin, ListView):
    """
    Vista para mostrar la lista de tareas del usuario autenticado, permite filtrar por título,
    estado (completas/incompletas) y ordenar por fecha o estado
    """
    model = Tarea
    template_name = 'tareas/principal.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        """
        Obtiene las tareas filtradas y ordenadas según los parámetros GET:
        - buscar: filtro por el título que contenga el texto
        - mostrar: si es'incompletas', muestras solo las tareas sin completar
        - orden: puede ser 'fecha' o 'estado? para ordenar las tareas
        """
        usuario = self.request.user
        orden = self.request.GET.get('orden', 'estado')
        buscar = self.request.GET.get('buscar', '').strip()
        mostrar = self.request.GET.get('mostrar')

        qs = Tarea.objects.filter(usuario=usuario)

        if buscar:
            qs = qs.filter(titulo__icontains=buscar)

        if mostrar == 'incompletas':
            qs = qs.filter(completo=False)

        if orden == 'fecha':
            qs = qs.order_by('-creado')
        else:
            qs = qs.order_by('completo', '-creado')

        return qs

    def get_context_data(self, **kwargs):
        """
        Añade al contexto las variables para mantener los filtros y orden en la plantilla
        """
        context = super().get_context_data(**kwargs)
        context['orden_actual'] = self.request.GET.get('orden', 'estado')
        context['buscar'] = self.request.GET.get('buscar', '')
        context['mostrar'] = self.request.GET.get('mostrar', '')
        return context

class DetalleTarea(LoginRequiredMixin, DetailView):
    """
    Vista para mostrar los detalles de una tarea, solo puede acceder a ellas su usuario autenticado
    """
    model = Tarea
    template_name = 'tareas/detalle.html'
    context_object_name = 'tarea'

    def get_queryset(self):
        return Tarea.objects.filter(usuario=self.request.user)

class CrearTarea(LoginRequiredMixin, CreateView):
    """
    Vista para crear nueva tarea, asocia automaticamente la tarea con el usuario autenticado
    """
    model = Tarea
    form_class = TareaForm
    success_url = reverse_lazy('lista_tareas')

    def form_valid(self, form):
        """
        Antes de guardar, asigna el usuario actual a la tarea y muestra un mensaje de éxito tras la creación
        """
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Tarea creada con éxito')
        return super().form_valid(form)

class ToggleCompleto(LoginRequiredMixin, View):
    """
    Vista para alternar el estado 'completo' de una tarea
    """
    def get(self, request, pk):
        tarea = get_object_or_404(Tarea, pk=pk, usuario=request.user)
        tarea.completo = not tarea.completo
        tarea.save()
        return redirect('lista_tareas')

class EditarTarea(LoginRequiredMixin, UpdateView):
    """
    Vista para editar una tarea existente del usuario autenticado
    """
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/editar.html'
    success_url = reverse_lazy('lista_tareas')

    def get_queryset(self):
        """
        Limita las tareas que se pueden editar al usuario actual
        """
        return Tarea.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Tarea actualizada con éxito')
        return super().form_valid(form)

class EliminarTarea(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una tarea del usuario autenticado
    """
    model = Tarea
    success_url = reverse_lazy('lista_tareas')

    def get_queryset(self):
        """
        Limita las tareas que se pueden eliminar al usuario actual
        """
        return Tarea.objects.filter(usuario=self.request.user)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class RegistroUsuario(View):
    """
    Vista para registrar un nuevo usuario
    """
    def get(self, request):
        form = RegistroUsuarioForm()
        return render(request, 'tareas/registro.html', {'form': form})

    def post(self, request):
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('lista_tareas')
        return render(request, 'tareas/registro.html', {'form': form})

class EliminarUsuario(LoginRequiredMixin, View):
    """
    Vista para que el usuario autenticado pueda eliminar su propia cuenta
    """
    def get(self, request):
        return render(request, 'tareas/eliminar_usuario.html')

    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        return redirect('login')