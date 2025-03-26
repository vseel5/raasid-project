from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging, os

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(title="Raasid Handball Detection API")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
from api.routers import ai_endpoints, base, decision, output

app.include_router(ai_endpoints.router)
app.include_router(base.router)
app.include_router(decision.router)
app.include_router(output.router)
