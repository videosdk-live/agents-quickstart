"""
Pipeline Hooks Example
Demonstrates how to intercept and modify the pipeline at each stage using @pipeline.on() hooks.

Available hooks:
  - "stt"              : Preprocess audio before STT and normalize transcript after STT
  - "tts"              : Transform text before synthesis
  - "llm"              : Observe LLM output (text, full response)
  - "user_turn_start"  : Called when user starts speaking (transcript available)
  - "user_turn_end"    : Called when user's turn ends
  - "agent_turn_start" : Called when agent starts responding
  - "agent_turn_end"   : Called when agent finishes responding
  - "vision_frame"     : Preprocess video frames before passing to LLM

Env: see `.env.example` at the repo root for all variables (VideoSDK auth + provider keys).
"""

import logging
import re
from videosdk.agents import Agent, AgentSession, Pipeline, WorkerJob, JobContext, RoomOptions, run_stt, run_tts
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
from videosdk.plugins.google import GoogleLLM
from videosdk.plugins.cartesia import CartesiaTTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

pre_download_model()


class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant. Keep responses clear and concise.")

    async def on_enter(self):
        await self.session.say("Hello! How can I help you today?")

    async def on_exit(self):
        await self.session.say("Goodbye!")


async def entrypoint(ctx: JobContext):
    agent = VoiceAgent()

    pipeline = Pipeline(
        stt=DeepgramSTT(),
        llm=GoogleLLM(),
        tts=CartesiaTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector(),
    )

    # -------------------------------------------------------------------------
    # STT Hook: filter noise, strip filler words, normalize key phrases
    # -------------------------------------------------------------------------
    @pipeline.on("stt")
    async def stt_hook(audio_stream):
        async def audio_phase():
            async for audio in audio_stream:
                # Skip very short audio chunks (background noise)
                if len(audio) < 300:
                    continue
                yield audio

        async for event in run_stt(audio_phase()):
            if event.data and event.data.text:
                text = event.data.text.lower()

                # Strip common filler words
                text = re.sub(r"\b(uh|um|like|you know)\b", "", text)

                # Normalize domain-specific phrases
                replacements = {
                    "working hours": "office hours",
                    "timing": "office hours",
                }
                for src, dst in replacements.items():
                    text = re.sub(rf"\b{src}\b", dst, text)

                event.data.text = " ".join(text.split())
                logger.info(f"[STT] Transcript: {event.data.text}")

            yield event

    # -------------------------------------------------------------------------
    # Turn detection hooks: observe conversation flow
    # -------------------------------------------------------------------------
    @pipeline.on("user_turn_start")
    async def on_user_turn_start(transcript: str):
        logger.info(f"[USER TURN START] {transcript}")

    @pipeline.on("user_turn_end")
    async def on_user_turn_end():
        logger.info("[USER TURN END]")

    @pipeline.on("agent_turn_start")
    async def on_agent_turn_start():
        logger.info("[AGENT TURN START]")

    @pipeline.on("agent_turn_end")
    async def on_agent_turn_end():
        logger.info("[AGENT TURN END]")

    # -------------------------------------------------------------------------
    # LLM Hook: observe generated text
    # -------------------------------------------------------------------------
    @pipeline.on("llm")
    async def on_llm(data: dict):
        text = data.get("text", "")
        logger.info(f"[LLM] Generated: {text[:120]}...")

    # -------------------------------------------------------------------------
    # TTS Hook: normalize text before synthesis (e.g. time formatting)
    # -------------------------------------------------------------------------
    @pipeline.on("tts")
    async def tts_hook(text_stream):
        async def preprocess_text():
            async for text in text_stream:
                # Spell out AM/PM so TTS reads them correctly
                text = text.replace("AM", "A M").replace("PM", "P M")
                yield text

        async for audio in run_tts(preprocess_text()):
            yield audio

    # -------------------------------------------------------------------------
    # Vision Hook: passthrough (add custom frame processing here) When Vision is Enabled. In Room Options.
    # -------------------------------------------------------------------------
    @pipeline.on("vision_frame")
    async def vision_hook(frame_stream):
        async for frame in frame_stream:
            yield frame

    session = AgentSession(agent=agent, pipeline=pipeline)
    await session.start(wait_for_participant=True, run_until_shutdown=True)


def make_context() -> JobContext:
    return JobContext(
        room_options=RoomOptions(
            room_id="<room_id>",  # Replace with your actual room_id
            name="Pipeline Hooks Agent",
            playground=True,
        )
    )


if __name__ == "__main__":
    WorkerJob(entrypoint=entrypoint, jobctx=make_context).start()
