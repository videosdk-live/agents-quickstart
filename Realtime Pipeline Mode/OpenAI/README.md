# 🚀 OpenAI Agent for VideoSDK

This directory contains example code for integrating an OpenAI-powered voice agent into VideoSDK meetings with Model Context Protocol (MCP) support.

## 🛠️ Installation

Install the OpenAI-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-openai"
pip install fastmcp  # For MCP server support
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder API key in `openai_realtime_agent.py` with your actual OpenAI API key
   ```python
   model = OpenAIRealtime(
       model="gpt-4o-realtime-preview",
       api_key="your-openai-api-key",  # Or use environment variable OPENAI_API_KEY
       # ...
   )
   ```

2. Set your VideoSDK credentials via environment variables — set **either** `VIDEOSDK_AUTH_TOKEN`, **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT). No `auth_token=` argument needed on `RoomOptions`:
   ```python
   from videosdk.agents import JobContext, RoomOptions

   def make_context() -> JobContext:
       room_options = RoomOptions(
           room_id="your-meeting-id",               # VideoSDK meeting ID
           name="OpenAI Agent",
           playground=True
       )
       return JobContext(room_options=room_options)
   ```

   See [`.env.example`](../../.env.example) at the repo root for all variables (`OPENAI_API_KEY` plus VideoSDK auth).

## Running the Example

To run the OpenAI-powered agent:

```bash
python openai_realtime_agent.py
```

When running in playground mode (`playground=True` in `RoomOptions`), a direct link will be printed to your console. You can open this link in your browser to interact with the agent.

```
Agent started in playground mode
Interact with agent here at:
https://playground.videosdk.live?token=...&meetingId=...
```

## ✨ Key Features

- **Real-time Voice Conversations**: Natural voice interactions with AI agents
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination
- **🔗 MCP Integration**: Connect to multiple Model Context Protocol servers for extended functionality
  - **MCPServerStdio**: Local process communication for development and testing
  - **MCPServerHTTP**: Remote service integration for production environments
  - **Multiple MCP Servers**: Support for simultaneous connections to various data sources and tools

## 🔗 MCP (Model Context Protocol) Integration

This agent demonstrates MCP integration with both STDIO and HTTP transport methods:

```python
from videosdk.agents import MCPServerStdio, MCPServerHTTP

# STDIO transport for local MCP server
mcp_script = Path(__file__).parent.parent / "MCP Server" / "mcp_stdio_example.py"
MCPServerStdio(
    executable_path=sys.executable,
    process_arguments=[str(mcp_script)],
    session_timeout=30
)

# HTTP transport for remote services (e.g., Zapier)
MCPServerHTTP(
    endpoint_url="https://mcp.zapier.com/api/mcp/s/your-server-id",
    session_timeout=30
)
```

For more details on MCP integration, see the [MCP Server README](../MCP Server/README.md).

## 🧠 OpenAI Configuration

The agent uses OpenAI's real-time models for text and audio interactions. Configuration options include:

- `model`: The OpenAI model to use (e.g., `"gpt-4o-realtime-preview"`)
- `api_key`: Your OpenAI API key (can also be set via environment variable)
- `config`: Advanced configuration options including voice, temperature, turn detection, etc.

For complete configuration options, see the [official VideoSDK OpenAI plugin documentation](https://docs.videosdk.live/ai_agents/plugins/openai).

## 📝 Transcription Support

You can capture real-time transcripts from both the user and the agent. Enable input audio transcription in the model config and subscribe to the transcription event on the pipeline:

```python
# Enable transcription in the model config
model = OpenAIRealtime(
    model="gpt-4o-realtime-preview",
    config=OpenAIRealtimeConfig(
        # ... other config
        input_audio_transcription=InputAudioTranscription(model="whisper-1"),
    ),
)

# Listen for transcripts (user and agent)
def on_transcription(data: dict):
    role = data.get("role")
    text = data.get("text")
    print(f"[TRANSCRIPT][{role}]: {text}")

pipeline.on("realtime_model_transcription", on_transcription)
```

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
