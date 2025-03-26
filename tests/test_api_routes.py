import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import httpx
from api.main import app

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_pose_estimation():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/pose_estimation", json={
            "frame": 123,
            "hand_position": "unnatural",
            "limb_angles": {"elbow": 120, "shoulder": 40},
            "certainty_score": 95.0
        })
        assert response.status_code == 200
        assert response.json()["status"] == "Success"

@pytest.mark.asyncio
async def test_ball_contact():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/ball_contact_ai", json={
            "frame": 123,
            "ball_contact": True,
            "impact_force": 3.5,
            "contact_duration": 0.05,
            "sensor_source": "Smart Ball"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "Success"

@pytest.mark.asyncio
async def test_final_decision_with_reason():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Certainty < 95 should trigger low-confidence reason
        response = await client.post("/decision_making_ai", json={
            "frame": 999,
            "final_decision": "Handball Violation",
            "certainty_score": 89.5,
            "VAR_review": False
        })
        assert response.status_code == 200
        data = response.json()
        assert "reason" in data
        assert data["reason"] == "Uncertain decision — confidence below 95%"

@pytest.mark.asyncio
async def test_final_decision_natural_hand():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/decision_making_ai", json={
            "frame": 1000,
            "final_decision": "No Handball",
            "certainty_score": 97.0,
            "VAR_review": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["reason"] == "Hand position judged natural; no violation"


@pytest.mark.asyncio
async def test_event_context():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/event_context_ai", json={
            "frame": 123,
            "handball_decision": "intentional",
            "certainty_score": 91.0,
            "rule_violation": True
        })
        assert response.status_code == 200
        assert response.json()["status"] == "Success"

@pytest.mark.asyncio
async def test_final_decision():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/decision_making_ai", json={
            "frame": 123,
            "final_decision": "Handball Violation",
            "certainty_score": 94.5,
            "VAR_review": False
        })
        assert response.status_code == 200
        assert response.json()["status"] == "Success"

@pytest.mark.asyncio
async def test_var_override():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/var_review", json={
            "frame": 123,
            "override_decision": "No Handball"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "Success"

# Invalid input test – should return 422
@pytest.mark.asyncio
async def test_pose_estimation_invalid():
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/pose_estimation", json={
            "frame": 123,
            "hand_position": "flying",  # invalid
            "limb_angles": {"elbow": 120},
            "certainty_score": 150.0     # invalid > 100
        })
        assert response.status_code == 422





