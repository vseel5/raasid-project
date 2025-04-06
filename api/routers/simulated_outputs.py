# api/routers/simulated_outputs.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/referee_smartwatch")
async def referee_smartwatch(request: Request):
    payload = await request.json()
    print("Referee Smartwatch received:", payload)
    return JSONResponse(content={"status": "Smartwatch received"}, status_code=200)

@router.post("/tv_broadcast")
async def tv_broadcast(request: Request):
    payload = await request.json()
    print("TV Broadcast received:", payload)
    return JSONResponse(content={"status": "TV Broadcast received"}, status_code=200)

@router.post("/cloud_storage")
async def cloud_storage(request: Request):
    payload = await request.json()
    print("Cloud Storage received:", payload)
    return JSONResponse(content={"status": "Cloud Storage received"}, status_code=200)
