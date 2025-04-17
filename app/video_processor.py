import cv2
import numpy as np
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple, Callable
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import psutil
import gc

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = None
        self._initialize_video()
        
        # Processing settings
        self.frame_skip = max(1, int(self.fps / 10))  # Process 10 frames per second
        self.motion_threshold = 25
        self.edge_threshold1 = 100
        self.edge_threshold2 = 200
        
        # Resource monitoring
        self.max_memory_usage = 0
        self.start_time = time.time()
        
        # Initialize background subtractor for motion detection
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500,
            detectShadows=False
        )
        
        logger.info(f"Initialized video processor for {video_path}")
        logger.info(f"Video properties: {self.total_frames} frames, {self.fps} fps, {self.width}x{self.height}")

    def _initialize_video(self):
        """Initialize video capture and validate video properties."""
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                raise ValueError(f"Could not open video file: {self.video_path}")
            
            # Video properties
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            if self.total_frames <= 0:
                raise ValueError("Invalid video: No frames detected")
            if self.fps <= 0:
                raise ValueError("Invalid video: Invalid frame rate")
                
        except Exception as e:
            self.cleanup()
            raise ValueError(f"Error initializing video: {str(e)}")

    def _monitor_resources(self):
        """Monitor and log resource usage."""
        process = psutil.Process()
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        self.max_memory_usage = max(self.max_memory_usage, memory_usage)
        
        if memory_usage > 1000:  # If memory usage exceeds 1GB
            logger.warning(f"High memory usage detected: {memory_usage:.2f}MB")
            gc.collect()  # Trigger garbage collection

    def process_frame(self, frame: np.ndarray, frame_number: int) -> Dict[str, Any]:
        """Process a single video frame and extract features."""
        try:
            # Monitor resources
            self._monitor_resources()
            
            # Convert to grayscale for processing
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Edge detection
            edges = cv2.Canny(blurred, self.edge_threshold1, self.edge_threshold2)
            
            # Motion detection
            fg_mask = self.bg_subtractor.apply(blurred)
            motion_area = np.sum(fg_mask > 0) / (self.width * self.height)
            
            # Calculate frame statistics
            frame_stats = {
                "frame_number": frame_number,
                "timestamp": frame_number / self.fps,
                "motion_intensity": float(motion_area),
                "edge_density": float(np.sum(edges > 0) / (self.width * self.height)),
                "brightness": float(np.mean(gray)),
                "contrast": float(np.std(gray))
            }
            
            return frame_stats
            
        except Exception as e:
            logger.error(f"Error processing frame {frame_number}: {str(e)}")
            return {
                "frame_number": frame_number,
                "error": str(e)
            }

    def process_video(self, progress_callback: Optional[Callable[[float], None]] = None) -> Dict[str, Any]:
        """Process the entire video and return analysis results."""
        results = {
            "video_info": {
                "total_frames": self.total_frames,
                "fps": self.fps,
                "duration": self.duration,
                "resolution": f"{self.width}x{self.height}",
                "start_time": datetime.now().isoformat()
            },
            "frame_analyses": [],
            "summary": {
                "total_motion": 0.0,
                "average_motion": 0.0,
                "motion_peaks": [],
                "processing_duration": 0.0,
                "max_memory_usage": 0.0,
                "frames_processed": 0
            }
        }

        try:
            frame_count = 0
            motion_values = []
            processed_frames = 0

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = []
                
                while self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if not ret:
                        break
                    
                    if frame_count % self.frame_skip == 0:
                        future = executor.submit(self.process_frame, frame, frame_count)
                        futures.append(future)
                        processed_frames += 1
                    
                    frame_count += 1
                    
                    # Update progress
                    if progress_callback:
                        progress = (frame_count / self.total_frames) * 100
                        progress_callback(progress)

                # Collect results from futures
                for future in as_completed(futures):
                    frame_result = future.result()
                    results["frame_analyses"].append(frame_result)
                    if "motion_intensity" in frame_result:
                        motion_values.append(frame_result["motion_intensity"])

            # Calculate summary statistics
            if motion_values:
                results["summary"]["total_motion"] = float(sum(motion_values))
                results["summary"]["average_motion"] = float(np.mean(motion_values))
                
                # Find motion peaks (frames with motion intensity > 2 * average)
                threshold = 2 * results["summary"]["average_motion"]
                peaks = [i for i, m in enumerate(motion_values) if m > threshold]
                results["summary"]["motion_peaks"] = peaks

            results["summary"]["processing_duration"] = time.time() - self.start_time
            results["summary"]["max_memory_usage"] = self.max_memory_usage
            results["summary"]["frames_processed"] = processed_frames
            results["video_info"]["end_time"] = datetime.now().isoformat()

            logger.info(f"Completed video processing: {processed_frames} frames analyzed")
            return results

        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise
        finally:
            self.cleanup()

    def get_video_thumbnail(self, frame_number: int = 0) -> Optional[np.ndarray]:
        """Extract a thumbnail from the video."""
        try:
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(self.video_path)
            
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.cap.read()
            if ret:
                return frame
            return None
        except Exception as e:
            logger.error(f"Error extracting thumbnail: {str(e)}")
            return None

    def cleanup(self):
        """Clean up resources."""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.cap = None
        gc.collect()  # Force garbage collection

    def __del__(self):
        """Ensure resources are cleaned up when object is destroyed."""
        self.cleanup() 