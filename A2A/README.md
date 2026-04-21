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
- VideoSDK credentials — either `VIDEOSDK_AUTH_TOKEN`, **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT)
- Google Gemini API key
- OpenAI API key (for specialist agents)
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

Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in: `GOOGLE_API_KEY`, `OPENAI_API_KEY`.

For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime).

4. **Update meeting ID** in `main.py`:
```python
room_id="YOUR_MEETING_ID"  # Replace with your meeting ID
```
> ⚠️ **Important:** Ensure that the JobContext is created only for the primary (main) agent, i.e., the agent responsible for user-facing interaction (e.g., Customer Agent). The background agent (e.g., Loan Agent) should not have its own context or initiate a separate connection.

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
- **Pipeline (Realtime Pipeline Mode)** with Gemini Realtime model for low-latency voice interaction
- **Audio-enabled** with voice "Leda" for real-time conversation
- **Joins VideoSDK meeting** for user communication
- **Routes queries** to appropriate specialists

### Loan Specialist Agent
- **Pipeline (Cascade Pipeline Mode)** with OpenAI LLM for efficient text processing
- **Text-based processing** for specialist responses
- **Background operation** (no meeting join required)
- **Domain expertise** in loan products and rates

## 🔧 Pipeline Architecture

The system uses a **hybrid pipeline approach** for optimal performance:

### Pipeline — Realtime Mode (Customer Agent)
- **Model**: Gemini Realtime (`gemini-2.5-flash-native-audio-preview-09-2025`)
- **Voice**: "Leda" with audio response modality
- **Purpose**: Low-latency voice interaction with users
- **Benefits**: Natural conversation flow, real-time audio processing

### Pipeline — Cascade Mode (Specialist Agent)
- **Model**: OpenAI LLM
- **Processing**: Text-only for efficient specialist responses
- **Purpose**: Background processing of domain-specific queries
- **Benefits**: Cost-effective, optimized for text-based reasoning

This architecture ensures **fast user interaction** while maintaining **efficient specialist processing** in the background.

### 🔧 Pipeline Flexibility

The VideoSDK AI Agents framework provides **flexible pipeline configurations**. You can run a full **Pipeline (Realtime Mode)** or **Pipeline (Cascade Mode)** for both modalities, or create a **hybrid setup** that combines the two. This allows you to tailor the use of STT, TTS, and LLM to suit your specific use case, whether for low-latency interactions, complex processing flows, or a mix of both.

**Configuration Examples** (available in `session_manager.py`):
- **Hybrid Setup** (Current): Pipeline (Realtime Mode) + Pipeline (Cascade Mode)
- **Full Realtime**: Both agents using Pipeline (Realtime Mode)
- **Full Cascading**: Both agents using Pipeline (Cascade Mode)
- **Custom Mix**: Any combination based on your requirements

### ⚠️ Important
> While setting up pipelines:
>
> - The **customer agent** must have **voice capabilities only** using `Pipeline` in Realtime Mode.
> - The **specialist agent** should operate in **text-only mode** using `Pipeline` in Cascade Mode.

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
