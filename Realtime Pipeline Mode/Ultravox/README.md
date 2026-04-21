# 🚀 Ultravox Agent for VideoSDK

This directory contains example code for integrating an Ultravox-powered voice agent into VideoSDK meetings.

## 🛠️ Installation

Install the Ultravox-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-ultravox"
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder API key in `ultravox_realtime_agent.py` with your actual Ultravox API key
   ```python
   model = UltravoxRealtime(
       model="fixie-ai/ultravox",
       api_key="your-ultravox-api-key",  # Or use environment variable ULTRAVOX_API_KEY
       # ...
   )
   ```

2. Set your VideoSDK credentials via environment variables — set **either** `VIDEOSDK_AUTH_TOKEN`, **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT). No `auth_token=` argument needed on `RoomOptions`:
   ```python
   from videosdk.agents import JobContext, RoomOptions

   def make_context() -> JobContext:
       room_options = RoomOptions(
           room_id="your-meeting-id",                 # VideoSDK meeting ID
           name="Ultravox Agent",
           playground=True,
       )
       return JobContext(room_options=room_options)
   ```

   See [`.env.example`](../../.env.example) at the repo root for all variables (`ULTRAVOX_API_KEY` plus VideoSDK auth).

## Running the Example

To run the Ultravox-powered agent:

```bash
python ultravox_realtime_agent.py
```

When running in playground mode (`playground=True` in `RoomOptions`), a direct link will be printed to your console. You can open this link in your browser to interact with the agent.

```
Agent started in playground mode
Interact with agent here at:
https://playground.videosdk.live?token=...&meetingId=...
```

## ✨ Key Features

- **Multi-modal Interactions**: Utilize Ultravox's powerful real-time AI models
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination

## 🧠 Ultravox Configuration

The agent uses Ultravox models for real-time AI interactions. Configuration options include:

- `model`: The Ultravox model to use (e.g., `"fixie-ai/ultravox"`)
- `api_key`: Your Ultravox API key (can also be set via environment variable `ULTRAVOX_API_KEY`)
- `config`: Advanced configuration options including:
  - `voice`: Voice ID (e.g., `"54ebeae1-88df-4d66-af13-6c41283b4332"`)
  - `language_hint`: Language code for the conversation (e.g., `"en"`)
  - `temperature`: Controls randomness in responses (0.0 to 1.0)
  - `vad_turn_endpoint_delay`: Voice activity detection turn endpoint delay in milliseconds
  - `vad_minimum_turn_duration`: Minimum turn duration in milliseconds

For complete configuration options, see the [official VideoSDK Ultravox plugin documentation](https://docs.videosdk.live/ai_agents/plugins/ultravox).

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
