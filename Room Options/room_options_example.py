"""
RoomOptions Configuration Example

Demonstrates the full range of RoomOptions parameters:

  - Connection & Identity    : room_id, auth_token, name, agent_participant_id
  - Session Management       : auto_end_session, session_timeout_seconds, no_participant_timeout_seconds
  - Media & Features         : vision, recording, RecordingOptions, background_audio
  - Telemetry                : TracesOptions, MetricsOptions, LoggingOptions (OpenTelemetry export)
  - Dashboard                : send_logs_to_dashboard, dashboard_log_level
  - Transport Modes          : VideoSDK (default), WebSocket, WebRTC

Select a configuration by setting CONFIG_MODE at the bottom of this file:
  "basic"       — minimal setup, playground mode
  "production"  — session timeouts, recording, no playground
  "telemetry"   — OpenTelemetry traces + metrics + log export
  "websocket"   — WebSocket transport
  "webrtc"      — WebRTC transport with custom signaling

See docs: https://docs.videosdk.live/ai_agents/core-components/room-options

Env: VIDEOSDK_AUTH_TOKEN, OPENAI_API_KEY, DEEPGRAM_API_KEY, ELEVENLABS_API_KEY
"""

import logging
from videosdk.agents import (
    Agent,
    AgentSession,
    JobContext,
    Pipeline,
    RoomOptions,
    RecordingOptions,
    TracesOptions,
    MetricsOptions,
    LoggingOptions,
    WebSocketConfig,
    WebRTCConfig,
    WorkerJob,
)
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
pre_download_model()


class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant.")

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")


async def entrypoint(ctx: JobContext):
    agent = VoiceAgent()

    pipeline = Pipeline(
        stt=DeepgramSTT(),
        llm=OpenAILLM(),
        tts=ElevenLabsTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector(),
    )

    session = AgentSession(agent=agent, pipeline=pipeline)
    await session.start(wait_for_participant=True, run_until_shutdown=True)


# ---------------------------------------------------------------------------
# Configuration selector
# Set CONFIG_MODE to switch between different RoomOptions configurations.
# ---------------------------------------------------------------------------
CONFIG_MODE = "basic"
# Choices: "basic" | "production" | "telemetry" | "websocket" | "webrtc"


def make_context() -> JobContext:
    room_id = "<room_id>"  # Replace with your actual room_id

    if CONFIG_MODE == "basic":
        # Minimal setup — good for local development and playground testing
        room_options = RoomOptions(
            room_id=room_id,
            name="My Agent",
            playground=True,            # Prints a playground URL to the console
        )

    elif CONFIG_MODE == "production":
        # Production-ready: timeouts, recording, no playground
        room_options = RoomOptions(
            room_id=room_id,
            name="Production Agent",
            playground=False,
            # Session management
            auto_end_session=True,
            session_timeout_seconds=10,         # Wait 10s after last participant leaves before ending
            no_participant_timeout_seconds=60,  # Shut down if no participant joins within 60s
            # Audio recording (default track recording)
            recording=True,
            recording_options=RecordingOptions(video=True),  # Also capture composite video
        )

    elif CONFIG_MODE == "telemetry":
        # Full OpenTelemetry observability: traces, metrics, logs exported to your collector
        room_options = RoomOptions(
            room_id=room_id,
            name="Telemetry Agent",
            playground=True,
            # OpenTelemetry trace export
            traces=TracesOptions(
                enabled=True,
                export_url="https://your-otel-collector.example.com/v1/traces",
                export_headers={"Authorization": "Bearer YOUR_TOKEN"},
            ),
            # OpenTelemetry metrics export
            metrics=MetricsOptions(
                enabled=True,
                export_url="https://your-otel-collector.example.com/v1/metrics",
                export_headers={"Authorization": "Bearer YOUR_TOKEN"},
            ),
            # Log export
            logs=LoggingOptions(
                enabled=True,
                level="DEBUG",  # DEBUG | INFO | WARNING | ERROR
                export_url="https://your-otel-collector.example.com/v1/logs",
                export_headers={"Authorization": "Bearer YOUR_TOKEN"},
            ),
            # Also send logs to the VideoSDK dashboard
            send_logs_to_dashboard=True,
            dashboard_log_level="INFO",
        )

    elif CONFIG_MODE == "websocket":
        # WebSocket transport — useful for custom server-side integrations
        room_options = RoomOptions(
            transport_mode="websocket",
            websocket=WebSocketConfig(
                port=8080,
                path="/ws",
            ),
            name="WebSocket Agent",
            playground=False,
        )

    elif CONFIG_MODE == "webrtc":
        # WebRTC transport with custom signaling server
        room_options = RoomOptions(
            transport_mode="webrtc",
            webrtc=WebRTCConfig(
                signaling_url="wss://your-signaling-server.example.com",
                signaling_type="websocket",
                ice_servers=[
                    {"urls": "stun:stun.l.google.com:19302"},
                    {
                        "urls": "turn:your-turn-server.example.com:3478",
                        "username": "user",
                        "credential": "pass",
                    },
                ],
            ),
            name="WebRTC Agent",
            playground=False,
        )

    else:
        raise ValueError(
            f"Unknown CONFIG_MODE={CONFIG_MODE!r}. "
            'Use "basic", "production", "telemetry", "websocket", or "webrtc".'
        )

    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
