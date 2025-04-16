import streamlit as st
from PIL import Image
import time
import requests
import json
import cv2
import numpy as np
import tempfile
from fpdf import FPDF
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(page_title="Raasid AI Dashboard", layout="wide")

# --- Session State Initialization ---
if "decision_history" not in st.session_state:
    st.session_state.decision_history = []

# --- Styling ---
st.markdown("""
<style>
body, html, .css-18e3th9 {
    background-color: #F7F9FC;
    color: #1C1C1C;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
}
h1, h2, h3 {
    color: #004085;
}
.metric-card {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    transition: 0.3s ease-in-out;
}
.metric-card:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    transform: scale(1.01);
}
.stButton>button {
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: bold;
    transition: 0.3s ease-in-out;
}
.stButton>button:hover {
    background-color: #0056b3;
    transform: scale(1.03);
}
hr {
    border-top: 1px solid #DADCE0;
    margin: 25px 0;
}
.small {
    font-size: 13px;
    color: #6C757D;
}
</style>
""", unsafe_allow_html=True)

# --- Configuration ---
BACKEND_URL = "http://127.0.0.1:8000/real_time_decision"  # Endpoint for real-time decision data

# --- Function to Fetch Real-Time Data from Backend ---
def get_real_time_data():
    try:
        response = requests.get(f"{BACKEND_URL}")
        if response.status_code == 200:
            return response.json()  # Assuming backend sends real-time data in JSON format
        else:
            st.error("Failed to fetch data from backend")
            return None
    except Exception as e:
        st.error(f"Error fetching real-time data: {e}")
        return None

# --- Display Real-Time Decision Data ---
def display_real_time_decisions():
    st.title("Real-Time Decision Updates")
    decision_display = st.empty()  # Placeholder for real-time updates
    
    while True:
        data = get_real_time_data()  # Fetch real-time data from backend
        if data:
            decision_display.write(f"Frame: {data['frame']} | Decision: {data['final_decision']} | Confidence: {data['certainty_score']}%")
        
        time.sleep(1)  # Update every second to simulate real-time data
        if st.button('Stop'):
            break  # Allow user to stop the display loop if needed

# --- PDF Generation Function ---
def generate_pdf_report(decision_data, distribution_data, file_name="decision_report.pdf"):
    # Create PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Add title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Raasid AI Decision Report", ln=True, align="C")

    # Add metadata
    pdf.ln(10)  # Line break
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)
    pdf.cell(200, 10, txt="Distribution ID: " + distribution_data.get("distribution_id", "N/A"), ln=True)

    # Add Decision Summary
    pdf.ln(10)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Decision Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"""
    Handball Detected: {'Yes' if decision_data.get('handball_detected') else 'No'}
    Intentional: {'Yes' if decision_data.get('intentional') else 'No'}
    Confidence Score: {decision_data.get('confidence_score', 'N/A')}%
    Contact Duration: {decision_data.get('contact_duration', 'N/A')}s
    Impact Force: {decision_data.get('impact_force', 'N/A')} N
    Pose Unusual: {'Yes' if decision_data.get('pose_unusual') else 'No'}
    """)

    # Add Distribution Details
    pdf.ln(10)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Distribution Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"""
    Timestamp: {distribution_data.get('timestamp', 'N/A')}
    Delivered To: {', '.join(distribution_data.get('delivered_to', []))}
    """)

    # Add Decision Data (JSON)
    pdf.ln(10)
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Full Decision Data (JSON)", ln=True)
    pdf.set_font("Arial", size=10)
    json_data = json.dumps(decision_data, indent=4)
    pdf.multi_cell(0, 10, json_data)

    # Save the PDF
    pdf.output(file_name)
    return file_name

