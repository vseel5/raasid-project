# System Technical Architecture

## Overview
The technical architecture of Raasid outlines the detailed infrastructure and technical components that support the system’s functionality. It describes the interaction between various software and hardware layers, focusing on the integration of AI models, data processing pipelines, and external system communication. The architecture ensures that Raasid can efficiently handle real-time video analysis, sensor data processing, and decision distribution.

## Core Components

### 1. AI Models
The AI models are the heart of the Raasid system, responsible for detecting handball incidents and making decisions based on the data received. These models are:

- **Pose Estimation Model**: Detects hand positioning and limb angles using computer vision techniques.
- **Ball Contact Detection Model**: Analyzes sensor data to detect ball contact, focusing on impact force and contact duration.
- **Event Context Classification Model**: Classifies the handball incident as intentional or accidental and checks for rule violations based on event context.

These models are deployed as part of the backend and exposed as API endpoints for integration with the frontend.

### 2. Data Flow
The data flow in Raasid is structured in several stages:

1. **Data Collection**: Data is collected in real-time, including video frames, sensor data from smart balls, and event context from match events.
2. **Data Preprocessing**: The collected data is preprocessed for analysis. Video frames are converted into formats suitable for pose estimation, and sensor data is processed for ball contact analysis.
3. **AI Inference**: The preprocessed data is passed to the AI models for pose estimation, ball contact detection, and event context classification.
4. **Decision Making**: The results from the AI models are combined to make a final decision on whether a handball occurred, and if so, whether it was intentional or accidental.
5. **Data Distribution**: The final decision is distributed to external systems, such as the referee smartwatch, TV broadcast, and cloud storage for long-term retention.

### 3. Backend Architecture
The backend of the Raasid system is responsible for managing API requests, handling AI inference, and storing decision logs. It is built using **FastAPI**, a modern, fast web framework for Python.

- **API Endpoints**: The backend exposes multiple endpoints for interacting with the system. These endpoints include `/pose_estimation`, `/ball_contact_ai`, `/event_context_ai`, `/decision_making_ai`, and `/output_distribution`.
- **AI Inference Engine**: The backend serves as the host for the AI models, executing inference on incoming data from the frontend and other sources.
- **Data Management**: All data (e.g., decisions, logs, sensor data) is stored locally or in the cloud. Logs of decisions are retained for audit purposes and further analysis.

### 4. Frontend Architecture
The frontend provides the user interface where referees and analysts can interact with the system. It is built using **Streamlit**, a lightweight framework for building data-driven web applications. The frontend performs the following tasks:

- **Video Upload**: The referee or analyst uploads the match video or image for processing.
- **Real-Time Decision Display**: The frontend displays the real-time analysis from the backend, including handball detection and event classification.
- **History and Reports**: It provides access to the history of decisions and downloadable reports of match events.

The frontend communicates with the backend through RESTful API calls, using FastAPI endpoints exposed by the backend.

### 5. Integration with External Systems
Raasid integrates with several external systems to distribute decisions in real-time:

- **Referee Smartwatch**: Displays the final decision to the referee for immediate action.
- **TV Broadcast**: Sends the final decision to the TV broadcast system for displaying to the audience.
- **Cloud Storage**: Stores the final decisions and metadata for long-term access and analysis.

These integrations are simulated via API calls to external endpoints, enabling seamless data distribution across systems.

## Data Flow Diagram

Below is a diagram illustrating the technical data flow of the Raasid system:

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
                            |   AI Inference Engine|
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
Raasid is deployed in a containerized environment using Docker. The backend and frontend are packaged as Docker containers to ensure portability and consistency across environments. The deployment steps are as follows:

1. **Docker Setup**: Build the Docker images for both the frontend and backend:
   ```bash
   docker-compose up --build
   ```

2. **Container Orchestration**: Use Docker Compose to manage and orchestrate the containers, ensuring they communicate seamlessly.

3. **Model Deployment**: The AI models are loaded into the backend containers, ensuring that real-time inference can be performed as video and sensor data are received.

4. **Scaling**: The system is designed to scale horizontally, allowing multiple backend instances to be deployed to handle a larger volume of incoming requests.

## Scalability Considerations
The Raasid system is designed to scale horizontally, accommodating multiple matches or events concurrently. Key scalability features include:

- **Load Balancing**: The backend can be scaled to multiple instances using a load balancer to distribute traffic efficiently.
- **Cloud Storage**: Cloud storage is utilized for long-term data storage, allowing for the scalability of data retention.
- **Distributed AI Inference**: As the system grows, the AI models can be distributed across multiple servers or GPUs to handle increased inference demand.

## Security Considerations
Security is a top priority for the Raasid system. The following measures are implemented to protect the system:

- **Encryption**: All data in transit is encrypted using HTTPS and TLS. Sensitive data, including decision logs, is stored securely with encryption.
- **Authentication**: Future iterations of the system may include authentication mechanisms, such as JWT or OAuth, to secure the APIs.
- **Data Access Control**: Role-based access control (RBAC) is implemented to ensure that only authorized personnel can access sensitive data.

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

