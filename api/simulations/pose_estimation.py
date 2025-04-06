import requests
import logging
from typing import Dict, Any

# --- Configuration ---
POSE_API_ENDPOINT = "http://127.0.0.1:8000/pose_estimation"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pose_simulation")

# --- Sample Pose Estimation Payload ---
def get_simulated_pose_data() -> Dict[str, Any]:
    return {
        "frame": 123,
        "hand_position": "unnatural",
        "limb_angles": {
            "elbow": 110,
            "shoulder": 45
        },
        "certainty_score": 96.0
    }

# --- Send Request to API ---
def simulate_pose_estimation():
    data = get_simulated_pose_data()
    try:
        logger.info("Sending simulated pose data to API...")
        response = requests.post(POSE_API_ENDPOINT, json=data)
        response.raise_for_status()
        logger.info(f"Response: {response.status_code} | Data: {response.json()}")
    except requests.RequestException as e:
        logger.error(f"Pose Estimation API call failed: {e}")


if __name__ == "__main__":
    simulate_pose_estimation()
