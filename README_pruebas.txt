PASOS PARA EJECUTAR LA PRÁCTICA

1. Crear entorno e instalar dependencias:
   python -m venv venv
   venv\Scripts\activate
   pip install flask requests werkzeug

2. Ejecutar aplicación vulnerable:
   python app_vulnerable.py

3. En otra terminal, ejecutar pruebas de seguridad:
   python pruebas_seguridad.py

4. Pruebas manuales con curl:
   curl http://127.0.0.1:5000/saludo
   curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{\"usuario\":\"admin\",\"password\":\"mala\"}"
   curl "http://127.0.0.1:5000/datos?user=' OR '1'='1"
   curl -X POST http://127.0.0.1:5000/registro -H "Content-Type: application/json" -d "{}"

5. JMeter:
   - Crear Thread Group.
   - Number of Threads: 50.
   - Ramp-up Period: 10.
   - HTTP Request: GET /lento, servidor 127.0.0.1, puerto 5000.
   - Agregar Summary Report y View Results Tree.
   - Ejecutar y capturar tiempo promedio, porcentaje de error y throughput.
