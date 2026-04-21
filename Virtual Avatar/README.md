# 🎭 Virtual Avatar Examples

Enhance your AI agents with realistic, lip-synced virtual avatars using [Simli](https://simli.com/) or [Anam](https://www.anam.ai/) integrations. Create more engaging and interactive experiences with:

- **Real-time Lip Sync**: Avatars that speak in sync with your AI agent's voice
- **Visual Engagement**: Provide a face to your AI agent for better user connection
- **Multiple Avatar Options**: Choose from various avatar faces or use custom ones
- **Seamless Integration**: Works with both RealtimePipeline and CascadingPipeline approaches
- **Multiple Providers**: Choose between Simli and Anam based on your needs

## Prerequisites

### Installation

Install the required packages for your chosen avatar provider:

```bash
# For Simli Avatar
pip install "videosdk-plugins-simli"

# For Anam Avatar
pip install "videosdk-plugins-anam"
```

### API Keys Required

Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in the keys you need:

- **VideoSDK auth** (pick one): `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY`
- **Simli avatar examples**: `SIMLI_API_KEY` (and optionally `SIMLI_FACE_ID`)
- **Anam avatar examples**: `ANAM_API_KEY`, `ANAM_AVATAR_ID`
- **Cascade Pipeline Mode examples**: `DEEPGRAM_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`
- **Realtime Pipeline Mode examples (Gemini Live API)**: `GOOGLE_API_KEY`

### Getting Avatar Credentials

#### Simli
1. Visit the [Simli Dashboard](https://simli.com/dashboard) to get your API key
2. Optionally, you can specify a custom `faceId` if you have one
3. If no `faceId` is provided, Simli will use a default avatar

#### Anam
1. Visit the [Anam Dashboard](https://www.anam.ai/) to get your API key
2. Get your `avatar_id` from the Anam platform
3. Both `api_key` and `avatar_id` are required for Anam avatars

## Examples

### Simli Avatar Examples

#### 1. Cascade Pipeline Mode with Simli Avatar

**File:** `simli_cascading_example.py`

This example uses a cascading pipeline with:
- **STT:** Deepgram (Nova 3)
- **LLM:** OpenAI (GPT-4o-mini)
- **TTS:** ElevenLabs
- **Avatar:** Simli Avatar
- **VAD:** Silero VAD
- **Turn Detector:** VideoSDK Turn Detector

**Usage:**
```bash
python simli_cascading_example.py
```

#### 2. Realtime Pipeline Mode with Simli Avatar

**File:** `simli_realtime_example.py`

This example uses a realtime pipeline with:
- **Model:** Google Gemini 2.5 Flash Native Audio
- **Avatar:** Simli Avatar
- **Voice:** Leda (configurable)

**Usage:**
```bash
python simli_realtime_example.py
```

### Anam Avatar Examples

#### 3. Cascade Pipeline Mode with Anam Avatar

**File:** `anam_cascading_example.py`

This example uses a cascading pipeline with:
- **STT:** Deepgram (Nova 3)
- **LLM:** OpenAI (GPT-4o-mini)
- **TTS:** ElevenLabs
- **Avatar:** Anam Avatar
- **VAD:** Silero VAD
- **Turn Detector:** VideoSDK Turn Detector

**Usage:**
```bash
python anam_cascading_example.py
```

#### 4. Realtime Pipeline Mode with Anam Avatar

**File:** `anam_realtime_example.py`

This example uses a realtime pipeline with:
- **Model:** Google Gemini 2.5 Flash Native Audio
- **Avatar:** Anam Avatar
- **Voice:** Leda (configurable)

**Usage:**
```bash
python anam_realtime_example.py
```

## Configuration

### Room Options

Before running any script, make sure to update the `room_id` in the `make_context()` function:

```python
room_options = RoomOptions(
    room_id="YOUR_MEETING_ID",  # Replace with your actual meeting ID
    name="Your Agent Name",
    playground=False
    )
```

### Simli Configuration

Simli examples use `SimliConfig` with the following options:

```python
simli_config = SimliConfig(
    faceId="your_face_id",
    maxSessionLength=1800,  # 30 minutes (default)
    maxIdleTime=600,  # 10 minutes
)

simli_avatar = SimliAvatar(
    api_key=os.getenv("SIMLI_API_KEY"),
    config=simli_config,
    is_trinity_avatar=True,
)
```

### Anam Configuration

Anam examples use `AnamAvatar` with the following options:

```python
anam_avatar = AnamAvatar(
    api_key=os.getenv("ANAM_API_KEY"),
    avatar_id=os.getenv("ANAM_AVATAR_ID"),
)
```

## Available Functions

All avatar agents come with these built-in function tools:

### 1. Weather Lookup
Ask about weather in any location:
- "What's the weather in New York?"
- "How's the weather in Tokyo?"


## Customization

### Changing Voice (Realtime Pipeline Mode)

For the realtime pipeline examples, you can change the Gemini voice:

```python
config=GeminiLiveConfig(
    voice="Puck",  # Options: Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, Zephyr
    response_modalities=["AUDIO"]
)
```

### Changing Avatar Face

**Simli:** Use different faces by setting the `faceId` in `SimliConfig` or finding available faces in the [Simli Documentation](https://docs.simli.com/).

**Anam:** Use different avatars by setting the `ANAM_AVATAR_ID` environment variable or browsing available avatars on the [Anam platform](https://www.anam.ai/).

### Adding More Providers (Cascade Pipeline Mode)

The cascading examples can be easily modified to use different providers for STT, LLM, or TTS. Check the commented lines in the scripts for alternatives like OpenAI, ElevenLabs, Deepgram, etc.


## Learn More

- [VideoSDK AI Agents Documentation](https://docs.videosdk.live/ai_agents/)
- [VideoSDK Simli Plugin Documentation](https://docs.videosdk.live/ai_agents/plugins/avatar/simli)
- [VideoSDK Anam Plugin Documentation](https://docs.videosdk.live/ai_agents/plugins/avatar/anam)
- [Simli Documentation](https://docs.simli.com/)
- [Anam Documentation](https://www.anam.ai/)
