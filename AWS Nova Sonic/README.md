# 🚀 AWS Nova Sonic Agent for VideoSDK

This directory contains example code for integrating an AWS Nova Sonic-powered voice agent into VideoSDK meetings with Model Context Protocol (MCP) support.

## Prerequisites

Before using AWS Nova Sonic with the VideoSDK AI Agent, ensure the following:

- **AWS Account**: You have an active AWS account with permissions to access Amazon Bedrock.
- **Model Access**: You've requested and obtained access to the Amazon Nova models (Nova Lite and Nova Canvas) via the Amazon Bedrock console.
- **Region Selection**: You're operating in the US East (N. Virginia) (us-east-1) region, as model access is region-specific.
- **AWS Credentials**: Your AWS credentials (aws_access_key_id and aws_secret_access_key) are configured.

## 🛠️ Installation

Install the AWS-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-aws"
pip install fastmcp  # For MCP server support
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder AWS credentials in `aws_novasonic_agent_quickstart.py` with your actual AWS credentials
   ```python
   model = NovaSonicRealtime(
       model="amazon.nova-sonic-v1:0",
       region="us-east-1",  # Currently, only "us-east-1" is supported for Amazon Nova Sonic
       aws_access_key_id="your-aws-access-key-id",  # Or use environment variable
       aws_secret_access_key="your-aws-secret-access-key",  # Or use environment variable
       # ...
   )
   ```

2. Set your VideoSDK credentials in the `make_context` function:
   ```python
   from videosdk.agents import JobContext, RoomOptions

   def make_context() -> JobContext:
       room_options = RoomOptions(
           room_id="your-meeting-id",               # VideoSDK meeting ID
           auth_token="your-videosdk-auth-token",   # Or use environment variable VIDEOSDK_AUTH_TOKEN
           name="AWS Agent",
           playground=True
       )
       return JobContext(room_options=room_options)
   ```

   You can also use environment variables for `VIDEOSDK_MEETING_ID` and `VIDEOSDK_AUTH_TOKEN`.

## Running the Example

To run the AWS-powered agent:

```bash
python aws_novasonic_agent_quickstart.py
```

When running in playground mode (`playground=True` in `RoomOptions`), a direct link will be printed to your console. You can open this link in your browser to interact with the agent.

```
Agent started in playground mode
Interact with agent here at:
https://playground.videosdk.live?token=...&meetingId=...
```

> **Note**: To initiate a conversation with Amazon Nova Sonic, the user must speak first. The model listens for user input to begin the interaction.

## ✨ Key Features

- **Speech-to-Speech AI**: Direct speech interaction without intermediate text conversion
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination
- **🔗 MCP Integration**: Connect to multiple Model Context Protocol servers for extended functionality
  - **MCPServerStdio**: Local process communication for development and testing
  - **MCPServerHTTP**: Remote service integration for production environments
  - **Multiple MCP Servers**: Support for simultaneous connections to various data sources and tools

## 🧠 Nova Sonic Configuration

The agent uses Amazon's Nova Sonic model for real-time, speech-to-speech AI interactions. Configuration options include:

- `model`: The Nova Sonic model to use (e.g., `"amazon.nova-sonic-v1:0"`)
- `region`: AWS region where the model is hosted (currently only `"us-east-1"` is supported)
- `aws_access_key_id` and `aws_secret_access_key`: Your AWS credentials
- `config`: Advanced configuration options including voice, temperature, top_p, max_tokens, etc.

For complete configuration options, see the [official VideoSDK AWS Nova Sonic plugin documentation](https://docs.videosdk.live/ai_agents/plugins/aws-nova-sonic).

## 📝 Transcription Support

Capture real-time transcripts from both the user and the agent by subscribing to the transcription event on the pipeline:

```python
def on_transcription(data: dict):
    role = data.get("role")
    text = data.get("text")
    print(f"[TRANSCRIPT][{role}]: {text}")

pipeline.on("realtime_model_transcription", on_transcription)
```

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

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team

