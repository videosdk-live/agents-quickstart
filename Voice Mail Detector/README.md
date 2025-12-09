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

    Create a `.env` file in the root of the project and add the following:

    ```
    DEEPGRAM_API_KEY=<your_deepgram_api_key>
    OPENAI_API_KEY=<your_openai_api_key>
    ELEVENLABS_API_KEY=<your_elevenlabs_api_key>
    VIDEOSDK_AUTH_TOKEN=<your_videosdk_auth_token>
    ```

3.  **Run the agent**:
    ```bash
    python "Voice Mail Detector/voice_mail_detector.py"
    ```
