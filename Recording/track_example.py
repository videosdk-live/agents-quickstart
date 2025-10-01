import asyncio, os, aiohttp, requests
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig
from openai.types.beta.realtime.session import  TurnDetection
from dotenv import load_dotenv
load_dotenv()

auth_token = os.getenv("VIDEOSDK_AUTH_TOKEN")

ROOM_ID=None


async def start_meeting_recording(room_id) -> dict:
    url = "https://api.videosdk.live/v2/recordings/start"
    headers = {
        "Authorization": auth_token,
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



async def stop_meeting_recording(room_id) -> dict:
    url = "https://api.videosdk.live/v2/recordings/end"
    headers = {
        "Authorization": auth_token,
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
        
# Create a ROOM ID
def get_room_id() -> str:
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": os.getenv("VIDEOSDK_AUTH_TOKEN")
    }
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["roomId"]


class MyVoiceAgent(Agent):
    def __init__(self, room_id):
        super().__init__(instructions="You are a helpful voice assistant that can answer questions and help with tasks.")
        self.room_id = room_id

    async def on_enter(self) -> None:
        await self.session.say("Hello! I will start recording this meeting.")
        try:
            await start_meeting_recording(self.room_id)
        except Exception as e:
            pass

    async def on_exit(self) -> None:
        await self.session.say("Goodbye! Stopping the recording now.")
        try:
            await stop_meeting_recording(self.room_id)
        except Exception as e:
            pass
    
    # Called automatically when a participant's stream is enabled
    def on_stream_enabled(self, participant_id: str, kind="audio"):
        start_track_recording(participant_id, kind)

    # Called automatically when a participant's stream is disabled
    def on_stream_disabled(self, participant_id: str, kind="audio"):
        stop_track_recording(participant_id, kind)

        
async def start_session(context: JobContext):
    
    # Initialize Model
    model = OpenAIRealtime(
        model="gpt-realtime-2025-08-28",
        config=OpenAIRealtimeConfig(
            voice="alloy",  # Available voices:alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, and verse
            modalities=["text", "audio"],
            turn_detection=TurnDetection(
                type="server_vad",
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=200,
            )
        )
    )

    # Create pipeline
    pipeline = RealTimePipeline(
        model=model
    )

    session = AgentSession(
        agent=MyVoiceAgent(room_id=ROOM_ID),
        pipeline=pipeline
    )

    try:
        await context.connect()
        await session.start()
        # Keep the session running until manually terminated
        await asyncio.Event().wait()
    finally:
        # Clean up resources when done
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    global ROOM_ID
    room_id = get_room_id()
    ROOM_ID = room_id
    room_options = RoomOptions(
        # room_id= ROOM_ID,  # omit to auto-create
        name="VideoSDK Realtime Agent",
        playground=True,
        recording= True
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()