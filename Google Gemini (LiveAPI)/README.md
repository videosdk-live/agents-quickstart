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

2. Set your VideoSDK credentials in the context dictionary:
   ```python
   def make_context():
       return {
           "meetingId": "your-meeting-id",               # VideoSDK meeting ID
           "name": "Gemini Agent",                       # Name displayed in the meeting
           "videosdk_auth": "your-videosdk-auth-token"   # VideoSDK auth token
       }
   ```

   You can also use environment variables instead:
   ```python
   def make_context():
       return {
           "meetingId": os.environ.get("VIDEOSDK_MEETING_ID"),
           "name": "Gemini Agent",
           "videosdk_auth": os.environ.get("VIDEOSDK_AUTH_TOKEN")
       }
   ```

## Running the Example

To run the Gemini-powered agent:

```bash
python gemini_agent_quickstart.py
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

Google Gemini Live can also accept `video stream` directly from the VideoSDK room. To enable this, simply turn on your camera and set the vision flag to true in the session context. Once that's done, start your agent as usual—no additional changes are required in the pipeline.

```python
pipeline = RealTimePipeline(model=model)

session = AgentSession(
    agent=my_agent,
    pipeline=pipeline,
    context={
        "meetingId": "your_actual_meeting_id_here",  # Replace with actual meeting ID
        "name": "AI Voice Agent", 
        "videosdk_auth": "your_videosdk_auth_token_here"  # Replace with actual token
        "vision": True
    }
)
```

* `vision` (bool, session context) – when `True`, forwards Video Stream from VideoSDK's room to Gemini’s LiveAPI (defaults to `False`).

## 🔗 MCP (Model Context Protocol) Integration

This agent demonstrates MCP integration with both STDIO and HTTP transport methods:

```python
from videosdk.agents import MCPServerStdio, MCPServerHTTP

# STDIO transport for local MCP server
mcp_script = Path(__file__).parent.parent / "MCP Server" / "mcp_stdio_example.py"
MCPServerStdio(
    command=sys.executable,
    args=[str(mcp_script)],
    client_session_timeout_seconds=30
)

# HTTP transport for remote services (e.g., Zapier)
MCPServerHTTP(
    url="https://mcp.zapier.com/api/mcp/s/your-server-id",
    client_session_timeout_seconds=30
)
```

For more details on MCP integration, see the [MCP Server README](../MCP Server/README.md).

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
