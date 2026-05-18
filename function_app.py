import azure.functions as func
import psycopg2
import json
import logging
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="verificar-tarjeta", methods=["POST"])
def verificar_tarjeta(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Solicitud de verificacion de tarjeta Visa recibida.")

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"existe": False, "mensaje": "Body JSON invalido"}),
            mimetype="application/json",
            status_code=400
        )

    numero_tarjeta = data.get("numero_tarjeta")
    cvv = data.get("cvv")

    if not numero_tarjeta or not cvv:
        return func.HttpResponse(
            json.dumps({"existe": False, "mensaje": "Campos requeridos: numero_tarjeta, cvv"}),
            mimetype="application/json",
            status_code=400
        )

    conn = None
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM tarjetas_visa WHERE numero_tarjeta = %s AND cvv = %s",
            (numero_tarjeta, cvv)
        )
        existe = cur.fetchone() is not None
        cur.close()

        logging.info(f"Verificacion completada: existe={existe}")
        return func.HttpResponse(
            json.dumps({
                "existe": existe,
                "mensaje": "Tarjeta verificada correctamente" if existe else "Tarjeta no encontrada"
            }),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error al verificar tarjeta: {e}")
        return func.HttpResponse(
            json.dumps({"existe": False, "mensaje": "Error interno del servicio"}),
            mimetype="application/json",
            status_code=500
        )
    finally:
        if conn:
            conn.close()