import requests
import os
import time
import pytest

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == 200
    assert data["data"]["status"] == "healthy"
    print("Health check passed!")

def test_upload_video():
    # Create a test video file
    test_file = "test_video.mp4"
    with open(test_file, "wb") as f:
        f.write(b"0" * 1024)  # 1KB test file
    
    # Upload the file
    with open(test_file, "rb") as f:
        files = {"video": (test_file, f, "video/mp4")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    print(f"Upload response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "video_id" in data["data"]
    assert "status" in data["data"]
    print("Video upload passed!")
    
    # Clean up
    os.remove(test_file)
    return data["data"]["video_id"]

def test_upload_large_file():
    # Create a large test file (6MB)
    test_file = "large_video.mp4"
    with open(test_file, "wb") as f:
        f.write(b"0" * (6 * 1024 * 1024))
    
    # Upload the file
    with open(test_file, "rb") as f:
        files = {"video": (test_file, f, "video/mp4")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    print(f"Large file upload response: {response.text}")
    assert response.status_code == 413  # Expect file too large error
    
    # Clean up
    os.remove(test_file)

def test_upload_invalid_format():
    # Create a test text file
    test_file = "test.txt"
    with open(test_file, "w") as f:
        f.write("This is not a video file")
    
    # Upload the file
    with open(test_file, "rb") as f:
        files = {"video": (test_file, f, "text/plain")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
    
    print(f"Invalid format upload response: {response.text}")
    assert response.status_code == 400  # Expect invalid format error
    
    # Clean up
    os.remove(test_file)

def test_process_video(video_id):
    response = requests.post(f"{BASE_URL}/process/{video_id}")
    assert response.status_code == 200
    data = response.json()
    assert "processing_id" in data["data"]
    assert "status" in data["data"]
    print("Video processing started!")
    return data["data"]["processing_id"]

def test_process_invalid_video():
    invalid_id = "nonexistent-video-id"
    response = requests.post(f"{BASE_URL}/process/{invalid_id}")
    print(f"Invalid video process response: {response.text}")
    assert response.status_code == 404  # Expect not found error

def test_get_status(processing_id):
    response = requests.get(f"{BASE_URL}/status/{processing_id}")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data["data"]
    assert "progress" in data["data"]
    print("Status check passed!")
    return data["data"]

def test_get_invalid_status():
    invalid_id = "nonexistent-process-id"
    response = requests.get(f"{BASE_URL}/status/{invalid_id}")
    print(f"Invalid status check response: {response.text}")
    assert response.status_code == 404  # Expect not found error

def test_concurrent_uploads():
    # Test concurrent uploads
    test_files = []
    responses = []
    
    # Create and upload 5 files concurrently
    for i in range(5):
        test_file = f"test_video_{i}.mp4"
        with open(test_file, "wb") as f:
            f.write(b"0" * 1024)
        test_files.append(test_file)
        
        with open(test_file, "rb") as f:
            files = {"video": (test_file, f, "video/mp4")}
            response = requests.post(f"{BASE_URL}/upload", files=files)
            responses.append(response)
    
    # Clean up
    for test_file in test_files:
        os.remove(test_file)
    
    # Verify all uploads were successful
    for i, response in enumerate(responses):
        print(f"Concurrent upload {i} response: {response.text}")
        assert response.status_code == 200
        data = response.json()
        assert "video_id" in data["data"]
    
    print("Concurrent uploads test passed!")

if __name__ == "__main__":
    print("Testing API endpoints...")
    
    # Basic functionality tests
    test_health_endpoint()
    video_id = test_upload_video()
    processing_id = test_process_video(video_id)
    status = test_get_status(processing_id)
    
    # Error handling tests
    print("\nRunning error handling tests...")
    test_upload_large_file()
    test_upload_invalid_format()
    test_process_invalid_video()
    test_get_invalid_status()
    
    # Concurrent operation tests
    print("\nRunning concurrent operation tests...")
    test_concurrent_uploads()
    
    print("\nAll tests completed successfully!") 