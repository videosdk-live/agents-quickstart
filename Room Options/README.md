# Room Options

`RoomOptions` is the central configuration class for VideoSDK AI Agents. It controls everything from how the agent connects to a meeting to recording, telemetry, transport mode, and session lifecycle.

## Configuration Modes

The example uses a `CONFIG_MODE` variable to demonstrate each configuration area:

| Mode | What it shows |
|---|---|
| `"basic"` | Minimal setup with playground mode |
| `"production"` | Session timeouts, recording, no playground |
| `"telemetry"` | Full OpenTelemetry: traces, metrics, log export |
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
    auth_token="your-token",        # or set VIDEOSDK_AUTH_TOKEN env var
    name="My Agent",
    agent_participant_id="agent-1", # optional custom participant ID
    playground=True,                # prints a playground URL to console
)
```

### Session Management
```python
RoomOptions(
    room_id="...",
    auto_end_session=True,
    session_timeout_seconds=10,         # wait 10s after last participant leaves
    no_participant_timeout_seconds=60,  # shut down if nobody joins within 60s
)
```

### Recording
```python
from videosdk.agents import RecordingOptions

RoomOptions(
    room_id="...",
    recording=True,                                          # audio always recorded
    recording_options=RecordingOptions(video=True,           # add camera video
                                       screen_share=True),  # add screen share (needs vision=True)
    vision=True,  # required when screen_share=True
)
```

### Telemetry (OpenTelemetry)
```python
from videosdk.agents import TracesOptions, MetricsOptions, LoggingOptions

RoomOptions(
    room_id="...",
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
        level="DEBUG",
        export_url="https://your-collector.com/v1/logs",
    ),
    send_logs_to_dashboard=True,
    dashboard_log_level="INFO",
)
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

```bash
VIDEOSDK_AUTH_TOKEN=your_token
OPENAI_API_KEY=your_openai_key
DEEPGRAM_API_KEY=your_deepgram_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

For full parameter reference, see: https://docs.videosdk.live/ai_agents/core-components/room-options
