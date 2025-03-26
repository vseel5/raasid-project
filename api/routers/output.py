from fastapi import APIRouter
import json, os, logging

router = APIRouter()

DECISION_LOGS_FILE = "data/decision_logs.json"

# Load the latest decision
def load_latest_decision():
    if os.path.exists(DECISION_LOGS_FILE):
        with open(DECISION_LOGS_FILE, "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, list) and data:
                    return data[-1]
            except json.JSONDecodeError:
                logging.warning("Failed to parse decision log file.")
    return None

@router.post("/output_distribution")
def distribute_decision():
    latest = load_latest_decision()
    if not latest:
        return {"status": "Error", "message": "No decisions available"}

    # Simulated distribution
    logging.info(f"📤 Referee Smartwatch: {latest}")
    logging.info(f"📺 TV Broadcast: {latest}")
    logging.info(f"💾 Cloud Storage: {latest}")

    return {"status": "Success", "message": "Decision distributed to all endpoints"}



