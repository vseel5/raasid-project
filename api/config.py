from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    API_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Security Settings
    ALLOWED_ORIGINS: List[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:8000"
    ).split(",")
    
    ALLOWED_HOSTS: List[str] = os.getenv(
        "ALLOWED_HOSTS",
        "localhost,127.0.0.1"
    ).split(",")
    
    # Storage Settings
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "raasid-decision-logs-bucket")
    S3_KEY: str = os.getenv("S3_KEY", "decision_logs.json")
    
    # API Settings
    POSE_API_ENDPOINT: str = os.getenv("POSE_API_ENDPOINT", "http://127.0.0.1:8000/pose_estimation")
    BALL_CONTACT_API_URL: str = os.getenv("BALL_CONTACT_API_URL", "http://127.0.0.1:8000/ball_contact_ai")
    EVENT_CONTEXT_API_URL: str = os.getenv("EVENT_CONTEXT_API_URL", "http://127.0.0.1:8000/event_context_ai")
    
    # Timeout Settings
    HTTP_TIMEOUT: float = float(os.getenv("HTTP_TIMEOUT", "10.0"))
    HTTP_CONNECT_TIMEOUT: float = float(os.getenv("HTTP_CONNECT_TIMEOUT", "5.0"))
    
    # Logging Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    
    # Simulation Settings
    DEFAULT_VIDEO_PATH: str = os.getenv("DEFAULT_VIDEO_PATH", "E:/test_raasid/accidental-handball-video.mp4")
    MAX_FRAMES: int = int(os.getenv("MAX_FRAMES", "500"))
    SKIP_FRAMES: int = int(os.getenv("SKIP_FRAMES", "5"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "10"))
    
    # Performance Settings
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "4"))
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1024"))
    
    # Metrics Settings
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "True").lower() == "true"
    METRICS_SAVE_INTERVAL: int = int(os.getenv("METRICS_SAVE_INTERVAL", "100"))
    METRICS_FILE: str = os.getenv("METRICS_FILE", "processing_metrics.json")
    
    # Decision Making Settings
    VAR_REVIEW_THRESHOLD: float = float(os.getenv("VAR_REVIEW_THRESHOLD", "95.0"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings() 