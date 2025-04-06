# Raasid – AI-Powered Handball Detection System

## Overview
Raasid is an AI-driven handball detection system designed to improve the accuracy, speed, and transparency of football refereeing. By integrating pose estimation, sensor data, and real-time analysis, Raasid ensures consistent enforcement of FIFA handball rules, minimizing human error and decision delays. The MVP focuses on real-time handball detection using AI and sensor data, making it a scalable solution for the future of football officiating.

## Problem Statement
Despite advancements like VAR, handball decisions remain inconsistent and controversial due to:
- Subjective human interpretation of handball incidents.
- Delays in VAR decision-making, impacting real-time match flow.
- Difficulty in distinguishing intent between accidental and intentional handball.
- Lack of standardization across leagues, causing variations in the enforcement of FIFA rules.

## Raasid's Solution
Raasid solves the problem by providing an AI-powered system that analyzes key factors such as player pose, ball contact, and event context to make accurate handball decisions. The MVP implements real-time analysis of player actions, detecting ball-hand contact and differentiating between intentional and accidental handballs. The solution ensures real-time decision-making for referees, reducing delays and improving consistency.

## MVP Features
- Pose Estimation AI: Detects hand positioning and limb angles to assess the likelihood of a handball.
- Ball Contact Detection: Identifies ball-hand contact and measures impact force and contact duration.
- Event Context Classification: Differentiates between intentional and accidental handball.
- Real-time Decision Engine: Provides immediate decisions based on AI analysis.
- Admin Dashboard: Allows for reviewing logs and managing decision overrides (limited functionality in MVP).

## Technology Stack
- Backend: Python, FastAPI
- Frontend: HTML, CSS, JavaScript (Streamlit for the dashboard)
- AI: TensorFlow, MediaPipe, Scikit-learn
- Logging & Storage: Local JSON files, logs, and cloud endpoint simulation
- Containerization: Docker for easy deployment and environment isolation

## Getting Started
Follow these steps to get the project running locally:

1. Clone the repository and set up the virtual environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate  # On macOS/Linux: source raasid-env/bin/activate
   pip install -r requirements.txt
   ```

2. Run the FastAPI backend:
   ```bash
   uvicorn api.main:app --reload
   ```

3. Open the frontend:
   - Open `frontend/index.html` in your browser.
   - For development, use VS Code with Live Server extension for automatic reloading.

## API Endpoints
Here are the available API endpoints for interacting with the system:

- `/pose_estimation`: Accepts pose estimation AI data (hand positioning and limb angles).
- `/ball_contact_ai`: Accepts ball contact sensor data (impact force, contact duration).
- `/event_context_ai`: Accepts context evaluation data (handball decision and rule violation).
- `/decision_making_ai`: Accepts the final decision from AI, integrating pose, ball contact, and event context.
- `/var_review`: Allows a manual VAR override of AI decisions (for referees).
- `/output_distribution`: Simulates sending decisions to external systems (referee smartwatch, TV broadcast, cloud).
- `/decision_logs`: Retrieves logs of all decisions made by the system.

## Project Status
The core MVP is functional:
- Data flows correctly from input to output layers.
- API logs decisions persistently.
- The Admin Dashboard interfaces with the backend to manage and review decisions.

### Next Milestones:
- Real-time timeline visualization of decisions and events.
- Real-time explanation engine for handball decisions (for transparency).
- Advanced analytics for match review and decision trends.

## License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)
