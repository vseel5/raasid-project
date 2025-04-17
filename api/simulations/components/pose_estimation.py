import logging
import time
import random
import cv2
import asyncio
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field
import httpx
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger
import numpy as np
from api.config import settings
import mediapipe as mp

# --- Constants ---
POSE_API_ENDPOINT = "http://127.0.0.1:8000/pose_estimation"
TIMEOUT = httpx.Timeout(10.0, connect=5.0)

# --- Data Models ---
class PoseData(BaseModel):
    """Data model for pose estimation results"""
    keypoints: Dict[str, List[float]] = Field(..., description="Detected keypoints with confidence scores")
    hand_positions: Dict[str, List[float]] = Field(..., description="Hand positions (left and right)")
    body_orientation: float = Field(..., description="Body orientation angle in degrees")
    confidence_score: float = Field(..., ge=0, le=1, description="Overall confidence score")

class DecisionLog(BaseModel):
    frame: int
    hand_position: str
    certainty_score: float
    var_review_status: bool

# --- Helper Functions ---
def get_real_time_pose_data(
    frame: int,
    hand_position: str,
    limb_angles: Dict[str, float],
    certainty_score: float
) -> PoseData:
    """
    Create a PoseData object with the given parameters.
    
    Args:
        frame: Frame number
        hand_position: Detected hand position
        limb_angles: Dictionary of limb angles
        certainty_score: Certainty score of the detection
        
    Returns:
        PoseData object
    """
    return PoseData(
        frame=frame,
        hand_positions={
            'left': limb_angles['left_wrist'],
            'right': limb_angles['right_wrist']
        },
        body_orientation=limb_angles['shoulder'],
        confidence_score=certainty_score
    )

async def process_video_frame(frame: int) -> PoseData:
    """
    Process a video frame for pose estimation.
    
    Args:
        frame: Frame number to process
        
    Returns:
        PoseData object with detection results
    """
    try:
        # Simulate pose detection logic (replace with actual model inference)
        hand_positions = {"left": [0.5, 0.5], "right": [0.5, 0.5]}
        body_orientation = 45
        certainty_score = random.uniform(85, 100)
        
        return get_real_time_pose_data(frame, "unnatural", hand_positions, certainty_score)
    except Exception as e:
        logger.error(f"Error processing frame {frame}: {e}")
        raise

async def log_decision_async(
    frame_number: int,
    hand_position: str,
    certainty_score: float,
    var_review_status: bool
) -> None:
    """
    Log decision asynchronously.
    
    Args:
        frame_number: Frame number
        hand_position: Detected hand position
        certainty_score: Certainty score
        var_review_status: Whether VAR review is required
    """
    try:
        logs = await load_decision_logs()
        
        decision = DecisionLog(
            frame=frame_number,
            hand_position=hand_position,
            certainty_score=certainty_score,
            var_review_status=var_review_status
        )

        logs.append(decision.dict())
        await save_decision_logs(logs)
        logger.info(f"Decision for frame {frame_number} logged successfully.")
    except Exception as e:
        logger.error(f"Failed to log decision for frame {frame_number}: {e}")
        raise

