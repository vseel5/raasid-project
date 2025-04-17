import logging
import httpx
import json
import asyncio
from typing import Dict, Any, Optional, List, Tuple
import numpy as np
from pydantic import BaseModel, Field
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger
from api.config import settings
import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image

# --- Constants ---
EVENT_CONTEXT_API_URL = "http://127.0.0.1:8000/event_context_ai"
TIMEOUT = httpx.Timeout(10.0, connect=5.0)

# --- Data Models ---
class EventContextData(BaseModel):
    """Data model for event context analysis results"""
    game_situation: str = Field(..., description="Current game situation")
    player_intent: str = Field(..., description="Estimated player intent")
    play_context: str = Field(..., description="Overall play context")
    confidence_score: float = Field(..., ge=0, le=1, description="Overall confidence score")

class DecisionLog(BaseModel):
    frame: int
    hand_position: str
    certainty_score: float
    var_review_status: bool

# --- Default Payload ---
DEFAULT_EVENT_CONTEXT_PAYLOAD = EventContextData(
    frame=2025,
    handball_decision="intentional",
    certainty_score=88.0,
    rule_violation=True
)

async def log_decision(
    frame_number: int,
    hand_position: str,
    certainty_score: float,
    var_review_status: bool
) -> None:
    """
    Log a decision for event context analysis.
    
    Args:
        frame_number: Frame number
        hand_position: Detected hand position
        certainty_score: Certainty score of the detection
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

async def send_event_context_data() -> Dict[str, Any]:
    """
    Send event context data to the API.
    
    Returns:
        Dictionary containing the API response
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            logger.info("Sending event context data to API...")
            response = await client.post(
                EVENT_CONTEXT_API_URL,
                json=DEFAULT_EVENT_CONTEXT_PAYLOAD.dict()
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info("Event context data sent successfully.")
            return result
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during event context analysis: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during event context analysis: {e}")
        raise

# --- Main Async Loop ---
if __name__ == "__main__":
    asyncio.run(send_event_context_data())  # Run the async function to send the request

class ContextCNN(nn.Module):
    """Custom CNN for analyzing game context"""
    
    def __init__(self):
        super(ContextCNN, self).__init__()
        
        # Feature extraction
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        
        # Classification heads
        self.game_situation_head = nn.Sequential(
            nn.Linear(128 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 5)  # 5 game situations
        )
        
        self.intent_head = nn.Sequential(
            nn.Linear(128 * 8 * 8, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, 4)  # 4 intent classes
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        
        game_situation = self.game_situation_head(x)
        intent = self.intent_head(x)
        
        return game_situation, intent

class ContextAnalyzer:
    """Analyzes the context of potential handball incidents using CNN"""
    
    def __init__(self):
        # Initialize CNN model
        self.model = ContextCNN()
        self.model.load_state_dict(torch.load('models/context_cnn.pth'))
        self.model.eval()
        
        # Define transforms
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                              std=[0.229, 0.224, 0.225])
        ])
        
        # Define class labels
        self.game_situations = [
            "defensive_block",
            "attacking_play",
            "set_piece",
            "open_play",
            "counter_attack"
        ]
        self.player_intents = [
            "deliberate",
            "accidental",
            "natural_position",
            "unnatural_position"
        ]
        
    def preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess frame for CNN"""
        try:
            # Convert to PIL Image
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # Apply transforms
            tensor = self.transform(image)
            # Add batch dimension
            tensor = tensor.unsqueeze(0)
            return tensor
        except Exception as e:
            logger.error(f"Error preprocessing frame: {str(e)}")
            raise

    def analyze_game_situation(self, 
                             frame: np.ndarray,
                             ball_position: List[float]) -> Tuple[str, float]:
        """
        Analyze the current game situation using CNN
        
        Args:
            frame: Input frame as numpy array
            ball_position: Current ball position [x, y]
            
        Returns:
            Tuple of (game_situation, confidence_score)
        """
        try:
            # Preprocess frame
            tensor = self.preprocess_frame(frame)
            
            # Run model inference
            with torch.no_grad():
                game_situation_logits, _ = self.model(tensor)
                probabilities = torch.softmax(game_situation_logits, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
            # Get predicted class and confidence
            situation_idx = predicted.item()
            game_situation = self.game_situations[situation_idx]
            confidence_score = confidence.item()
            
            return game_situation, confidence_score
            
        except Exception as e:
            logger.error(f"Error analyzing game situation: {str(e)}")
            return "unknown", 0.0

    def analyze_player_intent(self,
                            frame: np.ndarray,
                            pose_data: Dict[str, Any],
                            ball_contact_data: Dict[str, Any]) -> Tuple[str, float]:
        """
        Analyze player's intent using CNN and additional features
        
        Args:
            frame: Input frame as numpy array
            pose_data: Pose estimation results
            ball_contact_data: Ball contact detection results
            
        Returns:
            Tuple of (player_intent, confidence_score)
        """
        try:
            # Preprocess frame
            tensor = self.preprocess_frame(frame)
            
            # Run model inference
            with torch.no_grad():
                _, intent_logits = self.model(tensor)
                probabilities = torch.softmax(intent_logits, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                
            # Get predicted class and confidence
            intent_idx = predicted.item()
            player_intent = self.player_intents[intent_idx]
            confidence_score = confidence.item()
            
            # Adjust confidence based on additional features
            contact_prob = ball_contact_data.get('contact_probability', 0)
            contact_force = ball_contact_data.get('contact_force', 0)
            
            # Combine CNN confidence with contact features
            final_confidence = (confidence_score + contact_prob + contact_force) / 3
            
            return player_intent, final_confidence
            
        except Exception as e:
            logger.error(f"Error analyzing player intent: {str(e)}")
            return "unknown", 0.0

    def analyze_context(self,
                       frame: np.ndarray,
                       pose_data: Dict[str, Any],
                       ball_contact_data: Dict[str, Any]) -> EventContextData:
        """
        Perform comprehensive context analysis
        
        Args:
            frame: Input frame as numpy array
            pose_data: Pose estimation results
            ball_contact_data: Ball contact detection results
            
        Returns:
            EventContextData containing context analysis results
        """
        try:
            # Analyze game situation
            game_situation, game_confidence = self.analyze_game_situation(
                frame, ball_contact_data['ball_position']
            )
            
            # Analyze player intent
            player_intent, intent_confidence = self.analyze_player_intent(
                frame, pose_data, ball_contact_data
            )
            
            # Determine overall play context
            if game_situation == "defensive_block" and player_intent == "deliberate":
                play_context = "likely_handball"
            elif game_situation == "attacking_play" and player_intent == "accidental":
                play_context = "possible_handball"
            else:
                play_context = "unlikely_handball"
                
            # Calculate overall confidence
            confidence = (game_confidence + intent_confidence) / 2
            
            return EventContextData(
                game_situation=game_situation,
                player_intent=player_intent,
                play_context=play_context,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Error in context analysis: {str(e)}")
            raise

# Create a global context analyzer instance
context_analyzer = ContextAnalyzer()

