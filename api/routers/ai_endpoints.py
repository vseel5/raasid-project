from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from ..models.schemas import PoseEstimationInput, BallContactInput, EventContextInput
from api.utils.logger import logger
from api.utils.storage import load_decision_logs, save_decision_logs
import random

router = APIRouter()

# Unified response format
def generate_response(result: dict) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_200_OK, content={
        "status": "Success",
        "result": result
    })

# Optimized log function
def log_decision(frame_number, hand_position, certainty_score, var_review_status):
    logs = load_decision_logs()
    decision = {
        "frame": frame_number,
        "hand_position": hand_position,
        "certainty_score": certainty_score,
        "VAR_review": var_review_status
    }
    logs.append(decision)
    save_decision_logs(logs)
    logger.info(f"Decision for frame {frame_number} logged: {decision}")

# Pose Estimation endpoint
@router.post("/pose_estimation", summary="Simulate pose estimation AI")
async def pose_estimation(data: PoseEstimationInput):
    try:
        result = {
            "handball_detected": random.choice([True, False]),
            "intentional": random.choice([True, False]),
            "confidence_score": round(random.uniform(85, 98), 1),
            "contact_duration": round(random.uniform(0.03, 0.08), 3),
            "impact_force": round(random.uniform(1.5, 4.5), 2),
            "pose_unusual": random.choice([True, False])
        }
        log_decision(data.frame, data.hand_position, result['confidence_score'], result['pose_unusual'])
        return generate_response(result)
    except Exception as e:
        logger.exception("Pose estimation processing failed")
        raise HTTPException(status_code=500, detail="Pose estimation failed")

# Ball contact AI endpoint
@router.post("/ball_contact_ai", summary="Simulate ball contact AI")
async def ball_contact_ai(data: BallContactInput):
    try:
        result = {
            "ball_contact": data.ball_contact,
            "impact_force": data.impact_force,
            "contact_duration": data.contact_duration
        }
        log_decision(data.frame, data.hand_position, result['impact_force'], False)
        return generate_response(result)
    except Exception as e:
        logger.exception("Ball contact processing failed")
        raise HTTPException(status_code=500, detail="Ball contact analysis failed")

# Event context AI endpoint
@router.post("/event_context_ai", summary="Simulate event context AI")
async def event_context_ai(data: EventContextInput):
    try:
        result = {
            "handball_decision": data.handball_decision,
            "certainty_score": data.certainty_score,
            "rule_violation": data.rule_violation
        }
        log_decision(data.frame, data.hand_position, result['certainty_score'], data.rule_violation)
        return generate_response(result)
    except Exception as e:
        logger.exception("Event context processing failed")
        raise HTTPException(status_code=500, detail="Event context analysis failed")



