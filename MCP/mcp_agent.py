from videosdk.agents import Agent, AgentSession, RealTimePipeline,MCPServerStdio, MCPServerHTTP, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
import sys
import logging

logging.basicConfig(level=logging.INFO)

class MyVoiceAgent(Agent):
    def __init__(self):
        mcp_script = "/mcp_stdio_server.py"
        super().__init__(
            instructions="You Are VideoSDK's Voice Agent.You are a helpful voice assistant that can answer questions and help with tasks.",
            mcp_servers=[
                MCPServerStdio(
                    executable_path=sys.executable,
                    process_arguments=[str(mcp_script)],
                    session_timeout=30
                ),
                # MCPServerHTTP(
                #     endpoint_url="YOUR_ZAPIER_ENDPOINT",
                #     session_timeout=30
                # )
            ]
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")

async def start_session(context: JobContext):
    agent = MyVoiceAgent()
    model = GeminiRealtime(
        model="gemini-2.0-flash-live-001",
        config=GeminiLiveConfig(
            voice="Leda",
            response_modalities=["AUDIO"]
        )
    )

    pipeline = RealTimePipeline(model=model)
    session = AgentSession(
        agent=agent,
        pipeline=pipeline
    )

    await context.run_until_shutdown(session=session,wait_for_participant=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="<room_id>", # Replace it with your actual room_id
        name="MCP Agent",
        playground=True,
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()