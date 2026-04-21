# Voice Mail Detector

This example demonstrates how to detect if a call has been answered by a voicemail and handle it accordingly.

## Key Features

- **Voicemail Detection**: Automatically detect if the call is connected to a voicemail system.
- **Callback on Detection**: Trigger a callback function when a voicemail is detected, allowing for custom actions like hanging up or leaving a message.

## How It Works

The `voice_mail_detector.py` script shows how to use the `VoiceMailDetector`. It is initialized with an LLM, a duration to monitor for voicemail, and a callback function. The detector is then passed to the `AgentSession`.

If the detector determines it's a voicemail within the specified duration, it will invoke the `voice_mail_callback`.

## How to Run

1.  **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your environment variables**:

    Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in the keys this example uses: `DEEPGRAM_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`.

    For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime).

3.  **Run the agent**:
    ```bash
    python "Voice Mail Detector/voice_mail_detector.py"
    ```
