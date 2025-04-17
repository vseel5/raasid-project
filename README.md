# Raasid - AI-Powered Handball Detection System

A sophisticated AI system for detecting and analyzing handball events in video footage.

## Features

- Real-time video processing
- Object detection using Faster R-CNN
- Pose estimation using Keypoint R-CNN
- Multi-level caching system
- Comprehensive monitoring and metrics
- RESTful API interface
- Streamlit dashboard

## Prerequisites

- Python 3.8+
- Redis server
- CUDA-capable GPU (recommended)
- FFmpeg

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/raasid-project.git
cd raasid-project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Download models:
```bash
python scripts/download_models.py
```

## Configuration

The system can be configured through environment variables in the `.env` file:

```env
# Core Settings
MODEL_DIR=models
STORAGE_DIR=storage
LOG_DIR=logs

# Redis Settings
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

## Usage

1. Start the API server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

2. Start the Streamlit dashboard:
```bash
streamlit run dashboard/streamlit_app.py
```

3. Access the API documentation at `http://localhost:8000/api/docs`

## API Endpoints

- `POST /api/v1/videos/upload` - Upload a video for processing
- `POST /api/v1/videos/{video_id}/process` - Process a video
- `GET /api/v1/videos/{video_id}/status/{processing_id}` - Get processing status
- `GET /health` - Health check endpoint

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black .
flake8
mypy .
```

### Documentation
```bash
mkdocs serve
```

## Architecture

The system consists of several key components:

- **API Server**: FastAPI-based REST API
- **Model Manager**: Handles AI model loading and inference
- **Video Processor**: Processes video frames
- **Cache Manager**: Multi-level caching system
- **Monitoring**: System metrics and health checks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 