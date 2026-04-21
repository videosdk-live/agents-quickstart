# Room Options

`RoomOptions` is the central configuration class for VideoSDK AI Agents. It controls how the agent connects to a meeting, the transport mode, and the session lifecycle. Recording, traces, metrics, and logs now live on **`ObservabilityOptions`** and are passed to `session.start(...)`.

## Configuration Modes

The example uses a `CONFIG_MODE` variable to demonstrate each configuration area:

| Mode | What it shows |
|---|---|
| `"basic"` | Minimal setup with playground mode |
| `"production"` | Session timeouts, recording on `session.start`, no playground |
| `"telemetry"` | Full OpenTelemetry: traces, metrics, log export on `session.start` |
| `"websocket"` | WebSocket transport |
| `"webrtc"` | WebRTC transport with custom signaling + ICE servers |

## Running the Example

```bash
uv run python "Room Options/room_options_example.py"
```

Set `CONFIG_MODE` in the file to switch configurations.

## Key Parameters

### Connection & Identity
```python
RoomOptions(
    room_id="your-room-id",
    name="My Agent",
    agent_participant_id="agent-1", # optional custom participant ID
    playground=True,                # prints a playground URL to console
)
```

VideoSDK auth is read from env vars — set either `VIDEOSDK_AUTH_TOKEN`, **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT). No `auth_token=` argument is needed on `RoomOptions`.

### Session Management
```python
RoomOptions(
    room_id="...",
    auto_end_session=True,
    session_timeout_seconds=10,         # wait 10s after last participant leaves
    no_participant_timeout_seconds=60,  # shut down if nobody joins within 60s
)
```

### Recording (via `ObservabilityOptions` on `session.start`)
```python
from videosdk.agents import ObservabilityOptions, RecordingOptions

await session.start(
    wait_for_participant=True,
    run_until_shutdown=True,
    observability=ObservabilityOptions(
        recording=RecordingOptions(
            video=True,         # add camera video
            screen_share=True,  # add screen share (needs vision=True on RoomOptions)
        ),
    ),
)

# RoomOptions only needs vision=True when recording screen-share tracks:
RoomOptions(room_id="...", vision=True)
```

### Telemetry — OpenTelemetry traces / metrics / logs (via `ObservabilityOptions`)
```python
from videosdk.agents import (
    ObservabilityOptions,
    TracesOptions,
    MetricsOptions,
    LoggingOptions,
)

await session.start(
    wait_for_participant=True,
    run_until_shutdown=True,
    observability=ObservabilityOptions(
        traces=TracesOptions(
            enabled=True,
            export_url="https://your-collector.com/v1/traces",
            export_headers={"Authorization": "Bearer TOKEN"},
        ),
        metrics=MetricsOptions(
            enabled=True,
            export_url="https://your-collector.com/v1/metrics",
        ),
        logs=LoggingOptions(
            enabled=True,
            level=["INFO", "DEBUG"],
            export_url="https://your-collector.com/v1/logs",
        ),
    ),
)

# Dashboard log forwarding still lives on RoomOptions:
RoomOptions(room_id="...", send_logs_to_dashboard=True, dashboard_log_level="INFO")
```

### Transport Modes
```python
from videosdk.agents import WebSocketConfig, WebRTCConfig

# WebSocket
RoomOptions(transport_mode="websocket", websocket=WebSocketConfig(port=8080, path="/ws"))

# WebRTC
RoomOptions(
    transport_mode="webrtc",
    webrtc=WebRTCConfig(
        signaling_url="wss://your-signaling-server.com",
        ice_servers=[{"urls": "stun:stun.l.google.com:19302"}],
    ),
)
```

## Environment Variables

Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in the keys this example uses: `OPENAI_API_KEY`, `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`.

For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY`.

For full parameter reference, see: https://docs.videosdk.live/ai_agents/core-components/room-options
