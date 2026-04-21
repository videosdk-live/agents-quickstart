"""
RoomOptions Configuration Example

Demonstrates the full range of RoomOptions parameters AND the new
`ObservabilityOptions` surface (passed to `session.start(...)`):

  RoomOptions:
    - Connection & Identity    : room_id, name, agent_participant_id
    - Session Management       : auto_end_session, session_timeout_seconds, no_participant_timeout_seconds
    - Media & Features         : vision, background_audio
    - Dashboard                : send_logs_to_dashboard, dashboard_log_level
    - Transport Modes          : VideoSDK (default), WebSocket, WebRTC

  ObservabilityOptions (passed to session.start):
    - recording : RecordingOptions       (audio / video / screen-share recording)
    - traces    : TracesOptions          (OpenTelemetry trace export)
    - metrics   : MetricsOptions         (OpenTelemetry metrics export)
    - logs      : LoggingOptions         (log levels + OTel log export)

VideoSDK auth is read from env vars (`VIDEOSDK_AUTH_TOKEN` OR
`VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY`) — no `auth_token=` argument needed.

Select a configuration by setting CONFIG_MODE at the bottom of this file:
  "basic"       — minimal setup, playground mode
  "production"  — session timeouts, recording on session.start, no playground
  "telemetry"   — OpenTelemetry traces + metrics + log export
  "websocket"   — WebSocket transport
  "webrtc"      — WebRTC transport with custom signaling

See docs: https://docs.videosdk.live/ai_agents/core-components/room-options
Env: see `.env.example` at the repo root for all variables.
"""

import logging
from videosdk.agents import (
    Agent,
    AgentSession,
    JobContext,
    LoggingOptions,
    MetricsOptions,
    ObservabilityOptions,
    Pipeline,
    RecordingOptions,
    RoomOptions,
    TracesOptions,
    WebRTCConfig,
    WebSocketConfig,
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


# ---------------------------------------------------------------------------
# Configuration selector
# Set CONFIG_MODE to switch between different RoomOptions configurations.
# ---------------------------------------------------------------------------
CONFIG_MODE = "basic"
# Choices: "basic" | "production" | "telemetry" | "websocket" | "webrtc"


def make_observability() -> ObservabilityOptions | None:
    """Build the ObservabilityOptions for the current CONFIG_MODE."""
    if CONFIG_MODE == "production":
        # Recording (audio + composite camera video) plus structured logs
        return ObservabilityOptions(
            recording=RecordingOptions(video=True),
            logs=LoggingOptions(level=["INFO", "DEBUG"]),
        )

    if CONFIG_MODE == "telemetry":
        # Full OpenTelemetry observability: traces, metrics, logs
        return ObservabilityOptions(
            traces=TracesOptions(
                enabled=True,
                export_url="https://your-otel-collector.example.com/v1/traces",
                export_headers={"Authorization": "Bearer YOUR_TOKEN"},
            ),
            metrics=MetricsOptions(
                enabled=True,
                export_url="https://your-otel-collector.example.com/v1/metrics",
                export_headers={"Authorization": "Bearer YOUR_TOKEN"},
            ),
            logs=LoggingOptions(
                enabled=True,
                level=["INFO", "DEBUG"],
                export_url="https://your-otel-collector.example.com/v1/logs",
                export_headers={"Authorization": "Bearer YOUR_TOKEN"},
            ),
        )

    return None


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

    observability = make_observability()
    start_kwargs = {"wait_for_participant": True, "run_until_shutdown": True}
    if observability is not None:
        start_kwargs["observability"] = observability

    await session.start(**start_kwargs)


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
        # Production-ready: timeouts, no playground.
        # Recording is configured via ObservabilityOptions on session.start (see make_observability).
        room_options = RoomOptions(
            room_id=room_id,
            name="Production Agent",
            playground=False,
            # Session management
            auto_end_session=True,
            session_timeout_seconds=10,         # Wait 10s after last participant leaves before ending
            no_participant_timeout_seconds=60,  # Shut down if no participant joins within 60s
        )

    elif CONFIG_MODE == "telemetry":
        # Telemetry mode — traces/metrics/logs flow through ObservabilityOptions on session.start.
        room_options = RoomOptions(
            room_id=room_id,
            name="Telemetry Agent",
            playground=True,
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
