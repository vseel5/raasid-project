import os
import json
import aiofiles
import aioboto3
from typing import List, Dict, Optional
from api.utils.logger import logger
from botocore.exceptions import NoCredentialsError, ClientError

# --- Constants ---
DATA_DIR = "data"
DECISION_LOGS_FILE = os.path.join(DATA_DIR, "decision_logs.json")
S3_BUCKET_NAME = 'raasid-decision-logs-bucket'
S3_KEY = 'decision_logs.json'

# Initialize S3 client
s3_session = aioboto3.Session()

# Local directory for fallback (for development purposes)
os.makedirs(DATA_DIR, exist_ok=True)

async def load_decision_logs() -> List[Dict]:
    """
    Load decision logs from S3. Falls back to local file if S3 is unavailable.
    
    Returns:
        List[Dict]: List of decision logs
    """
    try:
        # Try loading from S3
        logger.info("Attempting to load decision logs from S3...")
        async with s3_session.client('s3') as s3:
            response = await s3.get_object(Bucket=S3_BUCKET_NAME, Key=S3_KEY)
            async with response['Body'] as stream:
                data = await stream.read()
                logs = json.loads(data.decode('utf-8'))
                logger.info("Decision logs loaded from S3.")
                return logs
    except (NoCredentialsError, ClientError) as e:
        logger.warning(f"Failed to load from S3: {e}. Falling back to local storage.")
    
    # Fallback to loading from local storage if S3 fails
    if os.path.exists(DECISION_LOGS_FILE):
        try:
            async with aiofiles.open(DECISION_LOGS_FILE, "r") as f:
                data = await f.read()
                return json.loads(data.strip()) if data.strip() else []
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse decision log file: {e}")
            return []
        except Exception as e:
            logger.exception(f"Unexpected error while loading decision logs: {e}")
            return []

    logger.warning("Decision log file not found. Returning empty list.")
    return []

async def save_decision_logs(logs: List[Dict]) -> None:
    """
    Save decision logs to S3. Falls back to local file if S3 is unavailable.
    
    Args:
        logs: List of decision logs to save
    """
    try:
        # Try saving to S3
        logger.info("Attempting to save decision logs to S3...")
        async with s3_session.client('s3') as s3:
            await s3.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=S3_KEY,
                Body=json.dumps(logs, indent=2).encode('utf-8')
            )
            logger.info("Decision logs saved to S3.")
            return
    except (NoCredentialsError, ClientError) as e:
        logger.warning(f"Failed to save to S3: {e}. Falling back to local storage.")
    
    # Fallback to local storage if S3 fails
    try:
        async with aiofiles.open(DECISION_LOGS_FILE, "w") as f:
            await f.write(json.dumps(logs, indent=2))
        logger.info("Decision logs saved to local storage.")
    except Exception as e:
        logger.error(f"Failed to save decision logs: {e}")
        raise

