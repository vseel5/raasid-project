import unittest
import requests
import json
from tests.base import BaseTest
from tests.config import get_api_settings

class TestAIModels(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_settings = get_api_settings()
        cls.base_url = cls.api_settings['base_url']
        cls.timeout = cls.api_settings['timeout']

    def test_list_models(self):
        """Test listing available AI models."""
        response = requests.get(
            f"{self.base_url}/models",
            timeout=self.timeout
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('models', data['data'])
        self.assertIsInstance(data['data']['models'], list)
        
        # Check model structure
        if data['data']['models']:
            model = data['data']['models'][0]
            self.assertIn('id', model)
            self.assertIn('name', model)
            self.assertIn('version', model)
            self.assertIn('status', model)

    def test_model_details(self):
        """Test getting model details."""
        # First get list of models
        list_response = requests.get(
            f"{self.base_url}/models",
            timeout=self.timeout
        )
        model_id = list_response.json()['data']['models'][0]['id']

        # Get model details
        response = requests.get(
            f"{self.base_url}/models/{model_id}",
            timeout=self.timeout
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('model', data['data'])
        model = data['data']['model']
        self.assertIn('id', model)
        self.assertIn('name', model)
        self.assertIn('version', model)
        self.assertIn('status', model)
        self.assertIn('metrics', model)
        self.assertIn('last_updated', model)

    def test_model_inference(self):
        """Test model inference endpoint."""
        # First get list of models
        list_response = requests.get(
            f"{self.base_url}/models",
            timeout=self.timeout
        )
        model_id = list_response.json()['data']['models'][0]['id']

        # Prepare test data
        test_data = {
            "frame_data": "base64_encoded_frame_data",
            "parameters": {
                "confidence_threshold": 0.8,
                "max_detections": 10
            }
        }

        # Make inference request
        response = requests.post(
            f"{self.base_url}/models/{model_id}/infer",
            json=test_data,
            timeout=self.timeout
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('predictions', data['data'])
        self.assertIn('processing_time', data['data'])
        self.assertIn('model_version', data['data'])

    def test_model_metrics(self):
        """Test getting model performance metrics."""
        # First get list of models
        list_response = requests.get(
            f"{self.base_url}/models",
            timeout=self.timeout
        )
        model_id = list_response.json()['data']['models'][0]['id']

        # Get metrics
        response = requests.get(
            f"{self.base_url}/models/{model_id}/metrics",
            timeout=self.timeout
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('metrics', data['data'])
        metrics = data['data']['metrics']
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1_score', metrics)
        self.assertIn('inference_time', metrics)

    def test_invalid_model_id(self):
        """Test handling of invalid model ID."""
        response = requests.get(
            f"{self.base_url}/models/invalid_id",
            timeout=self.timeout
        )
        
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn('error', data)
        self.assertIn('Model not found', data['error'])

    def test_model_versioning(self):
        """Test model version management."""
        # First get list of models
        list_response = requests.get(
            f"{self.base_url}/models",
            timeout=self.timeout
        )
        model_id = list_response.json()['data']['models'][0]['id']

        # Get versions
        response = requests.get(
            f"{self.base_url}/models/{model_id}/versions",
            timeout=self.timeout
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('versions', data['data'])
        self.assertIsInstance(data['data']['versions'], list)
        
        # Check version structure
        if data['data']['versions']:
            version = data['data']['versions'][0]
            self.assertIn('version', version)
            self.assertIn('status', version)
            self.assertIn('created_at', version)
            self.assertIn('metrics', version)

if __name__ == '__main__':
    unittest.main() 