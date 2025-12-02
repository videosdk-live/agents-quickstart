# DTMF Event Handler Agent Example

A telephony voice agent that responds to DTMF (Dual-Tone Multi-Frequency) keypad inputs during phone calls. This agent dynamically changes its behavior based on user button presses, enabling interactive voice response (IVR) systems.

## Features

- **DTMF Event Handling**: Listens for and responds to phone keypad button presses
- **Dynamic Context Switching**: Changes agent behavior based on user input
- **Multi-Service Support**: Handles different service options (Loan Recovery, Train Loan Assistance)
- **Real-time PubSub Integration**: Uses VideoSDK's PubSub feature to receive DTMF events

## How It Works

### DTMF Event Flow

1. **User Joins Call**: Agent greets the user with menu options
2. **User Presses Key**: DTMF event is published to the `DTMF_EVENT` topic
3. **Agent Receives Event**: PubSub callback processes the DTMF input
4. **Context Update**: Agent's system context is updated based on the pressed key
5. **Behavior Change**: Agent responds with specialized assistance

### DTMF Examples

- **Press 1**: Loan Recovery Agent
- **Press 2**: Train Loan Assistant

## Quick Start

### 1. Install Dependencies

```bash
pip install -r ../../requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root of the project and add the following:

```bash
# Required API Keys
DEEPGRAM_API_KEY=<your_deepgram_api_key>
GOOGLE_API_KEY=<your_google_api_key>
SARVAM_API_KEY=<your_sarvam_api_key>

# Optional VideoSDK Configuration
VIDEOSDK_AUTH_TOKEN=<your_videosdk_auth_token>
```

### 3. Run the Agent

```bash
python main.py
```

## Code Overview

### Main Components

#### `VoiceAgent` Class

The main agent that handles the conversation flow:

```python
class VoiceAgent(Agent):
    async def on_enter(self):
        # Greets user with menu options
        
    async def on_exit(self):
        # Says goodbye when session ends
```

#### `on_pubsub_message` Function

Processes DTMF events and updates agent context:

```python
def on_pubsub_message(message):
    # Receives DTMF digit
    # Updates agent's chat context
    # Triggers appropriate response
```

#### `entrypoint` Function

Sets up the agent session and PubSub subscription:

- Creates the agent and conversation flow
- Configures the cascading pipeline (STT → LLM → TTS)
- Subscribes to the `DTMF_EVENT` topic
- Starts the agent session

### Pipeline Configuration

The agent uses a `CascadingPipeline` with:

- **STT**: Deepgram for speech-to-text
- **LLM**: Google Gemini for language processing
- **TTS**: SarvamAI for text-to-speech
- **VAD**: Silero for voice activity detection
- **Turn Detector**: Manages conversation turn-taking

## DTMF Event Format

The agent expects DTMF events in the following format:

```json
{
  "payload": {
    "number": "1"
  }
}
```

The `number` field contains the pressed digit as a string.

## Customization

### Adding New DTMF Options

To add more menu options, extend the `on_pubsub_message` function:

```python
elif digit == "3":
    agent.chat_context.add_message(
        role="system",
        content="User pressed 3. You are now a [New Service] Agent..."
    )
    asyncio.create_task(agent.session.say("You selected [new service]. How may I help?"))
```

## Troubleshooting

### Common Issues

1. **DTMF Events Not Received**
   - Verify the PubSub topic name matches (`DTMF_EVENT`)
   - Check that DTMF events are being published correctly
   - Ensure the agent is properly subscribed to the topic

2. **Context Not Updating**
   - Confirm the `agent_obj` is passed in the PubSub wrapper
   - Check that the digit value is being parsed correctly
   - Verify the chat context is being modified

3. **Voice Issues**
   - Ensure all API keys are set correctly
   - Check Deepgram, Google, and SarvamAI API credentials
   - Verify network connectivity to API services