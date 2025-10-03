# Recording

The AI Agent SDK supports session recordings, enabled via a simple context flag. When enabled, all user–agent interactions are recorded. Recordings can be played back from the dashboard with autoscrolling transcripts and precise timestamps, or downloaded for offline analysis.


## Enabling Recording (Participant Recording)

Set the `recording` flag to `True` in the session context. No pipeline changes are required.

```python
from videosdk.agents import JobContext, RoomOptions

job_context = JobContext(
    room_options=RoomOptions(
        room_id="YOUR_ROOM_ID",
        name="Agent",
        recording=True
    )
)
```
Note: `recording` defaults to `False`.

## Meeting Recording
Meeting recording captures the entire meeting session as a single composite recording, including all participants and their interactions.

code snippet for starting the meeting recording
```python
import os
import requests
import aiohttp

async def start_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/start"
    headers = {
        "Authorization": VIDEOSDK_AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "roomId": room_id,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Failed to start meeting recording: {response.status}, {text}")
            return await response.json()



```
code snippet to end the recording
```python

async def stop_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/end"
    headers = {
        "Authorization": VIDEOSDK_AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "roomId": room_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Failed to stop meeting recording: {response.status}, {text}")
            return await response.json()

```

## Track Recording
Track recording provides granular control over individual audio and video tracks, allowing you to record specific streams with custom configurations.

script to start audio/video track recording
```python
def start_track_recording(participant_id: str, kind="audio"):
    url = "https://api.videosdk.live/v2/recordings/participant/track/start"
    payload = {
        "roomId": ROOM_ID,
        "participantId": participant_id,
        "kind": kind,
        "fileFormat": "webm",
        "webhookUrl": "https://www.example.com/",
        "bucketDirPath": "s3path"
    }
    headers = {
        "Authorization": VIDEOSDK_API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Started {kind} recording for participant {participant_id}: {response.text}")

```

script to end audio/video track recording
```python
def stop_track_recording(participant_id: str, kind="audio"):
    url = "https://api.videosdk.live/v2/recordings/participant/track/stop"
    payload = {
        "roomId": ROOM_ID,
        "participantId": participant_id,
        "kind": kind
    }
    headers = {
        "Authorization": VIDEOSDK_API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Stopped {kind} recording for participant {participant_id}: {response.text}")

```
Getting Participant IDs for Track Recording

Participant IDs can be extracted dynamically from stream events:
```python
# Called automatically when a participant's stream is enabled
def on_stream_enabled(self, participant_id: str, kind="audio"):
    start_track_recording(participant_id, kind)

# Called automatically when a participant's stream is disabled
def on_stream_disabled(self, participant_id: str, kind="audio"):
    stop_track_recording(participant_id, kind)
```

For more details, see the Recording guide: https://docs.videosdk.live/ai_agents/recording