from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint básico
@app.route('/saludo', methods=['GET'])
def saludo():
    return "Hola usuario"


# LOGIN CON MÚLTIPLES FALLAS
@app.route('/login', methods=['POST'])
def login():
    # 1. NO valida si el JSON existe
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    # 2. Mensaje inseguro (da pistas al atacante)
    if usuario != "admin":
        return jsonify({"mensaje": "Usuario no existe"}), 401
    if password != "1234":
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    # 3. Autenticación débil (hardcodeada)
    return jsonify({"mensaje": "Login exitoso"}), 200


# ENDPOINT INSEGURO (simula vulnerabilidad)
@app.route('/datos', methods=['GET'])
def datos():
    user = request.args.get('user')

    # 4. Simulación de mala práctica tipo inyección
    if user == "' OR '1'='1":
        return jsonify({"datos": "ACCESO TOTAL"}), 200

    return jsonify({"datos": f"Datos de {user}"}), 200


# ENDPOINT LENTO (problema de rendimiento)
@app.route('/lento', methods=['GET'])
def lento():
    import time

    # 5. Retraso artificial
    time.sleep(3)
    return jsonify({"mensaje": "Respuesta tardía"}), 200


# ENDPOINT SIN VALIDACIONES
@app.route('/registro', methods=['POST'])
def registro():
    data = request.json

    # 6. NO valida campos
    usuario = data.get("usuario")
    return jsonify({"mensaje": f"Usuario {usuario} registrado"}), 200


# 7. Configuración insegura
if __name__ == '__main__':
    app.run(debug=True)  # debug activado (mala práctica)
