from fastapi import APIRouter
import logging

router = APIRouter()

@router.get("/")
def root():
    logging.info("Health check: API is running")
    return {"message": "Raasid API is running"}



