from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from bson import ObjectId
from geopy.distance import geodesic
from google.oauth2 import id_token
from google.auth.transport import requests
from flask_mail import Mail, Message
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# Crear la instancia de la aplicación Flask
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'clave-secreta-muy-segura'  # Cambia esto a una clave secreta real y segura
# Configuración de Cloudinary
app.config['CLOUDINARY_URL'] = 'cloudinary://479949662832966:Y34rD0UC9rweboEnpeZwESkb1Xg@do83aatob'
CORS(app)
jwt = JWTManager(app)
db = get_db()

# Configuración de correo electrónico
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='tuemail@gmail.com',
    MAIL_PASSWORD='tucontraseña'
)
mail = Mail(app)

# Función auxiliar para convertir ObjectId a cadena
def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: str(value) if isinstance(value, ObjectId) else value for key, value in data.items()}
    else:
        return data

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint para registro de usuarios
@app.route("/api/usuarios", methods=["POST"])
def register_user():
    nombre = request.json.get("nombre")
    email = request.json.get("email")
    password = request.json.get("password")
    fecha_registro = request.json.get("fecha_registro")

    if db.usuarios.find_one({"email": email}):
        return jsonify({"mensaje": "El usuario ya existe"}), 400

    password_hash = generate_password_hash(password)
    nuevo_usuario = {
        "nombre": nombre,
        "email": email,
        "password_hash": password_hash,
        "fecha_registro": fecha_registro,
        "perfiles_mascotas": []
    }

    db.usuarios.insert_one(nuevo_usuario)
    return jsonify({"mensaje": "Usuario creado con éxito"}), 201

# Endpoint para confirmar correo electrónico
@app.route("/api/confirmar", methods=["POST"])
def confirmar():
    email = request.json.get("email")
    usuario = db.usuarios.find_one({"email": email})
    if usuario:
        token = create_access_token(identity=str(usuario["_id"]))
        msg = Message("Confirma tu cuenta",
                      sender="tuemail@gmail.com",
                      recipients=[email])
        msg.body = f"Confirma tu cuenta haciendo clic en este enlace: http://127.0.0.1:5000/api/confirmar/{token}"
        mail.send(msg)
        return jsonify({"mensaje": "Correo de confirmación enviado"}), 200
    return jsonify({"mensaje": "Usuario no encontrado"}), 404

# Endpoint para autenticación (login)
@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    usuario = db.usuarios.find_one({"email": email})
    if not usuario or not check_password_hash(usuario["password_hash"], password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    
    access_token = create_access_token(identity=str(usuario["_id"]))
    return jsonify(access_token=access_token), 200

# Endpoint para autenticación con Google
@app.route("/api/auth/google", methods=["POST"])
def google_auth():
    token = request.json.get("token")
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), "CLIENT_ID_AQUI260965527958-5sbmt8ivlo10uri0flg9421uo6rbm0fi.apps.googleusercontent.com")
        email = idinfo["email"]
        nombre = idinfo["name"]

        usuario = db.usuarios.find_one({"email": email})
        if not usuario:
            usuario = {
                "nombre": nombre,
                "email": email,
                "auth_type": "google",
                "fecha_registro": datetime.utcnow()
            }
            db.usuarios.insert_one(usuario)

        access_token = create_access_token(identity=str(usuario["_id"]))
        return jsonify(access_token=access_token), 200
    except ValueError:
        return jsonify({"mensaje": "Token inválido"}), 401
        # Endpoint para registrar una nueva mascota
@app.route("/api/mascotas", methods=["POST"])
@jwt_required()
def registrar_mascota():
    try:
        propietario_id = get_jwt_identity()  # Identificar al usuario que registra la mascota
        nombre = request.json.get("nombre")
        edad = request.json.get("edad")
        raza = request.json.get("raza")
        descripcion = request.json.get("descripcion")
        genero = request.json.get("género")
        ubicacion = request.json.get("ubicacion")
        
        # Verificar si todos los campos necesarios están presentes
        if not (nombre and edad and raza and genero and ubicacion):
            return jsonify({"mensaje": "Todos los campos son requeridos"}), 400

        nueva_mascota = {
            "propietario_id": propietario_id,
            "nombre": nombre,
            "edad": edad,
            "raza": raza,
            "descripcion": descripcion,
            "género": genero,
            "ubicacion": ubicacion
        }

        db.mascotas.insert_one(nueva_mascota)
        return jsonify({"mensaje": "Mascota registrada con éxito"}), 201
    except Exception as e:
        print(f"Error al registrar mascota: {e}")
        return jsonify({"mensaje": "Error al registrar la mascota"}), 500



