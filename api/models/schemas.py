from pydantic import BaseModel, Field, confloat, constr
from typing import Optional, Dict, Literal, List, Any

# ==============================
# Reusable Types & Base Classes
# ==============================

FrameNumber = Field(..., ge=0, description="Frame number in the video sequence")
CertaintyScore = confloat(ge=0.0, le=100.0)
PositiveFloat = confloat(gt=0.0)

class StrictBaseModel(BaseModel):
    class Config:
        extra = "forbid"
        anystr_strip_whitespace = True
        allow_population_by_field_name = True
        schema_extra = {"example": {}}

# ==================
# Pose Estimation
# ==================

class PoseEstimationInput(StrictBaseModel):
    frame: int = FrameNumber
    hand_position: Literal["natural", "unnatural"] = Field(..., description="Detected hand position")
    limb_angles: Dict[str, float] = Field(..., description="Joint angles like elbow, shoulder")
    certainty_score: CertaintyScore = Field(..., description="Confidence score from pose estimation AI")

    class Config(StrictBaseModel.Config):
        schema_extra = {
            "example": {
                "frame": 12,
                "hand_position": "unnatural",
                "limb_angles": {"elbow": 120.5, "shoulder": 45.2},
                "certainty_score": 92.4
            }
        }

# ==================
# Ball Contact
# ==================

class BallContactInput(StrictBaseModel):
    frame: int = FrameNumber
    ball_contact: bool = Field(..., description="Whether ball contact occurred")
    impact_force: PositiveFloat = Field(..., description="Impact force in Newtons")
    contact_duration: PositiveFloat = Field(..., description="Duration of contact in seconds")
    sensor_source: constr(min_length=1) = Field(..., description="Source of sensor data")

    class Config(StrictBaseModel.Config):
        schema_extra = {
            "example": {
                "frame": 12,
                "ball_contact": True,
                "impact_force": 3.2,
                "contact_duration": 0.045,
                "sensor_source": "Smart Ball Sensor"
            }
        }

# ==================
# Event Context
# ==================

class EventContextInput(StrictBaseModel):
    frame: int = FrameNumber
    handball_decision: Literal["intentional", "accidental"] = Field(..., description="Type of handball call")
    certainty_score: CertaintyScore = Field(..., description="Confidence level of the context decision")
    rule_violation: bool = Field(..., description="Whether this violates handball rule")

    class Config(StrictBaseModel.Config):
        schema_extra = {
            "example": {
                "frame": 12,
                "handball_decision": "intentional",
                "certainty_score": 95.7,
                "rule_violation": True
            }
        }

# ==================
# Final Decision
# ==================

class FinalDecisionInput(StrictBaseModel):
    frame: int = FrameNumber
    final_decision: constr(min_length=1) = Field(..., description="Final call by AI or VAR")
    certainty_score: CertaintyScore = Field(..., description="Certainty behind final call")
    VAR_review: bool = Field(..., description="True if reviewed/modified by VAR")
    reason: Optional[str] = Field(None, description="Justification or rationale for decision")

    class Config(StrictBaseModel.Config):
        schema_extra = {
            "example": {
                "frame": 12,
                "final_decision": "No Handball",
                "certainty_score": 88.9,
                "VAR_review": True,
                "reason": "Player's arm in natural position; accidental contact"
            }
        }

# ==================
# VAR Override
# ==================

class VAROverrideInput(StrictBaseModel):
    frame: int = FrameNumber
    override_decision: constr(min_length=1) = Field(..., description="Manual override decision by VAR")

    class Config(StrictBaseModel.Config):
        schema_extra = {
            "example": {
                "frame": 12,
                "override_decision": "Handball – Penalty"
            }
        }

# ==================
# Output Response
# ==================

class OutputDistributionResponse(StrictBaseModel):
    status: str = Field(..., description="Operation status (e.g., Success, Failure)")
    message: str = Field(..., description="Human-readable message or summary")
    decision: Dict[str, Any] = Field(..., description="The final decision object distributed")
    distribution_id: str = Field(..., description="Unique ID for tracking this delivery")
    timestamp: str = Field(..., description="UTC timestamp of delivery event")
    report_path: Optional[str] = Field(None, description="Path to saved report file, if any")
    delivered_to: List[str] = Field(..., description="List of target systems that received the decision")

    class Config(StrictBaseModel.Config):
        schema_extra = {
            "example": {
                "status": "Success",
                "message": "Decision distributed to all endpoints",
                "decision": {
                    "frame": 12,
                    "final_decision": "No Handball",
                    "certainty_score": 88.9,
                    "VAR_review": True,
                    "reason": "Player's arm in natural position; accidental contact"
                },
                "distribution_id": "a1b2c3d4-5678-9012-efgh-3456789abcd",
                "timestamp": "2025-04-06T15:22:01.456Z",
                "report_path": "logs/decisions/decision_a1b2c3d4_20250406_152201.json",
                "delivered_to": [
                    "Referee Smartwatch",
                    "TV Broadcast",
                    "Cloud Storage"
                ]
            }
        }
