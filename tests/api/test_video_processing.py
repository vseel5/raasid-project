import unittest
import requests
import os
import time
from tests.base import BaseTest
from tests.config import get_api_settings

class TestVideoProcessing(BaseTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.api_settings = get_api_settings()
        cls.base_url = cls.api_settings['base_url']
        cls.timeout = cls.api_settings['timeout']
        cls.retry_count = cls.api_settings['retry_count']
        cls.retry_delay = cls.api_settings['retry_delay']
        
        # Create a test video file
        cls.test_video_path = os.path.join(cls.test_dirs['videos'], 'test.mp4')
        with open(cls.test_video_path, 'wb') as f:
            f.write(b'FakeMP4Header' + b'\x00' * 1024)  # 1KB dummy video file

    @classmethod
    def tearDownClass(cls):
        # Clean up test video file
        if os.path.exists(cls.test_video_path):
            os.remove(cls.test_video_path)
        super().tearDownClass()

    def _make_request(self, method, endpoint, **kwargs):
        """Helper method to make requests with retry logic."""
        for attempt in range(self.retry_count):
            try:
                response = requests.request(
                    method,
                    f"{self.base_url}{endpoint}",
                    timeout=self.timeout,
                    **kwargs
                )
                return response
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_count - 1:
                    raise
                time.sleep(self.retry_delay * (attempt + 1))

    def test_upload_video(self):
        """Test video upload endpoint."""
        with open(self.test_video_path, 'rb') as video_file:
            files = {'video': ('test.mp4', video_file, 'video/mp4')}
            response = self._make_request('POST', '/upload', files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('video_id', data['data'])
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'uploaded')

    def test_process_video(self):
        """Test video processing endpoint."""
        # First upload a video
        with open(self.test_video_path, 'rb') as video_file:
            files = {'video': ('test.mp4', video_file, 'video/mp4')}
            upload_response = self._make_request('POST', '/upload', files=files)
        video_id = upload_response.json()['data']['video_id']

        # Then process it
        response = self._make_request('POST', f'/process/{video_id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('processing_id', data['data'])
        self.assertIn('status', data['data'])
        self.assertEqual(data['data']['status'], 'processing')

    def test_get_processing_status(self):
        """Test processing status endpoint."""
        # Upload and process a video
        with open(self.test_video_path, 'rb') as video_file:
            files = {'video': ('test.mp4', video_file, 'video/mp4')}
            upload_response = self._make_request('POST', '/upload', files=files)
        video_id = upload_response.json()['data']['video_id']
        
        process_response = self._make_request('POST', f'/process/{video_id}')
        processing_id = process_response.json()['data']['processing_id']

        # Check status
        response = self._make_request('GET', f'/status/{processing_id}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assert_response(data)
        self.assertIn('status', data['data'])
        self.assertIn('progress', data['data'])

    def test_invalid_video_format(self):
        """Test handling of invalid video format."""
        # Create a non-video file
        invalid_path = os.path.join(self.test_dirs['videos'], 'invalid.txt')
        with open(invalid_path, 'w') as f:
            f.write('Not a video file')
        
        try:
            with open(invalid_path, 'rb') as video_file:
                files = {'video': ('invalid.txt', video_file, 'text/plain')}
                response = self._make_request('POST', '/upload', files=files)
            
            self.assertEqual(response.status_code, 400)
            data = response.json()
            self.assertIn('error', data)
            self.assertIn('Invalid video format', data['error'])
        finally:
            if os.path.exists(invalid_path):
                os.remove(invalid_path)

    def test_large_video_handling(self):
        """Test handling of large video files."""
        # Create a large dummy file (5MB)
        large_path = os.path.join(self.test_dirs['videos'], 'large.mp4')
        with open(large_path, 'wb') as f:
            f.write(b'FakeMP4Header' + b'\x00' * (5 * 1024 * 1024))
        
        try:
            with open(large_path, 'rb') as video_file:
                files = {'video': ('large.mp4', video_file, 'video/mp4')}
                response = self._make_request('POST', '/upload', files=files)
            
            self.assertEqual(response.status_code, 413)
            data = response.json()
            self.assertIn('error', data)
            self.assertIn('File too large', data['error'])
        finally:
            if os.path.exists(large_path):
                os.remove(large_path)

if __name__ == '__main__':
    unittest.main() 