# 🤖 Agent to Agent (A2A) - VideoSDK Multi-Agent Framework

The Agent to Agent (A2A) protocol enables seamless collaboration between specialized AI agents, allowing them to communicate, share knowledge, and coordinate responses based on their unique capabilities and domain expertise.

![A2A Architecture](https://cdn.videosdk.live/website-resources/docs-resources/a2a_diagram.png)

## 🌟 How It Works

1. **Agent Registration**: Agents register with capabilities and domain expertise
2. **Client Query**: User sends query to main agent
3. **Agent Discovery**: Main agent finds relevant specialists
4. **Query Forwarding**: Forwards specialized queries to appropriate agents
5. **Response Chain**: Specialists process and respond back
6. **Client Response**: Main agent delivers final response to user

### Example Scenario

```
Client → "I want to know about personal loan rates"
   ↓
Customer Service Agent → Discovers Loan Specialist Agent
   ↓
Customer Service Agent → Forwards query to specialist
   ↓
Loan Specialist → Processes with domain expertise
   ↓
Customer Service Agent → Relays response to client
```

## 🏗️ Quick Start

### Prerequisites
- Python 3.12 or higher
- VideoSDK authentication token
- Google Gemini API key
- VideoSDK meeting ID

### Installation & Setup

1. **Navigate to A2A directory**:
```bash
cd agents-quickstart/A2A
```

2. **Install dependencies**:
```bash
pip install videosdk-agents
```

3. **Set environment variables**:
```bash
export VIDEOSDK_AUTH_TOKEN="your_videosdk_token"
export GOOGLE_API_KEY="your_gemini_api_key"
```

4. **Update meeting ID** in `main.py`:
```python
"meetingId": "YOUR_MEETING_ID"  # Replace with your meeting ID
```

5. **Run the system**:
```bash
python main.py
```

## 📁 Project Structure

```
A2A/
├── agents/
│   ├── customer_agent.py     # Voice-enabled customer service agent
│   ├── loan_agent.py         # Text-based loan specialist
│   └── README.md             # Implementation guide
├── session_manager.py        # Session and pipeline management
├── main.py                   # System entry point
└── README.md                 # This file
```

## 💬 Usage Example

1. **User**: *"Hi, I want to know about personal loan rates"*
2. **Customer Agent**: *"Let me get that information from our loan specialist..."*
3. **System**: Routes to Loan Agent → processes → returns response
4. **Customer Agent**: *"Personal loans are available starting at 8.5% APR..."*

## ✨ Key Features

- **Multi-Modal Communication**: Audio agents for users, text agents for processing
- **Domain Specialization**: Customer service, loans, and easily extensible to new domains
- **Intelligent Routing**: Automatic query detection and specialist forwarding
- **Real-Time Collaboration**: Seamless agent-to-agent communication

## 🔧 Agent Configuration

### Customer Service Agent
- **Audio-enabled** for real-time voice interaction
- **Joins VideoSDK meeting** for user communication
- **Routes queries** to appropriate specialists

### Loan Specialist Agent
- **Text-based processing** for efficient responses
- **Background operation** (no meeting join required)
- **Domain expertise** in loan products and rates

## 🌟 Benefits

- **Seamless Experience**: Single conversation with access to multiple specialists
- **Real-time Responses**: No waiting for transfers or callbacks
- **Expert Knowledge**: Domain-specific expertise delivered naturally
- **Cost Effective**: Reduce need for multiple human specialists

## 📚 Learn More

- **[A2A Overview](https://docs.videosdk.live/ai_agents/a2a/overview)** - Core concepts and components
- **[A2A Implementation](https://docs.videosdk.live/ai_agents/a2a/implementation)** - Complete implementation guide
- **[Agent Architecture Guide](./agents/README.md)** - Detailed code examples
- **[VideoSDK AI Agents](https://docs.videosdk.live/ai_agents/introduction)** - Framework documentation

---

**Made with ❤️ by the VideoSDK Team** | [Join our Discord](https://discord.com/invite/f2WsNDN9S5) 
