import logging
import httpx
import json
import asyncio
from api.utils.storage import load_decision_logs, save_decision_logs  # Import logging functions

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- API Endpoint ---
BALL_CONTACT_API_URL = "http://127.0.0.1:8000/ball_contact_ai"

# --- Simulated Ball Contact Detection Output ---
ball_contact_payload = {
    "frame": 2025,
    "ball_contact": True,
    "impact_force": 4.0,
    "contact_duration": 0.06,
    "sensor_source": "Smart Ball Sensor"
}

# --- Function to Log the Decision ---
def log_decision(frame_number, ball_contact, impact_force, certainty_score, var_review_status):
    # Load existing logs (from S3 or local)
    logs = load_decision_logs()

    # Create a new decision log entry
    decision = {
        "frame": frame_number,
        "ball_contact": ball_contact,
        "impact_force": impact_force,
        "certainty_score": certainty_score,
        "VAR_review": var_review_status
    }

    # Append the new decision to the list of logs
    logs.append(decision)

    # Save the updated logs to S3 or local storage
    save_decision_logs(logs)
    logging.info(f"Decision for frame {frame_number} logged successfully.")

# --- Asynchronous Function to Send Data ---
async def send_ball_contact_data():
    async with httpx.AsyncClient() as client:
        try:
            logging.info("Sending ball contact data to API...")
            response = await client.post(BALL_CONTACT_API_URL, json=ball_contact_payload)
            response.raise_for_status()  # Will raise an exception for non-200 responses

            # Simulated certainty score and VAR review status
            certainty_score = 94.0  # Example certainty score (replace with actual logic)
            var_review_status = certainty_score < 95  # Trigger VAR review for low confidence

            # Log the decision after sending the data
            log_decision(
                frame_number=ball_contact_payload['frame'],
                ball_contact=ball_contact_payload['ball_contact'],
                impact_force=ball_contact_payload['impact_force'],
                certainty_score=certainty_score,
                var_review_status=var_review_status
            )

            logging.info("API Response: %s", json.dumps(response.json(), indent=2))
        except httpx.RequestError as e:
            logging.error(f"Failed to communicate with Ball Contact API: {e}")

# --- Main Async Loop ---
if __name__ == "__main__":
    asyncio.run(send_ball_contact_data())  # Run the async function to send the request




