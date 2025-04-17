import os
from pathlib import Path

# Test environment settings
TEST_ENV = os.getenv("TEST_ENV", "local")

# Base paths
BASE_DIR = Path(__file__).parent.parent
TEST_DATA_DIR = BASE_DIR / "tests" / "data"
TEST_LOGS_DIR = BASE_DIR / "tests" / "logs"

# Create necessary directories
os.makedirs(TEST_DATA_DIR, exist_ok=True)
os.makedirs(TEST_LOGS_DIR, exist_ok=True)

# Test database settings
TEST_DB_SETTINGS = {
    "local": {
        "host": "localhost",
        "port": 5432,
        "database": "raasid_test",
        "user": "postgres",
        "password": "postgres"
    },
    "docker": {
        "host": "postgres",
        "port": 5432,
        "database": "raasid_test",
        "user": "postgres",
        "password": "postgres"
    }
}

# API test settings
API_TEST_SETTINGS = {
    "base_url": "http://localhost:8000",
    "timeout": 10,
    "retry_count": 3,
    "retry_delay": 1,
    "max_retry_delay": 5
}

# Model test settings
MODEL_TEST_SETTINGS = {
    "test_model_path": TEST_DATA_DIR / "models",
    "test_data_path": TEST_DATA_DIR / "test_videos",
    "batch_size": 4
}

# Logging settings
TEST_LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": TEST_LOGS_DIR / "test.log",
            "level": "DEBUG",
            "formatter": "standard"
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}

# Test data settings
TEST_DATA = {
    "video_samples": [
        "test_handball_1.mp4",
        "test_handball_2.mp4",
        "test_no_handball_1.mp4"
    ],
    "model_samples": [
        "pose_detection_model.pt",
        "ball_detection_model.pt"
    ]
}

# Get current environment settings
def get_db_settings():
    return TEST_DB_SETTINGS[TEST_ENV]

def get_api_settings():
    return API_TEST_SETTINGS

def get_model_settings():
    return MODEL_TEST_SETTINGS

def get_logging_config():
    return TEST_LOGGING

def get_test_data():
    return TEST_DATA 