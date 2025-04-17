import unittest
import time
import requests
import psutil
import os
import logging
from concurrent.futures import ThreadPoolExecutor

class TestPerformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        cls.logger = logging.getLogger(cls.__name__)
        
        # API settings
        cls.BASE_URL = "http://localhost:8000"
        cls.API_LATENCY_THRESHOLD = 2.5  # seconds
        
        # Create test video file
        cls.test_video_path = os.path.join(os.path.dirname(__file__), "test_video.mp4")
        with open(cls.test_video_path, "wb") as f:
            f.write(b"0" * 1024 * 1024)  # 1MB dummy video file
        
        # In-memory cache for testing
        cls.cache = {}
        
        # Resource monitoring thresholds
        cls.CPU_THRESHOLD = 80.0  # percentage
        cls.MEMORY_THRESHOLD = 80.0  # percentage

    @classmethod
    def tearDownClass(cls):
        # Clean up test video file
        if os.path.exists(cls.test_video_path):
            os.remove(cls.test_video_path)
        
        # Clear cache
        cls.cache.clear()

    def setUp(self):
        self.logger.info(f"Starting test: {self._testMethodName}")

    def tearDown(self):
        self.logger.info(f"Completed test: {self._testMethodName}")

    def test_api_latency(self):
        """Test API endpoint latency."""
        start_time = time.time()
        response = requests.get(f"{self.BASE_URL}/health")
        latency = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(latency, self.API_LATENCY_THRESHOLD,
                       f"API latency {latency:.3f}s exceeds threshold {self.API_LATENCY_THRESHOLD}s")

    def test_concurrent_requests(self):
        """Test system performance under concurrent load."""
        def make_request():
            return requests.get(f"{self.BASE_URL}/health")

        with ThreadPoolExecutor(max_workers=10) as executor:
            responses = list(executor.map(lambda _: make_request(), range(10)))

        for response in responses:
            self.assertEqual(response.status_code, 200)

    def simulate_work(self):
        """Simulate some CPU-intensive work."""
        result = 0
        for i in range(1000000):
            result += i
        return result

    def test_cache_performance(self):
        """Test in-memory cache performance."""
        test_key = "test_key"
        test_value = "test_value"
        
        # First request (cache miss)
        start_time = time.time()
        value = self.cache.get(test_key)
        if not value:
            # Simulate work needed to generate the value
            value = self.simulate_work()
            self.cache[test_key] = value
        latency1 = time.time() - start_time
        
        # Second request (cache hit)
        time.sleep(0.1)  # Small delay to ensure distinct measurements
        start_time = time.time()
        value = self.cache.get(test_key)
        latency2 = time.time() - start_time
        
        self.assertIsNotNone(value)
        self.assertLess(latency2, latency1,
                       f"Cache hit latency {latency2:.3f}s not faster than cache miss {latency1:.3f}s")

    def test_video_processing_performance(self):
        """Test video processing performance."""
        # Upload video
        with open(self.test_video_path, 'rb') as video_file:
            files = {'video': ('test_video.mp4', video_file, 'video/mp4')}
            start_time = time.time()
            response = requests.post(f"{self.BASE_URL}/upload", files=files)
            upload_time = time.time() - start_time

        self.assertEqual(response.status_code, 200)
        self.assertLess(upload_time, 5.0, f"Video upload took {upload_time:.3f}s")

    def test_system_resources(self):
        """Test system resource usage."""
        # Measure baseline
        initial_cpu = psutil.cpu_percent(interval=1)
        initial_memory = psutil.virtual_memory().percent

        # Make some API requests
        for _ in range(5):
            requests.get(f"{self.BASE_URL}/health")

        # Measure after load
        final_cpu = psutil.cpu_percent(interval=1)
        final_memory = psutil.virtual_memory().percent

        self.assertLess(final_cpu, self.CPU_THRESHOLD,
                       f"CPU usage {final_cpu}% exceeds threshold {self.CPU_THRESHOLD}%")
        self.assertLess(final_memory, self.MEMORY_THRESHOLD,
                       f"Memory usage {final_memory}% exceeds threshold {self.MEMORY_THRESHOLD}%")

if __name__ == '__main__':
    unittest.main() 