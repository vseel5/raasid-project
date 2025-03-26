# Data Strategy – Raasid AI-Powered Handball Detection

## 1. Overview

This document outlines the data collection, preprocessing, labeling, and management strategy used to train and evaluate the AI models in Raasid. A robust and diverse dataset is critical to achieving high-accuracy handball detection and intent classification.

---

## 2. Data Sources

Raasid’s models rely on multimodal inputs from a combination of real and synthetic sources:

| Source | Type | Purpose |
|--------|------|---------|
| VAR Camera Footage | Video | Pose estimation, hand/limb tracking |
| SAOT Sensors | Position | Accurate limb coordinates |
| Smart Ball Sensors | Force/Timing | Impact strength and duration |
| Snickometer Microphones | Audio | Ball-hand contact verification |
| Historical Match Replays | Annotated Video | Ground truth for handball scenarios |
| Simulated Handball Scenarios | Synthetic | Edge case generation and augmentation |

---

## 3. Data Collection Plan

- **Historical Matches**: Acquire publicly available match replays with known handball incidents.
- **Sensor Test Labs**: Conduct controlled simulations using smart ball + snickometer rigs.
- **Synthetic Generation**: Use motion capture and physics simulations to create edge cases (e.g. occluded hands, partial contact).

---

## 4. Data Labeling Strategy

All data is manually or semi-automatically labeled for model training:

| Label | Description |
|-------|-------------|
| `hand_position` | Natural / Unnatural (based on FIFA rules) |
| `ball_contact` | True / False |
| `impact_force` | Measured in Newtons |
| `contact_duration` | Time of contact (seconds) |
| `intent_class` | Intentional / Accidental |
| `rule_violation` | Boolean outcome based on FIFA logic |

> Labeled using in-house tools + review by football domain experts.

---

## 5. Preprocessing Pipeline

Each data stream undergoes specific preprocessing steps:

### Pose Data (Video/Sensor)
- Keypoint extraction (MediaPipe/OpenPose)
- Smoothing via Kalman filters
- Angle and velocity derivation

### Ball Sensor Data
- Outlier removal (Z-score thresholding)
- Unit normalization
- Synchronized with audio signals

### Audio (Snickometer)
- Noise filtering (bandpass)
- Contact peak detection
- Time alignment with ball sensor

---

## 6. Dataset Format & Structure

```plaintext
/dataset/
  ├── raw/
  │     ├── var_video/
  │     ├── ball_sensor/
  │     ├── audio/
  ├── processed/
  │     ├── pose_data.json
  │     ├── ball_contact.csv
  │     ├── labeled_events.json
  ├── annotations/
        ├── handball_events.csv
        ├── intent_labels.csv
```

- All final training data is stored in structured JSON/CSV format.

---

## 7. Data Security & Ethics

- All data complies with FIFA and GDPR data handling policies.
- Personally identifiable data is anonymized.
- Match footage used is either licensed or open-source.

---

## 8. Future Improvements

- Integrate real-time data ingestion from live stadium feeds.
- Increase geographic diversity of training data.
- Build active learning pipeline to auto-improve models using new decisions.

---

## 9. Conclusion

Raasid’s data strategy ensures high-quality, multi-source input for robust AI model training. By combining real-world footage, controlled experiments, and synthetic data, we provide the models with rich, diverse scenarios to reduce bias and improve generalizability.

---