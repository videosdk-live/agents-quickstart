# Recording

The AI Agent SDK supports session recordings via `RoomOptions`. VideoSDK provides three recording types, all controlled through `recording=True` and the optional `RecordingOptions` class.

## Recording Types

| Type | How | When to use |
|---|---|---|
| **Participant Recording** (audio) | `recording=True` | Default — captures audio track automatically |
| **Participant Recording** (audio + video) | `recording=True` + `RecordingOptions(video=True)` | Composite audio+video file per participant |
| **Screen Share Recording** | `recording=True` + `RecordingOptions(screen_share=True)` + `vision=True` | Capture screen-share tracks |

## Quick Start

```python
from videosdk.agents import JobContext, RoomOptions

# Audio only (simplest)
context = JobContext(
    room_options=RoomOptions(
        room_id="YOUR_ROOM_ID",
        recording=True,
    )
)
```

## Recording Modes

### Audio Only (default)
```python
RoomOptions(room_id="...", recording=True)
```

### Audio + Camera Video
```python
from videosdk.agents import RecordingOptions

RoomOptions(
    room_id="...",
    recording=True,
    recording_options=RecordingOptions(video=True),
)
```

### Audio + Screen Share
```python
RoomOptions(
    room_id="...",
    recording=True,
    vision=True,                                        # required for screen share
    recording_options=RecordingOptions(screen_share=True),
)
```

### Audio + Video + Screen Share
```python
RoomOptions(
    room_id="...",
    recording=True,
    vision=True,
    recording_options=RecordingOptions(video=True, screen_share=True),
)
```

> `screen_share=True` requires `vision=True` — vision subscribes to the video/share streams needed for recording. Omitting it raises a `ValueError` at startup.

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

```bash
VIDEOSDK_AUTH_TOKEN=your_token
DEEPGRAM_API_KEY=your_deepgram_key
GOOGLE_API_KEY=your_google_key
CARTESIA_API_KEY=your_cartesia_key
```

For more details, see: https://docs.videosdk.live/ai_agents/core-components/recording
