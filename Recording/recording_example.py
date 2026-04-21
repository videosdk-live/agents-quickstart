"""
Recording Example

Demonstrates all recording modes supported by VideoSDK AI Agents:

  - "off"               : No recording, vision enabled (agent still sees the screen)
  - "audio_only"        : Audio track recording only (default RecordingOptions)
  - "audio_video"       : Audio + camera video (composite participant recording)
  - "audio_screen"      : Audio + screen-share track (requires vision=True on RoomOptions)
  - "audio_video_screen": Audio + camera video + screen-share (requires vision=True)

Recording is configured via `ObservabilityOptions(recording=RecordingOptions(...))`
passed to `session.start(...)` — not via `RoomOptions`.

  - RecordingOptions()              : Default audio track recording
  - RecordingOptions.video          : Adds composite video+audio participant recording
  - RecordingOptions.screen_share   : Records screen-share tracks (requires vision=True)

See docs: https://docs.videosdk.live/ai_agents/core-components/recording

Env: see `.env.example` at the repo root for all variables (VideoSDK auth + provider keys).
"""

import logging
import aiohttp
from videosdk.agents import (
    Agent,
    AgentSession,
    JobContext,
    LoggingOptions,
    ObservabilityOptions,
    Pipeline,
    RecordingOptions,
    RoomOptions,
    WorkerJob,
    function_tool,
)
from videosdk.plugins.google import GoogleLLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
from videosdk.plugins.cartesia import CartesiaTTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()])
pre_download_model()


@function_tool
async def get_weather(latitude: str, longitude: str):
    """Called when the user asks about the weather. Estimates latitude and longitude from location name.

    Args:
        latitude: The latitude of the location
        longitude: The longitude of the location
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return {
                    "temperature": data["current"]["temperature_2m"],
                    "temperature_unit": "Celsius",
                }
            else:
                raise Exception(f"Failed to get weather data, status code: {response.status}")


class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a helpful voice assistant with screen analysis capability. "
                "When the user shares their screen, analyze what is visible and provide helpful guidance. "
                "You can also answer questions about weather and horoscopes."
            ),
            tools=[get_weather],
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")

    @function_tool
    async def get_horoscope(self, sign: str) -> dict:
        """Get today's horoscope for a given zodiac sign.

        Args:
            sign: The zodiac sign (e.g., Aries, Taurus, Gemini, etc.)
        """
        horoscopes = {
            "Aries": "Today is your lucky day!",
            "Taurus": "Focus on your goals today.",
            "Gemini": "Communication will be important today.",
        }
        return {
            "sign": sign,
            "horoscope": horoscopes.get(sign, "The stars are aligned for you today!"),
        }


# ---------------------------------------------------------------------------
# Recording mode selector
# Set RECORDING_MODE to exercise each RecordingOptions configuration.
#
# Recording is enabled by passing `ObservabilityOptions(recording=RecordingOptions(...))`
# to `session.start(...)`. RecordingOptions() defaults to audio track recording.
# `video=True` adds composite camera video; `screen_share=True` requires `vision=True` on RoomOptions.
# ---------------------------------------------------------------------------
RECORDING_MODE = "audio_only"
# Choices: "off" | "audio_only" | "audio_video" | "audio_screen" | "audio_video_screen"


def make_recording_options() -> RecordingOptions | None:
    if RECORDING_MODE == "off":
        return None
    if RECORDING_MODE == "audio_only":
        return RecordingOptions()
    if RECORDING_MODE == "audio_video":
        return RecordingOptions(video=True)
    if RECORDING_MODE == "audio_screen":
        return RecordingOptions(screen_share=True)
    if RECORDING_MODE == "audio_video_screen":
        return RecordingOptions(video=True, screen_share=True)
    raise ValueError(
        f"Unknown RECORDING_MODE={RECORDING_MODE!r}. "
        'Use "off", "audio_only", "audio_video", "audio_screen", or "audio_video_screen".'
    )


async def entrypoint(ctx: JobContext):
    agent = VoiceAgent()

    pipeline = Pipeline(
        stt=DeepgramSTT(),
        llm=GoogleLLM(),
        tts=CartesiaTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector()
    )

    session = AgentSession(agent=agent, pipeline=pipeline)

    recording = make_recording_options()
    observability = ObservabilityOptions(
        recording=recording,
        logs=LoggingOptions(level=["INFO", "DEBUG"]),
    ) if recording is not None else ObservabilityOptions(
        logs=LoggingOptions(level=["INFO", "DEBUG"]),
    )

    await session.start(
        wait_for_participant=True,
        run_until_shutdown=True,
        observability=observability,
    )


def make_context() -> JobContext:
    room_id = "<room_id>"  # Replace with your actual room_id
    name = "Recording Agent"
    playground = True

    # vision=True is required for any mode that records the screen-share track.
    needs_vision = RECORDING_MODE in ("audio_screen", "audio_video_screen", "off")

    room_options = RoomOptions(
        room_id=room_id,
        name=name,
        playground=playground,
        vision=needs_vision,
    )

    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
