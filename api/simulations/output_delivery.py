import json
import requests
import logging

logging.basicConfig(level=logging.INFO)



# Load final decision data
with open("final_decision_output.json", "r") as f:
    decision_data = json.load(f)



# Simulated Endpoints (Replace with actual API endpoints)
# Corrected URLs using port 8000
REFEREE_SMARTWATCH_API = "http://127.0.0.1:8000/referee_smartwatch"
VAR_REPLAY_SYSTEM_API = "http://127.0.0.1:8000/var_replay"
TV_BROADCAST_API = "http://127.0.0.1:8000/tv_broadcast"
CLOUD_STORAGE_API = "http://127.0.0.1:8000/cloud_storage"



def send_to_referee_smartwatch(decision):
    """ Sends decision notification to the referee's smartwatch. """
    payload = {
        "frame": decision["frame"],
        "final_decision": decision["final_decision"],
        "certainty_score": decision["certainty_score"]
    }
    response = requests.post(REFEREE_SMARTWATCH_API, json=payload)
    logging.info(f"Sent to Referee Smartwatch: {response.status_code}")



def send_to_var_replay(decision):
    """ Sends replay request to VAR system if a review is needed. """
    if decision["VAR_review_needed"]:
        payload = {"frame": decision["frame"], "reason": "VAR Review Required"}
        response = requests.post(VAR_REPLAY_SYSTEM_API, json=payload)
        logging.info(f"Sent to VAR Replay System: {response.status_code}")



def send_to_tv_broadcast(decision):
    """ Sends AI-generated decision overlays to TV broadcasts. """
    payload = {
        "frame": decision["frame"],
        "decision": decision["final_decision"],
        "certainty_score": decision["certainty_score"],
        "VAR_review": decision["VAR_review_needed"]
    }
    response = requests.post(TV_BROADCAST_API, json=payload)
    logging.info(f"Sent to TV Broadcast: {response.status_code}")



def store_in_cloud(decision):
    """ Stores match decision logs in cloud storage. """
    payload = {"match_decision": decision}
    response = requests.post(CLOUD_STORAGE_API, json=payload)
    logging.info(f"Stored in Cloud: {response.status_code}")



# Process each decision
for decision in decision_data:
    send_to_referee_smartwatch(decision)
    send_to_var_replay(decision)
    send_to_tv_broadcast(decision)
    store_in_cloud(decision)

logging.info("Output Delivery Process Completed.")
