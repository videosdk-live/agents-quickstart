import os
import requests
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig
from openai.types.beta.realtime.session import TurnDetection
from dotenv import load_dotenv
import asyncio

load_dotenv()

auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
ROOM_ID = None

def start_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/start"
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    payload = {"roomId": room_id}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def stop_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/end"
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    payload = {"roomId": room_id}
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
    def __init__(self, room_id: str):
        super().__init__(instructions="You are a helpful voice assistant that can start/stop meeting recording.")
        self.room_id = room_id

    async def on_enter(self) -> None:
        await self.session.say("Hello! I will start recording this meeting.")
        try:
            start_meeting_recording(self.room_id)
        except Exception as e:
            print("Failed to start meeting recording:", e)

    async def on_exit(self) -> None:
        await self.session.say("Goodbye! Stopping the recording now.")
        try:
            stop_meeting_recording(self.room_id)
        except Exception as e:
            print("Failed to stop meeting recording:", e)


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
    session = AgentSession(agent=MyVoiceAgent(room_id=ROOM_ID), pipeline=pipeline)

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait() 
    finally:
        await session.close()
        await context.shutdown()


def make_context() -> JobContext:
    global ROOM_ID
    ROOM_ID = get_room_id()
    room_options = RoomOptions(
        room_id=ROOM_ID,
        name="VideoSDK Realtime Agent",
        playground=True,
        recording=True
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
