# Raasid System Architecture

## Overview
Raasid is structured into five distinct layers for modularity and clarity. Each layer is responsible for a specific function and integrates with the next to create a real-time AI-powered handball detection system.


## 1. Data Capture Layer

**Sources:**
- VAR Cameras
- SAOT Sensors
- Smart Ball Sensors
- Snickometer Microphones

**Responsibilities:**
- Captures live match data (video, audio, sensor).
- Synchronizes signals with timestamp metadata.

---

## 2. Multi-Sensor Fusion Layer

**Purpose:**
- Combines heterogeneous sensor data.
- Aligns and filters signals for consistency.
- Generates structured input packages for the AI layer.

---

## 3. AI Processing Layer

**Components:**
- Pose Estimation AI
- Ball Contact AI
- Event Context AI

**Flow:**
- Pose & Ball Contact run in parallel.
- Event Context receives both outputs for final classification.

---

## 4. Decision-Making Layer

**Responsibilities:**
- Applies FIFA handball rulebook.
- Scores confidence of the AI decision.
- Sends to VAR if below 95% confidence.

---

## 5. Output Distribution Layer

**Integrations:**
- Referee Smartwatch
- VAR Room
- Broadcasters (TV overlays)
- Cloud Storage

**Function:**
- Sends final decision with explanation and certainty score to all stakeholders in real time.

---

## Architecture Diagram

```plaintext
[Camera + Sensor Data]
        ↓
[Multi-Sensor Fusion AI]
        ↓
┌────────────┬────────────┐
│ Pose AI    │ Ball AI    │
└────────────┴────────────┘
        ↓
[Event Context AI]
        ↓
[Decision Engine + Rulebook]
        ↓
[Smartwatch | TV | VAR | Cloud]
