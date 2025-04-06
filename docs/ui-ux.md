# UI/UX Design

## Overview
The UI/UX design for Raasid focuses on providing a user-friendly, intuitive, and efficient interface for referees, analysts, and stakeholders. The design ensures that the system can be used effectively during high-pressure, real-time football matches, allowing referees to make accurate decisions with minimal distractions. It also ensures that the data presented is clear and actionable for users.

## User Personas
The system is designed with several user personas in mind, each with different needs and workflows:

### 1. Referee
- **Primary Role**: Make real-time decisions on handball incidents.
- **Needs**: A clear display of match data, including real-time handball detection, pose estimation, and ball contact information. The interface should be intuitive and allow for fast decision-making under pressure.
- **Pain Points**: Difficulty interpreting complex data under time pressure, potential delays in receiving decision information.

### 2. Analyst
- **Primary Role**: Review match data and provide feedback for improving system accuracy.
- **Needs**: Access to detailed decision logs, historical match data, and analytics on decision accuracy. The interface should allow them to review past decisions and help optimize the AI model.
- **Pain Points**: Difficulty accessing decision logs, need for comprehensive yet easy-to-understand reports.

### 3. Fans
- **Primary Role**: Stay informed about the match and decision-making process.
- **Needs**: Clear and accessible explanations of decisions, visual replays of key events, and an understanding of how decisions were made.
- **Pain Points**: Lack of transparency in decision-making, difficulty understanding the reasoning behind AI decisions.

## Design Principles

### 1. Simplicity
The interface is designed to be simple and easy to use, with minimal distractions. Information is presented in a straightforward manner, allowing users to focus on the most important data without being overwhelmed by unnecessary details.

### 2. Clarity
Clear, concise visualizations are used to represent data. Key information, such as the status of a decision, the handball detection, and the certainty score, is presented in an easily digestible format. The interface avoids clutter and ensures that the most important data is always visible.

### 3. Real-Time Feedback
Since the system is used during live football matches, real-time feedback is crucial. The interface provides immediate feedback on handball detection, allowing the referee to make quick, informed decisions. The system's response time is minimized to ensure that decisions can be made as quickly as possible.

### 4. Transparency
Transparency is essential for both referees and fans. The system clearly explains the decision-making process, offering insight into why a particular decision was made and the data that supported it. Replays and decision histories are available to allow for review and accountability.

## Wireframes and UI Design

### 1. Dashboard Overview
The main dashboard provides an overview of the match, including video playback, live decisions, and a summary of key metrics. The UI layout is designed to be clean and uncluttered, with the following key sections:

- **Video Stream**: Displays the match footage for analysis.
- **AI Decision**: A panel showing the most recent decision made by the AI, including handball detection status and certainty score.
- **Event Context**: A section displaying information on the context of the handball event (e.g., intentional or accidental).
- **History**: A history panel showing previous decisions made during the match, with the option to review past events.

### 2. Decision Log
The decision log displays a detailed history of all AI-generated decisions. Each entry includes the following:

- **Frame Number**: The video frame in which the decision was made.
- **Decision**: The final decision made by the system (e.g., "No Handball," "Handball – Penalty").
- **Certainty Score**: The confidence level associated with the decision.
- **Event Details**: Information about the handball event, such as whether it was intentional or accidental.

The log is interactive, allowing users to filter decisions based on specific criteria (e.g., decision type, event context).

### 3. Decision Distribution
The decision distribution section shows where the final decision was sent. It includes the following:

- **Referee Smartwatch**: A notification indicating that the decision has been sent to the referee's smartwatch.
- **TV Broadcast**: A notification indicating that the decision has been sent to the TV broadcast system.
- **Cloud Storage**: A notification indicating that the decision has been stored in cloud storage for long-term access and analysis.

This section ensures that users can track the distribution of decisions to ensure they are transmitted in real-time to all relevant systems.

## User Flows

### 1. Referee Flow
- **Step 1**: Upload video/image of the match.
- **Step 2**: AI processes the video and generates decisions for pose estimation, ball contact, and event context.
- **Step 3**: The referee views the AI decision and can either confirm the decision or override it based on their judgment.
- **Step 4**: The final decision is distributed to the referee’s smartwatch, TV broadcast, and cloud storage.

### 2. Analyst Flow
- **Step 1**: View historical match data and decision logs.
- **Step 2**: Review AI decisions and check for accuracy.
- **Step 3**: Provide feedback on the decision-making process and suggest improvements for the AI models.
- **Step 4**: Generate reports for the development team to enhance the system.

### 3. Fan Flow
- **Step 1**: View live match information, including real-time decisions.
- **Step 2**: Watch replays of key events and decisions.
- **Step 3**: Understand the reasoning behind decisions through the explanation provided by the system.

## Visual Design and Branding
The design of Raasid reflects its role in a professional sports environment. The color scheme is inspired by traditional football refereeing equipment, with a focus on visibility and clarity. Key design elements include:

- **Colors**: A balanced use of dark and light tones ensures that the system is readable under different lighting conditions. Key elements, such as decision indicators and action buttons, use bright, contrasting colors for visibility.
- **Typography**: The font is clean, modern, and legible, with a focus on ensuring that text is easy to read even under pressure.
- **Icons and Buttons**: Simple, intuitive icons are used for key actions, such as confirming a decision or accessing history. Buttons are large and easy to click, even during fast-paced moments in the match.

## Usability Testing
Usability testing is conducted to ensure that the interface is intuitive and effective for the target users. The following testing strategies are used:

- **Referee Testing**: Referees are asked to use the system in simulated match scenarios to ensure that it meets their needs and that they can make decisions quickly and accurately.
- **Analyst Testing**: Analysts review the system's decision logs and reports to ensure that they can access and interpret the data easily.
- **Fan Testing**: Fans are asked to interact with the system to ensure that they can understand the decisions and follow the match effectively.

## Future Enhancements
The UI/UX design will be enhanced in future versions of the system to further improve user experience and expand functionality:

- **Mobile Compatibility**: Optimizing the user interface for mobile devices to ensure that referees and analysts can access the system on the go.
- **Real-Time Feedback**: Adding more interactive features for fans, such as real-time polls or feedback on decisions during matches.
- **AI Confidence Explanation**: Providing more detailed explanations of AI confidence scores to help users understand how decisions were made.

## License
This project is licensed under the MIT License – see the LICENSE file for details.

## Authors
- Aseel K. Rajab, Majd I. Rashid, Ali S. Alharthi
- [GitHub Profile](https://github.com/vseel5/raasid-project)

