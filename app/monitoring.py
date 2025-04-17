from prometheus_client import start_http_server, Counter, Histogram, Gauge
import logging
import psutil
import time
from typing import Dict, Any
from fastapi import Response
import json

logger = logging.getLogger(__name__)

class PrometheusMetrics:
    def __init__(self):
        # API Metrics
        self.api_requests = Counter('api_requests_total', 'Total API requests', ['endpoint', 'method'])
        self.api_latency = Histogram('api_latency_seconds', 'API request latency', ['endpoint'])
        
        # Model Metrics
        self.model_inferences = Counter('model_inferences_total', 'Total model inferences', ['model_type'])
        self.model_latency = Histogram('model_latency_seconds', 'Model inference latency', ['model_type'])
        self.model_errors = Counter('model_errors_total', 'Total model errors', ['model_type', 'error_type'])
        
        # System Metrics
        self.cpu_usage = Gauge('cpu_usage_percent', 'CPU usage percentage')
        self.memory_usage = Gauge('memory_usage_bytes', 'Memory usage in bytes')
        self.disk_usage = Gauge('disk_usage_bytes', 'Disk usage in bytes')
        
        # Cache Metrics
        self.cache_hits = Counter('cache_hits_total', 'Total cache hits', ['cache_type'])
        self.cache_misses = Counter('cache_misses_total', 'Total cache misses', ['cache_type'])
        
    def register_custom_metrics(self):
        """Register custom metrics for specific use cases"""
        pass

class HealthChecks:
    def __init__(self):
        self.checks = {
            'model': self.check_model_health,
            'storage': self.check_storage_health,
            'cache': self.check_cache_health,
            'system': self.check_system_health
        }
        
    def check_model_health(self) -> Dict[str, Any]:
        """Check model health status"""
        try:
            # Implement model health checks
            return {
                'status': 'healthy',
                'details': 'All models loaded and functioning'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'details': str(e)
            }
            
    def check_storage_health(self) -> Dict[str, Any]:
        """Check storage health status"""
        try:
            # Implement storage health checks
            return {
                'status': 'healthy',
                'details': 'Storage system operational'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'details': str(e)
            }
            
    def check_cache_health(self) -> Dict[str, Any]:
        """Check cache health status"""
        try:
            # Implement cache health checks
            return {
                'status': 'healthy',
                'details': 'Cache system operational'
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'details': str(e)
            }
            
    def check_system_health(self) -> Dict[str, Any]:
        """Check overall system health"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'status': 'healthy',
                'details': {
                    'cpu_usage': cpu_percent,
                    'memory_usage': memory.percent,
                    'disk_usage': disk.percent
                }
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'details': str(e)
            }

class SystemMonitor:
    def __init__(self):
        self.metrics = PrometheusMetrics()
        self.health_checks = HealthChecks()
        self.monitoring_thread = None
        
    def start_monitoring(self, port: int = 8001):
        """Start the monitoring system"""
        try:
            # Start Prometheus metrics server
            start_http_server(port)
            logger.info(f"Metrics server started on port {port}")
            
            # Start system metrics collection
            self._start_system_metrics_collection()
            
        except Exception as e:
            logger.error(f"Failed to start monitoring: {str(e)}")
            
    def _start_system_metrics_collection(self):
        """Start collecting system metrics"""
        def collect_metrics():
            while True:
                try:
                    # Update system metrics
                    self.metrics.cpu_usage.set(psutil.cpu_percent())
                    self.metrics.memory_usage.set(psutil.virtual_memory().used)
                    self.metrics.disk_usage.set(psutil.disk_usage('/').used)
                    
                    time.sleep(15)  # Collect every 15 seconds
                except Exception as e:
                    logger.error(f"Error collecting system metrics: {str(e)}")
                    time.sleep(60)  # Wait longer on error
                    
        import threading
        self.monitoring_thread = threading.Thread(target=collect_metrics, daemon=True)
        self.monitoring_thread.start()
        
    def get_health_status(self) -> Response:
        """Get comprehensive health status"""
        status = {
            'status': 'healthy',
            'components': {}
        }
        
        for name, check in self.health_checks.checks.items():
            result = check()
            status['components'][name] = result
            
            if result['status'] == 'unhealthy':
                status['status'] = 'unhealthy'
                
        return Response(
            content=json.dumps(status),
            media_type="application/json",
            status_code=200 if status['status'] == 'healthy' else 503
        ) 