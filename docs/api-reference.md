# Raasid API Reference

This document serves as the full API reference for the Raasid AI-Powered Handball Detection System. It outlines available endpoints, request/response formats, and error-handling behavior for developers and integrators.

---

## Root Endpoint

### `GET /`
Returns a simple health check to confirm that the API is live.

#### Response:
```json
{ "message": "Raasid API is running" }
```

---

## AI Input Endpoints

### `POST /pose_estimation`

Accepts limb position data from Pose Estimation AI.

#### Request Body:
```json
{
  "frame": 1024,
  "hand_position": "unnatural",
  "limb_angles": {
    "elbow": 120,
    "shoulder": 45
  },
  "certainty_score": 94.5
}
```

#### Response:
```json
{ "status": "Success", "message": "Pose estimation processed" }
```

---

### `POST /ball_contact_ai`

Receives ball-hand impact data from smart ball and audio sensors.

#### Request Body:
```json
{
  "frame": 1024,
  "ball_contact": true,
  "impact_force": 3.2,
  "contact_duration": 0.07,
  "sensor_source": "Smart Ball Sensor"
}
```

#### Response:
```json
{ "status": "Success", "message": "Ball contact processed" }
```

---

### `POST /event_context_ai`

Consumes combined analysis from Pose and Ball Contact AI to classify handball intent.

#### Request Body:
```json
{
  "frame": 1024,
  "handball_decision": "intentional",
  "certainty_score": 92.5,
  "rule_violation": true
}
```

#### Response:
```json
{ "status": "Success", "message": "Event context processed" }
```

---

## Decision-Making Layer

### `POST /decision_making_ai`

Receives the final AI decision. Stores it persistently and logs it.

#### Request Body:
```json
{
  "frame": 1024,
  "final_decision": "Handball Violation",
  "certainty_score": 93.5,
  "VAR_review": false
}
```

#### Response:
```json
{ "status": "Success", "message": "Decision making processed" }
```

---

## VAR Review Endpoint

### `POST /var_review`

Allows manual override of an AI decision via referee input.

#### Request Body:
```json
{
  "frame": 1024,
  "override_decision": "No Handball"
}
```

#### Response:
```json
{ "status": "Success", "message": "VAR decision updated" }
```

#### If frame not found:
```json
{ "status": "Error", "message": "Frame not found for review" }
```

---

## Output Distribution

### `POST /output_distribution`

Distributes the latest AI decision to referee smartwatch, VAR, TV broadcast, and cloud (simulated).

#### Response:
```json
{ "status": "Success", "message": "Decision distributed successfully" }
```

#### If no decision exists:
```json
{ "status": "Error", "message": "No decisions available" }
```

---

## Decision Log Retrieval

### `GET /decision_logs`

Returns the full list of stored decisions from persistent memory.

#### Response:
```json
[
  {
    "frame": 1024,
    "final_decision": "Handball Violation",
    "certainty_score": 93.5,
    "VAR_review": true
  },
  ...
]
```

---

## Error Handling

- All endpoints return meaningful `status` and `message` fields.
- Status codes follow HTTP conventions (`200`, `400`, etc.).
- Backend logs every call in `logs/server.log`.

---

## Testing Tips

You can test these endpoints using:
- Python `requests` module
- Postman or Insomnia REST clients
- The built-in Admin Dashboard in `frontend/index.html`

---

## Notes

- All endpoints accept `application/json` payloads.
- CORS is enabled for local testing via browser dashboard.
- Logging is enabled in `logs/server.log`.

