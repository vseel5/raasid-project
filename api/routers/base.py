from fastapi import APIRouter, status
from api.utils.logger import logger

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint for Raasid API.
    """
    logger.info("Health check: API is running")
    return {"status": "OK", "message": "Raasid API is running"}