async def capture_video_and_send_for_pose_estimation() -> Dict[str, Any]:
    """
    Capture video and send for pose estimation.
    
    Returns:
        Dictionary containing pose estimation results
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Simulate frame capture and processing
            frame_number = int(time.time())
            pose_data = await process_video_frame(frame_number)
            
            # Send to pose estimation API
            response = await client.post(
                POSE_API_ENDPOINT,
                json=pose_data.dict()
            )
            response.raise_for_status()
            
            return response.json()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during pose estimation: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during pose estimation: {e}")
        raise

# --- Main Async Loop ---
if __name__ == "__main__":
    asyncio.run(capture_video_and_send_for_pose_estimation())  # Run the async function

class PoseEstimator:
    """Handles pose estimation for players in video frames using MediaPipe"""
    
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # Initialize MediaPipe Drawing
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Define keypoint names
        self.keypoint_names = [
            'nose', 'left_eye_inner', 'left_eye', 'left_eye_outer',
            'right_eye_inner', 'right_eye', 'right_eye_outer',
            'left_ear', 'right_ear', 'mouth_left', 'mouth_right',
            'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
            'left_wrist', 'right_wrist', 'left_pinky', 'right_pinky',
            'left_index', 'right_index', 'left_thumb', 'right_thumb',
            'left_hip', 'right_hip', 'left_knee', 'right_knee',
            'left_ankle', 'right_ankle', 'left_heel', 'right_heel',
            'left_foot_index', 'right_foot_index'
        ]

    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess frame for pose estimation"""
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return rgb_frame
        except Exception as e:
            logger.error(f"Error preprocessing frame: {str(e)}")
            raise

    def estimate_pose(self, frame: np.ndarray) -> PoseData:
        """
        Estimate pose from a single frame using MediaPipe
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            PoseData containing detected keypoints and confidence scores
        """
        try:
            # Preprocess frame
            processed_frame = self.preprocess_frame(frame)
            
            # Process frame with MediaPipe
            results = self.pose.process(processed_frame)
            
            if not results.pose_landmarks:
                raise ValueError("No pose detected in frame")
            
            # Extract keypoints
            keypoints = {}
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                name = self.keypoint_names[idx]
                keypoints[name] = [
                    landmark.x,  # Normalized x coordinate
                    landmark.y,  # Normalized y coordinate
                    landmark.visibility  # Confidence score
                ]
            
            # Get hand positions
            left_hand = keypoints['left_wrist'][:2]
            right_hand = keypoints['right_wrist'][:2]
            
            # Calculate body orientation
            shoulder_vector = np.array(keypoints['right_shoulder'][:2]) - np.array(keypoints['left_shoulder'][:2])
            body_orientation = np.degrees(np.arctan2(shoulder_vector[1], shoulder_vector[0]))
            
            # Calculate overall confidence
            confidence_scores = [kp[2] for kp in keypoints.values()]
            overall_confidence = np.mean(confidence_scores)
            
            return PoseData(
                keypoints=keypoints,
                hand_positions={
                    'left': left_hand,
                    'right': right_hand
                },
                body_orientation=body_orientation,
                confidence_score=overall_confidence
            )
            
        except Exception as e:
            logger.error(f"Error in pose estimation: {str(e)}")
            raise

    def is_hand_unnatural(self, pose_data: PoseData) -> Tuple[bool, float]:
        """
        Determine if hand position is unnatural using advanced heuristics
        
        Args:
            pose_data: Pose estimation results
            
        Returns:
            Tuple of (is_unnatural, confidence_score)
        """
        try:
            # Get relevant keypoints
            left_shoulder = pose_data.keypoints['left_shoulder'][:2]
            right_shoulder = pose_data.keypoints['right_shoulder'][:2]
            left_elbow = pose_data.keypoints['left_elbow'][:2]
            right_elbow = pose_data.keypoints['right_elbow'][:2]
            left_hand = pose_data.hand_positions['left']
            right_hand = pose_data.hand_positions['right']
            
            # Calculate angles
            def calculate_angle(a, b, c):
                a = np.array(a)
                b = np.array(b)
                c = np.array(c)
                
                radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                angle = np.abs(radians*180.0/np.pi)
                
                if angle > 180.0:
                    angle = 360-angle
                    
                return angle
            
            # Calculate arm angles
            left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_hand)
            right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_hand)
            
            # Define thresholds for unnatural positions
            angle_threshold = 160  # Maximum angle for natural arm position
            height_threshold = 0.1  # Maximum height difference between shoulder and hand
            
            # Check if either arm is in unnatural position
            left_unnatural = (left_arm_angle > angle_threshold or 
                            abs(left_hand[1] - left_shoulder[1]) > height_threshold)
            right_unnatural = (right_arm_angle > angle_threshold or 
                             abs(right_hand[1] - right_shoulder[1]) > height_threshold)
            
            is_unnatural = left_unnatural or right_unnatural
            
            # Calculate confidence based on angle deviation
            max_angle_deviation = max(
                abs(left_arm_angle - 90),  # 90 degrees is typical natural position
                abs(right_arm_angle - 90)
            )
            confidence = min(1.0, max_angle_deviation / 90.0)
            
            return is_unnatural, confidence
            
        except Exception as e:
            logger.error(f"Error in unnatural hand detection: {str(e)}")
            return False, 0.0

# Create a global pose estimator instance
pose_estimator = PoseEstimator()
