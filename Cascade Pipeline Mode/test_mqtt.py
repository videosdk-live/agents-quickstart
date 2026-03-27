import asyncio
import logging
import ssl
import uuid

import paho.mqtt.client as mqtt

from videosdk.agents import (
    Agent,
    AgentSession,
    CascadingPipeline,
    ConversationFlow,
    JobContext,
    RoomOptions,
    WorkerJob,
    function_tool,
)
from videosdk.plugins.cartesia import CartesiaTTS
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.google import GoogleLLM
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
pre_download_model()


# MQTT payload -> transfer instruction mapping
MQTT_TO_TRANSFER = {
    "start_story": "Switch to story mode. Use transfer_to_story immediately.",
    "start_scifi": "Switch to sci-fi mode. Use transfer_to_scifi immediately.",
    "start_quiz": "Switch to quiz mode. Use transfer_to_quiz immediately.",
    "start_maths": "Switch to maths mode. Use transfer_to_maths immediately.",
}


class StoryAgent(Agent):
    def __init__(self, inherit_context: bool = False):
        super().__init__(
            instructions="""You are a storyteller for kids. You tell short, fun, and imaginative stories. Keep things magical and exciting. When asked to switch persona, use the transfer tools.""",
            inherit_context=inherit_context,
        )

    async def on_enter(self) -> None:
        await self.session.say("Hi! I'm the Story Agent. Are you ready for a fun tale?")

    async def on_exit(self) -> None:
        pass

    @function_tool()
    async def transfer_to_story(self) -> Agent:
        """Transfer to the Story Agent for fun tales."""
        return StoryAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_scifi(self) -> Agent:
        """Transfer to the Sci-Fi Agent for space adventures."""
        return ScifiAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_quiz(self) -> Agent:
        """Transfer to the Quiz Agent for trivia games."""
        return QuizAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_maths(self) -> Agent:
        """Transfer to the Maths Agent for number puzzles."""
        return MathsAgent(inherit_context=True)


class ScifiAgent(Agent):
    def __init__(self, inherit_context: bool = False):
        super().__init__(
            instructions="""You are a Sci-Fi explorer. You tell kids about space, aliens, and spaceships. Keep it fun and adventurous. When asked to switch persona, use the transfer tools.""",
            inherit_context=inherit_context,
        )

    async def on_enter(self) -> None:
        await self.session.say("Greetings, Earthling! I am the Sci-Fi Agent. Let's explore the galaxy!")

    async def on_exit(self) -> None:
        pass

    @function_tool()
    async def transfer_to_story(self) -> Agent:
        """Transfer to the Story Agent for fun tales."""
        return StoryAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_scifi(self) -> Agent:
        """Transfer to the Sci-Fi Agent for space adventures."""
        return ScifiAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_quiz(self) -> Agent:
        """Transfer to the Quiz Agent for trivia games."""
        return QuizAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_maths(self) -> Agent:
        """Transfer to the Maths Agent for number puzzles."""
        return MathsAgent(inherit_context=True)


class QuizAgent(Agent):
    def __init__(self, inherit_context: bool = False):
        super().__init__(
            instructions="""You are a Quiz Master for kids. Ask fun trivia questions about animals and the world. Keep it encouraging! When asked to switch persona, use the transfer tools.""",
            inherit_context=inherit_context,
        )

    async def on_enter(self) -> None:
        await self.session.say("Hello! I'm the Quiz Agent. Are you ready to play a game?")

    async def on_exit(self) -> None:
        pass

    @function_tool()
    async def transfer_to_story(self) -> Agent:
        """Transfer to the Story Agent for fun tales."""
        return StoryAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_scifi(self) -> Agent:
        """Transfer to the Sci-Fi Agent for space adventures."""
        return ScifiAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_quiz(self) -> Agent:
        """Transfer to the Quiz Agent for trivia games."""
        return QuizAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_maths(self) -> Agent:
        """Transfer to the Maths Agent for number puzzles."""
        return MathsAgent(inherit_context=True)


