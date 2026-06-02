import csv
import os
import threading
from datetime import datetime, timezone

LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "app.log")
FIELDS = [
    "timestamp", "log_id", "level", "event", "module",
    "transaction_id", "session_id", "user_id", "client_ip",
    "payment_provider", "status", "error_code", "duration_ms", "message",
]

_lock = threading.Lock()


def _ensure_file():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)


def _next_id():
    if not os.path.exists(LOG_PATH):
        return 1
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    data_rows = [r for r in rows[1:] if r]
    if not data_rows:
        return 1
    try:
        return int(data_rows[-1][1]) + 1
    except (IndexError, ValueError):
        return len(data_rows) + 1


def log(level, event, module, status, message,
        client_ip="", payment_provider="visa",
        error_code="", duration_ms="",
        transaction_id="", session_id="", user_id=""):
    _ensure_file()
    with _lock:
        log_id = _next_id()
        row = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") +
                         f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z",
            "log_id": log_id,
            "level": level,
            "event": event,
            "module": module,
            "transaction_id": transaction_id,
            "session_id": session_id,
            "user_id": user_id,
            "client_ip": client_ip,
            "payment_provider": payment_provider,
            "status": status,
            "error_code": error_code,
            "duration_ms": duration_ms,
            "message": message,
        }
        with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writerow(row)
