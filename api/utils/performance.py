import psutil
import time
from typing import Dict, Optional
from datetime import datetime
import logging
from functools import wraps
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
        self.start_time = time.time()
        
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self) -> float:
        """Get current memory usage percentage."""
        return psutil.virtual_memory().percent
    
    def get_disk_usage(self) -> float:
        """Get current disk usage percentage."""
        return psutil.disk_usage('/').percent
    
    def get_network_io(self) -> Dict:
        """Get network I/O statistics."""
        io = psutil.net_io_counters()
        return {
            'bytes_sent': io.bytes_sent,
            'bytes_recv': io.bytes_recv,
            'packets_sent': io.packets_sent,
            'packets_recv': io.packets_recv
        }
    
    def get_process_metrics(self) -> Dict:
        """Get metrics for the current process."""
        process = psutil.Process()
        return {
            'cpu_percent': process.cpu_percent(),
            'memory_percent': process.memory_percent(),
            'num_threads': process.num_threads(),
            'num_fds': process.num_fds() if hasattr(process, 'num_fds') else None
        }
    
    def collect_metrics(self) -> Dict:
        """Collect all system metrics."""
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime': time.time() - self.start_time,
            'cpu_usage': self.get_cpu_usage(),
            'memory_usage': self.get_memory_usage(),
            'disk_usage': self.get_disk_usage(),
            'network_io': self.get_network_io(),
            'process_metrics': self.get_process_metrics()
        }
    
    def save_metrics(self, metrics: Dict, log_dir: str = 'logs'):
        """Save metrics to a JSON file."""
        try:
            log_path = Path(log_dir)
            log_path.mkdir(parents=True, exist_ok=True)
            
            metrics_file = log_path / f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(metrics_file, 'w') as f:
                json.dump(metrics, f, indent=2)
                
            logger.info(f"Performance metrics saved to {metrics_file}")
            
        except Exception as e:
            logger.error(f"Error saving performance metrics: {str(e)}")

def measure_performance(func):
    """Decorator to measure function performance."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        start_cpu = psutil.cpu_percent()
        start_memory = psutil.Process().memory_info().rss
        
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            end_cpu = psutil.cpu_percent()
            end_memory = psutil.Process().memory_info().rss
            
            performance_metrics = {
                'function': func.__name__,
                'execution_time': end_time - start_time,
                'cpu_usage': end_cpu - start_cpu,
                'memory_usage': (end_memory - start_memory) / 1024 / 1024,  # Convert to MB
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Performance metrics for {func.__name__}: {json.dumps(performance_metrics)}")
    
    return wrapper

# Create a global performance monitor instance
performance_monitor = PerformanceMonitor() 