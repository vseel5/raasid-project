# AI Models – Raasid Handball Detection System

## Overview

Raasid uses a modular AI architecture designed to detect, analyze, and classify handball events in real time. It consists of three core AI models that work together in a sequential and parallel flow. Each model is responsible for a critical layer of understanding that leads to a final decision.

---

## 1. Pose Estimation AI

### Purpose
Analyzes player limb positions to determine whether the hand is in an unnatural position at the moment of potential contact.

### Inputs
- **VAR Camera Footage** – Player movement and posture
- **SAOT Sensor Data** – Real-time limb positioning

### Tasks
- Detect hand and arm locations
- Calculate joint angles (elbow, shoulder)
- Identify unnatural positioning using FIFA rule logic

### Output Example
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

---

## 2. Ball Contact AI

### Purpose
Confirms whether the ball made contact with the player’s hand using physical sensor data.

### Inputs
- **Smart Ball Sensor Logs** – Measures impact force and duration
- **Snickometer Audio Feed** – Detects sound of ball-hand contact

### Tasks
- Validate ball-hand contact event
- Measure intensity and duration
- Check if the contact altered ball trajectory

### Output Example
```json
{
  "frame": 1024,
  "ball_contact": true,
  "impact_force": 3.2,
  "contact_duration": 0.07,
  "sensor_source": "Smart Ball Sensor"
}
```

---

## 3. Event Context AI

### Purpose
Analyzes full context to determine intent and legality of the handball incident.

### Inputs
- **Pose Estimation AI Output**
- **Ball Contact AI Output**

### Tasks
- Assess positioning and timing
- Determine intentional vs. accidental
- Apply FIFA handball rule logic using decision trees

### Output Example
```json
{
  "frame": 1024,
  "handball_decision": "intentional",
  "certainty_score": 92.5,
  "rule_violation": true
}
```

---

## 4. Data Flow Between AI Models

### Processing Sequence
```
Multi-Sensor Fusion AI
         ↓
 ┌─────────────────────────────
 │ Pose Estimation AI │ ┐
 └─────────────────────────────┘
                       ├─> Event Context AI ─> Decision-Making Layer
 ┌─────────────────────────────┐
 │ Ball Contact AI     │ ┘
 └─────────────────────────────┘
```

- **Pose Estimation AI** and **Ball Contact AI** run in parallel.
- **Event Context AI** combines their outputs to make a contextual judgment.

---

## 5. Future Model Enhancements

- Predictive fallback for lost or occluded limb detection.
- Use LSTM for movement pattern analysis pre- and post-contact.
- Expand AI capabilities to cover fouls, offsides, and dives.

---

## Summary

| AI Model             | Role                                        | Output                                |
|----------------------|---------------------------------------------|----------------------------------------|
| Pose Estimation AI   | Detect hand and limb position               | Hand position, angles, certainty       |
| Ball Contact AI      | Confirm ball-hand contact                   | Impact force, duration, confirmation   |
| Event Context AI     | Classify intent and rule violation          | Final classification, confidence score |

These AI models serve as the backbone of Raasid’s decision pipeline, ensuring that each ruling is supported by sensor-validated data, positional analysis, and rule logic.

---

