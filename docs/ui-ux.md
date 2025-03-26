# Raasid UI/UX Design Documentation

## Overview

The Raasid Admin Dashboard serves as the central interface for referees, system operators, and reviewers to interact with the AI-Powered Handball Detection System. The design emphasizes clarity, accessibility, and operational efficiency.

---

## Design Goals

- Provide real-time control and visibility over AI decisions
- Simplify the referee override workflow
- Enable easy inspection of decision logs
- Maintain a clean and modern interface using minimal resources

---

## UI Features Breakdown

| Section          | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| System Status    | Displays whether the FastAPI backend is running                             |
| Decision Logs    | Allows users to load and view historical decisions from persistent storage  |
| VAR Override     | Enables manual adjustment of AI decisions by frame number                   |
| Output Delivery  | Simulates broadcasting decisions to all stakeholders (Ref, VAR, TV, Cloud)  |

---

## Interface Components

### 1. **System Status Panel**
- **Button:** "Check API"
- **Function:** Sends a GET request to the `/` root endpoint
- **Feedback:** Displays "Checking..." → "Raasid API is running" or an error

### 2. **Decision Logs Panel**
- **Button:** "Load Logs"
- **Function:** Fetches and displays contents of `decision_logs.json`
- **Display:** `pre` block styled for readability with scroll and formatting

### 3. **VAR Override Panel**
- **Inputs:**
  - Frame Number (`input[type=number]`)
  - New Decision (`input[type=text]`)
- **Button:** "Submit Override"
- **Function:** Sends `POST` request to `/var_review`
- **Feedback:** Shows status message (success or frame not found)

### 4. **Output Distribution Panel**
- **Button:** "Distribute Output"
- **Function:** Sends a `POST` request to `/output_distribution`
- **Feedback:** Shows confirmation of where the decision was sent

---

## Visual Styling Summary

- **Framework:** Vanilla CSS (custom, lightweight)
- **Fonts:** Segoe UI (clean, accessible)
- **Colors:** Neutral background with strong action color (#2563eb)
- **Layout:**
  - Card-based sections (using `section`)
  - Responsive, centered design with a max-width container
- **Interactions:**
  - Button hover states
  - Live updates on action (status text changes)

---

## UX Considerations

| Area               | UX Strategy                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Speed              | Optimized for fast interactions with low-latency local backend              |
| Clarity            | Simple language for buttons and messages                                    |
| Feedback           | Each button shows real-time feedback (e.g., "Submitting...", "Loading...") |
| Accessibility      | Keyboard-friendly, large buttons, readable font sizes                      |
| Maintainability    | Separation of concerns: HTML, CSS, and JS are modular                       |

---

## Frontend Testing

- **Live Server Preview** via VS Code
- **Simulated API Calls** connected to FastAPI backend
- **Input Validation** (basic: frame number required, empty override check)
- **Responsive Behavior** tested on small screens

---

## Future Enhancements

- Timeline View for chronological decision playback
- Dark Mode toggle for late-night matches or broadcast settings
- Role-based UI (referee vs admin)
- Real-time explanation overlays and animations
- Localization support (multi-language dashboard)

---

## Summary

The Raasid Admin Dashboard is clean, functional, and tightly coupled to the backend decision engine. It serves both as an operational panel and a foundation for advanced features in the future MVP versions.
