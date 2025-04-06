# AI Models

## Overview
The AI models in the Raasid system are designed to analyze and detect handball incidents in football matches. These models process various data inputs, such as player pose, ball contact, and event context, to generate accurate decisions. The MVP version of the system utilizes pre-trained models to provide real-time handball detection and classification, offering a foundational AI-driven solution for football officiating.

## Model Architecture
The AI models in Raasid are built on a combination of machine learning techniques, leveraging computer vision and sensor fusion. The models integrate information from pose estimation, ball contact detection, and event context classification to make decisions in real time.

### Pose Estimation Model
The pose estimation model is responsible for detecting the position and movement of players' limbs during a match. It analyzes video frames to identify hand positions and limb angles, which are crucial for determining whether a handball incident occurred.

- Model Type: Pre-trained model using MediaPipe for pose estimation.
- Input: Video frames of the match.
- Output: Hand position (natural or unnatural), limb angles (elbow, shoulder).
- Purpose: To detect the likelihood of handball incidents based on player pose.

### Ball Contact Detection Model
The ball contact detection model analyzes sensor data to determine if a player has made contact with the ball. It calculates impact force and the duration of contact to assess the severity of the interaction.

- Model Type: Custom model trained on sensor data (e.g., impact force, contact duration).
- Input: Sensor data from smart balls or other tracking devices.
- Output: Contact status (true/false), impact force, contact duration.
- Purpose: To detect whether a handball occurred based on physical interaction with the ball.

### Event Context Classification Model
The event context classification model evaluates the situation surrounding the handball incident, including the likelihood of a rule violation and whether the handball was accidental or intentional.

- Model Type: Classification model using Scikit-learn or TensorFlow.
- Input: Handball decision context (e.g., handball type: intentional or accidental), certainty score.
- Output: Classification of handball decision (intentional or accidental), rule violation status.
- Purpose: To provide context around the handball, aiding in decision-making.

## Training and Evaluation
The MVP currently uses pre-trained models, which are fine-tuned on the match data. The training process focuses on optimizing the models for accuracy in real-world scenarios while ensuring that they run efficiently in the system.

### Model Training Process
1. Data Collection: The models are trained on a combination of synthetic data (generated through simulations) and real match data (when available).
2. Model Fine-tuning: Pre-trained models, such as those from MediaPipe, are fine-tuned to handle the specific types of pose estimation relevant to football.
3. Cross-validation: A cross-validation process is used to ensure the models generalize well across various matches and scenarios.
4. Performance Metrics: The models are evaluated based on key performance indicators (KPIs) such as accuracy, precision, recall, and F1 score.

### Model Deployment
The models are deployed as part of the Raasid API, where they can be queried in real time during a match. The FastAPI backend handles the requests to the models, processes the inputs, and returns the decision outcomes.

- Deployment Framework: FastAPI for real-time processing and serving.
- Model Loading: Pre-trained models are loaded into memory when the system starts, ensuring fast access during live matches.
- Scalability: The models are designed to run efficiently, allowing the system to scale as more matches are analyzed simultaneously.

## Future Enhancements
The current AI models are effective for detecting handball incidents in real time, but several enhancements are planned for future versions:

- Model Expansion: Additional models for detecting other football-related incidents (e.g., offside detection).
- Improved Accuracy: Ongoing model improvement through new data collection and continuous fine-tuning.
- Real-Time Model Training: Integration of online learning techniques to enable the models to adapt in real-time during live matches.

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

