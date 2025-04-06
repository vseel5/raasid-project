import json
import logging
import requests
from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime
import os

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Constants: API Endpoints ---
REFEREE_SMARTWATCH_API = "http://127.0.0.1:8000/referee_smartwatch"
VAR_REPLAY_SYSTEM_API = "http://127.0.0.1:8000/var_replay"
TV_BROADCAST_API = "http://127.0.0.1:8000/tv_broadcast"
CLOUD_STORAGE_API = "http://127.0.0.1:8000/cloud_storage"
DECISION_FILE_PATH = "final_decision_output.json"
LOCAL_DECISION_LOG_DIR = "logs/decisions"

# --- Load Decision Data ---
def load_decision_data(path: str) -> List[Dict]:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("Decision file not found: %s", path)
    except json.JSONDecodeError:
        logging.error("Invalid JSON format in decision file: %s", path)
    return []

# --- Generic POST Sender ---
def send_post_request(endpoint: str, payload: Dict, label: str):
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        logging.info(f"{label} Success: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"{label} Failed: {e}")

# --- Specific Delivery Targets ---
def send_to_referee_smartwatch(decision: Dict):
    send_post_request(
        REFEREE_SMARTWATCH_API,
        {
            "frame": decision["frame"],
            "final_decision": decision["final_decision"],
            "certainty_score": decision["certainty_score"]
        },
        "Referee Smartwatch"
    )

def send_to_var_replay(decision: Dict):
    if decision.get("VAR_review_needed"):
        send_post_request(
            VAR_REPLAY_SYSTEM_API,
            {"frame": decision["frame"], "reason": "VAR Review Required"},
            "VAR Replay"
        )

def send_to_tv_broadcast(decision: Dict):
    send_post_request(
        TV_BROADCAST_API,
        {
            "frame": decision["frame"],
            "decision": decision["final_decision"],
            "certainty_score": decision["certainty_score"],
            "VAR_review": decision.get("VAR_review_needed", False)
        },
        "TV Broadcast"
    )

def store_in_cloud(decision: Dict):
    send_post_request(
        CLOUD_STORAGE_API,
        {"match_decision": decision},
        "Cloud Storage"
    )

# --- Save a Local Copy of Distributed Decision ---
def save_decision_to_local_log(decision: Dict, distribution_id: str) -> Optional[str]:
    os.makedirs(LOCAL_DECISION_LOG_DIR, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"decision_{distribution_id}_{timestamp}.json"
    file_path = os.path.join(LOCAL_DECISION_LOG_DIR, filename)

    try:
        with open(file_path, "w") as f:
            json.dump(decision, f, indent=2)
        logging.info(f"Decision saved locally: {file_path}")
        return file_path
    except Exception as e:
        logging.error(f"Failed to save decision locally: {e}")
        return None

# --- Public Function: Deliver to All Targets ---
def deliver_decision_to_all_endpoints(decision: Dict) -> Dict:
    distribution_id = str(uuid4())
    logging.info(f"Starting delivery | Distribution ID: {distribution_id}")

    send_to_referee_smartwatch(decision)
    send_to_var_replay(decision)
    send_to_tv_broadcast(decision)
    store_in_cloud(decision)

    report_path = save_decision_to_local_log(decision, distribution_id)

    logging.info(f"Distribution completed | ID: {distribution_id}")

    return {
        "distribution_id": distribution_id,
        "report_path": report_path,
        "timestamp": datetime.utcnow().isoformat(),
        "delivered_to": [
            "Referee Smartwatch",
            "VAR Replay" if decision.get("VAR_review_needed") else "VAR Skipped",
            "TV Broadcast",
            "Cloud Storage"
        ]
    }

# --- CLI Entry Point (Optional) ---
def main():
    decisions = load_decision_data(DECISION_FILE_PATH)
    if not decisions:
        logging.warning("No decisions to process.")
        return

    for decision in decisions:
        deliver_decision_to_all_endpoints(decision)

    logging.info("Output Delivery Completed")

if __name__ == "__main__":
    main()
