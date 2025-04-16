from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger
import random

# Define the log_decision function
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
def simulate_final_decision(frame):
    decision = random.choice(["Handball Violation", "No Handball"])
    certainty = round(random.uniform(89, 99), 2)
    payload = {
        "frame": frame,
        "final_decision": decision,
        "certainty_score": certainty,
        "VAR_review": certainty < 95
    }
    
    # Log the decision after simulation
    log_decision(frame_number=frame, 
                 hand_position="unnatural",  # Example value, replace with actual logic
                 certainty_score=certainty, 
                 var_review_status=(certainty < 95))
    
    print(f"Simulated decision for frame {frame}: {payload}")

# Simulate the decision pipeline (you can add more simulations for other aspects)
def run_simulation():
    frames = [101, 123, 150, 200]  # Example frame numbers
    for frame in frames:
        simulate_final_decision(frame)

# Run the simulation
run_simulation()
