# AI Training Pipeline Documentation

## Overview
The RAASID system's AI training pipeline consists of three main components:
1. Data Collection and Preparation
2. Model Training
3. Model Evaluation and Deployment

## 1. Data Collection and Preparation

### Data Collection Script
The `collect_training_data.py` script handles the collection and preparation of training data:

```python
python api/training/collect_training_data.py
```

#### Key Features:
- Video frame processing at configurable intervals
- Automatic pose estimation and ball detection
- Structured annotation generation
- Train/validation split (80/20)
- Error handling and logging

#### Configuration:
```python
config = {
    'video_path': 'data/videos/handball_incident.mp4',
    'output_dir': 'data/training',
    'game_situation': 'defensive_block',
    'player_intent': 'deliberate',
    'frame_interval': 30
}
```

### Data Structure
The collected data is stored in the following format:
```
data/training/
├── images/
│   └── frame_*.jpg
├── train_annotations.json
└── val_annotations.json
```

#### Annotation Format:
```json
{
    "image_path": "images/frame_123.jpg",
    "frame_number": 123,
    "game_situation": "defensive_block",
    "player_intent": "deliberate",
    "pose_data": {
        "keypoints": [...],
        "hand_positions": [...],
        "body_orientation": [...]
    },
    "ball_position": [x, y]
}
```

## 2. Model Training

### Training Script
The `train_context_model.py` script handles model training:

```python
python api/training/train_context_model.py
```

#### Key Features:
- Custom HandballDataset class for data loading
- Configurable training parameters
- Automatic model checkpointing
- Training progress logging
- GPU support (if available)

#### Configuration:
```python
config = {
    'data_dir': 'data/training',
    'model_save_path': 'models/context_cnn.pth',
    'num_epochs': 50,
    'batch_size': 32,
    'learning_rate': 0.001
}
```

### Training Process
1. Data Loading and Preprocessing
   - Image resizing and normalization
   - Label encoding
   - Data augmentation

2. Model Training
   - Cross-entropy loss for both game situation and intent classification
   - Adam optimizer with configurable learning rate
   - Early stopping based on validation loss

3. Model Evaluation
   - Validation metrics calculation
   - Best model checkpointing
   - Training progress visualization

## 3. Model Deployment

### Model Integration
The trained model is integrated into the RAASID system through:
- `ContextCNN` class in the event context analysis component
- Automatic model loading during system initialization
- Real-time inference during game analysis

### Performance Monitoring
- Inference time tracking
- Accuracy metrics logging
- Error rate monitoring

## Best Practices

### Data Collection
1. Use high-quality video footage
2. Ensure diverse game situations
3. Maintain consistent annotation standards
4. Regular data validation

### Training
1. Monitor training metrics
2. Regular model checkpointing
3. Validation set evaluation
4. Hyperparameter tuning

### Deployment
1. Model versioning
2. Performance benchmarking
3. Regular model updates
4. Error tracking and logging

## Troubleshooting

### Common Issues
1. Data Collection
   - Video format compatibility
   - Frame extraction errors
   - Annotation inconsistencies

2. Training
   - GPU memory issues
   - Training instability
   - Overfitting

3. Deployment
   - Model loading errors
   - Inference performance
   - Memory management

### Solutions
1. Check system requirements
2. Verify data integrity
3. Monitor resource usage
4. Regular system updates

## Technology Used
- Training Frameworks: TensorFlow, Keras, and Scikit-learn for model training and optimization.
- Data Processing: Pandas, NumPy, and OpenCV for data manipulation and preprocessing.
- Model Deployment: FastAPI for real-time deployment, Docker for containerization.
- Version Control: Git for code versioning, Docker for model versioning.

## Getting Started
To set up the training pipeline locally, follow these steps:

1. Clone the repository and set up the environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate  # On macOS/Linux: source raasid-env/bin/activate
   pip install -r requirements.txt
   ```

2. Train the models by running the following script:
   ```bash
   python train_models.py
   ```

3. Evaluate the models:
   ```bash
   python evaluate_models.py
   ```

4. Once the models are trained and evaluated, run the FastAPI backend to deploy the models:
   ```bash
   uvicorn api.main:app --reload
   ```

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

