"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db, User, Veterinario, Mascota, RecetaMedica
from api.routes import api
from api.admin import setup_admin
from api.commands import setup_commands
from datetime import datetime

# from models import Person

ENV = "development" if os.getenv("FLASK_DEBUG") == "1" else "production"
static_file_dir = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), '../public/')
app = Flask(__name__)
app.url_map.strict_slashes = False

# database condiguration
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db, compare_type=True)
db.init_app(app)

# add the admin
setup_admin(app)

# add the admin
setup_commands(app)

# Add all endpoints form the API with a "api" prefix
app.register_blueprint(api, url_prefix='/api')

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    if ENV == "development":
        return generate_sitemap(app)
    return send_from_directory(static_file_dir, 'index.html')

# any other endpoint will try to serve it like a static file
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = 'index.html'
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0  # avoid cache memory
    return response


#Obtener Usuario(Propietario)
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


#Obtener todas las recetas
@app.route('/recetas', methods=['GET'])
def get_recetas():
    fecha_inicio = request.args.get('fecha_inicio')  # Ejemplo: "2024-03-01"
    fecha_fin = request.args.get('fecha_fin')  # Ejemplo: "2024-03-09"

    query = RecetaMedica.query  # Consulta base

    # Filtrar si se pasan fechas en la consulta
    if fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            query = query.filter(RecetaMedica.fecha >= fecha_inicio)
        except ValueError:
            return jsonify({"error": "Formato de fecha incorrecto. Usa YYYY-MM-DD"}), 400

    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
            query = query.filter(RecetaMedica.fecha <= fecha_fin)
        except ValueError:
            return jsonify({"error": "Formato de fecha incorrecto. Usa YYYY-MM-DD"}), 400

    recetas = query.all()

    return jsonify([receta.serialize() for receta in recetas]), 200


#Crear una nueva receta
@app.route('/recetas', methods=['POST'])
def create_receta():
    data = request.get_json()
    
    if not data or not all(k in data for k in ["diagnostico", "tratamiento", "id_usuario", "id_veterinario", "id_mascota"]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    # Obtener la fecha del request, si no se envía, usar la fecha actual
    fecha = data.get('fecha')
    if fecha:
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')  # Convertir string a datetime
        except ValueError:
            return jsonify({"error": "Formato de fecha incorrecto. Usa YYYY-MM-DD HH:MM:SS"}), 400
    else:
        fecha = datetime.utcnow()  # Si no se envía fecha, usar la actual

    nueva_receta = RecetaMedica(
        fecha=fecha,
        diagnostico=data["diagnostico"],
        tratamiento=data["tratamiento"],
        id_usuario=data["id_usuario"],
        id_veterinario=data["id_veterinario"],
        id_mascota=data["id_mascota"]
    )
    
    db.session.add(nueva_receta)
    db.session.commit()
    
    return jsonify(nueva_receta.serialize()), 201


#Obtener todas las mascotas
@app.route('/mascotas', methods=['GET'])
def get_mascotas():
    mascotas = Mascota.query.all()
    return jsonify([mascota.serialize() for mascota in mascotas]), 200


#Crear una nueva mascota
@app.route('/mascotas', methods=['POST'])
def create_mascota():
    data = request.get_json()

    # Verifica si faltan datos obligatorios
    if not data or not all(k in data for k in ["nombre", "especie", "propietario_id"]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    # Verifica que el propietario exista
    propietario = User.query.get(data["propietario_id"])
    if not propietario:
        return jsonify({"error": "El propietario no existe"}), 404

    # Crear la mascota
    nueva_mascota = Mascota(
        nombre=data["nombre"],
        especie=data["especie"],
        raza=data.get("raza"),
        edad=data.get("edad"),
        peso=data.get("peso"),
        sexo=data.get("sexo"),
        propietario_id=data["propietario_id"]
    )

    db.session.add(nueva_mascota)
    db.session.commit()

    return jsonify(nueva_mascota.serialize()), 201


#Obtener Veterinario
@app.route('/veterinarios', methods=['GET'])
def get_veterinarios():
    veterinarios = Veterinario.query.all()
    return jsonify([veterinario.serialize() for veterinario in veterinarios]), 200


#Crear Veterinario
@app.route('/veterinarios', methods=['POST'])
def create_veterinario():
    data = request.get_json()

    # Validar que los datos requeridos están presentes
    if not data or not all(k in data for k in ["nombre", "email"]):
        return jsonify({"error": "Faltan datos obligatorios (nombre, email)"}), 400
    
    # Verificar si el email ya está registrado
    if Veterinario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "El email ya esta registrado"}), 400
    
    #Crear un nuevo veterinario
    nuevo_veterinario = Veterinario(
        nombre=data["nombre"],
        email=data["email"],
        telefono=data.get("telefono")
    )

    db.session.add(nuevo_veterinario)
    db.session.commit()

    return jsonify(nuevo_veterinario.serialize()), 201




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3001))
    app.run(host='0.0.0.0', port=PORT, debug=True)
