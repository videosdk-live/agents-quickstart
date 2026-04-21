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

    Copy [`.env.example`](../../.env.example) at the repo root to `.env` and fill in: `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`, `CARTESIA_API_KEY`.

    For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime).

3.  **Run the agent**:
    ```bash
    python "Multi Agent Switch /Health Care Agent /health_care_agent.py"
    ```