import json
import requests
import logging

logging.basicConfig(level=logging.INFO)

# Simulated Event Context AI Output
event_context_result = {
    "frame": 2025,
    "handball_decision": "intentional",
    "certainty_score": 93.5,
    "rule_violation": True
}

# API Endpoint for Event Context
EVENT_CONTEXT_API_ENDPOINT = "http://127.0.0.1:8000/event_context_ai"

# Send Data to API
response = requests.post(EVENT_CONTEXT_API_ENDPOINT, json=event_context_result)

#Response from API
logging.info(f"Event Context AI Sent Data: {response.status_code}, {response.json()}")

