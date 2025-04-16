from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger

# Function to log the decision
def log_decision(frame_number, hand_position, certainty_score, var_review_status):
    # Load existing logs (from S3 or local)
    logs = load_decision_logs()

    # Debugging log to show loaded logs
    logger.info(f"Loaded Logs: {logs}")

    # Create a new decision log entry
    decision = {
        "frame": frame_number,
        "hand_position": hand_position,
        "certainty_score": certainty_score,
        "VAR_review": var_review_status
    }

    # Append the new decision to the list of logs
    logs.append(decision)

    # Debugging log to show the new decision
    logger.info(f"New Decision: {decision}")

    # Save the updated logs to S3 or local storage
    save_decision_logs(logs)
    logger.info(f"Decision for frame {frame_number} logged successfully.")

# Test the logging function with some example data
log_decision(123, "unnatural", 90.0, True)
