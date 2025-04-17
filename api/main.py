from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import os
import time
from typing import Callable
from api.routers import simulated_outputs
from api.utils.logger import logger
from api.config import settings

# --- Logging Configuration ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --- Create FastAPI App ---
app = FastAPI(
    title="Raasid Handball Detection API",
    description="API for automated handball detection in football matches",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# --- Middleware ---
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Trusted hosts
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# --- Request Logging Middleware ---
@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} Path: {request.url.path} "
        f"Status: {response.status_code} Time: {process_time:.2f}s"
    )
    return response

# --- Error Handling ---
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred"}
    )

# --- Mount Routers ---
from api.routers import ai_endpoints, base, decision, output

app.include_router(ai_endpoints.router, prefix="/api/v1")
app.include_router(base.router, prefix="/api/v1")
app.include_router(decision.router, prefix="/api/v1")
app.include_router(output.router, prefix="/api/v1")
app.include_router(simulated_outputs.router, prefix="/api/v1")

# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
