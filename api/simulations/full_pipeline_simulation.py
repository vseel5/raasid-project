import logging
import time
import random
import cv2
import asyncio
from typing import Optional, Tuple, Dict, Any, AsyncGenerator, List
import numpy as np
from pydantic import BaseModel, Field
from datetime import datetime
from contextlib import asynccontextmanager
from api.simulations.components.pose_estimation import capture_video_and_send_for_pose_estimation
from api.simulations.components.ball_contact import send_ball_contact_data
from api.simulations.components.event_context import send_event_context_data
from api.utils.storage import load_decision_logs, save_decision_logs
from api.utils.logger import logger
from api.routers.decision import log_decision
from api.config import settings
from api.utils.metrics import metrics_tracker, ProcessingMetrics

# --- Custom Exceptions ---
class SimulationError(Exception):
    """Base exception for simulation errors"""
    pass

class FrameProcessingError(SimulationError):
    """Exception raised when frame processing fails"""
    pass

class VideoCaptureError(SimulationError):
    """Exception raised when video capture fails"""
    pass

# --- Data Models ---
class FrameData(BaseModel):
    frame_number: int = Field(..., description="Frame number in the video sequence")
    frame: np.ndarray = Field(..., description="Frame data as numpy array")
    timestamp: float = Field(..., description="Timestamp of frame capture")
    
    class Config:
        arbitrary_types_allowed = True

class ProcessingResult(BaseModel):
    frame_number: int = Field(..., description="Frame number in the video sequence")
    pose_data: Dict[str, Any] = Field(..., description="Pose estimation results")
    ball_contact_data: Dict[str, Any] = Field(..., description="Ball contact detection results")
    event_context_data: Dict[str, Any] = Field(..., description="Event context analysis results")
    certainty_score: float = Field(..., ge=0, le=100, description="Certainty score of the decision")
    var_review_status: bool = Field(..., description="Whether VAR review is required")

