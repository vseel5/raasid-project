import unittest
import os
import numpy as np
import torch
import cv2
from app.model_manager import ModelManager

class DummyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = torch.nn.Conv2d(3, 1, 3)
    
    def forward(self, x):
        return self.conv(x)

class TestModelManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.model_manager = ModelManager()
        
        # Create a test image (black background with a white rectangle)
        cls.test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(cls.test_frame, (100, 100), (200, 200), (255, 255, 255), -1)
    
    def test_model_loading(self):
        """Test that models are loaded correctly."""
        self.assertIn('object_detection', self.model_manager.models)
        self.assertIn('pose_estimation', self.model_manager.models)
    
    def test_preprocess_frame(self):
        """Test frame preprocessing."""
        processed = self.model_manager.preprocess_frame(self.test_frame)
        
        # Check tensor shape and properties
        self.assertEqual(len(processed.shape), 4)  # [batch, channels, height, width]
        self.assertEqual(processed.shape[0], 1)    # batch size
        self.assertEqual(processed.shape[1], 3)    # channels (RGB)
        self.assertTrue(torch.is_tensor(processed))
        self.assertEqual(processed.device, self.model_manager.device)
    
    def test_detect_objects(self):
        """Test object detection."""
        results = self.model_manager.detect_objects(self.test_frame)
        
        # Check result structure
        self.assertIn('boxes', results)
        self.assertIn('scores', results)
        self.assertIn('labels', results)
        
        # Check data types
        self.assertIsInstance(results['boxes'], list)
        self.assertIsInstance(results['scores'], list)
        self.assertIsInstance(results['labels'], list)
    
    def test_estimate_poses(self):
        """Test pose estimation."""
        results = self.model_manager.estimate_poses(self.test_frame)
        
        # Check result structure
        self.assertIn('keypoints', results)
        self.assertIn('scores', results)
        
        # Check data types
        self.assertIsInstance(results['keypoints'], list)
        self.assertIsInstance(results['scores'], list)
    
    def test_analyze_frame(self):
        """Test complete frame analysis."""
        results = self.model_manager.analyze_frame(self.test_frame)
        
        # Check result structure
        self.assertIn('objects', results)
        self.assertIn('poses', results)
        self.assertIn('timestamp', results)
        
        # Check objects result
        self.assertIn('boxes', results['objects'])
        self.assertIn('scores', results['objects'])
        self.assertIn('labels', results['objects'])
        
        # Check poses result
        self.assertIn('keypoints', results['poses'])
        self.assertIn('scores', results['poses'])
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        cls.model_manager.cleanup()

if __name__ == '__main__':
    unittest.main() 