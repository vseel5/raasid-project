import os
import json
import logging
import cv2
from typing import Dict, Any, List, Optional
import numpy as np
import torch
import torchvision
from torchvision import models, transforms
from PIL import Image
from pathlib import Path
from torchvision.models.detection import fasterrcnn_resnet50_fpn, keypointrcnn_resnet50_fpn

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.detection_model = None
        self.pose_model = None
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.load_models()

    def load_models(self):
        try:
            # Load object detection model
            self.detection_model = fasterrcnn_resnet50_fpn(pretrained=True)
            self.detection_model.to(self.device)
            self.detection_model.eval()

            # Load pose estimation model
            self.pose_model = keypointrcnn_resnet50_fpn(pretrained=True)
            self.pose_model.to(self.device)
            self.pose_model.eval()

            logging.info("Models loaded successfully")
            return True
        except Exception as e:
            logging.error(f"Error loading models: {str(e)}")
            return False

    def preprocess_frame(self, frame):
        try:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            pil_image = Image.fromarray(frame_rgb)
            
            # Apply transformations
            tensor = self.transform(pil_image)
            
            # Add batch dimension
            tensor = tensor.unsqueeze(0)
            
            return tensor.to(self.device)
        except Exception as e:
            logging.error(f"Error preprocessing frame: {str(e)}")
            return None

    def detect_objects(self, frame_tensor):
        try:
            with torch.no_grad():
                predictions = self.detection_model(frame_tensor)
                
            return [{
                'boxes': pred['boxes'].cpu().numpy(),
                'labels': pred['labels'].cpu().numpy(),
                'scores': pred['scores'].cpu().numpy()
            } for pred in predictions]
        except Exception as e:
            logging.error(f"Error detecting objects: {str(e)}")
            return None

    def estimate_poses(self, frame_tensor):
        try:
            with torch.no_grad():
                predictions = self.pose_model(frame_tensor)
                
            return [{
                'keypoints': pred['keypoints'].cpu().numpy(),
                'scores': pred['scores'].cpu().numpy()
            } for pred in predictions]
        except Exception as e:
            logging.error(f"Error estimating poses: {str(e)}")
            return None

    def analyze_frame(self, frame):
        try:
            # Preprocess frame
            frame_tensor = self.preprocess_frame(frame)
            if frame_tensor is None:
                return None
            
            # Detect objects
            detections = self.detect_objects(frame_tensor)
            
            # Estimate poses
            poses = self.estimate_poses(frame_tensor)
            
            return {
                'detections': detections,
                'poses': poses
            }
        except Exception as e:
            logging.error(f"Error analyzing frame: {str(e)}")
            return None

    def cleanup(self):
        """Clean up model resources."""
        try:
            for model in [self.detection_model, self.pose_model]:
                if isinstance(model, torch.nn.Module):
                    model.cpu()
                    del model
            torch.cuda.empty_cache()
            logger.info("Cleaned up model resources")
        except Exception as e:
            logger.error(f"Error cleaning up models: {str(e)}") 