from videosdk.agents import Agent, AgentSession, RealTimePipeline,JobContext, RoomOptions, WorkerJob
from videosdk.plugins.xai import XAIRealtime, XAIRealtimeConfig,XAITurnDetection
import logging
logging.getLogger().setLevel(logging.INFO)

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You Are VideoSDK's Voice Agent.You are a helpful voice assistant that can answer questions and help with tasks.")

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")

async def start_session(context: JobContext):
    agent = MyVoiceAgent()

    model = XAIRealtime(
        model="grok-4-1-fast-non-reasoning",
        # When XAI_API_KEY is set in .env - DON'T pass api_key parameter
        # api_key="xi-proj-1234567890", 
        config=XAIRealtimeConfig(
            voice="Eve", # Ara,Rex,Sal,Eve,Leo.
            enable_web_search=True,
            # enable_x_search=True,
            # allowed_x_handles=["elonmusk"],
            # collection_id="your-collection-id",
            turn_detection=XAITurnDetection(
                type="server_vad",
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=200,
            ),
        )
    )

    pipeline = RealTimePipeline(model=model)
    session = AgentSession(
        agent=agent,
        pipeline=pipeline
    )

    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        # room_id="<room_id>", # Replace it with your actual room_id
        name="xAI(Grok) Agent",
        playground=True,
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()