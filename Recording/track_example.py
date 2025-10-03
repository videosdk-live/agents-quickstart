import asyncio
import os
import requests
from dotenv import load_dotenv

from videosdk.agents import (
    Agent,
    AgentSession,
    RealTimePipeline,
    JobContext,
    RoomOptions,
    WorkerJob,
)
from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig
from openai.types.beta.realtime.session import TurnDetection

load_dotenv()
auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
ROOM_ID = None  # global room ID

def start_track_recording(room_id: str, participant_id: str, kind: str = "audio") -> dict:
    url = "https://api.videosdk.live/v2/recordings/participant/track/start"
    payload = {
        "roomId": room_id,
        "participantId": participant_id,
        "kind": kind,
    }
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()


def stop_track_recording(room_id: str, participant_id: str, kind: str = "audio") -> dict:
    url = "https://api.videosdk.live/v2/recordings/participant/track/stop"
    payload = {"roomId": room_id, "participantId": participant_id, "kind": kind}
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    return response.json()


def get_room_id() -> str:
    url = "https://api.videosdk.live/v2/rooms"
    headers = {"Authorization": auth_token}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["roomId"]


class MyVoiceAgent(Agent):
    def __init__(self, room_id):
        super().__init__(instructions="Track all participants")
        self.room_id = room_id

    async def on_enter(self):
        await self.session.say("Hello! Meeting started.")

    async def on_exit(self):
        await self.session.say("Goodbye! Meeting ended.")
        


async def start_session(context: JobContext):
    model = OpenAIRealtime(
        model="gpt-realtime-2025-08-28",
        config=OpenAIRealtimeConfig(
            voice="alloy",
            modalities=["text", "audio"],
            turn_detection=TurnDetection(
                type="server_vad",
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=200,
            ),
        ),
    )

    pipeline = RealTimePipeline(model=model)
    agent = MyVoiceAgent(room_id=ROOM_ID)
    session = AgentSession(agent=agent, pipeline=pipeline)

    await context.connect()

    
    async def monitor_participants():
        previous_ids = set()
        while True:
            current_ids = set(context.room.participants_data.keys())
            # Detect joins
            for pid in current_ids - previous_ids:
                pdata = context.room.participants_data.get(pid, {})
                name = pdata.get("name", "Unknown")
                
                
                asyncio.create_task(asyncio.to_thread(start_track_recording, ROOM_ID, pid))

            # Detect leaves
            for pid in previous_ids - current_ids:
                pdata = context.room.participants_data.get(pid, {})
                name = pdata.get("name", "Unknown")
                
                asyncio.create_task(asyncio.to_thread(stop_track_recording, ROOM_ID, pid))

            previous_ids = current_ids
            await asyncio.sleep(1)

    asyncio.create_task(monitor_participants())

    # Start agent session
    await session.start()
    
    await asyncio.Event().wait()


def make_context() -> JobContext:
    global ROOM_ID
    ROOM_ID = get_room_id()
    
    room_options = RoomOptions(
        room_id=ROOM_ID,
        name="VideoSDK Realtime Agent",
        playground=True
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
