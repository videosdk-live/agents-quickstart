import asyncio, os
from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig
from openai.types.beta.realtime.session import  TurnDetection

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant that can answer questions and help with tasks.")
    async def on_enter(self): await self.session.say("Hello! How can I help?")
    async def on_exit(self): await self.session.say("Goodbye!")

async def start_session(context: JobContext):

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
        agent=MyVoiceAgent(),
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
    room_options = RoomOptions(
    #   room_id="YOUR_MEETING_ID",  # Set to join a pre-created room; omit to auto-create
        name="VideoSDK Realtime Agent",
        playground=True,
        recording= True
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()