from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger

# You can either define log_decision() here or import it if it's already defined in another file
def log_decision(frame_number, hand_position, certainty_score, var_review_status):
    # Load existing logs (from S3 or local)
    logs = load_decision_logs()

    # Create a new decision log entry
    decision = {
        "frame": frame_number,
        "hand_position": hand_position,
        "certainty_score": certainty_score,
        "VAR_review": var_review_status
    }

    # Append the new decision to the list of logs
    logs.append(decision)

    # Save the updated logs to S3 or local storage
    save_decision_logs(logs)
    logger.info(f"Decision for frame {frame_number} logged successfully.")

# Simulate decision-making (use any logic for decision here)
def decision_making(data):
    frame_number = data['frame']
    hand_position = data['hand_position']
    certainty_score = data['certainty_score']
    var_review_status = data['VAR_review']

    # Call log_decision to log the decision
    log_decision(frame_number, hand_position, certainty_score, var_review_status)

    # Simulate decision result (logging the decision result)
    decision_result = {
        "frame": frame_number,
        "final_decision": "Handball Violation" if certainty_score > 90 else "No Handball",
        "certainty_score": certainty_score,
        "VAR_review": var_review_status
    }

    print(f"Decision for frame {frame_number}: {decision_result}")

# Test data
test_data = {
    "frame": 101,
    "hand_position": "unnatural",
    "certainty_score": 95.0,
    "VAR_review": False
}

# Simulate decision-making
decision_making(test_data)

