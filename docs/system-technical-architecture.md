# Raasid System Architecture & Data Flow

## 1. Overview

This document outlines the overall architecture of the Raasid AI-Powered Handball Detection System. It details the data flow between components, the system layers, and integration with external systems to ensure accurate, real-time decision-making in football matches.

---

## 2. Layered Architecture

Raasid is structured into a modular five-layer architecture:

### 2.1 Data Capture Layer
- **Purpose:** Collects real-time data from match hardware.
- **Components:**
  - VAR Cameras
  - SAOT Sensors
  - Smart Ball Sensors
  - Snickometer Microphones

### 2.2 Multi-Sensor Fusion AI
- **Purpose:** Synchronizes, filters, and formats raw sensor data.
- **Functionality:**
  - Timestamp alignment across sensors
  - Noise reduction and signal normalization
  - Converts raw input into structured data packets

### 2.3 AI Processing Layer
- **Purpose:** Executes AI models to extract insights.
- **Subcomponents:**
  - Pose Estimation AI
  - Ball Contact AI
  - Event Context AI
- **Data Flow:** Pose and Ball Contact AI run in parallel → results fed into Event Context AI sequentially.

### 2.4 Decision-Making Layer
- **Purpose:** Applies FIFA handball rules and confidence scoring.
- **Key Elements:**
  - Rule engine
  - VAR override logic
  - Final decision confidence calculation

### 2.5 Output Layer
- **Purpose:** Distributes decisions to stakeholders.
- **Endpoints:**
  - Referee Smartwatch
  - VAR Replay System
  - TV Broadcast API
  - Cloud Storage for analytics

---

## 3. Component Communication & Data Flow

### 3.1 High-Level Data Flow
```
Match Hardware
   ↓
Data Capture Layer
   ↓
Multi-Sensor Fusion AI
   ↓
 ┌────────────┐  ┌────────────┐
 │ Pose AI    │  │ Ball AI    │  (Parallel)
 └────────────┘  └────────────┘
        ↓              ↓
     Event Context AI  (Sequential)
        ↓
   Decision-Making Layer
        ↓
      Output Layer
```

### 3.2 API Endpoint Summary
| **Endpoint** | **Route** | **Description** |
|--------------|------------|-----------------|
| Root Check | `/` | Health check endpoint |
| Pose AI | `/pose_estimation` | Receives hand & limb data |
| Ball Contact AI | `/ball_contact_ai` | Receives contact force/duration data |
| Event Context AI | `/event_context_ai` | Receives combined analysis for intent |
| Decision AI | `/decision_making_ai` | Logs and stores final decision |
| VAR Override | `/var_review` | Enables referee to modify AI decision |
| Output Distribution | `/output_distribution` | Sends decisions to all output systems |
| Logs View | `/decision_logs` | Shows stored decision history |

---

## 4. Reliability Features

### 4.1 AI Failure Handling
| **Failure Type** | **Fallback Mechanism** |
|------------------|-------------------------|
| Pose not detected | Secondary camera, predictive estimation |
| Contact confidence low | Cross-verify with Snickometer |
| System uncertainty | Escalate to VAR for manual review |

### 4.2 Uptime & Redundancy
- Cloud + Edge AI fallback
- Persistent JSON logging for crash recovery
- Automated health checks via root endpoint

---

## 5. Security & Privacy
- HTTPS communication (in production)
- Role-based access for referees and officials
- Data encryption for cloud-stored logs

---

## 6. Conclusion

Raasid's architecture is designed for real-time, resilient, and transparent officiating. Its layered modular system ensures that handball decisions are made with high confidence and seamlessly distributed across all necessary channels.

