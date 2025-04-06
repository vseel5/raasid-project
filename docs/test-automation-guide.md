# Test Automation Guide

## Overview
This guide explains how to automate testing for the Raasid system, ensuring that the system remains reliable and efficient as new features are added. By using automated tests, we can catch regressions early, improve code quality, and accelerate the development process. This document covers setting up automated tests for the backend, frontend, and AI models.

## Prerequisites
Before setting up test automation, ensure the following prerequisites are met:

- **Python 3.8+**: Required for running automated tests.
- **pytest**: The testing framework used for unit and integration tests.
- **Selenium**: For end-to-end testing of the frontend.
- **Git**: For version control and continuous integration (CI) pipeline setup.
- **Docker**: For containerized testing environments.
- **CI/CD Tools**: GitHub Actions, Jenkins, or similar for continuous integration.

## Setting Up Automated Tests

### Step 1: Install Dependencies

To start setting up automated tests, install the necessary testing dependencies by running:

```bash
pip install pytest selenium
```

### Step 2: Test Structure
Organize your tests into the following structure:

```
/tests
  /backend
    test_api.py
    test_decision.py
    test_integration.py
  /frontend
    test_ui.py
    test_interactions.py
  /models
    test_model.py
```

- **backend**: Contains tests related to the FastAPI backend (e.g., API endpoint tests, database integration tests).
- **frontend**: Contains tests related to the UI, such as interactions and form submissions using Selenium.
- **models**: Contains tests for the AI models to verify accuracy, input/output format, and edge cases.

### Step 3: Write Unit Tests
Unit tests are designed to verify individual pieces of functionality in the system. Use `pytest` to write unit tests for functions, methods, and classes.

Example of a unit test for a backend API endpoint:

```python
# test_api.py
import pytest
import requests

def test_pose_estimation_api():
    payload = {
        "frame": 1,
        "hand_position": "unnatural",
        "limb_angles": {"elbow": 120.5, "shoulder": 45.2},
        "certainty_score": 92.4
    }
    response = requests.post("http://127.0.0.1:8000/pose_estimation", json=payload)
    assert response.status_code == 200
    assert response.json()['result']['handball_detected'] is not None
```

### Step 4: Integration Tests
Integration tests ensure that different parts of the system work together correctly. For example, you can write tests that verify the end-to-end flow of data through the backend API and AI models.

Example of an integration test:

```python
# test_integration.py
import pytest
import requests

def test_full_integration():
    # Step 1: Send pose estimation data
    pose_data = {
        "frame": 1,
        "hand_position": "unnatural",
        "limb_angles": {"elbow": 120.5, "shoulder": 45.2},
        "certainty_score": 92.4
    }
    pose_response = requests.post("http://127.0.0.1:8000/pose_estimation", json=pose_data)
    assert pose_response.status_code == 200
    
    # Step 2: Send ball contact data
    ball_data = {
        "frame": 1,
        "ball_contact": True,
        "impact_force": 3.2,
        "contact_duration": 0.05,
        "sensor_source": "Smart Ball Sensor"
    }
    ball_response = requests.post("http://127.0.0.1:8000/ball_contact_ai", json=ball_data)
    assert ball_response.status_code == 200
    
    # Step 3: Verify final decision
    final_decision = requests.post("http://127.0.0.1:8000/output_distribution")
    assert final_decision.status_code == 200
    assert "decision" in final_decision.json()
```

### Step 5: End-to-End Tests with Selenium
End-to-end tests simulate user interactions with the frontend to ensure that the system behaves as expected. For this, we use **Selenium** to automate browser interactions.

Example of a basic Selenium test:

```python
# test_ui.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_ui_interaction():
    driver = webdriver.Chrome()
    driver.get("http://localhost:8501")  # Adjust this URL to your local Streamlit app

    # Find the file uploader element and upload a test file
    upload_element = driver.find_element(By.XPATH, '//*[@id="fileUploader"]')
    upload_element.send_keys("/path/to/testfile.mp4")

    # Submit and check the result
    submit_button = driver.find_element(By.XPATH, '//*[@id="submitButton"]')
    submit_button.click()

    result_text = driver.find_element(By.XPATH, '//*[@id="result"]')
    assert "Decision Ready" in result_text.text

    driver.quit()
```

### Step 6: Continuous Integration (CI) Setup
To automate the testing process, integrate the tests into a CI pipeline (e.g., GitHub Actions, Jenkins).

#### Example GitHub Actions Workflow:

```yaml
name: CI Workflow

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install -r requirements.txt

      - name: Run tests
        run: |
          source venv/bin/activate
          pytest --maxfail=1 --disable-warnings -q
```

This configuration will run the tests automatically whenever there is a push to the `main` branch.

## Best Practices

- **Write small, focused tests**: Each test should focus on testing a single piece of functionality.
- **Use meaningful assertions**: Ensure that assertions clearly verify the expected behavior of the system.
- **Test edge cases**: Ensure that edge cases and unexpected inputs are tested to make the system more robust.
- **Test frequently**: Run tests frequently, especially before deploying new changes to production.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)
