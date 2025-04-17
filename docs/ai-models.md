# AI Models Documentation

## Overview
The RAASID system utilizes several AI models to analyze handball incidents. This document provides detailed information about each model, its architecture, and implementation.

## 1. Context Analysis Model

### Architecture
The Context Analysis Model is implemented as a Convolutional Neural Network (CNN) with the following structure:

```python
class ContextCNN(nn.Module):
    def __init__(self):
        super(ContextCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 8 * 8, 512)
        self.fc2 = nn.Linear(512, 256)
        self.fc_game = nn.Linear(256, num_game_situations)
        self.fc_intent = nn.Linear(256, num_intents)
```

### Input
- RGB image frames (64x64 pixels)
- Normalized pixel values

### Output
- Game situation classification
- Player intent classification

### Training Process
1. Data Preparation
   - Frame extraction from video
   - Pose estimation
   - Ball detection
   - Annotation generation

2. Model Training
   - Cross-entropy loss
   - Adam optimizer
   - Learning rate scheduling
   - Early stopping

3. Evaluation
   - Validation accuracy
   - Confusion matrix
   - ROC curves

## 2. Pose Estimation Model

### Architecture
- Pre-trained ResNet50 backbone
- Custom head for keypoint detection
- Multi-task learning for pose and orientation

### Input
- RGB image frames
- Player bounding boxes

### Output
- Keypoint coordinates
- Body orientation
- Hand positions

## 3. Ball Detection Model

### Architecture
- YOLOv5-based detector
- Custom training for ball detection
- Confidence thresholding

### Input
- RGB image frames
- Region of interest

### Output
- Ball position
- Detection confidence
- Ball trajectory

## Model Integration

### Pipeline Flow
1. Frame Preprocessing
   - Image resizing
   - Normalization
   - Region extraction

2. Model Inference
   - Parallel processing
   - Result aggregation
   - Confidence scoring

3. Decision Making
   - Rule application
   - Context analysis
   - Final classification

## Performance Metrics

### Context Analysis Model
- Accuracy: >90%
- Precision: >85%
- Recall: >88%
- F1 Score: >86%

### Pose Estimation Model
- Keypoint accuracy: >95%
- Orientation accuracy: >90%
- Inference time: <50ms

### Ball Detection Model
- Detection accuracy: >95%
- False positive rate: <2%
- Inference time: <30ms

## Model Deployment

### Requirements
- CUDA-capable GPU
- PyTorch 1.9+
- OpenCV 4.5+
- Python 3.8+

### Configuration
```python
{
    "model_path": "models/context_cnn.pth",
    "batch_size": 32,
    "confidence_threshold": 0.7,
    "device": "cuda"
}
```

## Best Practices

### Model Training
1. Data Quality
   - High-resolution video
   - Diverse scenarios
   - Accurate annotations

2. Training Process
   - Regular validation
   - Model checkpointing
   - Hyperparameter tuning

3. Evaluation
   - Cross-validation
   - Real-world testing
   - Performance monitoring

### Model Deployment
1. Version Control
   - Model versioning
   - Configuration tracking
   - Change logging

2. Monitoring
   - Performance metrics
   - Error tracking
   - Resource usage

3. Updates
   - Regular retraining
   - Performance optimization
   - Bug fixes

## Troubleshooting

### Common Issues
1. Training
   - Overfitting
   - Underfitting
   - Training instability

2. Inference
   - Memory issues
   - Performance degradation
   - False positives/negatives

3. Deployment
   - Model loading errors
   - Compatibility issues
   - Resource constraints

### Solutions
1. Training Issues
   - Data augmentation
   - Regularization
   - Learning rate adjustment

2. Inference Issues
   - Batch size optimization
   - Memory management
   - Hardware acceleration

3. Deployment Issues
   - Version compatibility
   - Resource allocation
   - Error handling

## Technology Used
- Pose Estimation: MediaPipe (pre-trained model for pose detection).
- Sensor Fusion: Custom models built on TensorFlow or Scikit-learn for combining sensor data.
- Deployment: FastAPI for API-based model deployment and real-time processing.

## Getting Started
To get started with the AI models:

1. Clone the repository and set up the environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate  # On macOS/Linux: source raasid-env/bin/activate
   pip install -r requirements.txt
   ```

2. Run the FastAPI backend to load the models:
   ```bash
   uvicorn api.main:app --reload
   ```

3. Use the `/pose_estimation`, `/ball_contact_ai`, and `/event_context_ai` endpoints to interact with the models in real time.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

