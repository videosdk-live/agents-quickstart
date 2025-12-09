# DTMF Handler

This example demonstrates how to handle DTMF (Dual-Tone Multi-Frequency) signals during a call. This allows the agent to respond to keypad inputs from the user.

## Key Features

- **DTMF Handling**: Capture and process keypad inputs (0-9, *, #) during a live call.
- **Callback Function**: Trigger a custom callback function when a DTMF signal is detected.

## How It Works

DTMF (Dual-Tone Multi-Frequency) events are generated when a participant presses keys (0-9, *, #) on their phone or SIP device during a call. These events are useful for building IVR flows, collecting user input, or triggering actions in your application.

The `dtmf_handler.py` script shows how to use the `DTMFHandler`. You provide a callback function to the `DTMFHandler`, which is then passed to the `AgentSession`. When the user presses a key on their phone, the `dtmf_callback` function is invoked with the digit pressed.

## Enabling DTMF Events

DTMF event detection can be enabled in two ways:

### Via Dashboard:

When creating or editing a SIP gateway in the VideoSDK dashboard, enable the DTMF option.

### Via API:

Set the `enableDtmf` parameter to `true` when creating or updating a SIP gateway using the API.

Once enabled, DTMF events will be detected and published for all calls routed through that gateway.

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
    python "DTMF Handler/dtmf_handler.py"
    ```
