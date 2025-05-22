# 🚀 OpenAI Agent for VideoSDK

This directory contains example code for integrating an OpenAI-powered voice agent into VideoSDK meetings.

## 🛠️ Installation

Install the OpenAI-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-openai"
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder API key in `openai_agent_quickstart.py` with your actual OpenAI API key
   ```python
   model = OpenAIRealtime(
       model="gpt-4o-realtime-preview",
       api_key="your-openai-api-key",  # Or use environment variable OPENAI_API_KEY
       # ...
   )
   ```

2. Set your VideoSDK credentials in the context dictionary:
   ```python
   def make_context():
       return {
           "meetingId": "your-meeting-id",               # VideoSDK meeting ID
           "name": "OpenAI Agent",                       # Name displayed in the meeting
           "videosdk_auth": "your-videosdk-auth-token"   # VideoSDK auth token
       }
   ```

   You can also use environment variables instead:
   ```python
   def make_context():
       return {
           "meetingId": os.environ.get("VIDEOSDK_MEETING_ID"),
           "name": "OpenAI Agent",
           "videosdk_auth": os.environ.get("VIDEOSDK_AUTH_TOKEN")
       }
   ```

## Running the Example

To run the OpenAI-powered agent:

```bash
python openai_agent_quickstart.py
```

## ✨ Key Features

- **Real-time Voice Conversations**: Natural voice interactions with AI agents
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination

## 🧠 OpenAI Configuration

The agent uses OpenAI's real-time models for text and audio interactions. Configuration options include:

- `model`: The OpenAI model to use (e.g., `"gpt-4o-realtime-preview"`)
- `api_key`: Your OpenAI API key (can also be set via environment variable)
- `config`: Advanced configuration options including voice, temperature, turn detection, etc.

For complete configuration options, see the [official VideoSDK OpenAI plugin documentation](https://docs.videosdk.live/ai_agents/plugins/openai).

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
