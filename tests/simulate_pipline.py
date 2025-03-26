import requests
import time

BASE_URL = "http://127.0.0.1:8000"

# Step 1: Simulate Pose Estimation AI Output
pose_data = {
    "frame": 1024,
    "hand_position": "unnatural",
    "limb_angles": {"elbow": 120, "shoulder": 45},
    "certainty_score": 94.5
}
res1 = requests.post(f"{BASE_URL}/pose_estimation", json=pose_data)
print("Pose Estimation:", res1.status_code, res1.json())

# Step 2: Simulate Ball Contact AI Output
contact_data = {
    "ball_contact": True,
    "contact_duration": 0.05,
    "force": 3.2,
    "sensor_source": "Smart Ball Sensor"
}
res2 = requests.post(f"{BASE_URL}/ball_contact_ai", json=contact_data)
print("Ball Contact:", res2.status_code, res2.json())

# Step 3: Simulate Event Context AI Output
context_data = {
    "handball_decision": "intentional",
    "certainty": 92.5,
    "rule_violation": True
}
res3 = requests.post(f"{BASE_URL}/event_context_ai", json=context_data)
print("Event Context:", res3.status_code, res3.json())

# Step 4: Simulate Decision-Making Output
final_decision = {
    "frame": 1024,
    "final_decision": "Handball Violation",
    "certainty_score": 95.0,
    "VAR_review": False
}
res4 = requests.post(f"{BASE_URL}/decision_making_ai", json=final_decision)
print("Final Decision:", res4.status_code, res4.json())

# Step 5: Simulate Optional VAR Override
# Uncomment to test VAR override
# var_override = {
#     "frame": 1024,
#     "override_decision": "No Handball"
# }
# res5 = requests.post(f"{BASE_URL}/var_review", json=var_override)
# print("VAR Override:", res5.status_code, res5.json())

# Step 6: Distribute the Final Decision
res6 = requests.post(f"{BASE_URL}/output_distribution")
print("Output Distribution:", res6.status_code, res6.json())
