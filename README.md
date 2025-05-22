# 🚀 VideoSDK AI Agent Quick Start

This repository contains quick start examples for integrating AI-powered voice agents into VideoSDK meetings using different LLM providers (OpenAI, Google Gemini, and AWS NovaSonic).

## What are VideoSDK AI Agents?

The VideoSDK AI Agent framework is a Python SDK that enables AI-powered agents to join VideoSDK rooms as participants. This framework serves as a real-time bridge between AI models (like OpenAI, Google Gemini, and AWS) and your users, facilitating seamless voice and media interactions.

### Architecture Overview

- **Your Backend**: Hosts the Worker and Agent Job that powers the AI agents
- **VideoSDK Cloud**: Manages the meeting rooms where agents and users interact in real time
- **Client SDK**: Applications on user devices (web, mobile, or SIP) that connect to VideoSDK meetings

## ✨ Key Features

- **Voice-Enabled AI Agents**: Integrate AI agents that can speak and listen in real-time meetings
- **Multiple LLM Providers**: Support for OpenAI, Google Gemini, and AWS Nova Sonic
- **Function Tools**: Enable your agents with capabilities like retrieving data or performing actions
- **Real-time Communication**: Seamless integration with VideoSDK's real-time communication platform

## 🧠 Core Components

The SDK consists of three primary components:

1. **Agent** - Base class for defining agent behavior and capabilities
2. **Pipeline** - Manages model selection and configuration
3. **Agent Session** - Combines all components into a cohesive workflow

## Prerequisites

Before you begin, ensure you have:

- Python 3.12 or higher
- A VideoSDK authentication token (generate from [app.videosdk.live](https://app.videosdk.live))
- A VideoSDK meeting ID (you can generate one using the [Create Room API](https://docs.videosdk.live/api-reference/realtime-communication/create-room))
- API key for your chosen LLM provider (OpenAI, Google Gemini, or AWS)
- Client-side implementation with any VideoSDK SDK

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/videosdk-live/agents-quickstart
```

2. Create and activate a virtual environment with Python 3.12 or higher:
```bash
# On macOS/Linux
python3.12 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install the base package:
```bash
pip install videosdk-agents
```

4. Then navigate to your choice of example available:
- [OpenAI Agent](./OpenAI)
- [Google Gemini Agent](./Google%20Gemini)
- [AWS Nova Sonic Agent](./AWS%20Nova%20Sonic)

## Environment Setup

It's recommended to use environment variables for secure storage of API keys and tokens. Create a `.env` file in your project root:

```bash
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token
```

## Generating a VideoSDK Meeting ID

Before your AI agent can join a meeting, you'll need to create a meeting ID. You can generate one using the VideoSDK Create Room API:

### Using cURL

```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: VIDEOSDK_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

For more details on the Create Room API, refer to the [VideoSDK documentation](https://docs.videosdk.live/api-reference/realtime-communication/create-room).

## Connecting with VideoSDK Client Applications

After setting up your AI Agent, you'll need a client application to connect with it. You can use any of the VideoSDK quickstart examples to create a client that joins the same meeting:

- [JavaScript](https://github.com/videosdk-live/quickstart/tree/main/js-rtc)
- [React](https://github.com/videosdk-live/quickstart/tree/main/react-rtc)
- [React Native](https://github.com/videosdk-live/quickstart/tree/main/react-native)
- [Android](https://github.com/videosdk-live/quickstart/tree/main/android-rtc)
- [Flutter](https://github.com/videosdk-live/quickstart/tree/main/flutter-rtc)
- [iOS](https://github.com/videosdk-live/quickstart/tree/main/ios-rtc)

When setting up your client application, make sure to use the same meeting ID that your AI Agent is using.

## Learn More

For more information about VideoSDK AI Agents:
- [Official Documentation](https://docs.videosdk.live/ai_agents/introduction)
- [AI Voice Agent Quick Start Guide](https://docs.videosdk.live/ai_agents/voice-agent-quick-start)
- [Core Components Overview](https://docs.videosdk.live/ai_agents/core-components/overview) 

---

🤝 Join our [Discord community](https://discord.com/invite/f2WsNDN9S5) for support and discussions.

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team 