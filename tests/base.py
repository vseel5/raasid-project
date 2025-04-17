import unittest
import logging
import logging.config
import os
from pathlib import Path
from typing import Any, Dict
import json
from tests.config import get_logging_config, get_test_data

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        # Configure logging
        logging.config.dictConfig(get_logging_config())
        cls.logger = logging.getLogger(cls.__name__)

        # Load test data
        cls.test_data = get_test_data()
        
        # Create test directories
        cls.setup_test_directories()

    @classmethod
    def setup_test_directories(cls):
        """Create necessary test directories."""
        base_dir = Path(__file__).parent
        cls.test_dirs = {
            'data': base_dir / 'data',
            'logs': base_dir / 'logs',
            'models': base_dir / 'data' / 'models',
            'videos': base_dir / 'data' / 'test_videos'
        }
        
        for dir_path in cls.test_dirs.values():
            os.makedirs(dir_path, exist_ok=True)

    def setUp(self):
        """Set up test case."""
        self.logger.info(f"Starting test: {self._testMethodName}")

    def tearDown(self):
        """Clean up after test case."""
        self.logger.info(f"Completed test: {self._testMethodName}")

    def assert_response(self, response: Dict[str, Any], expected_status: int = 200):
        """Assert API response format and status."""
        self.assertIn('status', response)
        self.assertEqual(response['status'], expected_status)
        self.assertIn('data', response)
        self.assertIn('timestamp', response)

    def load_test_data(self, filename: str) -> Dict:
        """Load test data from JSON file."""
        file_path = self.test_dirs['data'] / filename
        with open(file_path, 'r') as f:
            return json.load(f)

    def save_test_data(self, data: Dict, filename: str):
        """Save test data to JSON file."""
        file_path = self.test_dirs['data'] / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def get_test_video_path(self, video_name: str) -> Path:
        """Get path to test video file."""
        return self.test_dirs['videos'] / video_name

    def get_test_model_path(self, model_name: str) -> Path:
        """Get path to test model file."""
        return self.test_dirs['models'] / model_name

    def assert_file_exists(self, file_path: Path):
        """Assert that a file exists."""
        self.assertTrue(file_path.exists(), f"File not found: {file_path}")

    def assert_directory_exists(self, dir_path: Path):
        """Assert that a directory exists."""
        self.assertTrue(dir_path.exists(), f"Directory not found: {dir_path}")
        self.assertTrue(dir_path.is_dir(), f"Path is not a directory: {dir_path}")

    def assert_dict_structure(self, actual: Dict, expected: Dict):
        """Assert that dictionary has expected structure."""
        for key, value in expected.items():
            self.assertIn(key, actual, f"Missing key: {key}")
            if isinstance(value, dict):
                self.assert_dict_structure(actual[key], value)
            elif isinstance(value, list):
                self.assertIsInstance(actual[key], list)
                if value and isinstance(value[0], dict):
                    for i, item in enumerate(actual[key]):
                        self.assert_dict_structure(item, value[0]) 