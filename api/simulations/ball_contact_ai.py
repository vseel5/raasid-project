import json
import requests
import logging

logging.basicConfig(level=logging.INFO)




# Simulated Ball Contact Detection Output
ball_contact_result = {
    "frame": 2025,
    "ball_contact": True,
    "impact_force": 4.0,
    "contact_duration": 0.06,
    "sensor_source": "Smart Ball Sensor"
}

# API Endpoint for Ball Contact
BALL_CONTACT_API_ENDPOINT = "http://127.0.0.1:8000/ball_contact_ai"

# Send Data to API
response = requests.post(BALL_CONTACT_API_ENDPOINT, json=ball_contact_result)

# Response from API
logging.info(f"Ball Contact AI Sent Data: {response.status_code}, {response.json()}")
