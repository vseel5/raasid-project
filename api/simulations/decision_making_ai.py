import logging
import requests
import json

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Simulated Final AI Decision Payload ---
final_decision_payload = {
    "frame": 4004,
    "final_decision": "No Handball",
    "certainty_score": 89.2,
    "VAR_review": True
}

# --- API Endpoint ---
DECISION_API_URL = "http://127.0.0.1:8000/decision_making_ai"

# --- Send Request ---
try:
    logging.info("Sending final decision to AI Decision API...")
    response = requests.post(DECISION_API_URL, json=final_decision_payload)
    response.raise_for_status()
    logging.info("API Response: %s", json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException as e:
    logging.error("Error sending data to AI Decision API: %s", str(e))
