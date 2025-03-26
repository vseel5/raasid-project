# AI Model Training Pipeline – Raasid System

## 1. Introduction

This document outlines the training methodology for Raasid’s AI models that power real-time handball detection. Each model in the AI Processing Layer is trained on structured, labeled datasets using industry-standard machine learning techniques. This training pipeline ensures that Raasid can make accurate, high-confidence decisions during football matches.

---

## 2. Model Overview

| **AI Model**        | **Role**                                        |
|---------------------|--------------------------------------------------|
| Pose Estimation AI  | Detects player limb and hand positioning         |
| Ball Contact AI     | Detects ball-hand contact using sensors          |
| Event Context AI    | Determines intent and rule violation context     |

---

## 3. Dataset Preparation

### 3.1 Data Sources

| **Model**             | **Data Source**                                        |
|------------------------|--------------------------------------------------------|
| Pose Estimation AI     | VAR Camera Footage, SAOT Sensor Data                  |
| Ball Contact AI        | Smart Ball Sensor Data, Snickometer Audio             |
| Event Context AI       | Combined outputs of Pose and Ball Contact AI          |

### 3.2 Preprocessing Steps

- **Synchronization**: Align timestamps from multi-sensor inputs.
- **Noise Filtering**: Remove irrelevant or inconsistent signal data.
- **Feature Extraction**: Extract angles, impact force, posture, and sound frequency peaks.
- **Labeling**:
  - Handball vs. Non-handball
  - Intentional vs. Accidental
  - Confirmed vs. False Contact

---

## 4. Model Training Pipelines

### 4.1 Pose Estimation AI

- **Model Type**: Convolutional Neural Network (CNN)
- **Library**: [MediaPipe](https://google.github.io/mediapipe/) or OpenPose
- **Inputs**: Skeleton keypoints (elbow, shoulder, hand)
- **Outputs**: Hand position, limb angles, certainty score

**Training Flow:**
1. Extract pose keypoints from video frames.
2. Train CNN to classify hand position (natural vs. unnatural).
3. Optimize with reinforcement learning for dynamic motion recognition.

---

### 4.2 Ball Contact AI

- **Model Type**: Random Forest Classifier
- **Library**: scikit-learn
- **Inputs**: Force, duration, Snickometer sound peaks
- **Outputs**: Ball-hand contact status (True/False)

**Training Flow:**
1. Merge sensor readings with audio timestamps.
2. Extract relevant features (impact magnitude, duration).
3. Train model to differentiate hand contact from noise or body deflections.

---

### 4.3 Event Context AI

- **Model Type**: Recurrent Neural Network (LSTM)
- **Library**: TensorFlow / Keras
- **Inputs**: Pose + Ball Contact outputs
- **Outputs**: Final classification (intentional/accidental), rule violation flag

**Training Flow:**
1. Sequence event data pre- and post-contact.
2. Train LSTM to detect intent patterns based on movement and contact.
3. Use rule-based overlay (decision tree) to apply FIFA regulations.

---

## 5. Evaluation Metrics

| **Metric**         | **Purpose**                                       |
|--------------------|---------------------------------------------------|
| Accuracy           | Overall correct predictions                       |
| Precision          | Correctly identified handball vs. false positives |
| Recall             | Ability to detect all true handball events        |
| F1 Score           | Harmonic mean of precision and recall             |
| Inference Time     | Real-time decision capability                     |

---

## 6. Deployment Strategy

### 6.1 Testing Environments
- **Offline Testing**: Run inference on pre-recorded match data.
- **Simulated Matches**: Integrate AI outputs with mock refereeing interface.
- **Edge Testing**: Run lightweight models on edge devices (e.g., stadium servers).

### 6.2 Production Integration
- Expose each model’s output through FastAPI endpoints
- Log all predictions for retraining and auditing
- Flag low-confidence results for VAR override

---

## 7. Model Update & Improvement Loop

1. Log real-world match incidents
2. Annotate misclassified decisions
3. Retrain models with updated samples
4. Push versioned models with rollback capability

---

## 8. Summary

The AI training pipeline in Raasid is designed to ensure accuracy, consistency, and explainability in handball detection. By combining deep learning models with rule-based systems and real-time evaluation metrics, Raasid achieves high-performance decision-making that supports referees and enhances match integrity.

---

