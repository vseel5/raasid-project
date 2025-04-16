import logging
import time
import random
import cv2
import asyncio
from typing import Dict, Any
from api.utils.storage import load_decision_logs, save_decision_logs  # Import logging functions
from api.utils.logger import logger  # Ensure logger is available
from api.routers.decision import log_decision  # Import log_decision function
import httpx

POSE_API_ENDPOINT = "http://127.0.0.1:8000/pose_estimation"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pose_estimation")

# --- Real-Time Pose Estimation ---
def get_real_time_pose_data(frame: int, hand_position: str, limb_angles: Dict[str, float], certainty_score: float) -> Dict[str, Any]:
    return {
        "frame": frame,
        "hand_position": hand_position,
        "limb_angles": limb_angles,
        "certainty_score": certainty_score
    }

async def process_video_frame(frame: int) -> Dict[str, Any]:
    """ Simulate pose detection logic (replace with actual model inference) """
    hand_position = "unnatural"  # Example (you can replace this with model-based logic)
    limb_angles = {"elbow": 110, "shoulder": 45}  # Example
    certainty_score = random.uniform(85, 100)  # Example score
    return get_real_time_pose_data(frame, hand_position, limb_angles, certainty_score)

# --- Function to Log the Decision ---
async def log_decision_async(frame_number, hand_position, certainty_score, var_review_status):
    """ Log decision asynchronously to avoid blocking main loop """
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

# --- Real-Time Video Capture and API Call ---
async def capture_video_and_send_for_pose_estimation():
    cap = cv2.VideoCapture("E:/test_raasid/accidental_handball_video.mp4")  # Path to your video
    if not cap.isOpened():
        logger.error("Could not open video stream")
        return

    frame_count = 0
    max_frames = 500  # Set a max frame limit to avoid an infinite loop

    while True:
        ret, frame = cap.read()  # Read each frame
        if not ret:
            logger.info("End of video reached or failed to read frame.")
            break  # Exit the loop when video ends or frame read fails

        frame_number = int(time.time())  # Use timestamp as frame ID

        logger.info(f"Processing frame {frame_number}: Pose Estimation")

        # Step 1: Process Pose Estimation (Pose Estimation should be done once per frame)
        pose_data = await process_video_frame(frame_number)  # Pass the frame number to the function

        # Simulate the certainty score and VAR review status
        certainty_score = pose_data['certainty_score']
        var_review_status = certainty_score < 95  # Assume VAR review is triggered for low confidence

        # Log the decision for this frame asynchronously
        await log_decision_async(
            frame_number=frame_number,
            hand_position=pose_data['hand_position'],
            certainty_score=certainty_score,
            var_review_status=var_review_status
        )

        # Step 2: Send Pose Data to API
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(POSE_API_ENDPOINT, json=pose_data)
                response.raise_for_status()
                logger.info(f"Response: {response.status_code} | Data: {response.json()}")
            except httpx.RequestError as e:
                logger.error(f"Pose Estimation API call failed: {e}")

        # Optional: Display frame with pose annotations (for debugging purposes)
        cv2.imshow('Pose Estimation Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Press 'q' to quit

        frame_count += 1
        if frame_count >= max_frames:
            logger.info("Reached max frame count. Ending simulation.")
            break  # Exit the loop if we've reached the max frames

    cap.release()  # Release the video capture when done
    cv2.destroyAllWindows()  # Close all OpenCV windows

# --- Main Async Loop ---
if __name__ == "__main__":
    asyncio.run(capture_video_and_send_for_pose_estimation())  # Run the async function
