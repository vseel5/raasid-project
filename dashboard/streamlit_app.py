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
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
import sys

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/dashboard.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')
    UPLOAD_ENDPOINT = f"{API_BASE_URL}/upload"
    PROCESS_ENDPOINT = f"{API_BASE_URL}/process"
    STATUS_ENDPOINT = f"{API_BASE_URL}/status"
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 1))
    TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))

# --- Page Configuration ---
st.set_page_config(
    page_title="Raasid AI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/raasid',
        'Report a bug': 'https://github.com/your-repo/raasid/issues',
        'About': 'AI-powered handball detection system for football officiating'
    }
)

# --- Session State Initialization ---
if "decision_history" not in st.session_state:
    st.session_state.decision_history = []
if "video_id" not in st.session_state:
    st.session_state.video_id = None
if "process_id" not in st.session_state:
    st.session_state.process_id = None
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None
if "distribution_output" not in st.session_state:
    st.session_state.distribution_output = None

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
.error-message {
    color: #DC3545;
    background-color: #F8D7DA;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
.success-message {
    color: #28A745;
    background-color: #D4EDDA;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make an HTTP request with retry logic."""
    for attempt in range(Config.MAX_RETRIES):
        try:
            response = requests.request(
                method,
                url,
                timeout=Config.TIMEOUT,
                **kwargs
            )
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == Config.MAX_RETRIES - 1:
                logger.error(f"Request failed after {Config.MAX_RETRIES} attempts: {e}")
                raise
            logger.warning(f"Request attempt {attempt + 1} failed: {e}")
            time.sleep(Config.RETRY_DELAY)

def upload_video(video_file) -> dict:
    """Upload video to the API server."""
    try:
        files = {'video': video_file}
        response = make_request('POST', Config.UPLOAD_ENDPOINT, files=files)
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error uploading video: {e}")
        st.error(f"Upload failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during upload: {e}")
        st.error("An unexpected error occurred during upload")
        return None

def process_video(video_id: str) -> dict:
    """Start video processing."""
    try:
        response = make_request('POST', f"{Config.PROCESS_ENDPOINT}/{video_id}")
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error processing video: {e}")
        st.error(f"Processing failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")
        st.error("An unexpected error occurred during processing")
        return None

def get_processing_status(process_id: str) -> dict:
    """Get video processing status."""
    try:
        response = make_request('GET', f"{Config.STATUS_ENDPOINT}/{process_id}")
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        logger.error(f"Error checking status: {e}")
        st.error(f"Status check failed: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during status check: {e}")
        st.error("An unexpected error occurred while checking status")
        return None

def get_real_time_data() -> dict:
    """Fetch real-time data from backend."""
    try:
        response = make_request('GET', f"{Config.API_BASE_URL}/real_time_decision")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching real-time data: {e}")
        st.error("Failed to fetch data from backend")
        return None
    except Exception as e:
        logger.error(f"Unexpected error fetching real-time data: {e}")
        st.error("An unexpected error occurred while fetching data")
        return None

def display_real_time_decisions():
    """Display real-time decision updates."""
    st.title("Real-Time Decision Updates")
    decision_display = st.empty()
    
    while True:
        data = get_real_time_data()
        if data:
            decision_display.write(
                f"Frame: {data['frame']} | "
                f"Decision: {data['final_decision']} | "
                f"Confidence: {data['certainty_score']}%"
            )
        
        time.sleep(1)
        if st.button('Stop'):
            break

def generate_pdf_report(decision_data: dict, distribution_data: dict, file_name: str = "decision_report.pdf") -> str:
    """Generate PDF report from decision and distribution data."""
    try:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Add title
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="Raasid AI Decision Report", ln=True, align="C")

        # Add metadata
        pdf.ln(10)
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
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        st.error("Failed to generate PDF report")
        return None

# --- Header ---
st.markdown("""
<div style='text-align: center; padding: 30px 0;'>
    <h1 style='color: #004085; font-size: 3em;'>Raasid AI System</h1>
    <h3 style='color: #6C757D;'>AI-Powered Handball Detection for Football Officiating</h3>
    <p style='color: #495057;'>Precision. Speed. Fair Play. Built for the future of football officiating.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# --- Tabs Layout ---
tab1, tab2, tab3 = st.tabs(["Upload Snippet", "AI Analysis", "Final Decision Distribution"])

# --- Upload Snippet ---
with tab1:
    st.markdown('<h3 style="color:#004085;">Upload Match Snippet</h3>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload video snippet",
        type=["mp4", "avi", "mov", "mkv"],
        help="Upload a video file for analysis. Supported formats: MP4, AVI, MOV, MKV"
    )

    if uploaded_file is not None:
        # Display video information
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / (1024*1024):.2f} MB",
            "File type": uploaded_file.type
        }
        st.json(file_details)

        # Upload button
        if st.button("Upload Video", key="upload_button"):
            with st.spinner("Uploading video..."):
                result = upload_video(uploaded_file)
                if result:
                    st.success("Video uploaded successfully!")
                    st.session_state['video_id'] = result['video_id']
                    st.json(result)

        # Processing section
        if 'video_id' in st.session_state:
            if st.button("Start Processing", key="process_button"):
                with st.spinner("Processing video..."):
                    result = process_video(st.session_state['video_id'])
                    if result:
                        st.success("Processing started!")
                        st.session_state['process_id'] = result['processing_id']
                        st.json(result)

        # Status monitoring section
        if 'process_id' in st.session_state:
            st.header("Processing Status")
            
            # Create a placeholder for the status
            status_placeholder = st.empty()
            
            # Add a refresh button
            if st.button("Refresh Status", key="status_button"):
                with st.spinner("Checking status..."):
                    status = get_processing_status(st.session_state['process_id'])
                    if status:
                        status_placeholder.json(status)
                        
                        # Show progress bar if available
                        if 'progress' in status:
                            st.progress(status['progress'] / 100)
                        
                        # Show results if processing is complete
                        if status.get('status') == 'completed':
                            st.success("Processing completed!")
                            if 'results' in status:
                                st.session_state['ai_result'] = status['results']
                                st.json(status['results'])

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

    if st.button("Distribute to Referee Systems", key="distribute_button"):
        with st.spinner("Distributing to all endpoints..."):
            try:
                response = make_request('POST', f"{Config.API_BASE_URL}/output_distribution")
                response.raise_for_status()
                output_response = response.json()
                st.session_state["distribution_output"] = output_response
                st.success("Distribution completed successfully!")
            except requests.exceptions.RequestException as e:
                logger.error(f"Distribution failed: {e}")
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
                logger.error(f"Report file not found: {report_path}")
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

