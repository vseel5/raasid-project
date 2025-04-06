# Admin Dashboard

## Overview
The Admin Dashboard provides a centralized interface for managing and monitoring the handball detection system. It allows administrators to review decisions, override them if necessary, and manage logs for auditing and transparency purposes. The dashboard is designed to be intuitive and provides real-time updates on the system's performance and decision-making process.

## MVP Features
The Admin Dashboard in the MVP includes the following functionalities:

- Decision Logs: View logs of all decisions made by the system, including pose estimation, ball contact detection, and event context evaluation.
- Manual Override: Ability to manually override decisions made by the AI, particularly in scenarios where human intervention is required.
- Decision Distribution: Simulate sending decisions to external systems, such as the referee smartwatch, TV broadcast, and cloud storage.

## User Interface
The Admin Dashboard UI is designed with simplicity and efficiency in mind, ensuring ease of use for officials and administrators.

### Key UI Components:
- Log Viewer: Displays a detailed list of all decisions made by the AI, including timestamps, decision outcomes, and context.
- Decision Override Section: Allows administrators to modify AI decisions and provide justifications for manual overrides.
- Simulation Controls: Provides options to trigger decision distribution to external systems and view the status of the distribution.

## Data Flow
The dashboard pulls data from the system’s backend, where AI decisions are logged and stored. The following data flow occurs within the dashboard:

1. Decision Log Retrieval: The dashboard fetches decision logs from the backend to display in the Log Viewer.
2. Manual Override: When an administrator chooses to override a decision, the new decision is updated in the system’s database.
3. Decision Distribution: Administrators can trigger the distribution of decisions to external systems, simulating the communication process to referees, broadcasters, and storage systems.

## Future Enhancements
The MVP of the Admin Dashboard is functional with basic features, but several enhancements are planned for future versions:

- Real-time Event Monitoring: Provide live updates of ongoing matches, showing AI decision outcomes in real time.
- Enhanced Override Interface: Add more granular control for administrators to fine-tune decision overrides, including confidence thresholds and contextual information.
- Notification System: Integrate notifications to alert administrators of new decisions or overrides requiring attention.

## Technology Used
- Frontend: Streamlit for rapid development of interactive UI components and real-time updates.
- Backend: FastAPI for handling data requests and managing the communication between the dashboard and the AI system.
- Containerization: Docker to ensure consistent environment setup for both frontend and backend components.

## Getting Started
1. Clone the repository and navigate to the dashboard directory:
   ```bash
   git clone https://github.com/vseel5/raasid-project
   cd raasid-project
   cd dashboard
   ```

2. Run the Admin Dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```

3. Open the dashboard in your browser, and you will be able to interact with the features available in the MVP.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

