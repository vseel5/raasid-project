from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
from typing import Dict, Any, Optional
import json
import uvicorn
import os
import socket
import redis
from redis import Redis
import time
import logging
from pathlib import Path
from dotenv import load_dotenv
import sys
from pydantic import BaseModel
from .video_processor import VideoProcessor
from redis.exceptions import ConnectionError
from .storage_manager import StorageManager
from .model_manager import ModelManager
from .decision_engine import DecisionEngine
from app.config import Settings
from app.caching import CacheManager
from app.monitoring import SystemMonitor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/api.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    MAX_SIZE = int(os.getenv('MAX_FILE_SIZE', 5 * 1024 * 1024))  # 5MB default
    CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hour default
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    REDIS_SOCKET_TIMEOUT = 5
    REDIS_RETRY_ON_TIMEOUT = True
    ALLOWED_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv')
    UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR', 'uploads'))
    UPLOAD_DIR.mkdir(exist_ok=True)

    @classmethod
    def setup(cls):
        cls.UPLOAD_DIR.mkdir(exist_ok=True)

Config.setup()

# Initialize FastAPI app
app = FastAPI(
    title="Raasid API",
    version="1.0.0",
    description="AI-powered handball detection system API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('ALLOWED_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize storage
storage: Dict[str, Dict] = {}

# Initialize Redis connection
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    redis_client.ping()
    logger.info("Connected to Redis")
except redis.ConnectionError as e:
    logger.warning(f"Redis/Memurai connection failed: {str(e)}. Using in-memory storage as fallback.")
    redis_client = None

# Initialize settings
settings = Settings()

# Initialize system components with proper error handling
try:
    # Initialize model manager
    model_manager = ModelManager(
        model_dir=settings.MODEL_DIR,
        settings=settings
    )
    
    # Initialize storage manager
    storage_manager = StorageManager(settings.STORAGE_DIR)
    
    # Initialize cache manager with fallback
    try:
        cache_manager = CacheManager(settings)
    except Exception as e:
        logger.warning(f"Cache initialization failed: {str(e)}. Using in-memory fallback.")
        cache_manager = MemoryCache()
    
    # Initialize system monitor
    monitor = SystemMonitor()
    monitor.start_monitoring(settings.MONITORING_PORT)
    
except Exception as e:
    logger.error(f"System initialization failed: {str(e)}")
    raise

# In-memory storage for video processing status (fallback)
video_status: Dict[str, Dict] = {}

# In-memory storage for demo purposes
videos = {}
processes = {}
models = {
    "model1": {
        "id": "model1",
        "name": "Pose Detection Model",
        "version": "1.0.0",
        "status": "active",
        "metrics": {
            "accuracy": 0.95,
            "precision": 0.94,
            "recall": 0.93,
            "f1_score": 0.94,
            "inference_time": 0.05
        },
        "last_updated": "2024-04-17T00:00:00Z"
    },
    "model2": {
        "id": "model2",
        "name": "Ball Detection Model",
        "version": "1.0.0",
        "status": "active",
        "metrics": {
            "accuracy": 0.96,
            "precision": 0.95,
            "recall": 0.94,
            "f1_score": 0.95,
            "inference_time": 0.03
        },
        "last_updated": "2024-04-17T00:00:00Z"
    }
}

# Initialize managers
decision_engine = DecisionEngine()

def get_status(video_id: str) -> Optional[Dict]:
    """Get status from Redis/Memurai or fallback to in-memory storage."""
    if redis_client:
        try:
            status = redis_client.get(f"video_status:{video_id}")
            if status:
                return eval(status)
            return None
        except Exception as e:
            logger.error(f"Error getting status from Redis/Memurai: {str(e)}")
            return video_status.get(video_id)
    return video_status.get(video_id)

def set_status(video_id: str, status: Dict):
    """Set status in Redis/Memurai or fallback to in-memory storage."""
    if redis_client:
        try:
            redis_client.set(f"video_status:{video_id}", str(status))
            redis_client.expire(f"video_status:{video_id}", 3600)  # 1 hour expiry
        except Exception as e:
            logger.error(f"Error setting status in Redis/Memurai: {str(e)}")
            video_status[video_id] = status
    else:
        video_status[video_id] = status

def cache_response(key: str, data: dict, ttl: int = Config.CACHE_TTL) -> bool:
    """Cache API response."""
    redis_client = get_redis()
    if not redis_client:
        return False
    try:
        redis_client.setex(key, ttl, json.dumps(data))
        return True
    except Exception as e:
        logger.error(f"Failed to cache response: {e}")
        return False

def get_cached_response(key: str) -> Optional[dict]:
    """Get cached API response."""
    redis_client = get_redis()
    if not redis_client:
        return None
    try:
        cached = redis_client.get(key)
        return json.loads(cached) if cached else None
    except Exception as e:
        logger.error(f"Failed to get cached response: {e}")
        return None

def create_response(data: Any, status_code: int = 200, cache_key: str = None) -> JSONResponse:
    """Create a standardized API response with optional caching."""
    response = {
        "status": status_code,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if cache_key:
        cache_response(cache_key, response)
    
    return JSONResponse(content=response, status_code=status_code)

class APIError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

def create_error_response(status_code: int, message: str) -> JSONResponse:
    """Create a standardized error response"""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "error": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

def create_success_response(data: Any, status_code: int = 200) -> JSONResponse:
    """Create a standardized success response"""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests."""
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    logger.info(f"Request {request_id} completed with status {response.status_code}")
    return response

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handle custom API errors"""
    return create_error_response(exc.status_code, exc.detail)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    return create_error_response(exc.status_code, exc.detail)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler to ensure consistent error response format."""
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    # For unexpected errors, log them and return a 500
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "redis": "connected" if redis_client else "disconnected",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/version")
async def get_version():
    """Get API version information."""
    return create_response({
        "version": app.version,
        "build_date": "2024-04-17"
    })

@app.get("/models")
async def list_models():
    """List available AI models."""
    return create_response({
        "models": list(models.values())
    })

@app.get("/models/{model_id}")
async def get_model_details(model_id: str):
    """Get details of a specific model."""
    if model_id not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    return create_response({
        "model": models[model_id]
    })

@app.get("/models/{model_id}/metrics")
async def get_model_metrics(model_id: str):
    """Get performance metrics for a specific model."""
    # Try to get cached response
    cache_key = f"metrics:{model_id}"
    cached_response = get_cached_response(cache_key)
    if cached_response:
        return cached_response
    
    if model_id not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    response = create_response({
        "metrics": models[model_id]["metrics"]
    }, cache_key=cache_key)
    return response

@app.get("/models/{model_id}/versions")
async def get_model_versions(model_id: str):
    """Get version history for a specific model."""
    if model_id not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    return create_response({
        "versions": [{
            "version": models[model_id]["version"],
            "status": "active",
            "created_at": "2024-04-17T00:00:00Z",
            "metrics": models[model_id]["metrics"]
        }]
    })

@app.post("/models/{model_id}/infer")
async def model_inference(model_id: str, data: Dict):
    """Perform model inference."""
    if model_id not in models:
        raise HTTPException(status_code=404, detail="Model not found")
    
    # Simulate inference
    return create_response({
        "predictions": [
            {"label": "person", "confidence": 0.95, "bbox": [10, 10, 100, 200]},
            {"label": "ball", "confidence": 0.92, "bbox": [150, 150, 170, 170]}
        ],
        "processing_time": 0.05,
        "model_version": models[model_id]["version"]
    })

@app.post("/upload")
async def upload_video(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Upload a video file for processing."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in Config.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file format")
    
    # Generate unique video ID
    video_id = str(uuid.uuid4())
    
    try:
        # Save uploaded file temporarily
        temp_path = f"temp_{video_id}{file_ext}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            if len(content) > Config.MAX_SIZE:
                raise HTTPException(status_code=413, detail="File too large")
            buffer.write(content)
        
        # Store video and get final path
        stored_path = storage_manager.store_video(video_id, temp_path, file.filename)
        
        # Start background processing
        background_tasks.add_task(process_video_background, video_id, stored_path)
        
        return {
            "video_id": video_id,
            "status": "uploaded",
            "message": "Video uploaded successfully"
        }
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/{video_id}")
async def process_video(video_id: str):
    """Start video processing"""
    try:
        if video_id not in videos:
            raise APIError(404, "Video not found")
        
        process_id = str(uuid.uuid4())
        processes[process_id] = {
            "video_id": video_id,
            "status": "processing",
            "progress": 0,
            "start_time": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Started processing video {video_id} with process ID {process_id}")
        return create_success_response({
            "processing_id": process_id,
            "status": "processing"
        })
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing video: {str(e)}")
        raise APIError(500, "Internal server error")

@app.get("/status/{process_id}")
async def get_status(process_id: str):
    """Get processing status"""
    try:
        if process_id not in processes:
            raise APIError(404, "Process not found")
        
        return create_success_response(processes[process_id])
    except APIError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error getting status: {str(e)}")
        raise APIError(500, "Internal server error")

@app.get("/status/{video_id}")
async def get_processing_status(video_id: str):
    """Get the processing status of a video."""
    video_info = storage_manager.get_video_info(video_id)
    if not video_info:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return ProcessingStatus(
        status=video_info["status"],
        progress=video_info.get("progress"),
        result=video_info.get("processing_result"),
        error=video_info.get("error_message")
    )

def update_progress(video_id: str, progress: float):
    """Update processing progress for a video."""
    status = get_status(video_id)
    if status:
        status["progress"] = progress
        status["last_updated"] = datetime.now().isoformat()
        set_status(video_id, status)

async def process_video_background(video_id: str, file_path: str):
    """Background task to process video."""
    try:
        # Update status to processing
        storage_manager.update_status(video_id, "processing")
        
        # Process video
        processor = VideoProcessor(file_path)
        results = processor.process_video(
            lambda p: storage_manager.update_status(video_id, "processing", progress=p)
        )
        
        # Store results
        storage_manager.store_processing_result(video_id, results)
        
        # Update final status
        storage_manager.update_status(video_id, "completed")
        
        # Cleanup
        processor.cleanup()
        
    except Exception as e:
        logger.error(f"Error processing video {video_id}: {str(e)}")
        storage_manager.update_status(video_id, "failed", str(e))
        storage_manager.cleanup(video_id)

class ProcessingStatus(BaseModel):
    status: str
    progress: Optional[float] = None
    result: Optional[Dict] = None
    error: Optional[str] = None

@app.post("/api/v1/videos/upload")
async def upload_video_new(file: UploadFile = File(...)):
    """Upload a video file."""
    try:
        # Validate file type
        if not file.content_type.startswith("video/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only video files are accepted."
            )
        
        # Generate unique ID
        video_id = str(uuid.uuid4())
        
        # Save file
        file_path = f"storage/videos/{video_id}.mp4"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Store video info
        video_info = {
            "id": video_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "status": "uploaded",
            "created_at": datetime.now().isoformat()
        }
        
        if redis_client:
            redis_client.hmset(f"video:{video_id}", video_info)
        else:
            storage[video_id] = video_info
        
        return video_info
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/videos/{video_id}/process")
async def process_video_new(video_id: str, processing_type: str = "full_analysis"):
    """Process a video file."""
    try:
        # Get video info
        if redis_client:
            video_info = redis_client.hgetall(f"video:{video_id}")
            if not video_info:
                raise HTTPException(status_code=404, detail="Video not found")
        else:
            video_info = storage.get(video_id)
            if not video_info:
                raise HTTPException(status_code=404, detail="Video not found")
        
        # Generate processing ID
        processing_id = str(uuid.uuid4())
        
        # Update status
        processing_info = {
            "id": processing_id,
            "video_id": video_id,
            "type": processing_type,
            "status": "processing",
            "progress": 0.0,
            "started_at": datetime.now().isoformat()
        }
        
        if redis_client:
            redis_client.hmset(f"processing:{processing_id}", processing_info)
        else:
            storage[f"processing:{processing_id}"] = processing_info
        
        return processing_info
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/videos/{video_id}/status/{processing_id}")
async def get_processing_status_new(video_id: str, processing_id: str):
    """Get the status of a video processing job."""
    try:
        # Get processing info
        if redis_client:
            processing_info = redis_client.hgetall(f"processing:{processing_id}")
            if not processing_info:
                raise HTTPException(status_code=404, detail="Processing job not found")
        else:
            processing_info = storage.get(f"processing:{processing_id}")
            if not processing_info:
                raise HTTPException(status_code=404, detail="Processing job not found")
        
        return processing_info
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting processing status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    try:
        port = find_available_port()
        print(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Failed to start server: {e}")
        exit(1) 