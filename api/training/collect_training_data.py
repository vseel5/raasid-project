import cv2
import numpy as np
import json
import os
from typing import Dict, List, Tuple
from api.utils.logger import logger
from api.simulations.components.pose_estimation import pose_estimator
from api.simulations.components.ball_contact import ball_detector

class TrainingDataCollector:
    """Collects and prepares training data for context analysis"""
    
    def __init__(self, output_dir: str):
        """
        Initialize data collector
        
        Args:
            output_dir: Directory to save collected data
        """
        self.output_dir = output_dir
        self.annotations = []
        
        # Create output directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
        
    def process_video_frame(
        self,
        frame: np.ndarray,
        frame_number: int,
        game_situation: str,
        player_intent: str
    ) -> None:
        """
        Process a video frame and save training data
        
        Args:
            frame: Video frame
            frame_number: Frame number
            game_situation: Current game situation
            player_intent: Player's intent
        """
        try:
            # Get pose estimation
            pose_data = pose_estimator.estimate_pose(frame)
            
            # Get ball detection
            ball_position, _ = ball_detector.detect_ball(frame)
            
            # Save frame
            image_path = f'images/frame_{frame_number}.jpg'
            cv2.imwrite(
                os.path.join(self.output_dir, image_path),
                frame
            )
            
            # Create annotation
            annotation = {
                'image_path': image_path,
                'frame_number': frame_number,
                'game_situation': game_situation,
                'player_intent': player_intent,
                'pose_data': {
                    'keypoints': pose_data.keypoints,
                    'hand_positions': pose_data.hand_positions,
                    'body_orientation': pose_data.body_orientation
                },
                'ball_position': ball_position
            }
            
            self.annotations.append(annotation)
            
        except Exception as e:
            logger.error(f"Error processing frame {frame_number}: {str(e)}")
    
    def save_annotations(self, split: str = 'train') -> None:
        """
        Save collected annotations
        
        Args:
            split: 'train' or 'val'
        """
        try:
            # Split data into train/val
            np.random.shuffle(self.annotations)
            split_idx = int(len(self.annotations) * 0.8)
            
            if split == 'train':
                annotations = self.annotations[:split_idx]
            else:
                annotations = self.annotations[split_idx:]
            
            # Save annotations
            with open(
                os.path.join(self.output_dir, f'{split}_annotations.json'),
                'w'
            ) as f:
                json.dump(annotations, f, indent=2)
                
            logger.info(f"Saved {len(annotations)} {split} annotations")
            
        except Exception as e:
            logger.error(f"Error saving annotations: {str(e)}")

def collect_training_data(
    video_path: str,
    output_dir: str,
    game_situation: str,
    player_intent: str,
    frame_interval: int = 30
) -> None:
    """
    Collect training data from a video
    
    Args:
        video_path: Path to input video
        output_dir: Directory to save collected data
        game_situation: Current game situation
        player_intent: Player's intent
        frame_interval: Interval between frames to process
    """
    try:
        # Initialize collector
        collector = TrainingDataCollector(output_dir)
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        frame_number = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process every nth frame
            if frame_number % frame_interval == 0:
                collector.process_video_frame(
                    frame,
                    frame_number,
                    game_situation,
                    player_intent
                )
                
            frame_number += 1
            
        # Save annotations
        collector.save_annotations('train')
        collector.save_annotations('val')
        
        cap.release()
        
    except Exception as e:
        logger.error(f"Error collecting training data: {str(e)}")

if __name__ == '__main__':
    # Example usage
    config = {
        'video_path': 'data/videos/handball_incident.mp4',
        'output_dir': 'data/training',
        'game_situation': 'defensive_block',
        'player_intent': 'deliberate',
        'frame_interval': 30
    }
    
    collect_training_data(**config) 