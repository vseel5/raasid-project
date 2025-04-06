import logging
import os
from logging.handlers import RotatingFileHandler

# --- Logging Directory Setup ---
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "server.log")
os.makedirs(LOG_DIR, exist_ok=True)

# --- Logger Configuration ---
logger = logging.getLogger("raasid")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers when re-importing
if not logger.hasHandlers():
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


