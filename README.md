# Lista de Tareas

Aplicación web sencilla para gestionar tareas personales. Permite crear, editar, eliminar y marcar tareas como
completadas. Incluye registro, login y gestión básica de usuarios.

---

## Descripción

- Lista de tareas con filtro, búsqueda y ordenación.
- Gestión de usuarios con registro, login, logout y eliminación de cuenta.
- Interfaz limpia y funcional con estilos personalizados.
- Mensajes de confirmación para acciones importantes.

---

## Tecnologías y requisitos

- Python 3.8 o superior  
- Django 5.2.3

---

## Instalación y ejecución

1. Clona este repositorio y navega a la carpeta raíz del proyecto (donde está `manage.py`).
    **Importante:** Ejecuta el proyecto desde esta carpeta para que los imports funcionen correctamente.
2. (Opcional) Crea y activa un entorno virtual
3. Instala las dependencias:
   ```bash
    pip install -r requirements.txt
   ```
4. Ejecuta el servidor de desarrollo:
   ```bash
    python manage.py runserver
   ```
5. Abre el navegador e ingresa en la dirección que aparece en la consola (por defecto http://127.0.0.1:8000).

---

## Uso

- Regístrate o inicia sesión para acceder a tu lista de tareas.
- Crea nuevas tareas, edítalas, márcalas como completadas o elimínalas.
- Filtra las tareas por estado o busca por título.
- Elimina tu cuenta si lo deseas (acción irreversible).

---

## Autor

Alberto Barja Montes