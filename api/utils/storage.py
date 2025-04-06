import os
import json
from typing import List, Dict
from api.utils.logger import logger

# --- Constants ---
DATA_DIR = "data"
DECISION_LOGS_FILE = os.path.join(DATA_DIR, "decision_logs.json")
os.makedirs(DATA_DIR, exist_ok=True)


def load_decision_logs() -> List[Dict]:
    """
    Load decision logs from file. Returns an empty list if file doesn't exist or is unreadable.
    """
    if not os.path.exists(DECISION_LOGS_FILE):
        logger.warning("Decision log file not found. Returning empty list.")
        return []

    try:
        with open(DECISION_LOGS_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse decision log file: {e}")
        return []
    except Exception as e:
        logger.exception(f"Unexpected error while loading decision logs: {e}")
        return []


def save_decision_logs(logs: List[Dict]) -> None:
    """
    Save decision logs to file in pretty-printed JSON format.
    """
    try:
        with open(DECISION_LOGS_FILE, "w") as f:
            json.dump(logs, f, indent=4)
        logger.info("Decision logs saved successfully.")
    except Exception as e:
        logger.exception(f"Failed to save decision logs: {e}")
