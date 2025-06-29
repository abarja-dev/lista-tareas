from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Tarea

class EliminarUsuarioTest(TestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.usuario = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')

    def test_eliminar_usuario(self):
        # Hacer GET para asegurarnos que la página carga
        response = self.client.get(reverse('eliminar_usuario'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '¿Estás seguro de que quieres eliminar tu cuenta?')

        # Hacer POST para eliminar usuario
        response = self.client.post(reverse('eliminar_usuario'))
        # Debería redirigir al login
        self.assertRedirects(response, reverse('login'))

        # Verificar que el usuario ya no existe
        self.assertFalse(User.objects.filter(username='testuser').exists())

class UsuarioTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registro_usuario(self):
        url = reverse('registro')
        data = {
            'username': 'nuevo_usuario',
            'password1': 'contrasenaSegura123',
            'password2': 'contrasenaSegura123',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_tareas'))
        self.assertTrue(User.objects.filter(username='nuevo_usuario').exists())

    def test_login_usuario(self):
        User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        self.assertTrue(login)

    def test_acceso_protegido_sin_login(self):
        url = reverse('lista_tareas')
        response = self.client.get(url)
        self.assertRedirects(response, f'{reverse("login")}?next={url}')

class TareaTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.tarea = Tarea.objects.create(
            usuario=self.usuario,
            titulo='Tarea ejemplo',
            descripcion='Descripción',
            completo=False,
        )

    def test_crear_tarea(self):
        url = reverse('crear_tarea')
        data = {
            'titulo': 'Nueva tarea',
            'descripcion': 'Descripción tarea',
            'completo': False,
            'fecha_limite': '2025-12-31',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_tareas'))
        self.assertTrue(Tarea.objects.filter(titulo='Nueva tarea').exists())

    def test_editar_tarea(self):
        url = reverse('editar_tarea', args=[self.tarea.pk])
        data = {
            'titulo': 'Tarea editada',
            'descripcion': 'Nueva descripción',
            'completo': True,
            'fecha_limite': '2025-12-31',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('lista_tareas'))
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.titulo, 'Tarea editada')
        self.assertTrue(self.tarea.completo)

    def test_eliminar_tarea(self):
        url = reverse('eliminar_tarea', args=[self.tarea.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('lista_tareas'))
        self.assertFalse(Tarea.objects.filter(pk=self.tarea.pk).exists())

    def test_eliminar_tarea_otro_usuario(self):
        otro_usuario = User.objects.create_user(username='otro', password='12345')
        tarea_otro = Tarea.objects.create(
            usuario=otro_usuario,
            titulo='Tarea de otro',
            descripcion='Desc',
            completo=False,
        )
        url = reverse('eliminar_tarea', args=[tarea_otro.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tarea.objects.filter(pk=tarea_otro.pk).exists())