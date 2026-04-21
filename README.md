# 🚀 VideoSDK AI Agent Quick Start

This repository contains quick start examples for integrating AI-powered voice agents into VideoSDK meetings. **Featured**: Complete **Agent to Agent (A2A)** multi-agent system, **Hybrid Mode** for mixing realtime models with custom voices, **Pipeline Hooks** for intercepting and modifying pipeline stages, and virtual avatars with realistic lip-sync.

## What are VideoSDK AI Agents?

The VideoSDK AI Agent framework is a Python SDK that enables AI-powered agents to join VideoSDK rooms as participants. The framework serves as a real-time bridge between AI models (OpenAI, Google Gemini, AWS, xAI, and more) and your users, facilitating seamless voice and media interactions.

The framework offers three pipeline modes, all using the unified `Pipeline` class:

1. **Cascade Pipeline Mode** — Build agents by mixing and matching providers for STT, LLM, and TTS. Full control over every component, optimized for cost, language support, or compliance.

2. **Realtime Pipeline Mode** — Use a single realtime model (Gemini Live, OpenAI Realtime, xAI Grok, AWS Nova Sonic, Ultravox) that handles STT, LLM, and TTS in one ultra-low-latency model.

3. **Hybrid Mode** — Combine a realtime model with a custom TTS voice, or a custom STT with a realtime model. Best of both worlds.

### Architecture Overview

- **Your Backend**: Hosts the Worker and Agent Job that powers the AI agents
- **VideoSDK Cloud**: Manages the meeting rooms where agents and users interact in real time
- **Client SDK**: Applications on user devices (web, mobile, or SIP) that connect to VideoSDK meetings

## ✨ Key Features

