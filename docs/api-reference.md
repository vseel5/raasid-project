# API Reference

## Overview
The API Reference provides a detailed overview of the available endpoints in the Raasid system, allowing developers to interact with the AI models and access system functionalities. This API is designed to handle requests related to pose estimation, ball contact detection, event context classification, and decision-making for football officiating. It also supports external system integrations for real-time decision distribution.

## Base URL
The base URL for the API is:
```
http://127.0.0.1:8000
```

## Endpoints

### 1. Pose Estimation
**Endpoint**: `/pose_estimation`  
**Method**: `POST`  
**Description**: Accepts pose estimation data, including hand positioning and limb angles, to assess the likelihood of a handball incident.  
**Request Body**:
```json
{
  "frame": 1,
  "hand_position": "unnatural",
  "limb_angles": {
    "elbow": 120.5,
    "shoulder": 45.2
  },
  "certainty_score": 92.4
}
```
**Response**:
```json
{
  "handball_detected": true,
  "intentional": true,
  "confidence_score": 85.3,
  "contact_duration": 0.043,
  "impact_force": 3.45,
  "pose_unusual": true
}
```
**Status Codes**:
- `200 OK`: Successful pose estimation.
- `400 Bad Request`: Invalid input data.

### 2. Ball Contact Detection
**Endpoint**: `/ball_contact_ai`  
**Method**: `POST`  
**Description**: Accepts sensor data to detect whether the ball made contact with the player and returns the impact force and contact duration.  
**Request Body**:
```json
{
  "frame": 1,
  "ball_contact": true,
  "impact_force": 3.4,
  "contact_duration": 0.05,
  "sensor_source": "Smart Ball Sensor"
}
```
**Response**:
```json
{
  "ball_contact": true,
  "impact_force": 3.4,
  "contact_duration": 0.05
}
```
**Status Codes**:
- `200 OK`: Successful detection of ball contact.
- `400 Bad Request`: Invalid input data.

### 3. Event Context Classification
**Endpoint**: `/event_context_ai`  
**Method**: `POST`  
**Description**: Accepts event context data to classify the handball as intentional or accidental and checks if the incident violates FIFA rules.  
**Request Body**:
```json
{
  "frame": 1,
  "handball_decision": "intentional",
  "certainty_score": 85.2,
  "rule_violation": true
}
```
**Response**:
```json
{
  "handball_decision": "intentional",
  "certainty_score": 85.2,
  "rule_violation": true
}
```
**Status Codes**:
- `200 OK`: Successful classification of event context.
- `400 Bad Request`: Invalid input data.

### 4. Decision Making
**Endpoint**: `/decision_making_ai`  
**Method**: `POST`  
**Description**: Accepts inputs from pose estimation, ball contact detection, and event context classification, and returns the final decision (handball or no handball).  
**Request Body**:
```json
{
  "pose_estimation": {
    "hand_position": "unnatural",
    "limb_angles": {"elbow": 110.2, "shoulder": 45.3},
    "certainty_score": 90.1
  },
  "ball_contact": {
    "ball_contact": true,
    "impact_force": 4.0,
    "contact_duration": 0.06
  },
  "event_context": {
    "handball_decision": "accidental",
    "certainty_score": 88.7,
    "rule_violation": false
  }
}
```
**Response**:
```json
{
  "final_decision": "No Handball",
  "certainty_score": 90.1
}
```
**Status Codes**:
- `200 OK`: Successful decision making.
- `400 Bad Request`: Invalid input data.

### 5. VAR Review
**Endpoint**: `/var_review`  
**Method**: `POST`  
**Description**: Allows a manual VAR override of AI decisions.  
**Request Body**:
```json
{
  "frame": 1,
  "override_decision": "Handball - Penalty"
}
```
**Response**:
```json
{
  "status": "Success",
  "message": "Decision overridden successfully"
}
```
**Status Codes**:
- `200 OK`: Successful override.
- `400 Bad Request`: Invalid input data.

### 6. Output Distribution
**Endpoint**: `/output_distribution`  
**Method**: `POST`  
**Description**: Simulates sending the final decision to external systems such as the referee smartwatch, TV broadcast, and cloud storage.  
**Response**:
```json
{
  "status": "Success",
  "message": "Decision distributed to all endpoints",
  "distribution_id": "a1b2c3d4-5678-9012-efgh-3456789abcd",
  "timestamp": "2025-04-06T15:22:01.456Z",
  "delivered_to": ["Referee Smartwatch", "TV Broadcast", "Cloud Storage"]
}
```
**Status Codes**:
- `200 OK`: Successful distribution.
- `500 Internal Server Error`: Failure to distribute decision.

### 7. Decision Logs
**Endpoint**: `/decision_logs`  
**Method**: `GET`  
**Description**: Retrieves logs of all decisions made by the system, providing transparency and auditability.  
**Response**:
```json
[
  {
    "decision_id": "6d0a16a7-7572-43b0-965b-32c892d1e1b5",
    "frame": 1,
    "final_decision": "No Handball",
    "certainty_score": 90.1,
    "timestamp": "2025-04-06T15:22:01.456Z"
  },
  {
    "decision_id": "a1b2c3d4-5678-9012-efgh-3456789abcd",
    "frame": 2,
    "final_decision": "Handball - Penalty",
    "certainty_score": 85.3,
    "timestamp": "2025-04-06T15:23:01.789Z"
  }
]
```
**Status Codes**:
- `200 OK`: Successfully retrieved decision logs.
- `500 Internal Server Error`: Failure to retrieve decision logs.

## Authentication
Currently, the API does not require authentication for local testing. However, for production environments, it is recommended to implement OAuth or JWT authentication to secure the endpoints.

## Error Handling
The API returns standard HTTP status codes to indicate the success or failure of a request:

- `200 OK`: The request was successful, and the response contains the requested data.
- `400 Bad Request`: The request was malformed or missing required data.
- `500 Internal Server Error`: An error occurred on the server, and the request could not be processed.

For each endpoint, additional error messages may be provided in the response body to help with debugging.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)