# --- Header ---
st.markdown("""
<div style='text-align: center; padding: 30px 0;'>
    <h1 style='color: #004085; font-size: 3em;'>Raasid AI System</h1>
    <h3 style='color: #6C757D;'>AI-Powered Handball Detection for Football Officiating</h3>
    <p style='color: #495057;'>Precision. Speed. Fair Play. Built for the future of football officiating.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Run Full Simulation ---
if st.button("Run Full Simulation"):
    with st.spinner("Running complete AI pipeline..."):
        success = run_full_simulation()
        if success:
            st.success("Simulation and distribution complete!")
            # Generate PDF report after successful simulation
            pdf_file = generate_pdf_report(st.session_state.ai_result, st.session_state.distribution_output)
            
            # Provide the download link in Streamlit interface
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Download PDF Report",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
            st.rerun()

# --- Tabs Layout ---
tab1, tab2, tab3 = st.tabs(["Upload Snippet", "AI Analysis", "Final Decision Distribution"])

# --- Upload Snippet ---
with tab1:
    st.markdown('<h3 style="color:#004085;">Upload Match Snippet</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload image or video snippet", type=["jpg", "png", "mp4"])

    def send_post_request(endpoint, payload):
        try:
            res = requests.post(endpoint, json=payload)
            res.raise_for_status()
            return res.json().get("result", {})
        except Exception as e:
            st.error(f"API call to {endpoint} failed: {e}")
            return {}

    result = None
    if uploaded_file:
        if uploaded_file.type.startswith("video"):
            st.video(uploaded_file)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name

            video = cv2.VideoCapture(tmp_file_path)
            ret, frame = video.read()
            if ret:
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                st.image(image, use_container_width=True)
                pose_features = run_full_simulation()  # reuse if needed
            else:
                st.error("Could not read the video frame.")
        else:
            img = Image.open(uploaded_file)
            st.image(img, use_container_width=True)
            st.warning("Simulated image-based uploads are currently static.")

# --- AI Analysis ---
with tab2:
    if "ai_result" in st.session_state:
        result = st.session_state.ai_result

        st.success("AI Analysis Complete – Decision Ready")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<h3 style="color:#004085;">AI Decision Summary</h3>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Handball Detected", "✅ Yes" if result.get("handball_detected") else "❌ No")
            st.markdown('<div class="small">AI detected hand-ball contact</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Intent Classification", "🔴 Intentional" if result.get("intentional") else "⬜ Accidental")
            st.markdown('<div class="small">Player hand in unnatural position</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Confidence Score", f"{result.get('confidence_score', 0)}%")
            st.markdown('<div class="small">Based on multi-sensor fusion</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<h3 style="color:#004085;">Sensor Input Summary</h3>', unsafe_allow_html=True)
        st.json({
            "ball_contact": result.get("handball_detected"),
            "contact_duration": f"{result.get('contact_duration', 'N/A')}s",
            "impact_force": f"{result.get('impact_force', 'N/A')} N",
            "sensor_source": "Smart Ball Sensor",
            "pose_estimation": "Unnatural arm position detected" if result.get("pose_unusual") else "Normal arm movement",
            "snickometer_peak": "Detected audio impact"
        })

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<h3 style="color:#004085;">Download AI Decision Report</h3>', unsafe_allow_html=True)
        json_bytes = json.dumps(result, indent=4).encode("utf-8")
        st.download_button(
            label="Download Decision Report (JSON)",
            data=json_bytes,
            file_name="raasid_ai_decision.json",
            mime="application/json"
        )

# --- Final Distribution ---
with tab3:
    st.markdown('<h3 style="color:#004085;">Distribute Final Decision</h3>', unsafe_allow_html=True)

    if st.button("Distribute to Referee Systems"):
        with st.spinner("Distributing to all endpoints..."):
            try:
                response = requests.post("http://127.0.0.1:8000/output_distribution")
                response.raise_for_status()
                output_response = response.json()
                st.session_state["distribution_output"] = output_response
                st.success("Distribution completed successfully!")
            except requests.exceptions.RequestException as e:
                st.error(f"Distribution failed: {e}")

    if "distribution_output" in st.session_state:
        dist = st.session_state["distribution_output"]
        st.markdown("### Distribution Metadata")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Distribution ID:**", dist.get("distribution_id", "N/A"))
            st.write("**Timestamp:**", dist.get("timestamp", "N/A"))
        with col2:
            st.write("**Delivered To:**")
            st.write(dist.get("delivered_to", []))

        st.markdown("### Final AI Decision")
        st.json(dist.get("decision"))

        report_path = dist.get("report_path")
        if report_path:
            try:
                with open(report_path, "r") as f:
                    report_data = f.read()
                    st.download_button(
                        label="Download Distributed Report",
                        data=report_data,
                        file_name="distributed_decision_report.json",
                        mime="application/json"
                    )
            except FileNotFoundError:
                st.warning("Report file not found on the server.")

# --- Decision History ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<h3 style="color:#004085;">AI Decision History (This Session)</h3>', unsafe_allow_html=True)

if st.session_state.decision_history:
    for idx, entry in enumerate(reversed(st.session_state.decision_history), 1):
        with st.expander(f"Decision #{len(st.session_state.decision_history) - idx + 1}"):
            st.write(f"**Handball Detected:** {'Yes' if entry.get('handball_detected') else 'No'}")
            st.write(f"**Intentional:** {'Yes' if entry.get('intentional') else 'No'}")
            st.write(f"**Confidence Score:** {entry.get('confidence_score', 'N/A')}%")
            st.write(f"**Contact Duration:** {entry.get('contact_duration', 'N/A')}s")
            st.write(f"**Impact Force:** {entry.get('impact_force', 'N/A')} N")
            st.write(f"**Unnatural Pose:** {'Yes' if entry.get('pose_unusual') else 'No'}")
else:
    st.info("Upload match content or run a simulation to begin.")

