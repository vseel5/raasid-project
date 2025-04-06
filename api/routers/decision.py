from fastapi import APIRouter, HTTPException, status
from api.models.schemas import FinalDecisionInput, VAROverrideInput
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger

router = APIRouter()


@router.post("/decision_making_ai", status_code=status.HTTP_200_OK)
def decision_making(data: FinalDecisionInput):
    """
    Endpoint to simulate AI-driven final decision-making.
    Logs the decision, applies VAR review logic, and provides reasoning.
    """
    try:
        logger.info("Decision Making Request: %s", data.json())

        reason = data.reason or (
            "Uncertain decision — confidence below 95%" if data.certainty_score < 95 else
            "Ball contacted unnatural hand position" if data.final_decision.lower() == "handball violation" else
            "Hand position judged natural; no violation"
        )

        var_flag = data.VAR_review or data.certainty_score < 95

        entry = {
            "frame": data.frame,
            "final_decision": data.final_decision,
            "certainty_score": data.certainty_score,
            "VAR_review": var_flag,
            "reason": reason
        }

        logs = load_decision_logs()
        logs.append(entry)
        save_decision_logs(logs)

        logger.info("Decision Logged: %s", entry)
        return {"status": "Success", "message": "Decision processed", "reason": reason}

    except Exception as e:
        logger.exception("Decision Processing Failed")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/var_review", status_code=status.HTTP_200_OK)
def apply_var_override(data: VAROverrideInput):
    """
    Endpoint to allow manual VAR override of a decision.
    """
    try:
        logs = load_decision_logs()
        for decision in reversed(logs):
            if decision["frame"] == data.frame:
                decision["final_decision"] = data.override_decision
                decision["VAR_review"] = True
                save_decision_logs(logs)
                logger.info("VAR Override Applied: Frame %s -> %s", data.frame, data.override_decision)
                return {"status": "Success", "message": "VAR override updated"}

        logger.warning("Frame not found for VAR Override: %s", data.frame)
        raise HTTPException(status_code=404, detail="Frame not found")

    except Exception as e:
        logger.exception("VAR Override Failed")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/decision_logs", status_code=status.HTTP_200_OK)
def get_logs():
    """
    Endpoint to fetch all decision logs.
    """
    try:
        logs = load_decision_logs()
        logger.info("Fetched %d decision logs", len(logs))
        return logs
    except Exception as e:
        logger.exception("Fetching Decision Logs Failed")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


