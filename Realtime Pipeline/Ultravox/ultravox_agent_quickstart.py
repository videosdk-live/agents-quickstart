from videosdk.agents import Agent, AgentSession, RealTimePipeline,JobContext, RoomOptions, WorkerJob
from videosdk.plugins.ultravox import UltravoxRealtime, UltravoxLiveConfig
import logging
logging.getLogger().setLevel(logging.INFO)

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You Are VideoSDK's Voice Agent.You are a helpful voice assistant that can answer questions and help with tasks.",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")

async def start_session(context: JobContext):
    agent = MyVoiceAgent()
    model = UltravoxRealtime(
        model="fixie-ai/ultravox",
        # When ULTRAVOX_API_KEY is set in .env - DON'T pass api_key parameter
        # api_key="uvx-proj-1234567890", 
        config=UltravoxLiveConfig(
            voice="54ebeae1-88df-4d66-af13-6c41283b4332",
            language_hint="en",
            temperature=0.7,
            vad_turn_endpoint_delay=800,
            vad_minimum_turn_duration=600,
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
        name="Ultravox Agent",
        playground=True,
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()