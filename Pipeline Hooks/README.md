# Pipeline Hooks

This example demonstrates how to use `@pipeline.on()` decorators to intercept and modify pipeline stages in `Pipeline` (Cascade Pipeline Mode). Hooks give you a clean, event-driven way to run custom logic at specific points in a conversation without subclassing or overriding core framework components.

## What Are Pipeline Hooks?

Pipeline hooks are functions registered with the `@pipeline.on("<event>")` decorator. When the pipeline reaches the corresponding stage, it calls your function — allowing you to preprocess data, inject context, transform outputs, or trigger side effects.

```python
@pipeline.on("user_turn_start")
async def on_user_turn_start(agent, **kwargs):
    # Called at the start of each user turn
    pass
```

## Available Hooks

| Hook | When it fires | Common use cases |
| :--- | :------------ | :--------------- |
| `stt` | After STT produces a transcript | Normalize text, filter noise, log transcripts |
| `tts` | Before TTS receives agent text | Transform phrasing, strip markdown, inject SSML |
| `llm` | Before/after LLM call | Inject system context, log prompts/responses |
| `user_turn_start` | At the start of a user's turn | Retrieve memories, fetch user data, set context |
| `user_turn_end` | After the user finishes speaking | Store conversation facts, update databases |
| `agent_turn_start` | Before the agent begins responding | Inject dynamic instructions, update system prompt |
| `agent_turn_end` | After the agent finishes responding | Log responses, trigger downstream workflows |
| `vision_frame` | When a video frame is received | Run visual analysis, describe frame to LLM |

## When to Use Hooks

**Use hooks when you want to:**
- Preprocess audio transcripts (e.g. correct domain-specific terms)
- Normalize or clean transcripts before they reach the LLM
- Inject dynamic context (e.g. user profile, retrieved documents) into `agent.chat_context`
- Transform TTS text (e.g. strip markdown symbols that would be spoken aloud)
- Trigger external side effects (e.g. save conversation to a database, send a webhook)

**You do not need hooks when:**
- The default pipeline behavior is sufficient
- You only need to customize the system prompt at session start (use `agent.chat_context` directly)

## Setup Requirements

For stream-based hooks (`stt`, `tts`) that need to process audio streams, use the `run_stt` and `run_tts` helpers provided by the framework:

```python
from videosdk.agents import run_stt, run_tts
```

These helpers manage the async stream lifecycle so your hook can consume and re-yield chunks correctly.

## Code Examples

### Inject context at the start of a user turn

```python
@pipeline.on("user_turn_start")
async def on_user_turn_start(agent, **kwargs):
    # Example: inject the current time into the chat context
    from datetime import datetime
    agent.chat_context.append({
        "role": "system",
        "content": f"Current time: {datetime.now().strftime('%H:%M')}"
    })
```

### Normalize STT transcript

```python
@pipeline.on("stt")
async def on_stt(agent, transcript: str, **kwargs) -> str:
    # Correct a common mishearing before it reaches the LLM
    return transcript.replace("weather sdk", "VideoSDK")
```

### Transform TTS text before speaking

```python
@pipeline.on("tts")
async def on_tts(agent, text: str, **kwargs) -> str:
    import re
    # Strip markdown bold/italic markers so they are not read aloud
    return re.sub(r"[*_`]", "", text)
```

### Store information after a user turn

```python
@pipeline.on("user_turn_end")
async def on_user_turn_end(agent, transcript: str, **kwargs):
    # Example: save transcript to a database
    await my_database.save(transcript)
```

### Process video frames

```python
@pipeline.on("vision_frame")
async def on_vision_frame(agent, frame, **kwargs):
    # Analyze the frame and inject a description into the conversation
    description = await my_vision_model.describe(frame)
    agent.chat_context.append({"role": "system", "content": f"User's screen: {description}"})
```

## Running the Example

```bash
uv run python "Pipeline Hooks/pipeline_hooks_agent.py"
```

Make sure the following environment variables are set:

```
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```
