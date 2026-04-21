# Pub/Sub Agent Example

This example demonstrates how to use the Pub/Sub feature for messaging between a user and an agent during an ongoing session. The agent can send and receive Pub/Sub messages, which can be used as input for the agent's responses.

## Key Features

- **Send Pub/Sub Messages**: The agent can send messages to a specified Pub/Sub topic.
- **Receive Pub/Sub Messages**: The agent can subscribe to a Pub/Sub topic and receive messages from it.
- **Real-time Communication**: Enables real-time, bidirectional communication between the agent and the user.

## How It Works

The `pubsub_agent.py` script creates a `PubSubAgent` that connects to a room and uses a `CascadingPipeline` for speech-to-text, language model processing, and text-to-speech.

The agent has a `send_pubsub_message` function that is exposed as a tool. This function allows the agent to publish messages to the "CHAT" topic.

The agent also subscribes to the "CHAT" topic and uses the `on_pubsub_message` callback function to process incoming messages.

## How to Run

1. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Set up your environment variables**:
   Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in: `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `ANTHROPIC_API_KEY`.

   For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime).
3. **Run the agent**:
   ```bash
   python pubsub_agent.py
   ```
