# Deployment Guide

## Overview
This guide provides instructions for deploying the Raasid AI-powered handball detection system in both local and production environments. It covers the setup of the backend, frontend, required dependencies, and configuration for cloud storage, APIs, and external system integrations.

## Prerequisites
Before deploying the system, ensure the following prerequisites are met:

- **Docker**: Used for containerizing the system for easy deployment across various environments.
- **Python 3.8+**: Required for running the backend FastAPI server.
- **Git**: To clone the repository and manage version control.
- **Docker Compose**: For managing multi-container Docker applications.
- **Cloud Storage Account**: For storing decision logs and reports (AWS S3, Azure Blob Storage, etc.).

## Setting Up the Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv raasid-env
   raasid-env\Scripts\activate  # For macOS/Linux: source raasid-env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the FastAPI backend**:
   ```bash
   uvicorn api.main:app --reload
   ```

5. **Start the Streamlit frontend**:
   Navigate to the frontend directory and run:
   ```bash
   streamlit run streamlit_app.py
   ```

## Setting Up the Dockerized Environment

For easy deployment, we provide Docker configurations for both the backend and frontend.

1. **Build the Docker images**:
   First, ensure that Docker is installed and running. Then, build the images for both the frontend and backend using Docker Compose:
   ```bash
   docker-compose up --build
   ```

2. **Accessing the system**:
   Once the Docker containers are up and running, the system can be accessed through the following:
   - Backend API: `http://localhost:8000`
   - Frontend (Streamlit): `http://localhost:8501`

## Deploying to Production (Cloud)

1. **Cloud Setup**: For production deployment, set up cloud storage and other necessary services (e.g., AWS, Google Cloud). Ensure that storage buckets are created for decision logs, reports, and historical data.

2. **Environment Configuration**:
   - Set the necessary environment variables for the backend to connect to cloud storage and other services.
   - Use a production-grade database (e.g., PostgreSQL, MySQL) for persistent data storage.

3. **Deploying Using Docker**:
   Use Docker to deploy the system on cloud services like AWS ECS, Azure App Service, or Google Cloud Run.

   - Ensure Docker is installed on the cloud instance.
   - Push your Docker images to a container registry (e.g., Docker Hub, AWS ECR).
   - Use a container orchestration tool like Kubernetes if necessary for scaling the system.

4. **CI/CD Integration**:
   - Set up a CI/CD pipeline (e.g., GitHub Actions, Jenkins) for automated testing and deployment of new updates.
   - Configure webhooks to automatically trigger deployments when new code is pushed to the repository.

## Troubleshooting

1. **Backend Not Starting**:
   - Ensure that all environment variables are correctly set (e.g., cloud storage credentials).
   - Check the logs for any errors related to missing dependencies or incorrect configurations.

2. **Frontend Issues**:
   - Ensure the frontend dependencies are installed.
   - Check for CORS issues if the frontend cannot communicate with the backend.

3. **Deployment Failures**:
   - Verify that the Docker container is running correctly by checking the status of the containers:
     ```bash
     docker ps
     ```
   - Ensure cloud services (e.g., database, storage) are correctly configured and accessible.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

