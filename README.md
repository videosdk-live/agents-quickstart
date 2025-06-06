# 🚀 VideoSDK AI Agent Quick Start

This repository contains quick start examples for integrating AI-powered voice agents into VideoSDK meetings using different LLM providers (OpenAI, Google Gemini LiveAPI, and AWS NovaSonic). **Featured**: Complete **Agent to Agent (A2A)** multi-agent system implementation.

## What are VideoSDK AI Agents?

The VideoSDK AI Agent framework is a Python SDK that enables AI-powered agents to join VideoSDK rooms as participants. This framework serves as a real-time bridge between AI models (like OpenAI, Google Gemini LiveAPI, and AWS) and your users, facilitating seamless voice and media interactions.

### Architecture Overview

- **Your Backend**: Hosts the Worker and Agent Job that powers the AI agents
- **VideoSDK Cloud**: Manages the meeting rooms where agents and users interact in real time
- **Client SDK**: Applications on user devices (web, mobile, or SIP) that connect to VideoSDK meetings

## ✨ Key Features

- **Voice-Enabled AI Agents**: Integrate AI agents that can speak and listen in real-time meetings
- **Multiple LLM Providers**: Support for OpenAI, Google Gemini LiveAPI, and AWS Nova Sonic
- **🤖 Agent to Agent (A2A) Communication**: Enable specialized agents to collaborate and share domain expertise
- **Function Tools**: Enable your agents with capabilities like retrieving data or performing actions
- **Real-time Communication**: Seamless integration with VideoSDK's real-time communication platform

## 🧠 Core Components

The SDK consists of three primary components:

1. **Agent** - Base class for defining agent behavior and capabilities
2. **Pipeline** - Manages model selection and configuration
3. **Agent Session** - Combines all components into a cohesive workflow

## 🤖 Agent to Agent (A2A) Multi-Agent System

Our **featured A2A implementation** enables seamless collaboration between specialized AI agents, similar to [Google's A2A protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/). This allows different agents to communicate, share knowledge, and coordinate responses based on their unique capabilities.

### **How A2A Works**

1. **Agent Registration**: Agents register themselves with an `AgentCard` containing their capabilities and domain expertise
2. **Client Query**: Client sends a query to the main agent
3. **Agent Discovery**: Main agent discovers relevant specialist agents using agent cards
4. **Query Forwarding**: Main agent forwards specialized queries to appropriate agents
5. **Response Chain**: Specialist agents process queries and respond back to the main agent
6. **Client Response**: Main agent formats and delivers the final response to the client

### **Example A2A Use Case**:
When a user asks about loan rates, the Customer Service Agent (with audio capabilities) automatically forwards the query to the Loan Agent (text-based specialist), receives the expert response, and relays it back to the user - all within a single conversation flow.

```
Client → "I want to know about personal loan rates"
   ↓
Customer Service Agent → Discovers Loan Specialist Agent
   ↓  
Customer Service Agent → Forwards loan query to Loan Specialist
   ↓
Loan Specialist → Processes query and responds back (text format)
   ↓
Customer Service Agent → Relays response to client (audio format)
```

### **Key A2A Features**:
- **Multi-Modal Communication**: Audio agents for user interaction, text agents for specialized processing  
- **Domain Specialization**: Customer service agents coordinate with loan specialists, tech support, financial advisors
- **Intelligent Query Routing**: Automatic detection and forwarding of domain-specific queries
- **Real-Time Collaboration**: Agents communicate seamlessly without user intervention

For detailed A2A implementation, see the [A2A README](./A2A/README.md).

## Prerequisites

Before you begin, ensure you have:

- Python 3.12 or higher
- A VideoSDK authentication token (generate from [app.videosdk.live](https://app.videosdk.live))
- A VideoSDK meeting ID (you can generate one using the [Create Room API](https://docs.videosdk.live/api-reference/realtime-communication/create-room))
- API key for your chosen LLM provider (OpenAI, Google Gemini LiveAPI, or AWS)
- Client-side implementation with any VideoSDK SDK

## 🛠️ Installation

### Quick Setup (Recommended)

For the fastest setup, install all dependencies at once using the provided requirements file:

```bash
# 1. Clone this repository
git clone https://github.com/videosdk-live/agents-quickstart

# 2. Navigate to the project directory
cd agents-quickstart

# 3. Create and activate a virtual environment with Python 3.12 or higher
# On macOS/Linux
python3.12 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

# 4. Install all dependencies from requirements.txt
pip install -r requirements.txt
```

### Manual Installation

Alternatively, you can install packages individually:

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
- [🤖 Agent to Agent (A2A) Multi-Agent System](./A2A) **← Featured**
- [OpenAI Agent](./OpenAI)
- [Google Gemini LiveAPI Agent](./Google%20Gemini%20%28LiveAPI%29)
- [AWS Nova Sonic Agent](./AWS%20Nova%20Sonic)
- [🔗 MCP Server Examples](./MCP%20Server)

## 🔗 Model Context Protocol (MCP) Integration

All agent examples include Model Context Protocol (MCP) support for connecting to external data sources and tools:

- **Local MCP Servers**: Use `MCPServerStdio` for development and testing
- **Remote MCP Services**: Use `MCPServerHTTP` for production integrations
- **Multiple Servers**: Connect to various data sources simultaneously

For detailed MCP integration examples, see the [MCP Server README](./MCP%20Server/README.md).

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

## 📁 Repository Structure

```
agents-quickstart/
│
├── A2A/                           # Featured: Complete A2A multi-agent system
│   ├── agents/
│   │   ├── customer_agent.py      # Voice-enabled customer service agent
│   │   ├── loan_agent.py          # Text-based loan specialist agent
│   │   └── README.md              # Detailed A2A implementation guide
│   ├── session_manager.py         # Session and pipeline management
│   ├── main.py                    # A2A system entry point
│   └── README.md                  # A2A overview and setup
│
├── OpenAI/                        # OpenAI-based agent examples
├── Google Gemini (LiveAPI)/       # Google Gemini LiveAPI examples  
├── AWS Nova Sonic/                # AWS Nova Sonic examples
├── MCP Server/                    # Model Context Protocol examples
├── requirements.txt               # All dependencies
└── README.md                      # This file
```

## Learn More

For more information about VideoSDK AI Agents:
- [Official Documentation](https://docs.videosdk.live/ai_agents/introduction)
- [AI Voice Agent Quick Start Guide](https://docs.videosdk.live/ai_agents/voice-agent-quick-start)
- [Core Components Overview](https://docs.videosdk.live/ai_agents/core-components/overview) 
- [MCP Integration](https://docs.videosdk.live/ai_agents/mcp-integration)
- [A2A Integration Documentation](https://docs.videosdk.live/ai_agents/a2a/overview)
---

🤝 Join our [Discord community](https://discord.com/invite/f2WsNDN9S5) for support and discussions.

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team 