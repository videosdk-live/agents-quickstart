# Realtime Pipeline Mode Agent Quick Start

This directory contains examples for building voice agents using `Pipeline` (Realtime Pipeline Mode). Realtime Pipeline Mode connects directly to a realtime model endpoint (e.g. OpenAI Realtime, Google Gemini Live, xAI Grok) for ultra-low-latency audio-in / audio-out interaction — no separate STT or TTS providers needed.

## What is Realtime Pipeline Mode?

`Pipeline` in Realtime Mode uses a single realtime model to handle the full conversation loop — audio input is streamed directly to the model, and audio output is streamed back. This results in very low latency and natural-sounding responses.

Use Realtime Pipeline Mode when:
- You need the lowest possible response latency
- You want a simple setup with a single model provider
- Your target provider supports a native audio realtime API

Use Cascade Pipeline Mode (see `Cascade Pipeline Mode/`) when:
- You need to mix and match STT, LLM, and TTS providers independently
- You want fine-grained control over each stage of the pipeline
- Your chosen LLM does not support a native audio endpoint

## Supported Providers

| Provider | Directory | Model Example |
| :------- | :-------- | :------------ |
| OpenAI Realtime | `OpenAI/` | `gpt-4o-realtime-preview` |
| Google Gemini Live API | `Google Gemini (LiveAPI)/` | `gemini-2.5-flash-native-audio-preview-09-2025` |
| xAI (Grok) | `xAI(Grok)/` | grok realtime model |
| AWS Nova Sonic | `AWS Nova Sonic/` | nova-sonic |
| Ultravox | `Ultravox/` | ultravox realtime |

## How to Run

Each subdirectory contains its own agent script. Navigate into the relevant provider directory and follow its setup instructions, or run from the repo root, for example:

```bash
# OpenAI Realtime
uv run python "Realtime Pipeline Mode/OpenAI/agent.py"

# Google Gemini Live API
uv run python "Realtime Pipeline Mode/Google Gemini (LiveAPI)/agent.py"
```

## Environment Variables

Set the appropriate API keys for your chosen provider. At minimum you will need:

```
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token
```

Plus the provider-specific key, for example:

```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
```