import logging
import requests
import json

# --- Logging Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Simulated Ball Contact Detection Output ---
ball_contact_payload = {
    "frame": 2025,
    "ball_contact": True,
    "impact_force": 4.0,
    "contact_duration": 0.06,
    "sensor_source": "Smart Ball Sensor"
}

# --- API Endpoint ---
BALL_CONTACT_API_URL = "http://127.0.0.1:8000/ball_contact_ai"

# --- Send Request ---
try:
    logging.info("Sending ball contact data to API...")
    response = requests.post(BALL_CONTACT_API_URL, json=ball_contact_payload)
    response.raise_for_status()
    logging.info("API Response: %s", json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException as e:
    logging.error("Failed to communicate with Ball Contact API: %s", str(e))
