# API Reference Documentation

## Version Information
- **API Version**: 1.0.0
- **Base URL**: `http://localhost:8000`
- **Last Updated**: April 17, 2024

## Table of Contents
1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
3. [Data Models](#data-models)
4. [Error Handling](#error-handling)
5. [Rate Limiting](#rate-limiting)
6. [WebSocket Support](#websocket-support)

## Authentication

### API Key
All endpoints require an API key for authentication. Include the key in the request header:

```http
Authorization: Bearer your-api-key
```

### Key Management
- Keys can be generated through the admin dashboard
- Keys have specific permissions and expiration dates
- Rate limits are enforced per key

## Endpoints

### 1. Pose Estimation

#### POST /api/v1/pose/estimate
Estimates player pose from video frame.

**Request Body**:
```json
{
    "frame_data": {
        "image": "base64_encoded_image",
        "timestamp": "2024-04-17T12:00:00Z",
        "frame_number": 123
    },
    "parameters": {
        "confidence_threshold": 0.7,
        "max_players": 2
    }
}
```

**Response**:
```json
{
    "status": "success",
    "data": {
        "pose_data": {
            "keypoints": [...],
            "hand_positions": [...],
            "body_orientation": [...]
        },
        "confidence": 0.95,
        "processing_time": 45
    },
    "metadata": {
        "timestamp": "2024-04-17T12:00:00.045Z",
        "version": "1.0.0"
    }
}
```

### 2. Ball Detection

#### POST /api/v1/ball/detect
Detects ball position and movement.

**Request Body**:
```json
{
    "frame_data": {
        "image": "base64_encoded_image",
        "timestamp": "2024-04-17T12:00:00Z",
        "frame_number": 123
    },
    "parameters": {
        "confidence_threshold": 0.8,
        "track_velocity": true
    }
}
```

**Response**:
```json
{
    "status": "success",
    "data": {
        "ball_position": [x, y],
        "velocity": [vx, vy],
        "confidence": 0.92,
        "processing_time": 30
    },
    "metadata": {
        "timestamp": "2024-04-17T12:00:00.030Z",
        "version": "1.0.0"
    }
}
```

### 3. Context Analysis

#### POST /api/v1/context/analyze
Analyzes game context and player intent.

**Request Body**:
```json
{
    "frame_data": {
        "image": "base64_encoded_image",
        "timestamp": "2024-04-17T12:00:00Z",
        "frame_number": 123
    },
    "pose_data": {
        "keypoints": [...],
        "hand_positions": [...]
    },
    "ball_data": {
        "position": [x, y],
        "velocity": [vx, vy]
    }
}
```

**Response**:
```json
{
    "status": "success",
    "data": {
        "game_situation": "defensive_block",
        "player_intent": "deliberate",
        "confidence": 0.88,
        "processing_time": 60
    },
    "metadata": {
        "timestamp": "2024-04-17T12:00:00.060Z",
        "version": "1.0.0"
    }
}
```

### 4. Decision Making

#### POST /api/v1/decision/make
Makes final handball decision.

**Request Body**:
```json
{
    "pose_analysis": {
        "keypoints": [...],
        "hand_positions": [...],
        "confidence": 0.95
    },
    "ball_analysis": {
        "position": [x, y],
        "velocity": [vx, vy],
        "confidence": 0.92
    },
    "context_analysis": {
        "game_situation": "defensive_block",
        "player_intent": "deliberate",
        "confidence": 0.88
    }
}
```

**Response**:
```json
{
    "status": "success",
    "data": {
        "decision": "handball",
        "confidence": 0.92,
        "explanation": "Deliberate handball in defensive block situation",
        "processing_time": 75
    },
    "metadata": {
        "timestamp": "2024-04-17T12:00:00.075Z",
        "version": "1.0.0"
    }
}
```

## Data Models

### FrameData
```python
class FrameData(BaseModel):
    image: str  # base64 encoded
    timestamp: datetime
    frame_number: int
```

### PoseData
```python
class PoseData(BaseModel):
    keypoints: List[Tuple[float, float]]
    hand_positions: List[Tuple[float, float]]
    body_orientation: List[float]
    confidence: float
```

### BallData
```python
class BallData(BaseModel):
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    confidence: float
```

### ContextData
```python
class ContextData(BaseModel):
    game_situation: str
    player_intent: str
    confidence: float
```

## Error Handling

### Error Response Format
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Human-readable error message",
        "details": {
            "field": "additional error details"
        }
    },
    "metadata": {
        "timestamp": "2024-04-17T12:00:00Z",
        "version": "1.0.0"
    }
}
```

### Common Error Codes
- `INVALID_API_KEY`: Invalid or missing API key
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `INVALID_REQUEST`: Malformed request body
- `PROCESSING_ERROR`: Error during processing
- `SERVICE_UNAVAILABLE`: Service temporarily unavailable

## Rate Limiting

### Limits
- 100 requests per minute per API key
- 1000 requests per hour per API key

### Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1620000000
```

## WebSocket Support

### Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/v1/analysis');
```

### Events
- `frame_processed`: Frame analysis complete
- `decision_made`: Handball decision made
- `error`: Processing error occurred

### Example
```javascript
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch (data.type) {
        case 'frame_processed':
            handleFrameProcessed(data);
            break;
        case 'decision_made':
            handleDecision(data);
            break;
        case 'error':
            handleError(data);
            break;
    }
};
```

## Best Practices

### Request Optimization
1. Use appropriate image compression
2. Batch requests when possible
3. Implement proper error handling
4. Monitor rate limits

### Response Handling
1. Check status codes
2. Validate response data
3. Implement retry logic
4. Cache responses when appropriate

### Security
1. Keep API keys secure
2. Use HTTPS in production
3. Validate all input data
4. Monitor usage patterns

## Support
For API support and questions:
- Email: api-support@raasid.com
- Documentation: https://raasid.com/docs/api
- GitHub Issues: https://github.com/vseel5/raasid-project/issues

---

*Last updated: April 17, 2024*