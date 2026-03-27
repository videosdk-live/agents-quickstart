"""
Recording Example

Demonstrates all recording modes supported by VideoSDK AI Agents:

  - "off"               : No recording, vision enabled (agent still sees the screen)
  - "audio_only"        : Audio track recording only (default when recording=True)
  - "audio_video"       : Audio + camera video (composite participant recording)
  - "audio_screen"      : Audio + screen-share track (requires vision=True)
  - "audio_video_screen": Audio + camera video + screen-share (requires vision=True)

Recording types overview:
  - Participant Recording  : Built-in automatic recording managed by the agent framework (recording=True)
  - RecordingOptions.video : Adds composite video+audio participant recording
  - RecordingOptions.screen_share : Records screen-share tracks (requires vision=True)

See docs: https://docs.videosdk.live/ai_agents/core-components/recording

Env: VIDEOSDK_AUTH_TOKEN, DEEPGRAM_API_KEY, GOOGLE_API_KEY, CARTESIA_API_KEY
"""

import logging
import aiohttp
from videosdk.agents import (
    Agent,
    AgentSession,
    JobContext,
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
    await session.start(wait_for_participant=True, run_until_shutdown=True)


# ---------------------------------------------------------------------------
# Recording mode selector
# Set RECORDING_MODE to exercise each RoomOptions recording configuration.
#
# recording=True always enables audio (track API).
# RecordingOptions adds camera video and/or screen-share on top.
# screen_share=True requires vision=True (validated at connect time).
# ---------------------------------------------------------------------------
RECORDING_MODE = "audio_only"
# Choices: "off" | "audio_only" | "audio_video" | "audio_screen" | "audio_video_screen"


def make_context() -> JobContext:
    room_id = "<room_id>"  # Replace with your actual room_id
    name = "Recording Agent"
    playground = True

    if RECORDING_MODE == "off":
        # No recording; vision still enabled so agent can see the screen
        room_options = RoomOptions(
            room_id=room_id,
            name=name,
            playground=playground,
            recording=False,
            vision=True,
        )
    elif RECORDING_MODE == "audio_only":
        # Audio-only track recording (default behavior when recording=True)
        room_options = RoomOptions(
            room_id=room_id,
            name=name,
            playground=playground,
            recording=True,
        )
    elif RECORDING_MODE == "audio_video":
        # Composite participant recording: audio + camera video
        room_options = RoomOptions(
            room_id=room_id,
            name=name,
            playground=playground,
            recording=True,
            recording_options=RecordingOptions(video=True),
        )
    elif RECORDING_MODE == "audio_screen":
        # Audio track + screen-share track; vision=True required
        room_options = RoomOptions(
            room_id=room_id,
            name=name,
            playground=playground,
            recording=True,
            vision=True,
            recording_options=RecordingOptions(screen_share=True),
        )
    elif RECORDING_MODE == "audio_video_screen":
        # Audio + camera video + screen-share; vision=True required
        room_options = RoomOptions(
            room_id=room_id,
            name=name,
            playground=playground,
            recording=True,
            vision=True,
            recording_options=RecordingOptions(video=True, screen_share=True),
        )
    else:
        raise ValueError(
            f"Unknown RECORDING_MODE={RECORDING_MODE!r}. "
            'Use "off", "audio_only", "audio_video", "audio_screen", or "audio_video_screen".'
        )

    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
