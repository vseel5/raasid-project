 # Raasid: AI-Powered Handball Detection System

## Overview
Raasid is an AI-driven handball detection system built to enhance the accuracy, speed, and transparency of football refereeing. By integrating pose estimation, sensor data, and real-time analysis, Raasid ensures consistent enforcement of FIFA rules while minimizing human error.

## Problem Statement
Despite VAR advancements, handball decisions remain inconsistent and controversial due to:
- Subjective human interpretation
- Delays in VAR decision-making
- Inability to distinguish intent
- Lack of standardization across leagues

## Raasid's Solution
- **AI-Powered Detection**: Real-time analysis of ball-hand contact
- **Intent Recognition**: Differentiates intentional vs. accidental handball
- **Sensor Fusion**: Combines video, sensor, and audio inputs
- **Rule-Based AI**: Applies FIFA handball rules with high accuracy
- **Transparency Tools**: Provides live explanations and replays for fans and officials

## MVP Features
- Pose Estimation AI
- Ball Contact Detection
- Event Context Classification
- Real-time Decision Engine
- VAR Review API with Override
- Admin Dashboard (Logs, Override, Distribute)

## Technology Stack
- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, JS
- **AI**: TensorFlow, MediaPipe, Scikit-learn
- **Logging & Storage**: JSON files, Local logs, Cloud endpoint simulation

## Getting Started
1. Clone the repository and set up the virtual environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the FastAPI backend:
   ```bash
   uvicorn server:app --reload
   ```

3. Open the `frontend/index.html` in VS Code using Live Server

## API Endpoints
- `/pose_estimation` : Accepts pose AI data
- `/ball_contact_ai` : Accepts ball sensor data
- `/event_context_ai` : Accepts context evaluation
- `/decision_making_ai` : Accepts final decision from AI
- `/var_review` : Allows manual VAR override
- `/output_distribution` : Simulates sending data to referee, VAR, TV, and cloud
- `/decision_logs` : Returns all decisions

## Project Status
Core MVP is functional:
- Data flows correctly from input to output layers
- API logs decisions persistently
- Admin dashboard interfaces with backend

Next Milestones:
- Real-time timeline visualization
- Real-time explanation engine
- Advanced analytics for match review

## License
MIT License

## Authors
- **Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi**
- [GitHub Profile](https://github.com/vseel5/raasid-project/)