# --- Resource Management ---
@asynccontextmanager
async def video_capture_context(video_path: str):
    """Context manager for video capture with proper resource cleanup"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise VideoCaptureError(f"Could not open video stream: {video_path}")
    try:
        yield cap
    finally:
        cap.release()

# --- Helper Function for Frame Processing ---
async def process_frame(frame_data: FrameData) -> ProcessingResult:
    """
    Process a single video frame with comprehensive error handling and performance tracking.
    
    Args:
        frame_data: Frame data containing frame number and frame array
        
    Returns:
        ProcessingResult containing all analysis results
        
    Raises:
        FrameProcessingError: If any step in the processing pipeline fails
    """
    logger.info(f"Processing frame {frame_data.frame_number}")
    start_time = time.time()
    metrics = {}

    try:
        # Step 1: Process Pose Estimation
        pose_start_time = time.time()
        pose_data = await capture_video_and_send_for_pose_estimation()
        metrics['pose_time'] = time.time() - pose_start_time

        # Step 2: Parallel Processing of Ball Contact and Event Context
        async with asyncio.TaskGroup() as tg:
            ball_contact_task = tg.create_task(send_ball_contact_data())
            event_context_task = tg.create_task(send_event_context_data())
            
            ball_contact_data, event_context_data = await asyncio.gather(
                ball_contact_task,
                event_context_task,
                return_exceptions=True
            )
            
            metrics['ball_contact_time'] = time.time() - pose_start_time
            metrics['event_context_time'] = time.time() - pose_start_time

        # Step 3: Decision Making with Confidence Scoring
        certainty_score = random.uniform(85, 100)
        var_review_status = certainty_score < 95

        # Create and validate processing result
        result = ProcessingResult(
            frame_number=frame_data.frame_number,
            pose_data=pose_data,
            ball_contact_data=ball_contact_data,
            event_context_data=event_context_data,
            certainty_score=certainty_score,
            var_review_status=var_review_status
        )

        # Log decision and track metrics
        await log_decision(
            frame_number=frame_data.frame_number,
            hand_position="unnatural",
            certainty_score=certainty_score,
            var_review_status=var_review_status
        )

        if settings.ENABLE_METRICS:
            metrics_tracker.add_metric(ProcessingMetrics(
                frame_number=frame_data.frame_number,
                processing_time=time.time() - start_time,
                pose_estimation_time=metrics['pose_time'],
                ball_contact_time=metrics['ball_contact_time'],
                event_context_time=metrics['event_context_time'],
                certainty_score=certainty_score,
                var_review_status=var_review_status,
                timestamp=datetime.now()
            ))

        logger.info(f"Frame {frame_data.frame_number} processed successfully")
        return result

    except Exception as e:
        logger.error(f"Error processing frame {frame_data.frame_number}: {str(e)}")
        raise FrameProcessingError(f"Failed to process frame {frame_data.frame_number}: {str(e)}")

# --- Frame Generator with Resource Management ---
async def frame_generator(
    video_path: str,
    skip_frames: int = 5
) -> AsyncGenerator[FrameData, None]:
    """
    Generate frames from video file with proper resource management.
    
    Args:
        video_path: Path to the video file
        skip_frames: Number of frames to skip between processing
        
    Yields:
        FrameData objects containing frame information
        
    Raises:
        VideoCaptureError: If video capture fails
    """
    async with video_capture_context(video_path) as cap:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                logger.info("End of video reached")
                break

            if frame_count % skip_frames == 0:
                yield FrameData(
                    frame_number=frame_count,
                    frame=frame,
                    timestamp=time.time()
                )

            frame_count += 1

# --- Batch Processing Helper ---
async def process_batch(batch: List[FrameData]) -> List[ProcessingResult]:
    """
    Process a batch of frames in parallel with error handling.
    
    Args:
        batch: List of FrameData objects to process
        
    Returns:
        List of ProcessingResult objects
        
    Raises:
        FrameProcessingError: If batch processing fails
    """
    try:
        return await asyncio.gather(*[process_frame(fd) for fd in batch])
    except Exception as e:
        logger.error(f"Error processing batch: {str(e)}")
        raise FrameProcessingError(f"Batch processing failed: {str(e)}")

# --- Full Simulation Helper ---
async def full_system_simulation(
    video_path: str = settings.DEFAULT_VIDEO_PATH,
    max_frames: int = settings.MAX_FRAMES,
    skip_frames: int = settings.SKIP_FRAMES,
    batch_size: int = settings.BATCH_SIZE
) -> None:
    """
    Run the full system simulation with comprehensive error handling and resource management.
    
    Args:
        video_path: Path to the video file
        max_frames: Maximum number of frames to process
        skip_frames: Number of frames to skip between processing
        batch_size: Number of frames to process in parallel
        
    Raises:
        SimulationError: If simulation fails
    """
    try:
        if settings.ENABLE_METRICS:
            metrics_tracker.reset()
            metrics_tracker.start_batch()
        
        frame_gen = frame_generator(video_path, skip_frames)
        batch = []
        processed_frames = 0
        
        async for frame_data in frame_gen:
            if len(batch) >= batch_size:
                await process_batch(batch)
                processed_frames += len(batch)
                
                if settings.ENABLE_METRICS and processed_frames % settings.METRICS_SAVE_INTERVAL == 0:
                    metrics_tracker.save_metrics()
                    metrics_tracker.reset()
                    metrics_tracker.start_batch()
                
                batch = []
            
            batch.append(frame_data)
            
            if processed_frames + len(batch) >= max_frames:
                logger.info("Reached max frame count")
                break

        if batch:
            await process_batch(batch)
            if settings.ENABLE_METRICS:
                metrics_tracker.save_metrics()

    except Exception as e:
        logger.error(f"Simulation error: {str(e)}")
        raise SimulationError(f"Simulation failed: {str(e)}")
    finally:
        if settings.ENABLE_METRICS:
            metrics_tracker.save_metrics()

# --- Run Full System Simulation ---
if __name__ == "__main__":
    try:
        asyncio.run(full_system_simulation())
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise
