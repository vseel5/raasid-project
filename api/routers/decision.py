from fastapi import APIRouter
import logging
from api.models.schemas import FinalDecisionInput, VAROverrideInput
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger

router = APIRouter()

# Endpoint: AI Decision Processing
@router.post("/decision_making_ai")
def decision_making(data: FinalDecisionInput):
    logger.info(f"Decision Making Data Received: {data.dict()}")

    # Generate a reason if not provided
    reason = data.reason
    if not reason:
        if data.certainty_score < 95:
            reason = "Uncertain decision — confidence below 95%"
        elif data.final_decision.lower() == "handball violation":
            reason = "Ball contacted unnatural hand position"
        else:
            reason = "Hand position judged natural; no violation"

    # Auto-trigger VAR if low confidence
    var_flag = data.VAR_review or data.certainty_score < 95

    # Prepare decision entry
    entry = {
        "frame": data.frame,
        "final_decision": data.final_decision,
        "certainty_score": data.certainty_score,
        "VAR_review": var_flag,
        "reason": reason
    }

    # Save decision log
    logs = load_decision_logs()
    logs.append(entry)
    save_decision_logs(logs)

    logger.info(f"Decision logged with reason: {reason}")
    return {"status": "Success", "message": "Decision processed", "reason": reason}


# Endpoint: VAR Manual Override
@router.post("/var_review")
def apply_var_override(data: VAROverrideInput):
    logs = load_decision_logs()
    for decision in reversed(logs):  # Search latest first
        if decision["frame"] == data.frame:
            decision["final_decision"] = data.override_decision
            decision["VAR_review"] = True
            save_decision_logs(logs)
            logger.info(f"VAR Override Applied: {data.override_decision}")
            return {"status": "Success", "message": "VAR override updated"}
    return {"status": "Error", "message": "Frame not found"}


# Endpoint: Fetch Logs
@router.get("/decision_logs")
def get_logs():
    logger.info("Decision logs fetched")
    return load_decision_logs()




