# System Technical Architecture

## Overview
The RAASID system is built on a modular architecture that enables real-time handball incident detection and analysis. This document details the technical components and their interactions.

## 1. Core Components

### 1.1 Video Processing Pipeline
```python
class VideoProcessor:
    def __init__(self):
        self.frame_queue = Queue()
        self.processed_queue = Queue()
        
    def process_frame(self, frame: np.ndarray) -> Dict:
        # Frame preprocessing
        # Model inference
        # Result aggregation
        pass
```

### 1.2 AI Models
- Context Analysis Model (CNN)
- Pose Estimation Model (ResNet50)
- Ball Detection Model (YOLOv5)

### 1.3 Training Pipeline
```python
class TrainingPipeline:
    def __init__(self):
        self.data_collector = TrainingDataCollector()
        self.model_trainer = ModelTrainer()
        
    def run(self):
        # Data collection
        # Model training
        # Evaluation
        pass
```

## 2. System Architecture

### 2.1 Component Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Video Input    │────▶│  Frame Queue    │────▶│  Video Processor│
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Training Data  │────▶│  Data Collector │────▶│  Model Trainer  │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Model Storage  │◀────│  Model Saver    │◀────│  Model Evaluator│
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 2.2 Data Flow
1. Video Input
   - Frame extraction
   - Queue management
   - Batch processing

2. Model Inference
   - Parallel processing
   - Result aggregation
   - Confidence scoring

3. Training Pipeline
   - Data collection
   - Model training
   - Evaluation

## 3. Technical Specifications

### 3.1 Hardware Requirements
- CPU: 4+ cores
- RAM: 16GB minimum
- GPU: CUDA-capable (recommended)
- Storage: 100GB+ SSD

### 3.2 Software Requirements
- Python 3.8+
- PyTorch 1.9+
- OpenCV 4.5+
- FastAPI
- CUDA Toolkit

### 3.3 Performance Metrics
- Frame Processing: <100ms
- Model Inference: <50ms
- Training Time: <24 hours
- Memory Usage: <8GB

## 4. Implementation Details

### 4.1 Video Processing
```python
class VideoProcessor:
    def __init__(self):
        self.models = {
            'context': ContextCNN(),
            'pose': PoseEstimator(),
            'ball': BallDetector()
        }
        
    def process_frame(self, frame: np.ndarray) -> Dict:
        results = {}
        for name, model in self.models.items():
            results[name] = model.infer(frame)
        return results
```

### 4.2 Training Pipeline
```python
class TrainingPipeline:
    def __init__(self):
        self.data_collector = TrainingDataCollector()
        self.model_trainer = ModelTrainer()
        
    def run(self):
        # Collect training data
        data = self.data_collector.collect()
        
        # Train model
        model = self.model_trainer.train(data)
        
        # Evaluate model
        metrics = self.model_trainer.evaluate(model)
        
        return model, metrics
```

### 4.3 Model Management
```python
class ModelManager:
    def __init__(self):
        self.models = {}
        self.config = load_config()
        
    def load_model(self, name: str) -> nn.Module:
        model = self.models.get(name)
        if not model:
            model = self._load_from_disk(name)
            self.models[name] = model
        return model
```

## 5. Security Considerations

### 5.1 Data Security
- Encrypted storage
- Secure transfer
- Access control

### 5.2 Model Security
- Model encryption
- Version control
- Access logging

### 5.3 API Security
- Authentication
- Rate limiting
- Input validation

## 6. Monitoring and Logging

### 6.1 Performance Monitoring
- Frame processing time
- Model inference time
- Memory usage
- GPU utilization

### 6.2 Error Logging
- Exception handling
- Error tracking
- Debug information

### 6.3 System Health
- Resource monitoring
- Service status
- Alert system

## 7. Deployment

### 7.1 Containerization
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### 7.2 Orchestration
```yaml
services:
  api:
    image: raasid-api
    ports:
      - "8000:8000"
    environment:
      - CUDA_VISIBLE_DEVICES=0
    volumes:
      - ./models:/app/models
```

### 7.3 Scaling
- Horizontal scaling
- Load balancing
- Resource allocation

## 8. Maintenance

### 8.1 Updates
- Model updates
- System updates
- Security patches

### 8.2 Backup
- Data backup
- Model backup
- Configuration backup

### 8.3 Monitoring
- Performance monitoring
- Error monitoring
- Resource monitoring

## Future Enhancements
The technical architecture will continue to evolve to support new features and improve performance. Potential future enhancements include:

- **Microservices Architecture**: Splitting the backend into smaller services that can be independently deployed and scaled.
- **Real-Time Data Processing**: Implementing more efficient real-time data processing pipelines using technologies like Apache Kafka or Apache Flink for high-throughput data streams.
- **AI Model Retraining**: Automating the retraining of AI models with new match data to improve detection accuracy and decision-making over time.

## Technology Used
- **Frontend**: Streamlit for building interactive dashboards.
- **Backend**: FastAPI for building scalable and asynchronous APIs.
- **AI Models**: TensorFlow, MediaPipe, and Scikit-learn for AI model training and inference.
- **Data Storage**: Local storage for temporary data, cloud storage (AWS S3, Azure Blob Storage) for long-term storage.
- **Deployment**: Docker and Docker Compose for containerization and deployment.

## Getting Started
To set up the system locally, follow these steps:

1. Clone the repository and set up the environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate  # On macOS/Linux: source raasid-env/bin/activate
   pip install -r requirements.txt
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the frontend at `http://localhost:8501` to interact with the system.

4. Start the FastAPI backend:
   ```bash
   uvicorn api.main:app --reload
   ```

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

