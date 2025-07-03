# 🚀 Cascading Pipeline Agent Quick Start

This example demonstrates how to use the `CascadingPipeline` to build a flexible and powerful AI voice agent. The `CascadingPipeline` allows you to mix and match different providers for Speech-to-Text (STT), Large Language Models (LLM), and Text-to-Speech (TTS), giving you complete control over your agent's architecture.

## ✨ What is the Cascading Pipeline?

The `CascadingPipeline` is a core component of the VideoSDK AI Agent framework that provides a modular approach to building AI agents. Instead of being locked into a single provider, you can choose the best service for each part of your pipeline, optimizing for cost, performance, or specific features.

### Key Features:

- **Modular Component Selection**: Independently choose providers for STT, LLM, and TTS.
- **Flexible Configuration**: Easily switch between providers like Google, OpenAI, Deepgram, and more.
- **Provider Agnostic**: Integrate a wide range of supported AI services.
- **Advanced Control**: Fine-tune each component to meet your application's needs.

For more in-depth information, please refer to the [official documentation on Cascading Pipeline](https://docs.videosdk.live/ai_agents/core-components/cascading-pipeline).

## 💬 Conversation Flow

The `CascadingPipeline` works together with the `ConversationFlow` class to manage the turn-based logic of the conversation. `ConversationFlow` allows you to implement custom logic for handling user input, preprocessing transcripts, and managing the state of the conversation before it's processed by the LLM. This is essential for building sophisticated, stateful AI agents.

In this example, the `MyConversationFlow` class is used to:
- Receive the transcript from the pipeline.
- Add the user's message to the agent's chat context.
- Process the context with the LLM to generate a response.

For a deeper dive into its capabilities, check out the [Conversation Flow documentation](https://docs.videosdk.live/ai_agents/core-components/conversation-flow).

## 🛠️ Supported Providers

This quick start script includes commented-out code for various providers, making it easy to experiment.

| Speech-to-Text (STT) | Large Language Model (LLM) | Text-to-Speech (TTS) |
| :------------------- | :------------------------- | :------------------- |
| `GoogleSTT`          | `GoogleLLM`                | `GoogleTTS`          |
| `OpenAISTT`          | `OpenAILLM`                | `OpenAITTS`          |
| `SarvamAISTT`        | `SarvamAILLM`              | `SarvamAITTS`        |
| `DeepgramSTT`        | `AnthropicLLM`             | `ElevenLabsTTS`      |
| `CartesiaSTT`        | `CerebrasLLM`              | `CartesiaTTS`        |
|                      |                            | `SmallestAITTS`      |
|                      |                            | `ResembleTTS`        |
|                      |                            | `AWSTTS`             |
|                      |                            | `GroqTTS`            |
|                      |                            | `HumeAITTS`          |
|                      |                            | `InworldAITTS`       |
|                      |                            | `LMNTTTS`            |
|                      |                            | `NeurophonicTTS`     |
|                      |                            | `RimeTTS`            |
|                      |                            | `SpeechifyTTS`       |

## 📦 Plugin Installation

While the `requirements.txt` file in the root directory installs all necessary dependencies, you can also install provider-specific plugins individually if you prefer a minimal setup. This is useful if you only plan to use a specific set of STT, LLM, or TTS services.

For example, to use OpenAI's plugins, you would run:
```bash
pip install "videosdk-plugins-openai"
```

Here are the installation commands for the providers used in this example:

| Provider   | Installation Command                            |
| :--------- | :---------------------------------------------- |
| Anthropic  | `pip install "videosdk-plugins-anthropic"`      |
| AWS        | `pip install "videosdk-plugins-aws"`            |
| Cartesia   | `pip install "videosdk-plugins-cartesia"`       |
| Cerebras   | `pip install "videosdk-plugins-cerebras"`       |
| Deepgram   | `pip install "videosdk-plugins-deepgram"`       |
| ElevenLabs | `pip install "videosdk-plugins-elevenlabs"`     |
| Google     | `pip install "videosdk-plugins-google"`         |
| Groq       | `pip install "videosdk-plugins-groq"`           |
| Hume AI    | `pip install "videosdk-plugins-humeai"`         |
| Inworld AI | `pip install "videosdk-plugins-inworldai"`      |
| LMNT       | `pip install "videosdk-plugins-lmnt"`           |
| Neuphonic  | `pip install "videosdk-plugins-neuphonic"`      |
| OpenAI     | `pip install "videosdk-plugins-openai"`         |
| Resemble   | `pip install "videosdk-plugins-resemble"`       |
| Rime       | `pip install "videosdk-plugins-rime"`           |
| SarvamAI   | `pip install "videosdk-plugins-sarvamai"`       |
| SmallestAI | `pip install "videosdk-plugins-smallestai"`     |
| Speechify  | `pip install "videosdk-plugins-speechify"`      |

## ⚙️ How to Run This Example

### 1. Set Up Your Environment

Before running the script, make sure you have the necessary API keys for the providers you intend to use. Store them in a `.env` file at the root of the project.

```
# .env
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
# ... and so on for other services
```

### 2. Configure the Pipeline

Open the `cascading_agent_quickstart.py` file. In the `start_session` function, you can select your desired STT, LLM, and TTS providers by commenting and uncommenting the relevant lines.

```python
async def start_session(context: JobContext):
    # This example uses Google's services by default.
    # You can switch to other providers by commenting and uncommenting the relevant lines.

    # STT Providers
    stt = GoogleSTT(model="latest_long")
    # stt = OpenAISTT(api_key=os.getenv("OPENAI_API_KEY"))
    # ...

    # LLM Providers
    llm = GoogleLLM(api_key=os.getenv("GOOGLE_API_KEY"))
    # llm = OpenAILLM(api_key=os.getenv("OPENAI_API_KEY"))
    # ...

    # TTS Providers
    tts = GoogleTTS(api_key=os.getenv("GOOGLE_API_KEY"))
    # tts = OpenAITTS(api_key=os.getenv("OPENAI_API_KEY"))
    # ...
```

### 3. Set Your Meeting ID

Update the `make_context` function with your VideoSDK Meeting ID.

```python
def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="YOUR_MEETING_ID", # Replace it with your actual meetingID
        name="Cascading Agent",
        playground=True,
    )
    return JobContext(room_options=room_options)
```

### 4. Run the Agent

Execute the script from your terminal:

```bash
python "Cascading Pipeline/cascading_agent_quickstart.py"
```

The agent will start and print a playground link to your console, which you can use to interact with it directly in your browser. 