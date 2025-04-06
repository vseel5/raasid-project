from fastapi import APIRouter, HTTPException, status
from api.utils.logger import logger
from api.utils.storage import load_decision_logs
from api.simulations.output_delivery import deliver_decision_to_all_endpoints
from api.models.schemas import OutputDistributionResponse

router = APIRouter()

@router.post(
    "/output_distribution",
    response_model=OutputDistributionResponse,
    status_code=status.HTTP_200_OK
)
def distribute_decision():
    """
    Distributes the latest decision to all output endpoints
    (e.g., smartwatch, TV broadcast, cloud storage),
    and returns metadata including UUID and report path.
    """
    try:
        decisions = load_decision_logs()

        if not decisions:
            logger.warning("No decisions found to distribute.")
            raise HTTPException(
                status_code=404,
                detail="No decisions available for distribution"
            )

        latest_decision = decisions[-1]
        logger.info("Distributing latest decision to all systems")

        delivery_metadata = deliver_decision_to_all_endpoints(latest_decision)

        return OutputDistributionResponse(
            status="Success",
            message="Decision distributed to all endpoints",
            decision=latest_decision,
            distribution_id=delivery_metadata["distribution_id"],
            timestamp=delivery_metadata["timestamp"],
            report_path=delivery_metadata.get("report_path"),
            delivered_to=delivery_metadata["delivered_to"]
        )

    except Exception as e:
        logger.exception("Distribution failed due to internal error.")
        raise HTTPException(
            status_code=500,
            detail="Failed to distribute decision"
        )
