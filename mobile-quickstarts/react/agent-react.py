import asyncio
import logging
from videosdk.agents import Agent, AgentSession, RealTimePipeline, function_tool, WorkerJob, JobContext, RoomOptions
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig

logging.getLogger().setLevel(logging.CRITICAL)
class RealtimeAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""You are a high-energy game-show host guiding the caller to guess a secret number from 1 to 100 to win 1,000,000$.""",
        )

    async def on_enter(self) -> None:
        await self.session.say("Welcome to the Videosdk's AI Agent game show! I'm your host, and we're about to play for 1,000,000$. Are you ready to play?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")

async def entrypoint(ctx: JobContext):

# Initialize Model
    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        config=GeminiLiveConfig(
            voice="Leda",
            response_modalities=["AUDIO"],
        )
    )

    pipeline = RealTimePipeline(model=model)
    
    agent = RealtimeAgent()
    
    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
    )

    try:
        await ctx.connect()
        print("Waiting for participant...")
        await ctx.room.wait_for_participant()
        print("Participant joined")
        await session.start()
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await session.close()
        await ctx.shutdown()

def make_context() -> JobContext:
    # Static meeting ID - same as used in frontend
    room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True) 
    return JobContext(
        room_options=room_options
        )


if __name__ == "__main__":

    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()