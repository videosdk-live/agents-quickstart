"""
Hybrid Mode: Custom STT + Realtime LLM

In this mode, a custom Speech-to-Text provider is used for transcription (giving you
control over language, accuracy, or cost), while a Realtime model handles language
processing and audio generation.

Use this when:
- You need a specific STT provider for a particular language or accent (e.g. SarvamAI for Indian languages)
- You want STT accuracy control while benefiting from realtime model speed
- You need a custom knowledge base integrated with a realtime LLM

Pipeline auto-detects Hybrid Mode when both stt= and llm= (realtime model) are provided.

Env: VIDEOSDK_AUTH_TOKEN, GOOGLE_API_KEY, SARVAMAI_API_KEY
"""

import logging
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
from videosdk.plugins.sarvamai import SarvamAISTT
from videosdk.plugins.silero import SileroVAD

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class HybridVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant with strong multilingual support. Respond naturally."
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm using a custom STT with a realtime model. How can I help you?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")


async def entrypoint(ctx: JobContext):
    # Realtime model handles LLM + audio output (TTS built-in)
    llm = GeminiRealtime(
        model="gemini-3.1-flash-live-preview",
        # When GOOGLE_API_KEY is set in .env - DON'T pass api_key parameter
        # api_key="AI...",
        config=GeminiLiveConfig(
            voice="Puck",  # Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, Zephyr
            response_modalities=["AUDIO"],
        )
    )

    # Hybrid Mode: Custom STT + Realtime LLM
    # SarvamAI STT transcribes audio (especially effective for Indian languages),
    # then the Gemini Realtime model processes the transcript and generates audio responses.
    pipeline = Pipeline(
        stt=SarvamAISTT(),  # Custom STT — overrides the realtime model's built-in speech recognition
        llm=llm,
        vad=SileroVAD(),
    )

    session = AgentSession(agent=HybridVoiceAgent(), pipeline=pipeline)
    await session.start(wait_for_participant=True, run_until_shutdown=True)


def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="<room_id>",  # Replace with your actual room_id
        name="Hybrid Mode Agent (Custom STT + Realtime)",
        playground=True,
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
