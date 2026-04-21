# Recording

The AI Agent SDK supports session recording via **`ObservabilityOptions`** passed to `session.start(...)`. VideoSDK provides three recording types, all controlled through `RecordingOptions`.

## Recording Types

| Type | How | When to use |
|---|---|---|
| **Participant Recording** (audio) | `RecordingOptions()` | Default — captures audio track automatically |
| **Participant Recording** (audio + video) | `RecordingOptions(video=True)` | Composite audio+video file per participant |
| **Screen Share Recording** | `RecordingOptions(screen_share=True)` + `vision=True` on RoomOptions | Capture screen-share tracks |

## Quick Start

```python
from videosdk.agents import (
    AgentSession,
    LoggingOptions,
    ObservabilityOptions,
    RecordingOptions,
)

# Audio only (simplest)
await session.start(
    wait_for_participant=True,
    run_until_shutdown=True,
    observability=ObservabilityOptions(
        recording=RecordingOptions(),
        logs=LoggingOptions(level=["INFO", "DEBUG"]),
    ),
)
```

## Recording Modes

### Audio Only (default)
```python
observability=ObservabilityOptions(recording=RecordingOptions())
```

### Audio + Camera Video
```python
observability=ObservabilityOptions(recording=RecordingOptions(video=True))
```

### Audio + Screen Share
```python
# On session.start
observability=ObservabilityOptions(recording=RecordingOptions(screen_share=True))

# On RoomOptions (vision=True required for screen-share recording)
RoomOptions(room_id="...", vision=True)
```

### Audio + Video + Screen Share
```python
# On session.start
observability=ObservabilityOptions(
    recording=RecordingOptions(video=True, screen_share=True),
)

# On RoomOptions
RoomOptions(room_id="...", vision=True)
```

> `screen_share=True` requires `vision=True` on `RoomOptions` — vision subscribes to the video/share streams needed for recording. Omitting it raises a `ValueError` at startup.

## Running the Example

The example uses a `RECORDING_MODE` variable at the top of the file to switch between all modes:

```bash
uv run python "Recording/recording_example.py"
```

Set `RECORDING_MODE` in the file to one of:
- `"off"` — no recording, vision on
- `"audio_only"` — audio track only
- `"audio_video"` — audio + camera video
- `"audio_screen"` — audio + screen share
- `"audio_video_screen"` — audio + video + screen share

## Environment Variables

Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in the keys this example uses: `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`, `CARTESIA_API_KEY`.

For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime).

For more details, see: https://docs.videosdk.live/ai_agents/core-components/recording
