# 🚀 Google Gemini (LiveAPI) Agent for VideoSDK

This directory contains example code for integrating a Google Gemini-powered voice and vision agent (via Live API) into VideoSDK meetings, with full support for the Model Context Protocol (MCP).

## 🛠️ Installation

Install the Gemini-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-google"
pip install fastmcp  # For MCP server support
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder API key in `gemini_agent_quickstart.py` with your actual Google Gemini (LiveAPI) API key
   ```python
   model = GeminiRealtime(
       model="gemini-2.0-flash-live-001",
       api_key="your-google-api-key",  # Or use environment variable
       # ...
   )
   ```

2. Set your VideoSDK credentials in the `make_context` function:
   ```python
   from videosdk.agents import JobContext, RoomOptions

   def make_context() -> JobContext:
       room_options = RoomOptions(
           room_id="your-meeting-id",                 # VideoSDK meeting ID
           auth_token="your-videosdk-auth-token",     # Or use environment variable VIDEOSDK_AUTH_TOKEN
           name="Gemini Agent",
           playground=True,
           vision=True  # Enable vision for Gemini
       )
       return JobContext(room_options=room_options)
   ```

   You can also use environment variables for `VIDEOSDK_MEETING_ID` and `VIDEOSDK_AUTH_TOKEN`.

## Running the Example

To run the Gemini-powered agent:

```bash
python gemini_agent_quickstart.py
```

When running in playground mode (`playground=True` in `RoomOptions`), a direct link will be printed to your console. You can open this link in your browser to interact with the agent.

```
Agent started in playground mode
Interact with agent here at:
https://playground.videosdk.live?token=...&meetingId=...
```

## ✨ Key Features

- **Multi-modal Interactions**: Utilize Google's powerful Gemini models
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination
- **Vision Support**: Direct video input from VideoSDK rooms to Gemini Live by setting `vision=True` in the session context.
- **🔗 MCP Integration**: Connect to multiple Model Context Protocol servers for extended functionality
  - **MCPServerStdio**: Local process communication for development and testing
  - **MCPServerHTTP**: Remote service integration for production environments
  - **Multiple MCP Servers**: Support for simultaneous connections to various data sources and tools

## 🧠 Gemini Configuration

The agent uses Google's Gemini models for real-time, multi-modal AI interactions. Configuration options include:

- `model`: The Gemini model to use (e.g., `"gemini-2.0-flash-live-001"`) and Other supported models include: "gemini-2.5-flash-preview-native-audio-dialog" and "gemini-2.5-flash-exp-native-audio-thinking-dialog".
- `api_key`: Your Google API key (can also be set via environment variable)
- `config`: Advanced configuration options including voice, language code, temperature, etc.

For complete configuration options, see the [official VideoSDK Google Gemini (LiveAPI) plugin documentation](https://docs.videosdk.live/ai_agents/plugins/google).


## Vision Support

Google Gemini Live can also accept `video stream` directly from the VideoSDK room. To enable this, simply turn on your camera and set the `vision` flag to `True` in `RoomOptions`. Once that's done, start your agent as usual—no additional changes are required in the pipeline.

```python
def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="your-meeting-id",
        name="Gemini Agent",
        vision=True  # Set to True to enable video streaming
    )
    return JobContext(room_options=room_options)
```

* `vision` (bool, RoomOptions) – when `True`, forwards Video Stream from VideoSDK's room to Gemini's LiveAPI (defaults to `False`).

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

## 📝 Transcription Support

Capture real-time transcripts from both the user and the agent by subscribing to the transcription event on the pipeline:

```python
def on_transcription(data: dict):
    role = data.get("role")
    text = data.get("text")
    print(f"[TRANSCRIPT][{role}]: {text}")

pipeline.on("realtime_model_transcription", on_transcription)
```

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
