from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import time
from datetime import datetime
import json
import os
from pathlib import Path
import asyncio
from api.config import settings

@dataclass
class ProcessingMetrics:
    frame_number: int
    processing_time: float
    pose_estimation_time: float
    ball_contact_time: float
    event_context_time: float
    certainty_score: float
    var_review_status: bool
    timestamp: datetime
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None

class MetricsTracker:
    def __init__(self):
        self.metrics: List[ProcessingMetrics] = []
        self.start_time: Optional[float] = None
        self.current_batch_start: Optional[float] = None
        self._lock = asyncio.Lock()
        
    async def start_batch(self):
        """Start tracking a new batch of frames"""
        async with self._lock:
            self.current_batch_start = time.time()
        
    async def add_metric(self, metric: ProcessingMetrics):
        """Add a new processing metric with thread safety"""
        async with self._lock:
            self.metrics.append(metric)
        
    def get_batch_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics for the current batch"""
        if not self.metrics:
            return {}
            
        batch_metrics = {
            "total_frames": len(self.metrics),
            "avg_processing_time": sum(m.processing_time for m in self.metrics) / len(self.metrics),
            "avg_pose_time": sum(m.pose_estimation_time for m in self.metrics) / len(self.metrics),
            "avg_ball_contact_time": sum(m.ball_contact_time for m in self.metrics) / len(self.metrics),
            "avg_event_context_time": sum(m.event_context_time for m in self.metrics) / len(self.metrics),
            "avg_certainty_score": sum(m.certainty_score for m in self.metrics) / len(self.metrics),
            "var_review_count": sum(1 for m in self.metrics if m.var_review_status),
            "var_review_percentage": (sum(1 for m in self.metrics if m.var_review_status) / len(self.metrics)) * 100,
            "timestamp": datetime.now().isoformat(),
            "performance_metrics": {
                "avg_memory_usage": sum(m.memory_usage for m in self.metrics if m.memory_usage is not None) / 
                                  sum(1 for m in self.metrics if m.memory_usage is not None) if any(m.memory_usage for m in self.metrics) else None,
                "avg_cpu_usage": sum(m.cpu_usage for m in self.metrics if m.cpu_usage is not None) / 
                               sum(1 for m in self.metrics if m.cpu_usage is not None) if any(m.cpu_usage for m in self.metrics) else None
            }
        }
        return batch_metrics
        
    async def save_metrics(self):
        """Save metrics to a JSON file with proper error handling"""
        if not self.metrics:
            return
            
        try:
            # Ensure log directory exists
            log_dir = Path(settings.LOG_DIR)
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            metrics_file = log_dir / f"processing_metrics_{timestamp}.json"
            
            # Prepare metrics data
            metrics_data = {
                "batch_metrics": self.get_batch_metrics(),
                "frame_metrics": [vars(m) for m in self.metrics],
                "system_info": {
                    "python_version": os.sys.version,
                    "platform": os.sys.platform,
                    "processor": os.sys.processor if hasattr(os.sys, 'processor') else "unknown"
                }
            }
            
            # Save with proper error handling
            async with self._lock:
                with open(metrics_file, 'w') as f:
                    json.dump(metrics_data, f, default=str)
                    
            logger.info(f"Metrics saved to {metrics_file}")
            
        except Exception as e:
            logger.error(f"Error saving metrics: {str(e)}")
            raise
            
    async def reset(self):
        """Reset the metrics tracker with thread safety"""
        async with self._lock:
            self.metrics = []
            self.start_time = None
            self.current_batch_start = None

# Create a global metrics tracker instance
metrics_tracker = MetricsTracker() 