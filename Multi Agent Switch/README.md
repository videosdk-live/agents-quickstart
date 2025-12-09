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

    Create a `.env` file in the root of the project and add the following:

    ```
    DEEPGRAM_API_KEY=<your_deepgram_api_key>
    GOOGLE_API_KEY=<your_google_api_key>
    CARTESIA_API_KEY=<your_cartesia_api_key>
    ```

3.  **Run the agent**:
    ```bash
    python "Multi Agent Switch /multi_agent_switch.py"
    ```
