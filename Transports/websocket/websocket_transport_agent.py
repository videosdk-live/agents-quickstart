import logging
from videosdk.agents import Agent, AgentSession, CascadingPipeline, function_tool, WorkerJob,ConversationFlow, JobContext, RoomOptions,WebSocketConfig
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.cartesia import CartesiaTTS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", handlers=[logging.StreamHandler()])
pre_download_model()

class WebSocketTransportAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant that can answer questions and help with tasks and help with horoscopes.",
        )
    
    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")
    
    @function_tool
    async def get_horoscope(self, sign: str) -> dict:
        """Get today's horoscope for a given zodiac sign.

        Args:
            sign: The zodiac sign (e.g., Aries, Taurus, Gemini, etc.)
        """
        horoscopes = {
            "Aries": "Today is your lucky day!",
            "Taurus": "Focus on your goals today.",
            "Gemini": "Communication will be important today.",
        }
        return {
            "sign": sign,
            "horoscope": horoscopes.get(sign, "The stars are aligned for you today!"),
        }

async def entrypoint(ctx: JobContext):
    
    agent = WebSocketTransportAgent()
    conversation_flow = ConversationFlow(agent)

    pipeline = CascadingPipeline(
        stt=DeepgramSTT(),
        llm=OpenAILLM(),
        tts=CartesiaTTS(),
        vad=SileroVAD(), 
        turn_detector=TurnDetector()
    )
    session = AgentSession(
        agent=agent, 
        pipeline=pipeline,
        conversation_flow=conversation_flow
    )

    await session.start(wait_for_participant=True, run_until_shutdown=True)

def make_context() -> JobContext:

    # --- WebSocket Transport (Raw PCM) ---
    # Used with Transports/websocket/websocket_transport.html
    # 1. Open websocket_transport.html in your browser
    # 2. Run this Python script
    # 3. Click "Connect" in the browser
    room_options = RoomOptions(
       transport_mode="websocket",
       websocket=WebSocketConfig(
           port=8080,
           path="/ws"
       )
    )
    
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    WorkerJob(entrypoint=entrypoint, jobctx=make_context).start()