import logging
import time
import random
import cv2
import asyncio
from api.simulations.pose_estimation import capture_video_and_send_for_pose_estimation
from api.simulations.ball_contact_ai import send_ball_contact_data
from api.simulations.event_context_ai import send_event_context_data
from api.utils.storage import load_decision_logs, save_decision_logs  # Log decisions
from api.utils.logger import logger
from api.routers.decision import log_decision  # Import log_decision function

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Helper Function for Frame Processing ---
async def process_frame(frame_number, frame):
    """
    Process a single video frame:
    - Perform pose estimation
    - Simulate ball contact detection
    - Simulate event context analysis
    - Log decision for the frame
    """
    logger.info(f"Processing frame {frame_number}")

    try:
        # Step 1: Process Pose Estimation
        pose_data = await capture_video_and_send_for_pose_estimation()

        # Step 2: Simulate Ball Contact Detection and Event Context Analysis in Parallel
        ball_contact_task = send_ball_contact_data()
        event_context_task = send_event_context_data()
        ball_contact_data, event_context_data = await asyncio.gather(ball_contact_task, event_context_task)

        # Step 3: Simulate decision-making
        certainty_score = random.uniform(85, 100)  # Example score
        var_review_status = certainty_score < 95  # Assume VAR review is triggered for low confidence

        # Log the decision for this frame
        log_decision(
            frame_number=frame_number,
            hand_position="unnatural",  # Example value
            certainty_score=certainty_score,
            var_review_status=var_review_status
        )

        logger.info(f"Frame {frame_number} processed successfully.")
    except Exception as e:
        logger.error(f"Error processing frame {frame_number}: {e}")

# --- Full Simulation Helper ---
async def full_system_simulation(video_path="E:/test_raasid/intentional_handball.jpg", max_frames=500, skip_frames=5):
    """
    Run the full system simulation:
    - Capture video frames
    - Process frames using the simulation pipeline
    """
    try:
        cap = cv2.VideoCapture(video_path)  # Path to your video
        if not cap.isOpened():
            logger.error("Could not open video stream")
            return

        frame_count = 0

        while True:
            ret, frame = cap.read()  # Read each frame
            if not ret:
                logger.info("End of video reached or failed to read frame.")
                break  # Exit the loop when video ends or frame read fails

            if frame_count % skip_frames != 0:  # Skip frames for optimization
                frame_count += 1
                continue  # Skip this frame and move to the next

            frame_number = int(time.time())  # Use timestamp as frame ID

            # Process the frame
            await process_frame(frame_number, frame)

            # Optional: Display frame with pose annotations (for debugging purposes)
            cv2.imshow('Pose Estimation Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                logger.info("Quit signal received. Exiting simulation.")
                break  # Press 'q' to quit

            frame_count += 1
            if frame_count >= max_frames:
                logger.info("Reached max frame count. Ending simulation.")
                break  # Exit the loop if we've reached the max frames

    except Exception as e:
        logger.error(f"Error in full_system_simulation: {e}")
    finally:
        cap.release()  # Release the video capture when done
        cv2.destroyAllWindows()  # Close all OpenCV windows

# --- Run Full System Simulation ---
if __name__ == "__main__":
    asyncio.run(full_system_simulation())  # Run the full pipeline simulation


