import os
from pathlib import Path
from typing import AsyncIterator

from videosdk.agents import Agent, AgentSession, CascadingPipeline,JobContext, RoomOptions, WorkerJob, ConversationFlow
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model

# Pre-downloading the Turn Detector model
pre_download_model()
class MyVoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are VideoSDK's Voice Agent. You are a helpful voice assistant that can answer questions about weather, horoscopes and help with other tasks.")

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")
        

async def start_session(context: JobContext):
    
    agent = MyVoiceAgent()
    conversation_flow = ConversationFlow(agent)

    pipeline = CascadingPipeline(
        stt= DeepgramSTT(),
        llm=OpenAILLM(),
        tts=ElevenLabsTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector()
    )
    session = AgentSession(
        agent=agent, 
        pipeline=pipeline,
        conversation_flow=conversation_flow
    )

    await context.run_until_shutdown(session=session,wait_for_participant=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="<room_id>", # Replace it with your actual room_id
        name="Recording Example Agent",
        playground=True,
        recording=True
    )

    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 