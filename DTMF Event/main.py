import asyncio
import aiohttp
from dotenv import load_dotenv
from videosdk.agents import (Agent, AgentSession, CascadingPipeline, WorkerJob, ConversationFlow, JobContext, RoomOptions, Options)
from videosdk import PubSubSubscribeConfig
from videosdk.plugins.google import GoogleLLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.sarvamai import SarvamAITTS
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model

load_dotenv()
pre_download_model()


class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice assistant.")

    async def on_enter(self):
        await self.session.say(
            "Hello! Press 1 for loan recovery. Press 2 for train loan assistance."
        )

    async def on_exit(self):
        await self.session.say("Goodbye!")


def on_pubsub_message(message):
    """
    message example:
    {
        "digit": "1"
    }

    We extend this to include agent_obj so the callback
    can modify the agent's chat_context.
    """
    print("PubSub DTMF message received:", message)

    agent = message.get("agent_obj")
    if agent is None:
        print("Agent object missing in PubSub message.")
        return

    digit = str(message.get("payload", {}).get("number"))

    if digit == "1":
        agent.chat_context.add_message(
            role="system",
            content=(
                "User pressed 1. You are now a Loan Recovery Agent. "
                "Assist the user with overdue loan details, EMI payments, "
                "outstanding balance, and repayment options."
            ),
        )
        asyncio.create_task(
            agent.session.say(
                "You selected loan recovery. How may I assist you?"
            )
        )
    elif digit == "2":
        agent.chat_context.add_message(
            role="system",
            content=(
                'User pressed 2. You are now a "Train Loan Assistant." '
                "Help the user with travel loan information, application "
                "process, required documents, and eligibility criteria."
            ),
        )
        asyncio.create_task(
            agent.session.say(
                "You selected train loan assistance. How may I help?"
            )
        )
    else:
        print("Unknown DTMF input:", digit)


async def entrypoint(ctx: JobContext):
    agent = VoiceAgent()
    conversation_flow = ConversationFlow(agent)

    pipeline = CascadingPipeline(
        stt=DeepgramSTT(),
        llm=GoogleLLM(),
        tts=SarvamAITTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector(),
    )

    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
        conversation_flow=conversation_flow,
    )

    def pubsub_callback_wrapper(msg):
        msg["agent_obj"] = agent
        on_pubsub_message(msg)

    try:
        await ctx.connect()

        subscribe_config = PubSubSubscribeConfig(
            topic="DTMF_EVENT",
            cb=pubsub_callback_wrapper,
        )
        await ctx.room.subscribe_to_pubsub(subscribe_config)

        await session.start()

        # Keep session alive
        await asyncio.Event().wait()

    finally:
        await session.close()
        await ctx.run_until_shutdown()


def make_context() -> JobContext:
    room_options = RoomOptions(
        name="DTMF Agent",
        auto_end_session=True,
        session_timeout_seconds=5,
    )
    return JobContext(room_options=room_options)


options = Options(
    agent_id="dtmf_agent",
    max_processes=5,
    register=True,
    log_level="INFO",
    host="localhost",
    port=8071,
)

if __name__ == "__main__":
    job = WorkerJob(
        entrypoint=entrypoint,
        jobctx=make_context,
        options=options,
    )
    job.start()