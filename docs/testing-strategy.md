# Raasid Testing Strategy

## Overview

This document outlines the testing strategy for the Raasid AI-Powered Handball Detection System. It covers all major layers of the system from AI data simulation to frontend interaction, ensuring that each module operates correctly, reliably, and in real-time.

---

## Testing Goals

- Ensure that **each API endpoint** functions as expected.
- Validate the **end-to-end decision flow** from input to output.
- Test **manual override mechanisms** through the VAR interface.
- Simulate realistic match scenarios using test payloads.
- Confirm **frontend-backend communication** is robust.
- Log and resolve bugs through persistent log inspection.

---

## Test Coverage Areas

| Layer                      | Method                        | Tools / Methodology           |
|---------------------------|-------------------------------|-------------------------------|
| API Endpoints (FastAPI)   | Manual & Scripted POSTs       | Postman / Python requests     |
| AI Data Simulators        | JSON test scripts             | Python-based mock inputs      |
| Decision Engine           | Input → Log Validation        | JSON inspection, assertions   |
| VAR Override              | Dashboard + API override      | Browser testing + API trigger |
| Output Distribution       | Mock cloud endpoint logs      | Log response status (200/404) |
| Frontend UI               | Button → API flow             | Live Server + Developer Tools |
| Logging                   | File and console logs         | `logs/server.log`, stdout     |

---

## Test Scenarios

### 1. Pose Estimation AI Simulation
- Send a valid frame payload.
- Check for:
  - API response (`200 OK`)
  - Console log message
  - No errors in backend

### 2. Ball Contact Detection Test
- Send mock ball impact data.
- Confirm:
  - Valid contact payload stored
  - Contact details printed in logs

### 3. Event Context AI Flow
- Trigger with combined inputs.
- Ensure:
  - Decision (e.g. "intentional") is printed
  - Certainty score and rule violation are valid

### 4. Final Decision Submission
- Send final decision payload.
- Confirm:
  - Entry is saved to `data/decision_logs.json`
  - "Decision making processed" response

### 5. VAR Override Scenario
- Use the admin dashboard to:
  - Enter frame ID
  - Submit override
- Check:
  - Decision file updates
  - Confirmation message in UI + backend log

### 6. Distribute Output
- Click "Distribute" button in UI
- Verify:
  - Log shows output sent to: Referee, TV, Cloud
  - Correct payload printed in logs

---

## Testing Tools Used

- **Python `requests`** – For endpoint simulation
- **Postman** – For visual testing and response checking
- **Browser DevTools** – For testing UI interactions
- **Visual Studio Code** – Log file monitoring
- **FastAPI Docs (`/docs`)** – Built-in testing UI

---

## Known Limitations

- No unit testing for AI model logic (currently mocked)
- Not yet integrated with real-time sensor feeds
- No automated CI/CD testing pipeline yet

---

## Future Testing Plans

- Implement **unit tests** using `pytest` or `unittest`
- Add **integration test scripts** for all endpoints
- Build **CI pipeline** with GitHub Actions
- Simulate **edge case scenarios** (e.g., missing data, low confidence)

---

## Summary

This testing strategy ensures Raasid’s MVP is reliable and all key flows work as expected. Manual testing is currently effective for development, and future iterations will introduce automated pipelines for robustness and scalability.

