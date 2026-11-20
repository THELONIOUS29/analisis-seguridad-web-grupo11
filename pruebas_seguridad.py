"""Pruebas prácticas básicas para la app vulnerable.
Ejecutar primero: python app_vulnerable.py
Luego: python pruebas_seguridad.py
"""
import requests

BASE = "http://127.0.0.1:5000"

casos = [
    ("Login usuario incorrecto", "POST", "/login", {"usuario": "hacker", "password": "CONFIGURAR_LOCALMENTE"}, None),
    ("Login contraseña incorrecta", "POST", "/login", {"usuario": "admin", "password": "CONFIGURAR_LOCALMENTE"}, None),
    ("Login correcto", "POST", "/login", {"usuario": "admin", "password": "CONFIGURAR_LOCALMENTE"}, None),
    ("Registro vacío", "POST", "/registro", {}, None),
    ("Inyección simple", "GET", "/datos", None, {"user": "' OR '1'='1"}),
    ("Endpoint lento", "GET", "/lento", None, None),
]

for nombre, metodo, ruta, json_body, params in casos:
    print(f"\n=== {nombre} ===")
    try:
        if metodo == "POST":
            r = requests.post(BASE + ruta, json=json_body, timeout=10)
        else:
            r = requests.get(BASE + ruta, params=params, timeout=10)
        print("Código:", r.status_code)
        print("Respuesta:", r.text)
        print("Tiempo:", round(r.elapsed.total_seconds(), 3), "s")
    except Exception as e:
        print("Error durante la prueba:", e)
