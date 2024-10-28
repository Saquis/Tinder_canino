#Tinder Canino
Tinder Canino es una aplicación web que conecta a dueños de mascotas para facilitar la amistad o reproducción de sus mascotas. Los usuarios pueden crear perfiles para sus mascotas, ver perfiles cercanos mediante geolocalización, hacer "swipe" para indicar interés, y chatear con otros dueños una vez que se produce una coincidencia (match).

#Tabla de Contenidos
Características
Tecnologías
Instalación
Configuración
Uso
API Endpoints
Contribuir
Licencia
Características
Registro de Usuarios: Los usuarios pueden registrarse utilizando correo electrónico y autenticación con Google.
Perfiles de Mascotas: Los usuarios pueden crear y editar perfiles de sus mascotas con información como nombre, edad, raza, y personalidad.
Geolocalización: Se muestran mascotas cercanas basándose en la ubicación del usuario.
Sistema de Coincidencias (Match): Los usuarios pueden hacer "me gusta" o "descartar" en los perfiles de otras mascotas. Si el interés es mutuo, se crea una coincidencia.
Mensajería en Tiempo Real: Los dueños pueden chatear una vez que se produce una coincidencia.
Notificaciones: Se envían notificaciones para nuevos mensajes y coincidencias.
Reputación: Sistema de valoraciones y comentarios después de cada cita.
Tecnologías
Frontend: HTML, CSS, JavaScript, Google OAuth para autenticación.
Backend: Flask (Python), Flask-JWT-Extended para autenticación, Flask-Mail para notificaciones por correo electrónico, geopy para cálculo de distancia.
Base de Datos: MongoDB.
APIs: Google Maps API para geolocalización, Cloudinary para almacenamiento de archivos multimedia.
Instalación
Clona el repositorio:

bash
Copiar código
git clone https://github.com/TuUsuario/TinderCanino.git
cd TinderCanino
Configura un entorno virtual (opcional pero recomendado):

bash
Copiar código
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
Instala las dependencias:

bash
Copiar código
pip install -r requirements.txt
Configuración
Configura las variables de entorno:

Crea un archivo .env en el directorio principal del proyecto con las siguientes variables:

env
Copiar código
JWT_SECRET_KEY=clave-secreta-muy-segura
CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tuemail@gmail.com
MAIL_PASSWORD=tucontraseña
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET
Configura MongoDB:

Asegúrate de tener un servidor de MongoDB en funcionamiento y que la función get_db() en el archivo db.py esté configurada para conectarse a la base de datos.

Obtén las credenciales de Google API:

Ve a Google Cloud Console y crea un proyecto. Habilita Google OAuth, configura el ID del cliente y el secreto, y añade el CLIENT_ID en index.html y en app.py.

Uso
Inicia la aplicación:

bash
Copiar código
python app.py
La aplicación estará disponible en http://127.0.0.1:5000.

Interfaz del usuario:

Login y Registro: Los usuarios pueden iniciar sesión o registrarse.
Registro de Mascotas: Los usuarios pueden añadir información de su mascota.
Explorar Mascotas Cercanas: Los usuarios pueden ver perfiles de otras mascotas y hacer "me gusta" o "descartar".
Chat: Si hay una coincidencia, se habilita la opción de chat.
API Endpoints
Usuarios

POST /api/usuarios: Registrar usuario
POST /api/login: Iniciar sesión
POST /api/auth/google: Iniciar sesión con Google
Mascotas

POST /api/mascotas: Registrar una mascota
PUT /api/mascotas/<mascota_id>: Actualizar perfil de una mascota
POST /api/mascotas/cercanas: Buscar mascotas cercanas
Match y Mensajería

POST /api/swipe: Hacer "me gusta" o "descartar" en otra mascota
POST /api/mensajes/enviar: Enviar un mensaje en un chat de match
PUT /api/mensajes/marcar_leido/<mensaje_id>: Marcar mensaje como leído
Contribuir
Fork este repositorio.
Clona tu fork y crea una nueva rama para tu característica.
Realiza tus cambios y haz commit.
Envía una pull request detallando las características o correcciones de errores.
Licencia
Este proyecto está bajo la licencia MIT. Para más información, consulta el archivo LICENSE.
