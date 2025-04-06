import time
import random
import requests
import logging
from typing import Dict

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
NUM_FRAMES = 5
DELAY_BETWEEN_REQUESTS = 0.5  # seconds

# --- Logger Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Helper Functions ---
def send_post(endpoint: str, payload: Dict, label: str):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        response.raise_for_status()
        logging.info(f"{label} Sent (Frame {payload.get('frame')}): {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{label} Failed: {e}")

# --- Simulation Functions ---
def simulate_pose_estimation(frame: int):
    payload = {
        "frame": frame,
        "hand_position": random.choice(["natural", "unnatural"]),
        "limb_angles": {
            "elbow": random.randint(90, 140),
            "shoulder": random.randint(30, 60)
        },
        "certainty_score": round(random.uniform(85, 98), 2)
    }
    send_post("/pose_estimation", payload, "Pose Estimation")

def simulate_ball_contact(frame: int):
    payload = {
        "frame": frame,
        "ball_contact": random.choice([True, False]),
        "impact_force": round(random.uniform(1.5, 4.0), 2),
        "contact_duration": round(random.uniform(0.03, 0.09), 2),
        "sensor_source": "Smart Ball Sensor"
    }
    send_post("/ball_contact_ai", payload, "Ball Contact")

def simulate_event_context(frame: int):
    decision = random.choice(["intentional", "accidental"])
    payload = {
        "frame": frame,
        "handball_decision": decision,
        "certainty_score": round(random.uniform(85, 98), 2),
        "rule_violation": decision == "intentional"
    }
    send_post("/event_context_ai", payload, "Event Context")

def simulate_final_decision(frame: int):
    decision = random.choice(["Handball Violation", "No Handball"])
    certainty = round(random.uniform(89, 99), 2)
    payload = {
        "frame": frame,
        "final_decision": decision,
        "certainty_score": certainty,
        "VAR_review": certainty < 95
    }
    send_post("/decision_making_ai", payload, "Final Decision")

# --- Main Simulation Loop ---
def main():
    logging.info("Starting AI Simulation for Raasid System")
    for i in range(NUM_FRAMES):
        frame_id = 1000 + i
        simulate_pose_estimation(frame_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        simulate_ball_contact(frame_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        simulate_event_context(frame_id)
        time.sleep(DELAY_BETWEEN_REQUESTS)

        simulate_final_decision(frame_id)
        time.sleep(1)  # Slightly longer after full frame

    logging.info("Simulation complete.")

if __name__ == "__main__":
    main()
