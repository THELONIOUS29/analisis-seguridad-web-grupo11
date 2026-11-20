import os
import re
import time
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Usuario de ejemplo para práctica local. En producción debe estar en una base de datos.
USUARIOS = {
    "admin": generate_password_hash(os.getenv("ADMIN_PASSWORD", "AdminSeguro2026!"))
}

PATRON_USUARIO = re.compile(r"^[a-zA-Z0-9_]{3,20}$")


def json_obligatorio():
    if not request.is_json:
        return None, (jsonify({"mensaje": "Solicitud inválida. Envíe JSON."}), 400)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, (jsonify({"mensaje": "JSON inválido."}), 400)
    return data, None


def validar_usuario(valor):
    return isinstance(valor, str) and bool(PATRON_USUARIO.fullmatch(valor))


@app.route('/saludo', methods=['GET'])
def saludo():
    return "Hola usuario"


@app.route('/login', methods=['POST'])
def login():
    data, error = json_obligatorio()
    if error:
        return error

    usuario = data.get("usuario", "")
    password = data.get("password", "")

    if not validar_usuario(usuario) or not isinstance(password, str) or len(password) < 8:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    hash_guardado = USUARIOS.get(usuario)
    if not hash_guardado or not check_password_hash(hash_guardado, password):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    return jsonify({"mensaje": "Login exitoso"}), 200


@app.route('/datos', methods=['GET'])
def datos():
    user = request.args.get('user', '')

    if not validar_usuario(user):
        return jsonify({"mensaje": "Parámetro user inválido"}), 400

    # En una app real se usarían consultas parametrizadas/ORM, nunca concatenación SQL.
    return jsonify({"datos": f"Datos permitidos de {user}"}), 200


@app.route('/lento', methods=['GET'])
def lento():
    # Se elimina el retraso artificial. Se mide tiempo para auditoría básica.
    inicio = time.perf_counter()
    respuesta = jsonify({
        "mensaje": "Respuesta optimizada",
        "tiempo_estimado_ms": round((time.perf_counter() - inicio) * 1000, 2)
    })
    return respuesta, 200


@app.route('/registro', methods=['POST'])
def registro():
    data, error = json_obligatorio()
    if error:
        return error

    usuario = data.get("usuario", "")
    if not validar_usuario(usuario):
        return jsonify({"mensaje": "Usuario inválido. Use 3 a 20 caracteres alfanuméricos o guion bajo."}), 400

    return jsonify({"mensaje": f"Usuario {usuario} registrado correctamente"}), 201


if __name__ == '__main__':
    # En producción usar: gunicorn app_corregida:app
    app.run(debug=False)
