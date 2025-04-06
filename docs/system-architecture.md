# System Architecture

## Overview
The system architecture of Raasid outlines the key components and their interactions to provide a seamless, real-time handball detection system for football officiating. This architecture is designed to handle the complexities of video analysis, sensor data integration, and AI decision-making, ensuring accurate and timely decisions during matches.

## Key Components
The Raasid system is composed of several key components, each responsible for different aspects of the handball detection pipeline:

- **Frontend**: Provides the user interface for match video uploads, AI analysis, and decision review.
- **Backend**: Handles data processing, API requests, and model inference.
- **AI Models**: Perform pose estimation, ball contact detection, and event context classification.
- **Data Storage**: Stores decision logs, video frames, and sensor data for long-term access and analysis.
- **External Integrations**: Distributes decisions to external systems such as the referee smartwatch, TV broadcast, and cloud storage.

### Frontend
The frontend provides a dashboard for referees and analysts to interact with the system. It is built using **Streamlit**, a Python-based framework for building data applications. The main features of the frontend include:

- **Video Upload**: Upload match videos or images for processing.
- **AI Analysis Display**: Displays AI-generated decisions, including handball detection, event context, and decision confidence.
- **History and Reports**: Shows the history of decisions made during the match and allows downloading of decision reports.

The frontend communicates with the backend through HTTP requests, using the FastAPI endpoints exposed by the backend.

### Backend
The backend serves as the core of the Raasid system, processing incoming requests, running the AI models, and managing data flow. It is built using **FastAPI**, a fast, asynchronous web framework for Python. The backend performs the following functions:

- **API Endpoints**: Exposes RESTful APIs for interacting with the system, including endpoints for pose estimation, ball contact detection, event context classification, and final decision-making.
- **Model Inference**: Runs the trained AI models to process input data (video frames, sensor data, etc.) and generate predictions.
- **Data Management**: Handles the storage and retrieval of decision logs, video frames, and sensor data.

### AI Models
The AI models in Raasid perform the following tasks:

- **Pose Estimation**: Detects player hand positions and limb angles to assess whether a handball incident occurred.
- **Ball Contact Detection**: Analyzes sensor data to detect ball contact, including impact force and contact duration.
- **Event Context Classification**: Classifies handball incidents as intentional or accidental, and checks for rule violations.

The models are trained on labeled data and deployed in the backend, where they can be queried via API endpoints.

### Data Storage
Data storage in Raasid is split between **local storage** for temporary data and **cloud storage** for long-term retention. The system stores the following types of data:

- **Video Frames**: Captured from the match for pose estimation and ball contact analysis.
- **Sensor Data**: Includes data from smart balls, tracking ball impact and contact duration.
- **Decision Logs**: Logs all decisions made by the system, including frame numbers, final decisions, and certainty scores.

Data is stored securely and is accessible for analysis, audit, and retraining purposes.

### External Integrations
Raasid supports integration with external systems to distribute decisions in real time. These systems include:

- **Referee Smartwatch**: Receives the final decision in real time for immediate display to the referee.
- **TV Broadcast**: Displays the handball decision and relevant match information to viewers.
- **Cloud Storage**: Stores final decisions and related metadata for long-term access and analytics.

These integrations are simulated using API calls to external endpoints, allowing the Raasid system to distribute decisions automatically after they are made.

## Architecture Diagram

Below is the architecture diagram of the Raasid system, illustrating the flow of data and interactions between different components.

```plaintext
+------------------+        +-------------------------+        +----------------------+
|                  |        |                         |        |                      |
|  Video Input     +------->+   Frontend (Streamlit)  +------->+   Backend (FastAPI)  |
|                  |        |                         |        |                      |
+------------------+        |   - Video Upload        |        |   - API Endpoints     |
                            |   - AI Analysis Display |        |   - Model Inference   |
                            |   - History and Reports |        |   - Data Management   |
                            +-------------------------+        +----------------------+
                                      |
                                      |
                            +----------------------+
                            |                      |
                            |   AI Models          |
                            |   - Pose Estimation  |
                            |   - Ball Contact     |
                            |   - Event Context    |
                            +----------------------+
                                      |
                                      |
                           +--------------------------+
                           |                          |
                           |   External Integrations  |
                           |   - Referee Smartwatch   |
                           |   - TV Broadcast         |
                           |   - Cloud Storage        |
                           +--------------------------+
```

## Deployment
Raasid is designed to be deployed in a containerized environment using Docker. The following components are containerized:

- **Frontend**: The Streamlit dashboard is packaged as a Docker container for easy deployment.
- **Backend**: The FastAPI backend is also containerized to ensure consistent deployment across different environments.
- **AI Models**: The AI models are loaded into the backend containers and used for real-time inference.

Deployment is straightforward and involves setting up the backend and frontend containers, along with any necessary dependencies (e.g., TensorFlow, OpenCV) in the environment.

## Scalability
The Raasid system is designed to be scalable to handle multiple matches simultaneously. Key scalability features include:

- **Load Balancing**: Multiple backend instances can be deployed to balance the load of incoming requests from the frontend or external systems.
- **Cloud Storage**: Data storage is handled by cloud platforms, which can scale to accommodate large amounts of match data and decision logs.
- **Model Inference**: The system is optimized for fast model inference, ensuring real-time decision-making even under high load conditions.

## Future Enhancements
The system architecture will be enhanced in future iterations of the project:

- **Microservices Architecture**: Breaking down the backend into smaller microservices to handle specific tasks (pose estimation, ball contact detection, etc.) for better maintainability and scalability.
- **Distributed Data Processing**: Implementing distributed data processing to handle large-scale video and sensor data more efficiently.
- **Cloud-Native Features**: Leveraging cloud-native features, such as Kubernetes for container orchestration and AWS Lambda for serverless model inference.

## Technology Used
- **Frontend**: Streamlit for building interactive dashboards.
- **Backend**: FastAPI for creating fast, scalable APIs.
- **AI Models**: TensorFlow, MediaPipe, and Scikit-learn for model training and inference.
- **Data Storage**: Local storage for temporary data, cloud storage (e.g., AWS S3, Azure Blob Storage) for long-term storage.
- **Deployment**: Docker for containerization and deployment.

## Getting Started
To set up the system architecture locally, follow these steps:

1. Clone the repository and set up the environment:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   python -m venv raasid-env
   raasid-env\Scripts\activate  # On macOS/Linux: source raasid-env/bin/activate
   pip install -r requirements.txt
   ```

2. Build and start the Docker containers for the backend and frontend:
   ```bash
   docker-compose up --build
   ```

3. Access the frontend at `http://localhost:8501` and interact with the system.

4. Start the FastAPI backend:
   ```bash
   uvicorn api.main:app --reload
   ```

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)