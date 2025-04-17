import logging
import httpx
import json
import asyncio
from typing import Dict, Any, Optional, List, Tuple
import numpy as np
import cv2
from pydantic import BaseModel, Field
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger
from api.config import settings
from ultralytics import YOLO

# --- Constants ---
BALL_CONTACT_API_URL = "http://127.0.0.1:8000/ball_contact_ai"
TIMEOUT = httpx.Timeout(10.0, connect=5.0)

# --- Data Models ---
class BallContactData(BaseModel):
    """Data model for ball contact detection results"""
    ball_position: List[float] = Field(..., description="Ball position [x, y]")
    hand_position: List[float] = Field(..., description="Hand position [x, y]")
    contact_probability: float = Field(..., ge=0, le=1, description="Probability of contact")
    contact_force: float = Field(..., ge=0, description="Estimated force of contact")
    confidence_score: float = Field(..., ge=0, le=1, description="Overall confidence score")

class DecisionLog(BaseModel):
    frame: int
    ball_contact: bool
    impact_force: float
    certainty_score: float
    var_review_status: bool

# --- Default Payload ---
DEFAULT_BALL_CONTACT_PAYLOAD = BallContactData(
    frame=2025,
    ball_contact=True,
    impact_force=4.0,
    contact_duration=0.06,
    sensor_source="Smart Ball Sensor"
)

async def log_decision(
    frame_number: int,
    ball_contact: bool,
    impact_force: float,
    certainty_score: float,
    var_review_status: bool
) -> None:
    """
    Log a decision for ball contact detection.
    
    Args:
        frame_number: Frame number
        ball_contact: Whether ball contact was detected
        impact_force: Force of impact
        certainty_score: Certainty score of the detection
        var_review_status: Whether VAR review is required
    """
    try:
        logs = await load_decision_logs()
        
        decision = DecisionLog(
            frame=frame_number,
            ball_contact=ball_contact,
            impact_force=impact_force,
            certainty_score=certainty_score,
            var_review_status=var_review_status
        )

        logs.append(decision.dict())
        await save_decision_logs(logs)
        logger.info(f"Decision for frame {frame_number} logged successfully.")
    except Exception as e:
        logger.error(f"Failed to log decision for frame {frame_number}: {e}")
        raise

async def send_ball_contact_data() -> Dict[str, Any]:
    """
    Send ball contact data to the API.
    
    Returns:
        Dictionary containing the API response
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            logger.info("Sending ball contact data to API...")
            response = await client.post(
                BALL_CONTACT_API_URL,
                json=DEFAULT_BALL_CONTACT_PAYLOAD.dict()
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info("Ball contact data sent successfully.")
            return result
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during ball contact detection: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during ball contact detection: {e}")
        raise

class BallDetector:
    """Handles ball detection and contact analysis using YOLOv8"""
    
    def __init__(self):
        # Initialize YOLOv8 model
        self.model = YOLO('yolov8n.pt')  # Load pretrained model
        self.ball_class_id = 32  # COCO class ID for sports ball
        
        # Initialize optical flow for velocity estimation
        self.prev_frame = None
        self.prev_ball_pos = None
        
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess frame for ball detection"""
        try:
            # Resize frame to model input size
            resized = cv2.resize(frame, (640, 640))
            return resized
        except Exception as e:
            logger.error(f"Error preprocessing frame: {str(e)}")
            raise

    def detect_ball(self, frame: np.ndarray) -> Tuple[List[float], float]:
        """
        Detect ball position in frame using YOLOv8
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            Tuple of (ball_position, confidence_score)
        """
        try:
            # Preprocess frame
            processed_frame = self.preprocess_frame(frame)
            
            # Run YOLOv8 inference
            results = self.model(processed_frame, classes=[self.ball_class_id])
            
            if len(results) == 0 or len(results[0].boxes) == 0:
                return [0.0, 0.0], 0.0
                
            # Get the most confident detection
            box = results[0].boxes[0]
            confidence = float(box.conf)
            
            # Get ball position (normalized coordinates)
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            ball_position = [
                (x1 + x2) / (2 * frame.shape[1]),  # Normalized x
                (y1 + y2) / (2 * frame.shape[0])   # Normalized y
            ]
            
            return ball_position, confidence
            
        except Exception as e:
            logger.error(f"Error in ball detection: {str(e)}")
            return [0.0, 0.0], 0.0

    def estimate_velocity(self, 
                        current_pos: List[float],
                        prev_pos: List[float],
                        time_interval: float = 1.0/30.0) -> float:
        """
        Estimate ball velocity between frames
        
        Args:
            current_pos: Current ball position
            prev_pos: Previous ball position
            time_interval: Time between frames in seconds
            
        Returns:
            Estimated velocity in pixels per second
        """
        try:
            if prev_pos is None:
                return 0.0
                
            # Calculate displacement
            displacement = np.linalg.norm(
                np.array(current_pos) - np.array(prev_pos)
            )
            
            # Calculate velocity
            velocity = displacement / time_interval
            
            return velocity
            
        except Exception as e:
            logger.error(f"Error estimating velocity: {str(e)}")
            return 0.0

    def detect_contact(self, 
                      frame: np.ndarray, 
                      ball_position: List[float],
                      hand_position: List[float]) -> BallContactData:
        """
        Detect contact between ball and hand
        
        Args:
            frame: Input frame as numpy array
            ball_position: Detected ball position [x, y]
            hand_position: Detected hand position [x, y]
            
        Returns:
            BallContactData containing contact analysis results
        """
        try:
            # Calculate distance between ball and hand
            distance = np.linalg.norm(np.array(ball_position) - np.array(hand_position))
            
            # Calculate contact probability based on distance
            contact_prob = max(0, 1 - distance)
            
            # Estimate contact force based on ball velocity
            velocity = self.estimate_velocity(ball_position, self.prev_ball_pos)
            contact_force = min(1.0, velocity / 100.0)  # Normalize velocity
            
            # Update previous positions
            self.prev_ball_pos = ball_position
            self.prev_frame = frame
            
            # Calculate overall confidence
            confidence = min(contact_prob, 0.9)  # Cap confidence at 0.9
            
            return BallContactData(
                ball_position=ball_position,
                hand_position=hand_position,
                contact_probability=contact_prob,
                contact_force=contact_force,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Error in contact detection: {str(e)}")
            raise

# Create a global ball detector instance
ball_detector = BallDetector()

# --- Main Async Loop ---
if __name__ == "__main__":
    asyncio.run(send_ball_contact_data())  # Run the async function to send the request




