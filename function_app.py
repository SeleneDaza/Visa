import azure.functions as func
import psycopg2
import json
import logging
import os
import time

import logger as csv_logger

MODULE = "visa.verification"
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="verificar-tarjeta", methods=["POST"])
def verificar_tarjeta(req: func.HttpRequest) -> func.HttpResponse:
    client_ip = req.headers.get("X-Forwarded-For", req.headers.get("client-ip", ""))

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

    last4 = str(numero_tarjeta)[-4:]
    csv_logger.log(
        level="INFO", event="CARD_VERIFICATION_RECEIVED", module=MODULE,
        status="STARTED", client_ip=client_ip,
        message=f"Verification request received, last4={last4}",
    )

    conn = None
    start = time.monotonic()
    try:
        conn = psycopg2.connect(os.environ["DATABASE_URL"])
        cur = conn.cursor()
        cur.execute(
            "SELECT 1 FROM tarjetas_visa WHERE numero_tarjeta = %s AND cvv = %s",
            (numero_tarjeta, cvv)
        )
        existe = cur.fetchone() is not None
        cur.close()
        duration_ms = int((time.monotonic() - start) * 1000)

        if existe:
            csv_logger.log(
                level="SUCCESS", event="CARD_FOUND", module=MODULE,
                status="SUCCESS", client_ip=client_ip, duration_ms=duration_ms,
                message="Card verified",
            )
        else:
            csv_logger.log(
                level="ERROR", event="CARD_NOT_FOUND", module=MODULE,
                status="FAILED", client_ip=client_ip, duration_ms=duration_ms,
                error_code="CARD_NOT_FOUND", message="Card not found",
            )

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
        duration_ms = int((time.monotonic() - start) * 1000)
        csv_logger.log(
            level="ERROR", event="CARD_VERIFICATION_ERROR", module=MODULE,
            status="FAILED", client_ip=client_ip, duration_ms=duration_ms,
            error_code="INTERNAL_ERROR", message=f"Internal error: {e}",
        )
        logging.error(f"Error al verificar tarjeta: {e}")
        return func.HttpResponse(
            json.dumps({"existe": False, "mensaje": "Error interno del servicio"}),
            mimetype="application/json",
            status_code=500
        )
    finally:
        if conn:
            conn.close()