class MathsAgent(Agent):
    def __init__(self, inherit_context: bool = False):
        super().__init__(
            instructions="""You are a Math Teacher for kids. Ask simple addition or subtraction questions. Be very patient and encouraging. When asked to switch persona, use the transfer tools.""",
            inherit_context=inherit_context,
        )

    async def on_enter(self) -> None:
        await self.session.say("Hi there! I'm the Maths Agent. Let's solve some number puzzles together!")

    async def on_exit(self) -> None:
        pass

    @function_tool()
    async def transfer_to_story(self) -> Agent:
        """Transfer to the Story Agent for fun tales."""
        return StoryAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_scifi(self) -> Agent:
        """Transfer to the Sci-Fi Agent for space adventures."""
        return ScifiAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_quiz(self) -> Agent:
        """Transfer to the Quiz Agent for trivia games."""
        return QuizAgent(inherit_context=True)

    @function_tool()
    async def transfer_to_maths(self) -> Agent:
        """Transfer to the Maths Agent for number puzzles."""
        return MathsAgent(inherit_context=True)


def setup_mqtt(session: AgentSession, loop: asyncio.AbstractEventLoop):
    state = {"timer": None, "instruction": None, "payload": None}

    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            logging.info("Connected to HiveMQ broker successfully.")
            client.subscribe("persona/button")
        else:
            logging.error(f"Failed to connect to HiveMQ, return code {reason_code}")

    def on_message(client, userdata, msg):
        payload = msg.payload.decode().lower().strip()
        logging.info(f"Received MQTT message on topic {msg.topic}: {payload}")

        if payload not in MQTT_TO_TRANSFER:
            logging.warning(f"Unknown persona '{payload}', ignoring.")
            return

        instruction = MQTT_TO_TRANSFER[payload]

        def schedule():
            if state["timer"]:
                state["timer"].cancel()
            state["instruction"] = instruction
            state["payload"] = payload

            async def do_transfer_async():
                inst = state["instruction"]
                if inst:
                    logging.info(f"Switching persona to {state['payload'].replace('start_', '').capitalize()} via session.reply()")
                    session.interrupt(force=True)
                    await asyncio.sleep(0.2)  
                    await session.reply(instructions=inst, wait_for_playback=False)
                state["timer"] = None
                state["instruction"] = None
                state["payload"] = None

            def do_transfer():
                asyncio.run_coroutine_threadsafe(do_transfer_async(), loop)

            state["timer"] = loop.call_later(0.4, do_transfer)

        loop.call_soon_threadsafe(schedule)

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"videosdk_agent_{uuid.uuid4().hex[:8]}",
    )
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("karan", "Karan0708")
    client.tls_set(tls_version=ssl.PROTOCOL_TLS)
    client.connect("d25e623a5d2c4f45a8ecdae5632cd8c6.s1.eu.hivemq.cloud", 8883, 60)
    client.loop_start()
    return client


async def entrypoint(ctx: JobContext):
    agent = StoryAgent()
    conversation_flow = ConversationFlow(agent)

    pipeline = CascadingPipeline(
        stt=DeepgramSTT(),
        llm=GoogleLLM(),
        tts=CartesiaTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector(),
    )
    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
        conversation_flow=conversation_flow,
    )

    loop = asyncio.get_running_loop()
    mqtt_client = setup_mqtt(session, loop)

    try:
        await session.start(wait_for_participant=True, run_until_shutdown=True)
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="jx2y-f8sk-x358",
        name="Kid Persona Agent",
        playground=True,
        auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlrZXkiOiI1MzE0YzVkZC0wN2MzLTRjZTgtYThmYi03ZmY0ZDZiMDdhYTIiLCJwZXJtaXNzaW9ucyI6WyJhbGxvd19qb2luIl0sImlhdCI6MTc1MTI2MTQ4MCwiZXhwIjoxNzgyNzk3NDgwfQ.yMH2talasjiL7ftJt2hl9h6_L96G1YU_tjujycAEi9M"
    )
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
