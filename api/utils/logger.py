import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional
from api.config import settings

class CustomFormatter(logging.Formatter):
    """Custom formatter for logging with colors and additional information"""
    
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt: str):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(
    name: str = "raasid",
    level: Optional[int] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Setup a logger with console and file handlers.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Path to log file
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    
    # Set level
    if level is None:
        level = getattr(logging, settings.LOG_LEVEL.upper())
    logger.setLevel(level)
    
    # Create formatters
    console_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter(console_format))
    logger.addHandler(console_handler)
    
    # File handler if log_file is provided
    if log_file:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(file_format))
        logger.addHandler(file_handler)
    
    return logger

# Create default logger instance
logger = setup_logger(
    name="raasid",
    log_file="logs/raasid.log" if not settings.DEBUG else None
)


