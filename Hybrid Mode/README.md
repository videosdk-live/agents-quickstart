# Hybrid Mode

Hybrid Mode lets you mix a realtime LLM with a custom STT or TTS provider inside a single `Pipeline(...)` call. This gives you the ultra-low-latency of a realtime model while still controlling which voice speaks or which speech recognizer listens.

## What is Hybrid Mode?

Normally you choose one of two pipeline modes:

- **Cascade Pipeline Mode** — bring your own STT + LLM + TTS (full control, slightly higher latency)
- **Realtime Pipeline Mode** — single realtime model handles audio end-to-end (lowest latency, less control)

**Hybrid Mode** sits between the two. You use a realtime LLM but override either the STT or TTS with a provider of your choice.

## Two Variants

### Variant 1 — Realtime LLM + Custom TTS

**File**: `hybrid_realtime_custom_tts.py`

```python
pipeline = Pipeline(llm=realtimeModel, tts=customTTS)
```

Use this when:
- You want the low latency of a realtime model
- You need a specific voice that the realtime model does not offer natively
- You want to use a TTS provider with better language support for your market

Example: use a Gemini or OpenAI realtime model for fast responses, but route audio output through ElevenLabs for a custom branded voice.

### Variant 2 — Custom STT + Realtime LLM

**File**: `hybrid_custom_stt_realtime.py`

```python
pipeline = Pipeline(stt=customSTT, llm=realtimeModel, vad=vadModel)
```

Use this when:
- You need a specific STT provider (e.g. for a language or accent not well supported by the realtime model's built-in transcription)
- You want to pre-process or normalize transcripts before they reach the LLM
- You require domain-specific speech recognition (medical, legal, etc.)

A VAD (Voice Activity Detection) model is typically required when supplying a custom STT so the pipeline knows when the user has finished speaking.

## Required Environment Variables

Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in:

- **VideoSDK auth** (pick one): `VIDEOSDK_AUTH_TOKEN`, **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT).
- **Provider keys** for whichever providers you configure, for example: `OPENAI_API_KEY` (OpenAI realtime LLM/TTS), `DEEPGRAM_API_KEY` (Deepgram STT), `ELEVENLABS_API_KEY` (ElevenLabs TTS), `GOOGLE_API_KEY` (Gemini realtime), `XAI_API_KEY` (xAI realtime), `CARTESIA_API_KEY` (Cartesia TTS), `SARVAMAI_API_KEY` (SarvamAI STT).

## Run Commands

```bash
# Realtime LLM + Custom TTS
uv run python "Hybrid Mode/hybrid_realtime_custom_tts.py"

# Custom STT + Realtime LLM
uv run python "Hybrid Mode/hybrid_custom_stt_realtime.py"
```

## When to Use Each Variant

| Scenario | Recommended Variant |
| :------- | :------------------ |
| You want a specific voice / branded audio output | Realtime LLM + Custom TTS |
| Your users speak a language with better 3rd-party STT support | Custom STT + Realtime LLM |
| You need domain-specific speech recognition (medical, legal) | Custom STT + Realtime LLM |
| You want the simplest low-latency setup | Standard Realtime Pipeline Mode |
| You need full control over all three stages | Standard Cascade Pipeline Mode |
