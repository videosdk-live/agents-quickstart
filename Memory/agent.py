import asyncio
import os
from typing import List, Optional
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import NamoTurnDetectorV1
from memory_utils import Mem0MemoryManager, build_agent_instructions


class ConciergeVoiceAgent(Agent):
    def __init__(self, instructions: str, remembered_facts: Optional[List[str]] = None):
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

    # Build agent with pre-loaded memories as instructions context
    instructions, remembered_facts = await build_agent_instructions(memory_manager)
    agent = ConciergeVoiceAgent(instructions=instructions, remembered_facts=remembered_facts)

    pipeline = Pipeline(
        stt=DeepgramSTT(model="nova-2", language="en"),
        llm=OpenAILLM(model="gpt-4o"),
        tts=ElevenLabsTTS(model="eleven_flash_v2_5"),
        vad=SileroVAD(threshold=0.35),
        turn_detector=NamoTurnDetectorV1(),
    )

    pending_user_message = None

    # Pipeline hook: search and inject relevant memories at the start of each user turn
    @pipeline.on("user_turn_start")
    async def on_user_turn_start(transcript: str):
        nonlocal pending_user_message
        pending_user_message = transcript
        if not memory_manager:
            return
        relevant = await memory_manager.search(transcript)
        if relevant:
            context_str = "\n".join(f"- {m}" for m in relevant)
            agent.chat_context.add_message(
                role="system",
                content=f"Relevant memories about this caller:\n{context_str}\n\nUse these to personalize your response."
            )

    # Pipeline hook: store memory-worthy exchanges after the LLM responds
    @pipeline.on("llm")
    async def on_llm(data: dict):
        nonlocal pending_user_message
        if not memory_manager or not pending_user_message:
            pending_user_message = None
            return
        user_text = pending_user_message
        pending_user_message = None
        if memory_manager.should_store(user_text):
            await memory_manager.record_memory(user_text, data.get("text", "") or None)

    session = AgentSession(agent=agent, pipeline=pipeline)

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
