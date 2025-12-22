# Fallback Recovery

This example showcases automatic fallback and recovery mechanisms for STT (Speech-to-Text), LLM (Large Language Model), and TTS (Text-to-Speech) providers.

## Features

- **Automatic fallback to lower-priority providers on failure:** If a high-priority provider fails, the system automatically switches to a configured lower-priority provider.
- **Cooldown-based retry and auto-recovery of higher-priority providers:** Failed providers enter a cooldown period and are retried after the specified duration. Once healthy, they are automatically switched back to.
- **Automatic switch-back once a provider becomes healthy:** The system intelligently monitors provider health and switches back to higher-priority providers when they become available again.

## Configuration Options

- `temporary_disable_sec`: Specifies the cooldown period (in seconds) before retrying a failed provider.
- `permanent_disable_after_attempts`: Defines the maximum number of recovery attempts before a provider is permanently disabled.

## Example Usage

```python
from videosdk.agents import FallbackSTT,FallbackLLM,FallbackTTS

stt_provider = FallbackSTT([OpenAISTT(),DeepgramSTT()],temporary_disable_sec=30.0, permanent_disable_after_attempts=3)

llm_provider = FallbackLLM([OpenAILLM(model="gpt-4o-mini"),CerebrasLLM()],temporary_disable_sec=30.0, permanent_disable_after_attempts=3)

tts_provider = FallbackTTS([OpenAITTS(voice="alloy"),CartesiaTTS()],temporary_disable_sec=30.0, permanent_disable_after_attempts=3)
```
