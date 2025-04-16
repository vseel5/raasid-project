from fastapi import APIRouter
from api.utils.storage import load_decision_logs, save_decision_logs
import random
from api.utils.logger import logger
import requests

# Initialize router
router = APIRouter()

# Function to log the decision
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

# Function to send data to a given endpoint
def send_post(endpoint: str, payload: dict, action_name: str):
    """
    Function to send a POST request to the given endpoint with the payload.
    Logs the result of the request.

    Args:
    - endpoint (str): The API endpoint to which the data will be sent.
    - payload (dict): The data to be sent in the POST request.
    - action_name (str): The action name for logging purposes.
    """
    try:
        # Sending the POST request to the specified endpoint
        response = requests.post(endpoint, json=payload)

        # Check if the request was successful
        response.raise_for_status()

        # Log the response data
        logger.info(f"{action_name} request to {endpoint} was successful. Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        # Log any errors that occur during the request
        logger.error(f"Error sending {action_name} request to {endpoint}: {e}")

# Decision-making endpoint
@router.post("/decision_making_ai")
async def decision_making(data: dict):
    """
    Handle decision-making logic (simulated handball detection logic).
    Logs the decision to S3 or local storage.
    """
    frame_number = data['frame']
    hand_position = data['hand_position']
    certainty_score = random.uniform(85, 100)  # Example score between 85 and 100
    var_review_status = certainty_score < 95  # Assume VAR review is triggered for low confidence

    # Call log_decision to save the decision
    log_decision(frame_number=frame_number, 
                 hand_position=hand_position, 
                 certainty_score=certainty_score, 
                 var_review_status=var_review_status)

    # Additional logic for sending decision or processing (optional)
    decision_result = {
        "frame": frame_number,
        "final_decision": "Handball Violation" if certainty_score > 90 else "No Handball",
        "certainty_score": certainty_score,
        "VAR_review": var_review_status
    }
    
    # Send the decision to the endpoint for processing or display
    send_post("/decision_making_ai", decision_result, "Final Decision")

    return decision_result
