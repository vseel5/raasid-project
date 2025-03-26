import json
import requests
import logging

logging.basicConfig(level=logging.INFO)


# Simulated Pose Estimation Output
pose_estimation_result = {
  "frame": 123,
  "hand_position": "unnatural",
  "limb_angles": {"elbow": 110, "shoulder": 45},
  "certainty_score": 96.0
}

# API Endpoint for Pose Estimation
POSE_API_ENDPOINT = "http://127.0.0.1:8000/pose_estimation"

# Send Data to API
response = requests.post(POSE_API_ENDPOINT, json=pose_estimation_result)

# Response from API
logging.info(f"Pose Estimation AI Sent Data: {response.status_code}, {response.json()}")


 