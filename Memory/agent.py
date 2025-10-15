import asyncio
import os
from typing import List, Optional
from videosdk.agents import Agent, AgentSession, CascadingPipeline, ConversationFlow, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import NamoTurnDetectorV1
from memory_utils import Mem0MemoryManager, Mem0ConversationFlow, build_agent_instructions

class ConciergeVoiceAgent(Agent):
    def __init__(self, instructions: str, memory_manager: Optional[Mem0MemoryManager] = None, remembered_facts: Optional[List[str]] = None):
        self.memory_manager = memory_manager
        self._remembered_facts = remembered_facts or []
        super().__init__(instructions=instructions)

    async def on_enter(self):
        if self._remembered_facts:
            top_fact = "; ".join(self._remembered_facts[:2])
            await self.session.say(f"Welcome back! I remember that {top_fact}. What can I help with today?")
        else:
            await self.session.say("Hello! How can I help today?")

    async def on_exit(self):
        await self.session.say("Goodbye!")

async def start_session(context: JobContext):
    # Setup memory manager
    mem0_api_key = os.getenv("MEM0_API_KEY")
    memory_manager = None
    if mem0_api_key:
        memory_manager = Mem0MemoryManager(
            api_key=mem0_api_key,
            user_id=os.getenv("MEM0_DEFAULT_USER_ID", "demo-voice-user")
        )

    # Build agent
    instructions, remembered_facts = await build_agent_instructions(memory_manager)
    agent = ConciergeVoiceAgent(instructions=instructions, memory_manager=memory_manager, remembered_facts=remembered_facts)

    # Setup conversation flow
    flow_class = Mem0ConversationFlow if memory_manager else ConversationFlow
    conversation_flow = flow_class(
        agent=agent,
        memory_manager=memory_manager,
        stt=DeepgramSTT(model="nova-2", language="en"),
        llm=OpenAILLM(model="gpt-4o"),
        tts=ElevenLabsTTS(model="eleven_flash_v2_5"),
        vad=SileroVAD(threshold=0.35),
        turn_detector=NamoTurnDetectorV1(),
    )

    # Setup pipeline and session
    pipeline = CascadingPipeline(
        stt=conversation_flow.stt,
        llm=conversation_flow.llm,
        tts=conversation_flow.tts,
        vad=conversation_flow.vad,
        turn_detector=conversation_flow.turn_detector,
    )
    
    session = AgentSession(agent=agent, pipeline=pipeline, conversation_flow=conversation_flow)

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait()
    finally:
        await session.close()
        if memory_manager:
            await memory_manager.close()
        await context.shutdown()

def make_context() -> JobContext:
    return JobContext(room_options=RoomOptions(name="VideoSDK Concierge Agent with Mem0", playground=True))

if __name__ == "__main__":
    WorkerJob(entrypoint=start_session, jobctx=make_context).start()