import json
import requests
import logging

logging.basicConfig(level=logging.INFO)

# Simulated Decision-Making AI Output
final_decision_result = {
    "frame": 4004,
    "final_decision": "No Handball",
    "certainty_score": 89.2,
    "VAR_review": True
}

# API Endpoint for Final Decision
DECISION_API_ENDPOINT = "http://127.0.0.1:8000/decision_making_ai"


# Send Data to API
response = requests.post(DECISION_API_ENDPOINT, json=final_decision_result)

# Response from API
logging.info(f"Decision-Making AI Sent Data: {response.status_code}, {response.json()}")

