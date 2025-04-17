# Deployment Guide

## Version Information
- **Document Version**: 1.0.0
- **Last Updated**: April 17, 2024
- **Compatible System Version**: 1.0.0

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Deployment Options](#deployment-options)
3. [Configuration](#configuration)
4. [Monitoring](#monitoring)
5. [Scaling](#scaling)
6. [Backup and Recovery](#backup-and-recovery)
7. [Security](#security)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### Hardware Requirements
- CPU: 4+ cores (8+ recommended)
- RAM: 16GB minimum (32GB recommended)
- GPU: CUDA-capable (NVIDIA GPU with 8GB+ VRAM)
- Storage: 100GB+ SSD
- Network: 1Gbps connection

### Software Requirements
- Operating System: Ubuntu 20.04 LTS or later
- Docker: 20.10.0 or later
- Docker Compose: 2.0.0 or later
- NVIDIA Container Toolkit
- Python 3.8 or later
- CUDA Toolkit 11.0 or later

### Environment Setup
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/2.0.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

## Deployment Options

### 1. Docker Deployment (Recommended)

#### Configuration
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    image: raasid-api:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - CUDA_VISIBLE_DEVICES=0
      - MODEL_PATH=/app/models
      - LOG_LEVEL=INFO
    volumes:
      - ./models:/app/models
      - ./logs:/app/logs
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### Deployment Steps
```bash
# Build and start containers
docker-compose up --build -d

# Verify deployment
docker-compose ps
docker-compose logs -f
```

### 2. Kubernetes Deployment

#### Configuration
```yaml
# raasid-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: raasid-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: raasid-api
  template:
    metadata:
      labels:
        app: raasid-api
    spec:
      containers:
      - name: raasid-api
        image: raasid-api:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
        env:
        - name: MODEL_PATH
          value: "/app/models"
        volumeMounts:
        - name: models
          mountPath: "/app/models"
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: raasid-models-pvc
```

#### Deployment Steps
```bash
# Apply configuration
kubectl apply -f raasid-deployment.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

## Configuration

### Environment Variables
```bash
# Required
MODEL_PATH=/app/models
CUDA_VISIBLE_DEVICES=0
LOG_LEVEL=INFO

# Optional
BATCH_SIZE=32
CONFIDENCE_THRESHOLD=0.7
MAX_FRAMES=1000
SKIP_FRAMES=30
```

### Model Configuration
```json
{
    "context_model": {
        "path": "models/context_cnn.pth",
        "input_size": [64, 64],
        "batch_size": 32
    },
    "pose_model": {
        "path": "models/pose_estimator.pth",
        "input_size": [256, 256],
        "batch_size": 16
    },
    "ball_model": {
        "path": "models/ball_detector.pth",
        "input_size": [128, 128],
        "batch_size": 32
    }
}
```

## Monitoring

### System Metrics
```bash
# Install monitoring tools
sudo apt install prometheus node-exporter

# Configure Prometheus
cat <<EOF > prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'raasid'
    static_configs:
      - targets: ['localhost:8000']
EOF
```

### Logging Configuration
```python
# logging.conf
[loggers]
keys=root,raasid

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_raasid]
level=INFO
handlers=fileHandler
qualname=raasid
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=simpleFormatter
args=('logs/raasid.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

## Scaling

### Horizontal Scaling
```bash
# Scale API service
docker-compose up --scale api=3 -d

# Or with Kubernetes
kubectl scale deployment raasid-api --replicas=3
```

### Load Balancing
```nginx
# nginx.conf
upstream raasid_api {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    listen 80;
    server_name api.raasid.com;

    location / {
        proxy_pass http://raasid_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Backup and Recovery

### Data Backup
```bash
# Backup models
tar -czf models_backup.tar.gz models/

# Backup logs
tar -czf logs_backup.tar.gz logs/

# Schedule backups
0 0 * * * /usr/bin/tar -czf /backup/models_$(date +\%Y\%m\%d).tar.gz /app/models
```

### Recovery Procedure
```bash
# Stop services
docker-compose down

# Restore backup
tar -xzf models_backup.tar.gz -C /app/
tar -xzf logs_backup.tar.gz -C /app/

# Restart services
docker-compose up -d
```

## Security

### SSL Configuration
```nginx
# nginx-ssl.conf
server {
    listen 443 ssl;
    server_name api.raasid.com;

    ssl_certificate /etc/letsencrypt/live/api.raasid.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.raasid.com/privkey.pem;

    location / {
        proxy_pass http://raasid_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Firewall Configuration
```bash
# Configure UFW
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw enable
```

## Troubleshooting

### Common Issues

1. **GPU Not Detected**
   ```bash
   # Check NVIDIA drivers
   nvidia-smi
   
   # Verify Docker GPU access
   docker run --gpus all nvidia/cuda:11.0-base nvidia-smi
   ```

2. **High Memory Usage**
   ```bash
   # Monitor memory usage
   docker stats
   
   # Adjust batch size
   export BATCH_SIZE=16
   ```

3. **API Not Responding**
   ```bash
   # Check logs
   docker-compose logs api
   
   # Verify health endpoint
   curl http://localhost:8000/health
   ```

### Support
For deployment support:
- Email: deployment-support@raasid.com
- Documentation: https://raasid.com/docs/deployment
- GitHub Issues: https://github.com/vseel5/raasid-project/issues

---

*Last updated: April 17, 2024*

