from api.utils.logger import logger  

# Import the storage functions
from api.utils.storage import load_decision_logs, save_decision_logs

# Test loading decision logs
logs = load_decision_logs()
print("Loaded Logs:", logs)

# Test saving decision logs
new_logs = [{"frame": 123, "hand_position": "unnatural", "certainty_score": 98.0}]
save_decision_logs(new_logs)
print("Logs saved successfully.")


