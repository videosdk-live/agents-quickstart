import asyncio
import os
import requests
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig
from openai.types.beta.realtime.session import TurnDetection
from dotenv import load_dotenv

load_dotenv()

auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")
ROOM_ID = None

def start_track_recording(room_id: str, participant_id: str, kind: str = "audio") -> dict:
    url = "https://api.videosdk.live/v2/recordings/participant/track/start"
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    payload = {"roomId": room_id, "participantId": participant_id, "kind": kind}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()


def stop_track_recording(room_id: str, participant_id: str, kind: str = "audio") -> dict:
    url = "https://api.videosdk.live/v2/recordings/participant/track/stop"
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    payload = {"roomId": room_id, "participantId": participant_id, "kind": kind}
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
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant that starts/stops track recording.")

    async def on_enter(self):
        print("Agent entered the room")
        await self.session.say("Hello! Meeting started.")

    async def on_exit(self):
        print("Agent exiting the room")
        await self.session.say("Goodbye! Meeting ended.")

    async def on_stream_enabled(self, participant_id: str, kind="audio"):
        
        try:
            start_track_recording(ROOM_ID, participant_id, kind)
        except Exception as e:
            print(f"Error starting track: {e}")

    async def on_stream_disabled(self, participant_id: str, kind="audio"):
        
        try:
            stop_track_recording(ROOM_ID, participant_id, kind)
        except Exception as e:
            print(f"Error stopping track: {e}")



async def start_session(context: JobContext):
    model = OpenAIRealtime(
        model="gpt-realtime-2025-08-28",
        config=OpenAIRealtimeConfig(
            voice="alloy",
            modalities=["text", "audio"],
            turn_detection=TurnDetection(
                type="server_vad", threshold=0.5, prefix_padding_ms=300, silence_duration_ms=200
            ),
        ),
    )

    pipeline = RealTimePipeline(model=model)
    session = AgentSession(agent=MyVoiceAgent(), pipeline=pipeline)

    await context.connect()
    await session.start()
    
    await asyncio.Event().wait()


def make_context() -> JobContext:
    global ROOM_ID
    ROOM_ID = get_room_id()
    room_options = RoomOptions(room_id=ROOM_ID, name="VideoSDK Realtime Agent", recording=True)
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