- **Voice-Enabled AI Agents**: AI agents that can speak and listen in real-time meetings
- **Three Pipeline Modes**: Cascade, Realtime, and Hybrid — all via the unified `Pipeline` class
- **Pipeline Hooks**: Intercept and modify any pipeline stage (`stt`, `tts`, `llm`, turn events) with `@pipeline.on()` decorators
- **Multiple LLM Providers**: OpenAI, Google Gemini, AWS Nova Sonic, xAI Grok, Ultravox, Anthropic, Cerebras
- **Hybrid Mode**: Realtime LLM + custom TTS voice, or custom STT + Realtime LLM
- **🤖 Agent to Agent (A2A)**: Specialized agents collaborate and share domain expertise
- **Function Tools**: Enable agents with custom capabilities via `@function_tool`
- **MCP Integration**: Connect to external data sources with `MCPServerStdio` or `MCPServerHTTP`
- **Memory**: Long-term memory across sessions using Mem0
- **RAG**: Retrieval-Augmented Generation with ChromaDB and OpenAI embeddings
- **Virtual Avatar**: Realistic lip-synced avatars using [Simli](https://simli.com/) or [Anam](https://www.anam.ai/)
- **Human in the Loop (HITL)**: Escalate queries to a human operator via Discord
- **Vision**: Direct video input from VideoSDK rooms to Gemini Live
- **Wake Up Call**: Detect user inactivity and trigger callbacks
- **Recording**: Record complete sessions (audio and transcripts)
- **Background Audio**: Play audio while the agent is in thinking state
- **Pub/Sub Messaging**: Bidirectional text communication between agent and user
- **Reply and Interrupt**: Programmatically trigger speech or stop the agent
- **n8n Workflow Integration**: Automate outbound calls and workflow triggers via n8n MCP

## 🧠 Core Components

- **Agent**: Base class for your agent — define instructions, tools, MCP servers, and lifecycle hooks (`on_enter`, `on_exit`)
- **Pipeline**: Unified pipeline class that auto-detects the execution mode based on the components you provide:
  - `Pipeline(stt, llm, tts, vad, turn_detector)` → **Cascade Pipeline Mode**
  - `Pipeline(llm=realtimeModel)` → **Realtime Pipeline Mode**
  - `Pipeline(llm=realtimeModel, tts=customTTS)` → **Hybrid Mode** (custom voice)
  - `Pipeline(stt=customSTT, llm=realtimeModel, vad=...)` → **Hybrid Mode** (custom STT)
- **Pipeline Hooks**: `@pipeline.on("event")` decorators to intercept audio, text, and turn events at any stage
- **AgentSession**: Brings together the agent and pipeline to manage the full session lifecycle

```python
from videosdk.agents import Agent, AgentSession, Pipeline

class MyAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful assistant.", tools=[...])

    async def on_enter(self):
        await self.session.say("Hello!")

# Cascade Pipeline Mode
pipeline = Pipeline(stt=DeepgramSTT(), llm=OpenAILLM(), tts=ElevenLabsTTS(), vad=SileroVAD(), turn_detector=TurnDetector())

# Realtime Pipeline Mode
pipeline = Pipeline(llm=GeminiRealtime(...))

# Hybrid Mode — realtime model + custom voice
pipeline = Pipeline(llm=OpenAIRealtime(...), tts=CartesiaTTS())

session = AgentSession(agent=MyAgent(), pipeline=pipeline)
await session.start(wait_for_participant=True, run_until_shutdown=True)
```

## 🔗 Pipeline Hooks

Pipeline hooks let you intercept and modify any stage of the pipeline using the `@pipeline.on()` decorator — no subclassing required.

```python
# Normalize STT transcript (strip filler words)
@pipeline.on("stt")
async def stt_hook(audio_stream):
    async for event in run_stt(audio_stream):
        if event.data and event.data.text:
            event.data.text = re.sub(r"\b(uh|um)\b", "", event.data.text)
        yield event

# Inject context at turn start (RAG, memory, etc.)
@pipeline.on("user_turn_start")
async def on_user_turn_start(transcript: str):
    docs = await retrieve(transcript)
    agent.chat_context.add_message(role="system", content=f"Context: {docs}")

# Observe/modify text before TTS synthesis
@pipeline.on("tts")
async def tts_hook(text_stream):
    async def fix_text():
        async for text in text_stream:
            yield text.replace("AM", "A M")
    async for audio in run_tts(fix_text()):
        yield audio
```

Available hooks: `stt`, `tts`, `llm`, `user_turn_start`, `user_turn_end`, `agent_turn_start`, `agent_turn_end`, `vision_frame`

See the [Pipeline Hooks example](./Pipeline%20Hooks/pipeline_hooks_agent.py) for a complete walkthrough.

## 🤖 Agent to Agent (A2A) Multi-Agent System

Enable seamless collaboration between specialized AI agents, similar to [Google's A2A protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/).

### How A2A Works

1. Agents register with `AgentCard` containing their domain and capabilities
2. Main agent discovers specialists using `a2a.registry.find_agents_by_domain(domain)`
3. Main agent forwards queries with `a2a.send_message(to_agent, message_type, content)`
4. Specialist processes and responds back
5. Main agent relays response to the user

```
Client → "I want to know about personal loan rates"
   ↓
Customer Service Agent → Discovers Loan Specialist
   ↓
Customer Service Agent → Forwards loan query to Specialist
   ↓
Loan Specialist → Responds back
   ↓
Customer Service Agent → Relays response to client (audio)
```

For detailed A2A implementation, see the [A2A README](./A2A/README.md).

## Human in the Loop (HITL)

Escalate specific queries to a human operator via Discord, then relay the response back while preserving conversation flow. See `Human In The Loop/` and the [official guide](https://docs.videosdk.live/ai_agents/human-in-the-loop).

## Wake Up Call

Detect user inactivity and automatically trigger a callback to re-engage users. See `Wakeup Call/` and the [official guide](https://docs.videosdk.live/ai_agents/wakeup-call).

## Prerequisites

- Python 3.12 or higher
- VideoSDK credentials from [app.videosdk.live](https://app.videosdk.live) — either a pre-minted `VIDEOSDK_AUTH_TOKEN`, **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT at runtime)
- A VideoSDK meeting ID (from the [Create Room API](https://docs.videosdk.live/api-reference/realtime-communication/create-room))
- API key for your chosen LLM/STT/TTS provider
- Client-side implementation with any VideoSDK SDK

## 🛠️ Installation

### Quick Setup with uv (Recommended)

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone this repository
git clone https://github.com/videosdk-live/agents-quickstart

# 3. Navigate to the project directory
cd agents-quickstart

# 4. Install all dependencies
uv sync

# 5. Run any example
uv run python "Cascade Pipeline Mode/cascade_agent_quickstart.py"
```

### Quick Setup with pip

```bash
git clone https://github.com/videosdk-live/agents-quickstart
cd agents-quickstart
python3.12 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Manual Installation

```bash
pip install videosdk-agents
# Then install provider plugins as needed:
# pip install videosdk-plugins-openai videosdk-plugins-deepgram videosdk-plugins-elevenlabs ...
```

## 📁 Repository Structure

```
agents-quickstart/
│
├── A2A/                           # Featured: Complete A2A multi-agent system
│   ├── agents/
│   │   ├── customer_agent.py      # Voice-enabled customer service agent
│   │   └── loan_agent.py          # Text-based loan specialist agent
│   ├── session_manager.py         # Session and pipeline management
│   ├── main.py                    # A2A system entry point
│   └── README.md
│
├── Hybrid Mode/                   # Hybrid Mode examples
│   ├── hybrid_realtime_custom_tts.py  # Realtime LLM + custom TTS voice
│   └── hybrid_custom_stt_realtime.py  # Custom STT + Realtime LLM
│
├── Pipeline Hooks/                # Pipeline interception and modification
│   └── pipeline_hooks_agent.py    # All hook types demonstrated
│
├── n8n Workflow/                  # n8n workflow automation integration
│   ├── appointment_telephony.py   # Outbound appointment follow-up agent
│   ├── customer_followup_agent.json  # n8n workflow import file
│   └── README.md
│
├── Realtime Pipeline Mode/             # Realtime Pipeline Mode examples
│   ├── OpenAI/                    # OpenAI Realtime
│   ├── Google Gemini (LiveAPI)/   # Gemini Live
│   ├── AWS Nova Sonic/            # AWS Nova Sonic
│   ├── xAI(Grok)/                 # xAI Grok Realtime
│   └── Ultravox/                  # Ultravox
│
├── Cascade Pipeline Mode/            # Cascade Pipeline Mode (basic)
│   └── cascade_agent_quickstart.py
│
├── Advanced Cascade Pipeline Mode/   # Cascade Pipeline Mode (with EOUConfig, InterruptConfig)
│   └── advanced_cascade_pipeline.py
│
├── Memory/                        # Long-term memory with Mem0
│   ├── agent.py
│   └── memory_utils.py
│
├── RAG/                           # Retrieval-Augmented Generation with ChromaDB
│   └── rag.py
│
├── Virtual Avatar/                # Simli & Anam avatar integration
│   ├── simli_cascading_example.py
│   ├── simli_realtime_example.py
│   ├── anam_cascading_example.py
│   └── anam_realtime_example.py
│
├── Human In The Loop/             # Discord-based human oversight
├── Wakeup Call/                   # Inactivity detection and callback
├── Recording/                     # Session recording (audio, video, screen share modes)
├── Room Options/                  # Full RoomOptions config (telemetry, transports, session mgmt)
├── Reply Interrupt Agent/         # Reply and interrupt control
├── Background Audio/              # Background audio during thinking state
├── Pubsub/                        # Pub/Sub messaging
├── MCP/                           # Model Context Protocol examples
├── Vision/                        # Vision / video frame processing
├── Fallback Recovery/             # Fallback providers (FallbackSTT, FallbackTTS)
├── Multi Agent Switch/            # Dynamic agent switching via function tools
├── Call Transfer/                 # Call transfer examples
├── DTMF Handler/                  # DTMF tone handling
├── Voice Mail Detector/           # Voicemail detection
├── Knowledge Base/                # Custom knowledge base integration
├── Conversational Graph/          # State-based workflow agent
├── Utterance Handle/              # Utterance tracking and interruption handling
├── Transports/                    # Custom transport layer examples
├── mobile-quickstarts/            # Mobile-specific examples
├── IoT-quickstart/                # IoT integration
├── Unity-quickstart/              # Unity integration
│
├── pyproject.toml                 # Project configuration and dependencies
├── requirements.txt               # All dependencies
└── README.md                      # This file
```

## Environment Setup

A single `.env.example` lives at the **repo root**. Copy it to `.env` and fill in only the variables you actually need:

```bash
cp .env.example .env
```

### VideoSDK Auth — pick ONE setup

- **Setup A — pre-minted token**: set `VIDEOSDK_AUTH_TOKEN` (generated from the VideoSDK dashboard).
- **Setup B — API key + secret**: set `VIDEOSDK_API_KEY` and `VIDEOSDK_SECRET_KEY` (your dashboard credentials). The SDK auto-mints a JWT at runtime and uses it for meeting creation, join, recording, SIP, analytics, and inference.

Setup B is used **only when `VIDEOSDK_AUTH_TOKEN` is not set**. You don't need to pass anything to `RoomOptions(...)` — the SDK reads these env vars automatically.

### Provider keys

Set keys only for the providers used by the example you're running (e.g. `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `GOOGLE_API_KEY`, `CARTESIA_API_KEY`, …). See `.env.example` for the complete list.

## Generating a VideoSDK Meeting ID

```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: VIDEOSDK_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

See the [Create Room API docs](https://docs.videosdk.live/api-reference/realtime-communication/create-room).

## Connecting with VideoSDK Client Applications

Use any VideoSDK quickstart to build a client joining the same meeting:

- [JavaScript](https://github.com/videosdk-live/quickstart/tree/main/js-rtc)
- [React](https://github.com/videosdk-live/quickstart/tree/main/react-rtc)
- [React Native](https://github.com/videosdk-live/quickstart/tree/main/react-native)
- [Android](https://github.com/videosdk-live/quickstart/tree/main/android-rtc)
- [Flutter](https://github.com/videosdk-live/quickstart/tree/main/flutter-rtc)
- [iOS](https://github.com/videosdk-live/quickstart/tree/main/ios-rtc)

### Playground Mode

All examples are configured with `playground=True` by default. When you run an agent, a direct playground link is printed in your console:

```
Agent started in playground mode
Interact with agent here at:
https://playground.videosdk.live?token=...&meetingId=...
```

## 🔗 Model Context Protocol (MCP) Integration

All agent examples support MCP for connecting to external data sources and tools:

- **Local MCP Servers**: Use `MCPServerStdio` for development and testing
- **Remote MCP Services**: Use `MCPServerHTTP` for production integrations

## Learn More

- [Official Documentation](https://docs.videosdk.live/ai_agents/introduction)
- [AI Voice Agent Quick Start Guide](https://docs.videosdk.live/ai_agents/voice-agent-quick-start)
- [Core Components Overview](https://docs.videosdk.live/ai_agents/core-components/overview)
- [Cascade Pipeline Documentation](https://docs.videosdk.live/ai_agents/core-components/cascading-pipeline)
- [MCP Integration](https://docs.videosdk.live/ai_agents/mcp-integration)
- [A2A Integration Documentation](https://docs.videosdk.live/ai_agents/a2a/overview)
- [Virtual Avatar](https://docs.videosdk.live/ai_agents/plugins/avatar/simli)
- [Human in the Loop](https://docs.videosdk.live/ai_agents/human-in-the-loop)
- [Wake Up Call](https://docs.videosdk.live/ai_agents/wakeup-call)
- [Recording](https://docs.videosdk.live/ai_agents/recording)

---

🤝 Join our [Discord community](https://discord.com/invite/f2WsNDN9S5) for support and discussions.

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team
