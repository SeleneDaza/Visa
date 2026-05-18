import json
import logging
import os
import psycopg2
from flask import Flask, request, jsonify

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
log = logging.getLogger(__name__)

app = Flask(__name__)

def verificar_tarjeta_visa(numero_tarjeta: str, cvv: str) -> dict:
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM tarjetas_visa WHERE numero_tarjeta = %s AND cvv = %s",
            (numero_tarjeta, cvv)
        )
        existe = cur.fetchone() is not None
        cur.close()

        log.info(f"Verificacion tarjeta Visa: existe={existe}")
        return {
            "existe": existe,
            "mensaje": "Tarjeta verificada correctamente" if existe else "Tarjeta no encontrada"
        }
    except Exception as e:
        log.error(f"Error al verificar tarjeta Visa: {e}")
        return {"existe": False, "mensaje": "Error interno del servicio"}
    finally:
        if conn:
            conn.close()

@app.route("/visa/verificar-tarjeta", methods=["POST"])
def handle():
    data = request.get_json()
    numero_tarjeta = data.get("numero_tarjeta")
    cvv = data.get("cvv")

    if not numero_tarjeta or not cvv:
        log.warning("Peticion invalida: faltan campos")
        return jsonify({"existe": False, "mensaje": "Campos requeridos: numero_tarjeta, cvv"}), 400

    resultado = verificar_tarjeta_visa(numero_tarjeta, cvv)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)