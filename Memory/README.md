# Memory Agent with Mem0

A voice concierge agent that remembers conversations using [Mem0](https://app.mem0.ai/) for persistent memory storage.

## Features

- **Persistent Memory**: Remembers user preferences and details across conversations
- **Smart Memory Detection**: Automatically stores important information based on keywords
- **Personalized Greetings**: Welcomes returning users with remembered facts
- **Voice Interface**: Full voice conversation with speech-to-text and text-to-speech

## Quick Start

### 1. Get API Keys

You'll need several API keys to run this agent:

#### Mem0 API Key (Required for Memory)

1. Visit [https://app.mem0.ai/](https://app.mem0.ai/)
2. Sign up or log in to your account
3. Navigate to your dashboard to get your API key
4. Set it as an environment variable:
   ```bash
   export MEM0_API_KEY="your_mem0_api_key_here"
   ```

#### Other Required API Keys

- **OpenAI API Key**: For the LLM (GPT-4o)
  ```bash
  export OPENAI_API_KEY="your_openai_api_key_here"
  ```
- **Deepgram API Key**: For speech-to-text
  ```bash
  export DEEPGRAM_API_KEY="your_deepgram_api_key_here"
  ```
- **ElevenLabs API Key**: For text-to-speech
  ```bash
  export ELEVENLABS_API_KEY="your_elevenlabs_api_key_here"
  ```

### 2. Optional Environment Variables

```bash
# Mem0 configuration
export MEM0_DEFAULT_USER_ID="demo-voice-user"  # Default user ID for memories
export MEM0_MEMORY_LIMIT="5"                   # Number of recent memories to load

# VideoSDK configuration
export VIDEOSDK_API_KEY="your_videosdk_api_key"  # If using VideoSDK cloud
```

### 3. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 4. Run the Agent

```bash
python agent.py
```

## How It Works

### Memory Storage

The agent automatically stores memories when users say things like:

- "Remember that I like coffee"
- "My name is John"
- "I prefer morning calls"
- "My birthday is in December"

### Memory Retrieval

When a user returns, the agent:

1. Fetches their recent memories from Mem0
2. Includes them in the system prompt
3. Greets them with personalized information

### Conversation Flow

1. **Speech-to-Text**: Converts voice to text using Deepgram
2. **Memory Check**: Determines if the message should be stored
3. **LLM Processing**: Generates response using OpenAI GPT-4o
4. **Memory Storage**: Saves important information to Mem0
5. **Text-to-Speech**: Converts response to voice using ElevenLabs

## File Structure

```
Memory/
├── agent.py           # Main agent implementation
├── memory_utils.py    # Memory management utilities
└── README.md         # This file
```

## Code Overview

### `agent.py`

- Main entry point
- Sets up the voice agent with memory capabilities
- Handles session management and cleanup

### `memory_utils.py`

- `Mem0MemoryManager`: Handles all Mem0 interactions
- `Mem0ConversationFlow`: Extends conversation flow with memory storage
- `build_agent_instructions`: Creates personalized system prompts

## Testing Memory

Try these phrases to test the memory functionality:

1. **Store Information**:

   - "Remember that I prefer tea over coffee"
   - "My name is Alice"
   - "I like to be called in the morning"

2. **Retrieve Information**:
   - Start a new conversation and the agent should remember your preferences

## Troubleshooting

### Common Issues

1. **No Memory Storage**: Check that `MEM0_API_KEY` is set correctly
2. **Voice Issues**: Verify Deepgram and ElevenLabs API keys
3. **LLM Errors**: Ensure OpenAI API key is valid and has credits

### Debug Mode

Add logging to see memory operations:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## API Key Sources

- **Mem0**: [https://app.mem0.ai/](https://app.mem0.ai/)
- **OpenAI**: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Deepgram**: [https://console.deepgram.com/](https://console.deepgram.com/)
- **ElevenLabs**: [https://elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)

## Next Steps

- Customize memory keywords in `should_store()` method
- Adjust memory limit with `MEM0_MEMORY_LIMIT` environment variable
- Add more sophisticated memory categorization
- Implement memory deletion/editing capabilities
