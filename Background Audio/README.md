
# Background Audio

The VideoSDK AI Agent SDK allows you to play background audio while the agent is in a "thinking" state—specifically, after the agent has received a input from user and before it responds. This feature enhances the user experience by filling silences with subtle audio cues, making the interaction feel more natural and engaging.

## Use Cases

- **Simulating a Live Environment**: Play ambient sounds like a call center, office, or café to create a more immersive experience.
- **Indicating Agent Activity**: Use subtle sounds, such as keyboard typing, to signal that the agent is processing a request.
- **Brand Reinforcement**: Play on-brand jingles or sounds to reinforce brand identity during interactions.

## Supported Audio Format

The background audio feature currently supports **WAV** file format only.

## Implementation

To implement background audio, you need to import the `BackgroundAudioConfig` class and pass an instance of it to the `AgentSession`.

### `BackgroundAudioConfig`

The `BackgroundAudioConfig` class takes the following parameter:

- `file_path` (str): The local file path to the WAV audio file you want to play.

### Example

```python
from videosdk.agents import AgentSession, BackgroundAudioConfig

# ... other imports and agent setup

    session = AgentSession(
        agent=agent, 
        pipeline=pipeline,
        conversation_flow=conversation_flow,
        background_audio=BackgroundAudioConfig(
            file_path="./agent_keyboard.wav"
        ),
    )
```

## How to Run

1.  **Install the required dependencies**:
    ```bash
    pip install -r ../requirements.txt
    ```

2.  **Set up your environment variables**:
    Create a `.env` file in the root of the project and add the following:
    ```
    OPENAI_API_KEY=<your_openai_api_key>
    DEEPGRAM_API_KEY=<your_deepgram_api_key>
    ```

3.  **Run the agent**:
    ```bash
    python background_audio.py
    ```