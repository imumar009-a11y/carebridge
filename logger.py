"""logger.py - Logging and automation for CareBridge."""
import os
import csv
import datetime
import requests

from config import WEBHOOK


def notify(payload: dict) -> None:
    """Save event to CSV log and optionally send to n8n webhook."""
    payload["time"] = datetime.datetime.now().isoformat(timespec="seconds")
    os.makedirs("logs", exist_ok=True)
    path = os.path.join("logs", payload["type"] + "_log.csv")
    is_new = not os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(payload.keys()))
        if is_new:
            writer.writeheader()
        writer.writerow(payload)

    if WEBHOOK:
        try:
            requests.post(WEBHOOK, json=payload, timeout=5)
        except Exception:
            pass


def book_appointment(name: str, phone: str, preferred_time: str) -> None:
    """Log an appointment request."""
    notify({
        "type": "appointment",
        "name": name,
        "phone": phone,
        "preferred_time": preferred_time,
    })


def log_triage(urgency: str, source: str, lang: str) -> None:
    """Log a triage event (only urgency, never patient words - privacy)."""
    notify({
        "type": "triage",
        "urgency": urgency,
        "source": source,
        "language": lang,
    })