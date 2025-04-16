import logging
import httpx
import json
import asyncio
from api.utils.storage import load_decision_logs, save_decision_logs  # Import logging functions
from api.utils.logger import logger  # Ensure logger is available

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- API Endpoint ---
EVENT_CONTEXT_API_URL = "http://127.0.0.1:8000/event_context_ai"

# --- Simulated Event Context Detection Output ---
event_context_payload = {
    "frame": 2025,
    "handball_decision": "intentional",  # Placeholder value
    "certainty_score": 88.0,
    "rule_violation": True
}

# --- Function to Log the Decision ---
def log_decision(frame_number, hand_position, certainty_score, var_review_status):
    # Load existing logs (from S3 or local)
    logs = load_decision_logs()

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

    logger.info(f"New Decision: {decision}")

    # Save the updated logs to S3 or local storage
    save_decision_logs(logs)
    logger.info(f"Decision for frame {frame_number} logged successfully.")

# --- Asynchronous Function to Send Data ---
async def send_event_context_data():
    async with httpx.AsyncClient() as client:
        try:
            logging.info("Sending event context data to API...")
            response = await client.post(EVENT_CONTEXT_API_URL, json=event_context_payload)
            response.raise_for_status()  # Will raise an exception for non-200 responses
            logging.info("API Response: %s", json.dumps(response.json(), indent=2))

            # Extract the result from the API response
            result = response.json().get("result", {})
            hand_position = "unnatural"  # Placeholder (replace with actual model logic)
            certainty_score = 96.0  # Example score, replace with actual score
            var_review_status = certainty_score < 95  # Simulate VAR review status

            # Log the decision
            log_decision(frame_number=event_context_payload['frame'],
                         hand_position=hand_position,
                         certainty_score=certainty_score,
                         var_review_status=var_review_status)

        except httpx.RequestError as e:
            logging.error(f"Failed to communicate with Event Context API: {e}")

# --- Main Async Loop ---
if __name__ == "__main__":
    asyncio.run(send_event_context_data())  # Run the async function to send the request

