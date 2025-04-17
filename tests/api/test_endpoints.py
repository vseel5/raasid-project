import unittest
import os
import json
from fastapi.testclient import TestClient
from app.main import app
import numpy as np
import cv2

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test client
        cls.client = TestClient(app)
        
        # Create test video directory
        cls.test_dir = "tests/data/videos"
        os.makedirs(cls.test_dir, exist_ok=True)
        
        # Create a test video file
        cls.test_video_path = os.path.join(cls.test_dir, "test_video.mp4")
        cls._create_test_video()

    @classmethod
    def tearDownClass(cls):
        # Clean up
        import shutil
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)

    @classmethod
    def _create_test_video(cls):
        """Create a simple test video file."""
        # Create a black frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(cls.test_video_path, fourcc, 30.0, (640, 480))
        
        # Write 30 frames (1 second of video)
        for _ in range(30):
            out.write(frame)
        out.release()

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("redis", data)
        self.assertIn("timestamp", data)

    def test_video_upload(self):
        """Test video upload endpoint."""
        with open(self.test_video_path, "rb") as f:
            response = self.client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("filename", data)
        self.assertIn("content_type", data)
        self.assertIn("size", data)
        self.assertIn("status", data)
        self.assertIn("created_at", data)
        self.assertEqual(data["status"], "uploaded")

    def test_video_processing(self):
        """Test video processing endpoint."""
        # First upload a video
        with open(self.test_video_path, "rb") as f:
            upload_response = self.client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        video_id = upload_response.json()["id"]

        # Then process it
        response = self.client.post(
            f"/api/v1/videos/{video_id}/process",
            json={"processing_type": "full_analysis"}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("video_id", data)
        self.assertIn("type", data)
        self.assertIn("status", data)
        self.assertIn("progress", data)
        self.assertIn("started_at", data)
        self.assertEqual(data["status"], "processing")

    def test_processing_status(self):
        """Test processing status endpoint."""
        # First upload and process a video
        with open(self.test_video_path, "rb") as f:
            upload_response = self.client.post(
                "/api/v1/videos/upload",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        video_id = upload_response.json()["id"]
        
        process_response = self.client.post(
            f"/api/v1/videos/{video_id}/process",
            json={"processing_type": "full_analysis"}
        )
        processing_id = process_response.json()["id"]

        # Check status
        response = self.client.get(f"/api/v1/videos/{video_id}/status/{processing_id}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("id", data)
        self.assertIn("video_id", data)
        self.assertIn("type", data)
        self.assertIn("status", data)
        self.assertIn("progress", data)
        self.assertIn("started_at", data)

    def test_invalid_video_format(self):
        """Test handling of invalid video format."""
        # Create a non-video file
        invalid_path = os.path.join(self.test_dir, "invalid.txt")
        with open(invalid_path, "w") as f:
            f.write("This is not a video file")
        
        with open(invalid_path, "rb") as f:
            response = self.client.post(
                "/api/v1/videos/upload",
                files={"file": ("invalid.txt", f, "text/plain")}
            )
        
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data["detail"], "Invalid file type. Only video files are accepted.")

    def test_nonexistent_video(self):
        """Test handling of requests for non-existent video."""
        response = self.client.get("/api/v1/videos/invalid_id/status/invalid_processing_id")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Processing job not found")

if __name__ == "__main__":
    unittest.main() 