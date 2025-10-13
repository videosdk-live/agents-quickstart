from videosdk.agents import Agent, AgentSession, RealTimePipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.aws import NovaSonicRealtime, NovaSonicConfig

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You Are VideoSDK's Voice Agent. You are a helpful voice assistant that can answer questions and help with tasks.")

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")

async def start_session(context: JobContext):
    model = NovaSonicRealtime(
        model="amazon.nova-sonic-v1:0",
        # When AWS credentials and region are set in .env - DON'T pass credential parameters
        region="us-east-1",  
        aws_access_key_id="UKXXXXXXXXXXXXXXXXXXXX", 
        aws_secret_access_key="AECXXXXXXXXXXXXXXXXXXXX", 
        config=NovaSonicConfig(
            voice="tiffany", #  "tiffany","matthew", "amy"
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024
        )
    )

    agent = MyVoiceAgent()
    pipeline = RealTimePipeline(model=model)
    session = AgentSession(
        agent=agent,
        pipeline=pipeline
    )

    await context.run_until_shutdown(session=session,wait_for_participant=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="YOUR_MEETING_ID", # Replace it with your actual meetingID
        # auth_token = "<VIDEOSDK_AUTH_TOKEN>", # When VIDEOSDK_AUTH_TOKEN is set in .env - DON'T include videosdk_auth
        name="AWS Agent",
        playground=True,
    )

    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
