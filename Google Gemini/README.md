# 🚀 Google Gemini Agent for VideoSDK

This directory contains example code for integrating a Google Gemini-powered voice agent into VideoSDK meetings.

## 🛠️ Installation

Install the Gemini-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-google"
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder API key in `gemini_agent_quickstart.py` with your actual Google Gemini API key
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

## 🧠 Gemini Configuration

The agent uses Google's Gemini models for real-time, multi-modal AI interactions. Configuration options include:

- `model`: The Gemini model to use (e.g., `"gemini-2.0-flash-live-001"`) and Other supported models include: "gemini-2.5-flash-preview-native-audio-dialog" and "gemini-2.5-flash-exp-native-audio-thinking-dialog".
- `api_key`: Your Google API key (can also be set via environment variable)
- `config`: Advanced configuration options including voice, language code, temperature, etc.

For complete configuration options, see the [official VideoSDK Google Gemini plugin documentation](https://docs.videosdk.live/ai_agents/plugins/google).

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
