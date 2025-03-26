# Admin Dashboard – Raasid VAR System

## 1. Overview

The Admin Dashboard is a simple web interface that allows referees, officials, and developers to interact with the Raasid backend services. It enables manual overrides, log inspection, system health monitoring, and output distribution – all from a centralized visual panel.

---

## 2. Purpose

- Provide a frontend interface for API interaction
- Allow referees to override AI decisions (VAR)
- View logged decision data for analysis
- Distribute final decisions to output channels (TV, cloud, smartwatch)

---

## 3. Features & UI Layout

The dashboard is composed of four main sections:

### 3.1 System Status

| **Function** | **Description** |
|--------------|------------------|
| `Check API`  | Sends a GET request to `/` to verify if the backend is running. |
| **Feedback** | Displays "Raasid API is running" or error message. |

---

### 3.2 Decision Logs

| **Function**   | **Description** |
|----------------|------------------|
| `Load Logs`    | Fetches data from `/decision_logs` |
| **Output**     | Displays all previous decision-making entries in formatted JSON. |

---

### 3.3 VAR Override

| **Inputs**          | **Purpose**                        |
|----------------------|------------------------------------|
| `Frame Number`        | Identifies the decision to override |
| `New Decision Text`   | The updated decision by the referee |

| **Action**         | Sends POST to `/var_review` with new override |
|--------------------|-----------------------------------------------|
| `Submit Override`  | Triggers update of the decision JSON & log     |

---

### 3.4 Output Distribution

| **Function**        | **Description**                                        |
|---------------------|--------------------------------------------------------|
| `Distribute Output` | Sends the latest decision to TV, smartwatch, and cloud |
| **API Endpoint**    | POST request to `/output_distribution`                 |

---

## 4. Technologies Used

| **Component** | **Stack**                      |
|---------------|--------------------------------|
| Frontend      | HTML, CSS, JavaScript          |
| Backend API   | FastAPI (`http://127.0.0.1:8000`) |
| Preview Tool  | Live Server (VS Code Extension) |

---

## 5. File Structure

```plaintext
frontend/
├── index.html      # Main dashboard HTML
├── style.css       # UI styling
└── script.js       # API interaction logic
```

---

## 6. Sample Interactions

### 6.1 API Health Check

```bash
GET http://127.0.0.1:8000/
Response: { "message": "Raasid API is running" }
```

---

### 6.2 Load Logs

```bash
GET http://127.0.0.1:8000/decision_logs
Response: [
  {
    "frame": 1024,
    "final_decision": "Handball Violation",
    "certainty_score": 95.0,
    "VAR_review": false
  }
]
```

---

### 6.3 Submit Override

```bash
POST http://127.0.0.1:8000/var_review
Payload:
{
  "frame": 1024,
  "override_decision": "No Handball"
}
```

---

### 6.4 Distribute Final Decision

```bash
POST http://127.0.0.1:8000/output_distribution
```

---

## 7. Future Enhancements

- Real-time timeline visualization with event playback
- Decision certainty graph or meter
- Notification system for VAR officials
- Role-based login for secure access

---

## 8. Conclusion

The Admin Dashboard serves as the control center for human review, decision distribution, and system health monitoring in the Raasid ecosystem. While simple by design, it plays a critical role in verifying and validating AI-powered officiating in real time.

