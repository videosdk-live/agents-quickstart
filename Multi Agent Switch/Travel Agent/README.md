# Multi-Agent Switch

This example demonstrates how a running agent can be replaced by a new one, enabling seamless transitions between different agent capabilities. The new agent can optionally inherit the chat history from the previous agent.

## Key Features

- **Seamless Agent Transitions**: Switch between different agents during a conversation.
- **Context Inheritance**: Optionally, carry over the chat history to the new agent.

## How It Works

The `multi_agent_switch.py` script showcases a `TravelAgent` that can hand over the conversation to specialized agents like `BookingAgent` or `TravelSupportAgent`. This is achieved by having a function tool return a new `Agent` instance.

The `inherit_context` flag in the agent's constructor controls whether the conversation history is passed to the new agent.

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
    python "Multi Agent Switch /Travel Agent /travel_agent.py"
    ```
