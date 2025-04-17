from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
import aiohttp
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger
from pydantic import BaseModel

# Initialize router
router = APIRouter()

class DecisionLog(BaseModel):
    frame: int
    hand_position: str
    certainty_score: float
    var_review_status: bool

async def log_decision(
    frame_number: int,
    hand_position: str,
    certainty_score: float,
    var_review_status: bool
) -> None:
    """
    Log a decision for a specific frame.
    
    Args:
        frame_number: The frame number
        hand_position: The detected hand position
        certainty_score: The certainty score of the decision
        var_review_status: Whether VAR review is required
    """
    try:
        logs = await load_decision_logs()
        
        if not isinstance(logs, list):
            raise ValueError("Loaded logs are not in the expected list format.")
        
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

async def send_post(endpoint: str, payload: Dict[str, Any], action_name: str) -> Dict[str, Any]:
    """
    Send a POST request to the given endpoint with the payload.
    
    Args:
        endpoint: The API endpoint to send the request to
        payload: The data to send in the request
        action_name: Name of the action for logging purposes
        
    Returns:
        The response data from the endpoint
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload) as response:
                if response.status != 200:
                    error_msg = f"Failed to {action_name}. Status: {response.status}"
                    logger.error(error_msg)
                    raise HTTPException(status_code=response.status, detail=error_msg)
                
                return await response.json()
    except Exception as e:
        logger.error(f"Error during {action_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decision_making_ai")
async def decision_making(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process decision making data and return the result.
    
    Args:
        data: The input data for decision making
        
    Returns:
        The decision making result
    """
    try:
        # Process the decision making data
        result = await process_decision_data(data)
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error in decision making: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
