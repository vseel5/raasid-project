import requests

BASE = "http://127.0.0.1:8000"

# Pose Estimation
pose_data = {
    "frame": 101,
    "hand_position": "unnatural",
    "limb_angles": {"elbow": 120, "shoulder": 45},
    "certainty_score": 94.5
}
pose_res = requests.post(f"{BASE}/pose_estimation", json=pose_data)
print("Pose:", pose_res.status_code, pose_res.json())

# Ball Contact
contact_data = {
    "frame": 101,
    "ball_contact": True,
    "impact_force": 3.2,
    "contact_duration": 0.05,
    "sensor_source": "Smart Ball Sensor"
}
contact_res = requests.post(f"{BASE}/ball_contact_ai", json=contact_data)
print("Contact:", contact_res.status_code, contact_res.json())

# Event Context
context_data = {
    "frame": 101,
    "handball_decision": "intentional",
    "certainty_score": 91.0,
    "rule_violation": True
}
context_res = requests.post(f"{BASE}/event_context_ai", json=context_data)
print("Context:", context_res.status_code, context_res.json())

# Final Decision
final_data = {
    "frame": 101,
    "final_decision": "Handball Violation",
    "certainty_score": 95.1,
    "VAR_review": False
}
final_res = requests.post(f"{BASE}/decision_making_ai", json=final_data)
print("Final Decision:", final_res.status_code, final_res.json())

# VAR Override (Optional)
override_data = {
    "frame": 101,
    "override_decision": "No Handball"
}
override_res = requests.post(f"{BASE}/var_review", json=override_data)
print("VAR Override:", override_res.status_code, override_res.json())

""" bad_pose = {
    "frame": 101,
    "hand_position": "weird",  # invalid
    "limb_angles": {"elbow": 120},
    "certainty_score": 200     # invalid
}
res = requests.post(f"{BASE}/pose_estimation", json=bad_pose)
print("Bad Pose Test:", res.status_code, res.text)
"
"""

