from typing import Dict, Any, Tuple
from pydantic import BaseModel, Field
from datetime import datetime
import numpy as np
from api.config import settings
from api.utils.logger import logger

class DecisionInput(BaseModel):
    """Input data for decision making"""
    pose_data: Dict[str, Any] = Field(..., description="Pose estimation results")
    ball_contact_data: Dict[str, Any] = Field(..., description="Ball contact detection results")
    event_context_data: Dict[str, Any] = Field(..., description="Event context analysis results")
    frame_number: int = Field(..., description="Frame number in the sequence")
    timestamp: datetime = Field(default_factory=datetime.now)

class DecisionOutput(BaseModel):
    """Output data from decision making"""
    certainty_score: float = Field(..., ge=0, le=100, description="Certainty score of the decision")
    var_review_status: bool = Field(..., description="Whether VAR review is required")
    decision_reason: str = Field(..., description="Explanation of the decision")
    confidence_metrics: Dict[str, float] = Field(..., description="Detailed confidence metrics")
    timestamp: datetime = Field(default_factory=datetime.now)

class DecisionMaker:
    """Enhanced decision making system for handball incidents"""
    
    def __init__(self):
        self._pose_weights = {
            'hand_position': 0.4,
            'body_position': 0.3,
            'movement': 0.3
        }
        
        self._contact_weights = {
            'contact_probability': 0.5,
            'contact_location': 0.3,
            'contact_force': 0.2
        }
        
        self._context_weights = {
            'game_situation': 0.4,
            'player_intent': 0.3,
            'play_context': 0.3
        }

    def _analyze_pose(self, pose_data: Dict[str, Any]) -> Tuple[float, str]:
        """Analyze pose data for unnatural hand positions"""
        try:
            hand_position_score = pose_data.get('hand_position_score', 0)
            body_position_score = pose_data.get('body_position_score', 0)
            movement_score = pose_data.get('movement_score', 0)
            
            weighted_score = (
                hand_position_score * self._pose_weights['hand_position'] +
                body_position_score * self._pose_weights['body_position'] +
                movement_score * self._pose_weights['movement']
            )
            
            reason = "Natural position" if weighted_score < 0.5 else "Unnatural position"
            return weighted_score, reason
            
        except Exception as e:
            logger.error(f"Error analyzing pose: {str(e)}")
            return 0.0, "Error in pose analysis"

    def _analyze_contact(self, contact_data: Dict[str, Any]) -> Tuple[float, str]:
        """Analyze ball contact data"""
        try:
            contact_prob = contact_data.get('contact_probability', 0)
            location_score = contact_data.get('location_score', 0)
            force_score = contact_data.get('force_score', 0)
            
            weighted_score = (
                contact_prob * self._contact_weights['contact_probability'] +
                location_score * self._contact_weights['contact_location'] +
                force_score * self._contact_weights['contact_force']
            )
            
            reason = "No significant contact" if weighted_score < 0.5 else "Significant contact detected"
            return weighted_score, reason
            
        except Exception as e:
            logger.error(f"Error analyzing contact: {str(e)}")
            return 0.0, "Error in contact analysis"

    def _analyze_context(self, context_data: Dict[str, Any]) -> Tuple[float, str]:
        """Analyze event context"""
        try:
            game_situation = context_data.get('game_situation_score', 0)
            player_intent = context_data.get('player_intent_score', 0)
            play_context = context_data.get('play_context_score', 0)
            
            weighted_score = (
                game_situation * self._context_weights['game_situation'] +
                player_intent * self._context_weights['player_intent'] +
                play_context * self._context_weights['play_context']
            )
            
            reason = "Normal play" if weighted_score < 0.5 else "Suspicious play"
            return weighted_score, reason
            
        except Exception as e:
            logger.error(f"Error analyzing context: {str(e)}")
            return 0.0, "Error in context analysis"

    def make_decision(self, input_data: DecisionInput) -> DecisionOutput:
        """
        Make a decision based on all available data
        
        Args:
            input_data: DecisionInput containing all analysis results
            
        Returns:
            DecisionOutput with the final decision and confidence metrics
        """
        try:
            # Analyze each component
            pose_score, pose_reason = self._analyze_pose(input_data.pose_data)
            contact_score, contact_reason = self._analyze_contact(input_data.ball_contact_data)
            context_score, context_reason = self._analyze_context(input_data.event_context_data)
            
            # Calculate final scores
            final_score = (pose_score + contact_score + context_score) / 3
            certainty_score = final_score * 100
            
            # Determine if VAR review is needed
            var_review = certainty_score < settings.VAR_REVIEW_THRESHOLD
            
            # Prepare confidence metrics
            confidence_metrics = {
                'pose_confidence': pose_score,
                'contact_confidence': contact_score,
                'context_confidence': context_score,
                'final_confidence': final_score
            }
            
            # Prepare decision reason
            decision_reason = f"Pose: {pose_reason}, Contact: {contact_reason}, Context: {context_reason}"
            
            return DecisionOutput(
                certainty_score=certainty_score,
                var_review_status=var_review,
                decision_reason=decision_reason,
                confidence_metrics=confidence_metrics
            )
            
        except Exception as e:
            logger.error(f"Error in decision making: {str(e)}")
            return DecisionOutput(
                certainty_score=0.0,
                var_review_status=True,
                decision_reason=f"Error in decision making: {str(e)}",
                confidence_metrics={
                    'pose_confidence': 0.0,
                    'contact_confidence': 0.0,
                    'context_confidence': 0.0,
                    'final_confidence': 0.0
                }
            )

# Create a global decision maker instance
decision_maker = DecisionMaker()
