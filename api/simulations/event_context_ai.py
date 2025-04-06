import logging
import requests
import json

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Simulated Event Context Output ---
event_context_payload = {
    "frame": 2025,
    "handball_decision": "intentional",
    "certainty_score": 93.5,
    "rule_violation": True
}

# --- API Endpoint ---
EVENT_CONTEXT_API_URL = "http://127.0.0.1:8000/event_context_ai"

# --- Send Request ---
try:
    logging.info("Sending event context data to API...")
    response = requests.post(EVENT_CONTEXT_API_URL, json=event_context_payload)
    response.raise_for_status()
    logging.info("API Response: %s", json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException as e:
    logging.error("Failed to communicate with Event Context API: %s", str(e))
