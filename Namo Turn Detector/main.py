import os
from typing import AsyncIterator
from videosdk.agents import Agent, AgentSession, CascadingPipeline,JobContext, RoomOptions, WorkerJob, ConversationFlow
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import NamoTurnDetectorV1, pre_download_namo_turn_v1_model

# Pre-downloading the Namo Turn Detector model
pre_download_namo_turn_v1_model()

class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are VideoSDK's Voice Agent. You are a helpful voice assistant that can answer questions about weather.IMPORTANT: don't generate response above 2 lines",
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")
        

async def start_session(context: JobContext):

    agent = MyVoiceAgent()
    conversation_flow = ConversationFlow(agent)
    pipeline = CascadingPipeline(
        stt=DeepgramSTT(),
        llm=OpenAILLM(),
        tts=ElevenLabsTTS(),
        vad=SileroVAD(),
        turn_detector=NamoTurnDetectorV1()
    )

    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
        conversation_flow=conversation_flow
    )

    await context.run_until_shutdown(session=session,wait_for_participant=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="<room_id>",
        name="Namo Turn Detector Agent",
        auth_token=os.getenv("VIDEOSDK_AUTH_TOKEN"),
        playground=True,
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 