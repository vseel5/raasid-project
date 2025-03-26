import time
import random
import requests

BASE_URL = "http://127.0.0.1:8000"

# Define how many simulated frames you want to send
NUM_FRAMES = 5

def simulate_pose_estimation(frame):
    data = {
        "frame": frame,
        "hand_position": random.choice(["natural", "unnatural"]),
        "limb_angles": {
            "elbow": random.randint(90, 140),
            "shoulder": random.randint(30, 60)
        },
        "certainty_score": round(random.uniform(85, 98), 2)
    }
    r = requests.post(f"{BASE_URL}/pose_estimation", json=data)
    print(f"Pose Estimation Sent (Frame {frame}):", r.status_code)

def simulate_ball_contact(frame):
    data = {
        "frame": frame,
        "ball_contact": random.choice([True, False]),
        "impact_force": round(random.uniform(1.5, 4.0), 2),
        "contact_duration": round(random.uniform(0.03, 0.09), 2),
        "sensor_source": "Smart Ball Sensor"
    }
    r = requests.post(f"{BASE_URL}/ball_contact_ai", json=data)
    print(f"Ball Contact Sent (Frame {frame}):", r.status_code)

def simulate_event_context(frame):
    decision = random.choice(["intentional", "accidental"])
    rule_violation = decision == "intentional"
    data = {
        "frame": frame,
        "handball_decision": decision,
        "certainty_score": round(random.uniform(85, 98), 2),
        "rule_violation": rule_violation
    }
    r = requests.post(f"{BASE_URL}/event_context_ai", json=data)
    print(f"Event Context Sent (Frame {frame}):", r.status_code)

def simulate_final_decision(frame):
    decision = random.choice(["Handball Violation", "No Handball"])
    certainty = round(random.uniform(89, 99), 2)
    var_review = certainty < 95

    data = {
        "frame": frame,
        "final_decision": decision,
        "certainty_score": certainty,
        "VAR_review": var_review
    }
    r = requests.post(f"{BASE_URL}/decision_making_ai", json=data)
    print(f"Final Decision Sent (Frame {frame}):", r.status_code)

# -------- Run Simulation --------
for i in range(NUM_FRAMES):
    frame_id = 1000 + i

    simulate_pose_estimation(frame_id)
    time.sleep(0.5)

    simulate_ball_contact(frame_id)
    time.sleep(0.5)

    simulate_event_context(frame_id)
    time.sleep(0.5)

    simulate_final_decision(frame_id)
    time.sleep(1)

print("Simulation complete.")
