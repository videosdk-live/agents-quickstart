# Recording

The AI Agent SDK supports session recordings, enabled via a simple context flag. When enabled, all user–agent interactions are recorded. Recordings can be played back from the dashboard with autoscrolling transcripts and precise timestamps, or downloaded for offline analysis.

## Enabling Recording

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

For more details, see the Recording guide: https://docs.videosdk.live/ai_agents/recording