from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["tinder_canino"]

# Crear las colecciones
usuarios = db["usuarios"]
mascotas = db["mascotas"]
match = db["match"]
swipes = db["swipes"]
mensajes = db["mensajes"]
media = db["media"]

# Ejemplo de inserción en cada colección:

# 1. Insertar un Usuario
usuarios.insert_one({
    "nombre": "Juan Pérez",
    "email": "juan.perez@example.com",
    "password_hash": "hashed_password_example",
    "fecha_registro": "2024-10-25T12:00:00",
    "perfiles_mascotas": [],
    "preferencias": {
        "raza_preferida": "Labrador",
        "edad_minima": 1,
        "edad_maxima": 5
    }
})

# 2. Insertar una Mascota
mascotas.insert_one({
    "nombre": "Firulais",
    "edad": 3,
    "raza": "Labrador",
    "descripcion": "Le encanta jugar con pelotas.",
    "propietario_id": usuarios.find_one({"email": "juan.perez@example.com"})["_id"],
    "género": "Macho",
    "imagenes": ["https://ejemplo.com/foto1.jpg", "https://ejemplo.com/foto2.jpg"]
})

# 3. Insertar un Match
match.insert_one({
    "mascota_id_1": mascotas.find_one({"nombre": "Firulais"})["_id"],
    "mascota_id_2": "Otro ID de Mascota",
    "estado": "aceptado",
    "fecha_match": "2024-10-25T14:30:00"
})

# 4. Insertar un Swipe
swipes.insert_one({
    "mascota_id": mascotas.find_one({"nombre": "Firulais"})["_id"],
    "swipe_mascota_id": "Otro ID de Mascota",
    "tipo_swipe": "positivo",
    "fecha_swipe": "2024-10-25T15:00:00"
})

# 5. Insertar un Mensaje
mensajes.insert_one({
    "match_id": match.find_one({"estado": "aceptado"})["_id"],
    "emisor_mascota_id": mascotas.find_one({"nombre": "Firulais"})["_id"],
    "receptor_mascota_id": "Otro ID de Mascota",
    "contenido": "Hola, ¿quieres jugar?",
    "fecha_envio": "2024-10-25T16:00:00"
})

# 6. Insertar un Media (Foto/Video)
media.insert_one({
    "mascota_id": mascotas.find_one({"nombre": "Firulais"})["_id"],
    "url": "https://ejemplo.com/foto1.jpg",
    "tipo": "imagen",
    "fecha_subida": "2024-10-25T12:30:00"
})
mensajes.insert_one({
    "match_id": "match_id_aqui",
    "emisor_mascota_id": "emisor_id",
    "receptor_mascota_id": "receptor_id",
    "contenido": "Hola, ¿quieres jugar?",
    "fecha_envio": "2024-10-25T16:00:00",
    "leido": False  # Nuevo campo para indicar si el mensaje ha sido leído
})

print("Base de datos y colecciones creadas con éxito.")


