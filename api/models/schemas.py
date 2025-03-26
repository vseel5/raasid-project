from pydantic import BaseModel, Field
from typing import Optional, Dict


class PoseEstimationInput(BaseModel):
    frame: int = Field(..., description="Frame number of the video")
    hand_position: str = Field(
        ..., pattern ="^(natural|unnatural)$", description="Hand position status"
    )
    limb_angles: Dict[str, float] = Field(
        ..., description="Dictionary with joint angles like elbow, shoulder"
    )
    certainty_score: float = Field(
        ..., ge=0.0, le=100.0, description="Certainty score from the pose AI"
    )


class BallContactInput(BaseModel):
    frame: int = Field(..., description="Frame number")
    ball_contact: bool = Field(..., description="Whether ball-hand contact occurred")
    impact_force: float = Field(..., gt=0.0, description="Measured impact force")
    contact_duration: float = Field(..., gt=0.0, description="Duration of contact in seconds")
    sensor_source: str = Field(..., description="Source of contact data")


class EventContextInput(BaseModel):
    frame: int = Field(..., description="Frame number")
    handball_decision: str = Field(
        ..., pattern ="^(intentional|accidental)$", description="Handball decision type"
    )
    certainty_score: float = Field(
        ..., ge=0.0, le=100.0, description="Certainty of context classification"
    )
    rule_violation: bool = Field(..., description="Whether rules were violated")


class FinalDecisionInput(BaseModel):
    frame: int = Field(..., description="Frame number")
    final_decision: str = Field(..., description="Final call by AI or VAR")
    certainty_score: float = Field(..., ge=0.0, le=100.0)
    VAR_review: bool = Field(..., description="True if decision was overridden")
    reason: Optional[str] = Field(None, description="Explanation for the decision")


class VAROverrideInput(BaseModel):
    frame: int = Field(..., description="Frame to override")
    override_decision: str = Field(..., description="New manual decision")


class OutputDistributionResponse(BaseModel):
    status: str
    message: str


