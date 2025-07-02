# 🎭 Simli Virtual Avatar Examples

Enhance your AI agents with realistic, lip-synced virtual avatars using the [Simli](https://simli.com/) integration. Create more engaging and interactive experiences with:

- **Real-time Lip Sync**: Avatars that speak in sync with your AI agent's voice
- **Visual Engagement**: Provide a face to your AI agent for better user connection
- **Multiple Avatar Options**: Choose from various avatar faces or use custom ones
- **Seamless Integration**: Works with both RealtimePipeline and CascadingPipeline approaches

## Prerequisites

### Installation

Install the required packages:

```bash
pip install "videosdk-plugins-simli"
```

### API Keys Required

You'll need the following API keys in your `.env` file:

```env
# Required for Simli Avatar
SIMLI_API_KEY=your_simli_api_key_here
SIMLI_FACE_ID=your_face_id_here  # Optional - has default value

# Required for VideoSDK
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token

# For Cascading Pipeline (Google services)
GOOGLE_API_KEY=your_google_api_key

# For Realtime Pipeline (Gemini Live API)
# Uses GOOGLE_API_KEY from above
```

### Getting Simli Credentials

1. Visit the [Simli Dashboard](https://simli.com/dashboard) to get your API key
2. Optionally, you can specify a custom `faceId` if you have one
3. If no `faceId` is provided, Simli will use a default avatar

## Examples

### 1. Cascading Pipeline with Simli Avatar

**File:** `simli_cascading_example.py`

This example uses a cascading pipeline with:
- **STT:** Google Speech-to-Text
- **LLM:** Google LLM  
- **TTS:** Google Text-to-Speech
- **Avatar:** Simli Avatar
- **VAD:** Silero VAD
- **Turn Detector:** VideoSDK Turn Detector

**Usage:**
```bash
python simli_cascading_example.py
```

### 2. Realtime Pipeline with Simli Avatar

**File:** `simli_realtime_example.py`

This example uses a realtime pipeline with:
- **Model:** Google Gemini 2.0 Flash Live
- **Avatar:** Simli Avatar
- **Voice:** Leda (configurable)

**Usage:**
```bash
python simli_realtime_example.py
```

## Configuration

### Room Options

Before running either script, make sure to update the `room_id` in the `make_context()` function:

```python
room_options = RoomOptions(
    room_id="YOUR_MEETING_ID",  # Replace with your actual meeting ID
    name="Your Agent Name",
    playground=False
    )
```

### Simli Configuration

Both examples use `SimliConfig` with the following options:

```python
simli_config = SimliConfig(
    apiKey=os.getenv("SIMLI_API_KEY"),
    faceId=os.getenv("SIMLI_FACE_ID"),  # Optional
    maxSessionLength=1800,  # 30 minutes (default)
    maxIdleTime=300,  # 5 minutes (default)
)
```

## Available Functions

Both agents come with these built-in function tools:

### 1. Weather Lookup
Ask about weather in any location:
- "What's the weather in New York?"
- "How's the weather in Tokyo?"
  

## Customization

### Changing Voice (Realtime Pipeline)

For the realtime pipeline, you can change the Gemini voice:

```python
config=GeminiLiveConfig(
    voice="Puck",  # Options: Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, Zephyr
    response_modalities=["AUDIO"]
)
```

### Changing Avatar Face

You can use different Simli faces by setting the `SIMLI_FACE_ID` environment variable or finding available faces in the [Simli Documentation](https://docs.simli.com/).

### Adding More Providers (Cascading Pipeline)

The cascading example can be easily modified to use different providers for STT, LLM, or TTS. Check the commented lines in the script for alternatives like OpenAI, ElevenLabs, Deepgram, etc.


## Learn More

- [VideoSDK AI Agents Documentation](https://docs.videosdk.live/ai_agents/)
- [Simli Documentation](https://docs.simli.com/)
- [VideoSDK Simli Plugin Documentation](https://docs.videosdk.live/ai_agents/plugins/avatar/simli) 