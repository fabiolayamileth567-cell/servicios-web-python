from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import requests

app = Flask(__name__)

TOPICS = {
    "concepto": {
        "title": "¿Qué son los servicios web?",
        "subtitle": "Conectar aplicaciones para intercambiar información",
        "description": "Un servicio web permite que dos aplicaciones se comuniquen por una red. En este ejemplo, el navegador solicita información a una ruta de Flask y Python devuelve una respuesta JSON.",
        "code": """@app.get("/api/saludo")
def saludo():
    return jsonify({
        "mensaje": "Hola desde Python",
        "servicio": "Servicio web de ejemplo"
    })""",
        "explanation": [
            "La ruta /api/saludo queda disponible para recibir solicitudes HTTP.",
            "Cuando alguien la visita, se ejecuta la función saludo().",
            "jsonify convierte el diccionario de Python en una respuesta JSON.",
            "El navegador puede leer esa respuesta y mostrarla."
        ],
        "demo": "saludo"
    },
    "conexion": {
        "title": "¿Cómo funcionan y se conectan?",
        "subtitle": "Cliente → solicitud HTTP → servidor → respuesta",
        "description": "El cliente (por ejemplo, el navegador) envía una solicitud. El servidor Python la procesa y devuelve una respuesta. GET consulta datos y POST envía datos.",
        "code": """@app.get("/api/hora")
def hora():
    return jsonify({
        "hora_utc": datetime.now(timezone.utc).isoformat(),
        "metodo": request.method
    })""",
        "explanation": [
            "El navegador actúa como cliente y solicita /api/hora.",
            "Flask recibe la solicitud GET y ejecuta la función hora().",
            "Python obtiene la fecha y hora actual en UTC.",
            "El servidor responde con datos JSON."
        ],
        "demo": "hora"
    },
    "herramientas": {
        "title": "¿Cómo se aprovechan en Python?",
        "subtitle": "Requests consume APIs; Flask crea servicios web",
        "description": "Python puede consumir servicios de otros sistemas con requests y crear sus propias API con Flask. Este ejemplo consulta una API pública de GitHub desde el servidor.",
        "code": """import requests

respuesta = requests.get(
    "https://api.github.com",
    timeout=10
)
respuesta.raise_for_status()
datos = respuesta.json()

print(datos.get("current_user_url"))""",
        "explanation": [
            "requests.get() envía una solicitud HTTP GET a GitHub.",
            "timeout=10 evita esperar indefinidamente.",
            "raise_for_status() detecta errores HTTP.",
            "json() convierte la respuesta en datos utilizables por Python."
        ],
        "demo": "github"
    },
    "ejemplos": {
        "title": "Ejemplos en la vida diaria",
        "subtitle": "Clima, mapas, monedas, compras y redes sociales",
        "description": "Una app del clima consulta datos meteorológicos; una tienda conecta su catálogo con pagos; y un mapa solicita rutas. Este ejemplo simula una consulta de clima.",
        "code": """@app.get("/api/clima/<ciudad>")
def clima(ciudad):
    # Datos simulados para la demostración
    return jsonify({
        "ciudad": ciudad.title(),
        "temperatura": 28,
        "unidad": "°C",
        "condicion": "Soleado"
    })""",
        "explanation": [
            "La ciudad se recibe como parte de la dirección web.",
            "Python prepara una respuesta con temperatura y condición.",
            "La respuesta se envía en JSON para que otra app la utilice.",
            "En un proyecto real, los datos vendrían de una API meteorológica."
        ],
        "demo": "clima"
    },
    "ventajas": {
        "title": "Ventajas, seguridad y conclusión",
        "subtitle": "Reutilización, ahorro de tiempo y sistemas conectados",
        "description": "Los servicios web permiten reutilizar funciones, automatizar tareas e integrar sistemas. En proyectos reales se deben proteger las rutas, validar datos y utilizar HTTPS.",
        "code": """@app.post("/api/eco")
def eco():
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()

    if not nombre:
        return jsonify({"error": "Falta el nombre"}), 400

    return jsonify({"mensaje": f"Hola, {nombre}"}), 200""",
        "explanation": [
            "POST permite que el cliente envíe datos al servidor.",
            "request.get_json() lee el contenido JSON enviado.",
            "Python valida que el campo nombre no esté vacío.",
            "Si falta, responde 400; si está correcto, responde 200."
        ],
        "demo": "eco"
    }
}

@app.get("/")
def inicio():
    return render_template("index.html", topics=TOPICS)

@app.get("/api/demo/<demo>")
def demo(demo):
    if demo == "saludo":
        return jsonify({"mensaje": "Hola desde Python", "servicio": "Servicio web de ejemplo"})
    if demo == "hora":
        return jsonify({"hora_utc": datetime.now(timezone.utc).isoformat(), "metodo": request.method})
    if demo == "github":
        try:
            response = requests.get("https://api.github.com", timeout=8)
            response.raise_for_status()
            data = response.json()
            return jsonify({"estado": "Conexión exitosa", "api_github": data.get("current_user_url", "Dato no disponible")})
        except requests.RequestException as error:
            return jsonify({"estado": "No se pudo conectar", "detalle": str(error), "nota": "Revisa tu conexión a Internet."}), 502
    if demo == "clima":
        ciudad = request.args.get("ciudad", "San Salvador").strip() or "San Salvador"
        return jsonify({"ciudad": ciudad.title(), "temperatura": 28, "unidad": "°C", "condicion": "Soleado", "Datos":" simulados."})
    if demo == "eco":
        return jsonify({"instruccion": "Escribe tu nombre y envíalo mediante POST."})
    return jsonify({"error": "Demostración no encontrada"}), 404

@app.post("/api/demo/eco")
def demo_eco():
    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()
    if not nombre:
        return jsonify({"error": "Escribe un nombre para probar el servicio."}), 400
    return jsonify({"mensaje": f"¡Hola, {nombre}! Python recibió tu información mediante POST."})

if __name__ == "__main__":
    app.run(debug=True)
