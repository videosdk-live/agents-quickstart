# Healthcare Agent

A multi-agent healthcare system built with VideoSDK Agents that routes users to specialized healthcare services.

## Features

- **Healthcare Assistant**: General healthcare inquiries and initial routing
- **Appointment Specialist**: Schedule, modify, or cancel doctor visits and appointments
- **Medical Support Specialist**: Handle symptoms, health concerns, and basic guidance


## How to Run

1.  **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your environment variables**:

    Create a `.env` file in the root of the project and add the following:

    ```
    DEEPGRAM_API_KEY=<your_deepgram_api_key>
    GOOGLE_API_KEY=<your_google_api_key>
    CARTESIA_API_KEY=<your_cartesia_api_key>
    ```

3.  **Run the agent**:
    ```bash
    python "Multi Agent Switch /Health Care Agent /health_care_agent.py"
    ```

## Technology Stack

- VideoSDK Agents
- Deepgram STT (Speech-to-Text)
- Google LLM
- Cartesia TTS (Text-to-Speech)
- Silero VAD (Voice Activity Detection)
- Turn Detector