# Endpoint para actualizar el perfil de una mascota
@app.route("/api/mascotas/<mascota_id>", methods=["PUT"])
@jwt_required()
def update_mascota(mascota_id):
    propietario_id = get_jwt_identity()
    data = request.form

    # Extraer campos del formulario
    nombre = data.get("nombre")
    edad = data.get("edad")
    raza = data.get("raza")
    descripcion = data.get("descripcion")
    especie = data.get("especie")
    personalidad = data.get("personalidad")
    intereses = data.get("intereses")
    estado_salud = data.get("estado_salud")

    # Archivos de imagen y video
    imagen = request.files.get("imagen")
    video = request.files.get("video")

    # Construir actualización
    update_data = {
        "nombre": nombre,
        "edad": edad,
        "raza": raza,
        "descripcion": descripcion,
        "especie": especie,
        "personalidad": personalidad,
        "intereses": intereses,
        "estado_salud": estado_salud,
    }

    if imagen:
        resultado_imagen = upload(imagen)
        update_data["imagen"] = resultado_imagen.get("url")
    if video:
        resultado_video = upload(video, resource_type="video")
        update_data["video"] = resultado_video.get("url")

    # Actualizar solo si la mascota pertenece al propietario autenticado
    mascota = db.mascotas.find_one({"_id": ObjectId(mascota_id), "propietario_id": propietario_id})
    if not mascota:
        return jsonify({"mensaje": "Mascota no encontrada o no tiene permiso para editarla"}), 404

    db.mascotas.update_one({"_id": ObjectId(mascota_id)}, {"$set": update_data})
    return jsonify({"mensaje": "Perfil de mascota actualizado exitosamente"}), 200

# Endpoint para buscar mascotas cercanas
@app.route("/api/mascotas/cercanas", methods=["POST"])
@jwt_required()
def mascotas_cercanas():
    user_location = request.json.get("ubicacion")
    max_distancia = request.json.get("distancia", 10)

    mascotas = list(db.mascotas.find())
    cercanas = []

    for mascota in mascotas:
        if "ubicacion" in mascota:
            mascota_ubicacion = (mascota["ubicacion"]["latitud"], mascota["ubicacion"]["longitud"])
            distancia = geodesic((user_location["latitud"], user_location["longitud"]), mascota_ubicacion).km
            if distancia <= max_distancia:
                mascota["_id"] = str(mascota["_id"])
                cercanas.append(mascota)

    return jsonify(cercanas), 200

# Endpoint para manejar swipes y matches
@app.route("/api/swipe", methods=["POST"])
@jwt_required()
def handle_swipes():
    data = request.json
    mascota_id = data.get("mascota_id")
    swipe_mascota_id = data.get("swipe_mascota_id")
    tipo_swipe = data.get("tipo_swipe")

    # Verificar si ya existe un swipe duplicado
    existing_swipe = db.swipes.find_one({
        "mascota_id": mascota_id,
        "swipe_mascota_id": swipe_mascota_id
    })
    if existing_swipe:
        return jsonify({"mensaje": "Ya has hecho swipe a esta mascota."}), 400

    # Registrar el swipe en la base de datos
    db.swipes.insert_one({
        "mascota_id": mascota_id,
        "swipe_mascota_id": swipe_mascota_id,
        "tipo_swipe": tipo_swipe,
        "fecha_swipe": data.get("fecha_swipe")
    })

    # Verificar si es un swipe positivo y si existe un swipe mutuo positivo
    if tipo_swipe == "positivo":
        match = db.swipes.find_one({
            "mascota_id": swipe_mascota_id,
            "swipe_mascota_id": mascota_id,
            "tipo_swipe": "positivo"
        })
        if match:
            # Verificar si ya existe el match para evitar duplicados
            existing_match = db.match.find_one({
                "mascota_id_1": {"$in": [mascota_id, swipe_mascota_id]},
                "mascota_id_2": {"$in": [mascota_id, swipe_mascota_id]}
            })
            if not existing_match:
                db.match.insert_one({
                    "mascota_id_1": mascota_id,
                    "mascota_id_2": swipe_mascota_id,
                    "estado": "aceptado",
                    "fecha_match": data.get("fecha_swipe")
                })
                return jsonify({"mensaje": "¡Match encontrado!"}), 200

    return jsonify({"mensaje": "Swipe registrado"}), 200

# Endpoint para enviar mensajes entre mascotas que han hecho match
@app.route("/api/mensajes/enviar", methods=["POST"])
@jwt_required()
def enviar_mensaje_nuevo():
    nuevo_mensaje = {
        "match_id": request.json.get("match_id"),
        "emisor_mascota_id": request.json.get("emisor_mascota_id"),
        "receptor_mascota_id": request.json.get("receptor_mascota_id"),
        "contenido": request.json.get("contenido"),
        "fecha_envio": request.json.get("fecha_envio"),
        "leido": False  # El mensaje se envía como no leído
    }
    db.mensajes.insert_one(nuevo_mensaje)
    return jsonify({"mensaje": "Mensaje enviado"}), 201

# Endpoint para marcar mensajes como leídos
@app.route("/api/mensajes/marcar_leido/<mensaje_id>", methods=["PUT"])
@jwt_required()
def marcar_mensaje_leido(mensaje_id):
    db.mensajes.update_one({"_id": ObjectId(mensaje_id)}, {"$set": {"leido": True}})
    return jsonify({"mensaje": "Mensaje marcado como leído"}), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    print("Iniciando la aplicación Flask en http://127.0.0.1:5000")
    app.run(debug=True)
