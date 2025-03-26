from fastapi import APIRouter
from api.models.schemas import PoseEstimationInput, BallContactInput, EventContextInput
from api.utils.logger import logger

router = APIRouter()

@router.post("/pose_estimation")
def pose_estimation(data: PoseEstimationInput):
    logger.info(f"Pose Estimation Data Received: {data.dict()}")
    return {"status": "Success", "message": "Pose estimation processed"}

@router.post("/ball_contact_ai")
def ball_contact_ai(data: BallContactInput):
    logger.info(f"Ball Contact AI Received: {data.dict()}")
    return {"status": "Success", "message": "Ball contact processed"}

@router.post("/event_context_ai")
def event_context_ai(data: EventContextInput):
    logger.info(f"Event Context AI Received: {data.dict()}")
    return {"status": "Success", "message": "Event context processed"}




