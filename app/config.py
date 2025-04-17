from pydantic import BaseSettings
from pathlib import Path
from typing import Optional
import os

class Settings(BaseSettings):
    # Core Settings
    MODEL_DIR: Path = Path("models")
    STORAGE_DIR: Path = Path("storage")
    LOG_DIR: Path = Path("logs")
    
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SOCKET_TIMEOUT: int = 5
    REDIS_RETRY_ON_TIMEOUT: bool = True
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    WORKERS: int = 4
    
    # Model Settings
    MODEL_BATCH_SIZE: int = 32
    MODEL_CONFIDENCE_THRESHOLD: float = 0.5
    MODEL_DEVICE: str = "cuda"  # or "cpu"
    
    # Storage Settings
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB
    SUPPORTED_FORMATS: list = [".mp4", ".avi"]
    UPLOAD_DIR: Path = Path("uploads")
    
    # Monitoring Settings
    MONITORING_PORT: int = 8001
    METRICS_INTERVAL: int = 15  # seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_directories()
        
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        for dir_path in [self.MODEL_DIR, self.STORAGE_DIR, self.LOG_DIR, self.UPLOAD_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    @property
    def redis_url(self) -> str:
        """Get Redis connection URL"""
        auth = f":{self.REDIS_PASSWORD}@" if self.REDIS_PASSWORD else ""
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        
    @property
    def model_paths(self) -> dict:
        """Get paths to model files"""
        return {
            "faster_rcnn": self.MODEL_DIR / "faster_rcnn.pth",
            "keypoint_rcnn": self.MODEL_DIR / "keypoint_rcnn.pth"
        }
        
    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.DEBUG
        
    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.DEBUG 