import os
import json

DECISION_LOGS_FILE = os.path.join("data", "decision_logs.json")
os.makedirs("data", exist_ok=True)

def load_decision_logs():
    if not os.path.exists(DECISION_LOGS_FILE):
        return []
    with open(DECISION_LOGS_FILE, "r") as f:
        try:
            data = f.read().strip()
            return json.loads(data) if data else []
        except json.JSONDecodeError:
            return []

def save_decision_logs(logs):
    with open(DECISION_LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=4)
