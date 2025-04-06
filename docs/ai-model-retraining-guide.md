# AI Model Retraining Guide

## Overview
This guide provides instructions for retraining the AI models used in the Raasid system. AI models need periodic retraining with fresh data to ensure they maintain high accuracy and adapt to changing patterns in gameplay. This document explains the process of retraining the pose estimation, ball contact detection, and event context classification models, as well as best practices for model evaluation and deployment.

## Prerequisites
Before starting the retraining process, ensure the following prerequisites are met:

- **Python 3.8+**: Required for running the training scripts.
- **TensorFlow/Keras**: Deep learning frameworks used for training AI models.
- **Scikit-learn**: Used for machine learning algorithms.
- **Data Pipeline**: A consistent and reliable data pipeline that includes labeled training data.
- **GPU (Optional)**: For faster model training, especially for deep learning models.
- **Docker**: If using a containerized environment for model training and deployment.

## Retraining Workflow

### Step 1: Data Collection
The performance of AI models relies on high-quality labeled data. The following data sources should be used for retraining:

- **Pose Estimation Data**: Labeled video frames with hand positions and limb angles. This data is essential for improving the pose estimation model's accuracy.
- **Ball Contact Data**: Sensor data from smart balls, including impact force, contact duration, and sensor source. This data is used to improve the ball contact detection model.
- **Event Context Data**: Labeled handball events, including classifications of intentional or accidental handball and rule violations. This data helps train the event context classification model.

Make sure the data is cleaned, normalized, and split into training, validation, and test datasets.

### Step 2: Data Preprocessing
Data preprocessing is crucial for training deep learning models. The following preprocessing steps are recommended:

- **Normalization**: Scale the numerical values (e.g., limb angles, impact force) to ensure uniformity.
- **Augmentation**: Apply data augmentation techniques (e.g., rotation, flipping, color jittering) to increase the diversity of the training data.
- **Resizing**: Ensure that video frames are resized to a uniform size (e.g., 224x224 for image-based models).
- **Tokenization (for event context data)**: If event context data is text-based (e.g., "intentional", "accidental"), tokenize the text for input to the model.

### Step 3: Retraining the Models
The retraining process for each model is as follows:

#### 1. Pose Estimation Model
- **Model Type**: Convolutional Neural Network (CNN), specifically designed for keypoint detection.
- **Training**:
  - Use labeled video frames with known hand positions and limb angles.
  - Train the model to predict keypoints (hand position, elbow angle, shoulder angle).
  - Use techniques such as transfer learning to fine-tune pre-trained models (e.g., MediaPipe or OpenPose) on your specific dataset.

```bash
# Example command to start retraining the Pose Estimation Model
python retrain_pose_estimation.py --data-path /path/to/pose_data --epochs 50
```

#### 2. Ball Contact Detection Model
- **Model Type**: Classification model using sensor data (e.g., Random Forest, SVM).
- **Training**:
  - Train the model to predict ball contact based on impact force, contact duration, and sensor data.
  - Use cross-validation to ensure the model is generalized to unseen data.

```bash
# Example command to retrain the Ball Contact Detection Model
python retrain_ball_contact.py --data-path /path/to/sensor_data --epochs 50
```

#### 3. Event Context Classification Model
- **Model Type**: Decision trees, ensemble methods, or neural networks.
- **Training**:
  - Train the model to classify events as intentional or accidental based on the pose and ball contact data.
  - Use rule-based logic in conjunction with machine learning to improve accuracy.

```bash
# Example command to retrain the Event Context Classification Model
python retrain_event_context.py --data-path /path/to/event_data --epochs 50
```

### Step 4: Model Evaluation
After retraining the models, it is essential to evaluate their performance using the validation set. Use the following metrics to assess the models:

- **Accuracy**: The percentage of correct predictions.
- **Precision**: The proportion of true positives among all positive predictions.
- **Recall**: The proportion of true positives among all actual positive instances.
- **F1 Score**: The harmonic mean of precision and recall.

Example evaluation script:

```bash
python evaluate_model.py --model /path/to/model --data-path /path/to/validation_data
```

### Step 5: Hyperparameter Tuning
For improved model performance, tune hyperparameters such as the learning rate, batch size, and the number of layers. Use techniques like **Grid Search** or **Random Search** to find the optimal hyperparameters.

### Step 6: Model Deployment
Once the model is retrained and evaluated, deploy the new model to the backend system. Follow these steps:

1. **Export the Model**: Save the trained model using a format like `.h5` for TensorFlow/Keras models.
2. **Update the Backend**: Replace the old model with the newly trained model in the backend system.
3. **Test Deployment**: Run tests to verify that the new model works as expected in real-time, using sample video and sensor data.
4. **Monitor Model Performance**: Continuously monitor the model’s performance after deployment, tracking metrics like inference time and accuracy.

```bash
# Example command to export the trained model
python export_model.py --model /path/to/trained_model --output /path/to/save/model.h5
```

### Step 7: Continuous Model Improvement
Regularly retrain the model using new match data to ensure that the system adapts to evolving game patterns and improves accuracy. Set up a schedule for periodic retraining (e.g., monthly or quarterly) and use feedback from referees and analysts to guide improvements.

## Best Practices

- **Data Quality**: Ensure that training data is labeled accurately and covers a wide variety of scenarios.
- **Model Monitoring**: Continuously monitor the model’s performance to identify when retraining is necessary.
- **Version Control**: Keep track of model versions, including training data, hyperparameters, and performance metrics.
- **Scalability**: Consider training models on distributed systems (e.g., AWS Sagemaker, Google AI Platform) for scalability when processing large datasets.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)
