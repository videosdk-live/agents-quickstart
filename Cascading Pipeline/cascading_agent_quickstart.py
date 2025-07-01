import asyncio
import aiohttp
import os
from pathlib import Path
import sys
from typing import AsyncIterator

from videosdk.agents import Agent, AgentSession, CascadingPipeline, function_tool, MCPServerStdio, MCPServerHTTP, JobContext, RoomOptions, WorkerJob, ConversationFlow, ChatRole
from videosdk.plugins.openai import OpenAILLM, OpenAISTT, OpenAITTS
from videosdk.plugins.google import GoogleTTS, GoogleLLM, GoogleSTT
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from videosdk.plugins.sarvamai import SarvamAITTS, SarvamAILLM, SarvamAISTT
from videosdk.plugins.cartesia import CartesiaTTS, CartesiaSTT
from videosdk.plugins.smallestai import SmallestAITTS
from videosdk.plugins.resemble import ResembleTTS

# Pre-downloading the Turn Detector model
pre_download_model()

@function_tool
async def get_weather(
    latitude: str,
    longitude: str,
):
        """Called when the user asks about the weather. This function will return the weather for
        the given location. When given a location, please estimate the latitude and longitude of the
        location and do not ask the user for them.

        Args:
            latitude: The latitude of the location
            longitude: The longitude of the location
        """
        print("###Getting weather for", latitude, longitude)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"
        weather_data = {}
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    print("###Weather data", data)
                    weather_data = {
                        "temperature": data["current"]["temperature_2m"],
                        "temperature_unit": "Celsius",
                    }
                else:
                    raise Exception(
                        f"Failed to get weather data, status code: {response.status}"
                    )

        return weather_data


class MyVoiceAgent(Agent):
    def __init__(self):
        mcp_script = Path(__file__).parent.parent / "MCP Server" / "mcp_stdio_example.py"
        super().__init__(
            instructions="You are VideoSDK's Voice Agent. You are a helpful voice assistant that can answer questions about weather, horoscopes and help with other tasks.",
            tools=[get_weather],
            mcp_servers=[
                MCPServerStdio(
                    command=sys.executable,
                    args=[str(mcp_script)],
                    client_session_timeout_seconds=30
                ),
                MCPServerHTTP(
                    url="https://mcp.zapier.com/api/mcp/s/your-server-id",
                    client_session_timeout_seconds=30
                )
            ]
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
    
    @function_tool
    async def end_call(self) -> None:
        """End the call upon request by the user"""
        await self.session.say("Goodbye!")
        await asyncio.sleep(1)
        await self.session.leave()
        

class MyConversationFlow(ConversationFlow):
    def __init__(self, agent: Agent):
        super().__init__(agent)

    async def run(self, transcript: str) -> AsyncIterator[str]:
        """Main conversation loop: handle a user turn."""
        await self.on_turn_start(transcript)
        processed_transcript = transcript.lower().strip()
        self.agent.chat_context.add_message(
            role=ChatRole.USER, content=processed_transcript
        )
        async for response_chunk in self.process_with_llm():
            yield response_chunk
        await self.on_turn_end()

    async def on_turn_start(self, transcript: str) -> None:
        """Called at the start of a user turn."""
        self.is_turn_active = True
        print(f"User transcript: {transcript}")

    async def on_turn_end(self) -> None:
        """Called at the end of a user turn."""
        self.is_turn_active = False
        print("Agent turn ended.")


async def start_session(context: JobContext):
    # This example uses Google's services by default.
    # You can switch to other providers by commenting and uncommenting the relevant lines.
    # Make sure you have the necessary API keys set as environment variables.

    # STT Providers
    stt = GoogleSTT(model="latest_long")
    # stt = OpenAISTT(api_key=os.getenv("OPENAI_API_KEY"))
    # stt = DeepgramSTT(api_key=os.getenv("DEEPGRAM_API_KEY"))
    # stt = CartesiaSTT(api_key=os.getenv("CARTESIA_API_KEY"))
    # stt = SarvamAISTT(api_key=os.getenv("SARVAMAI_API_KEY"))

    # LLM Providers
    llm = GoogleLLM(api_key=os.getenv("GOOGLE_API_KEY"))
    # llm = OpenAILLM(api_key=os.getenv("OPENAI_API_KEY"))
    # llm = SarvamAILLM(api_key=os.getenv("SARVAMAI_API_KEY"))

    # TTS Providers
    tts = GoogleTTS(api_key=os.getenv("GOOGLE_API_KEY"))
    # tts = OpenAITTS(api_key=os.getenv("OPENAI_API_KEY"))
    # tts = ElevenLabsTTS(api_key=os.getenv("ELEVENLABS_API_KEY"))
    # tts = CartesiaTTS(api_key=os.getenv("CARTESIA_API_KEY"))
    # tts = SmallestAITTS(api_key=os.getenv("SMALLESTAI_API_KEY"))
    # tts = ResembleTTS(api_key=os.getenv("RESEMBLE_API_KEY"))
    # tts = SarvamAITTS(api_key=os.getenv("SARVAMAI_API_KEY"))
    
    vad = SileroVAD()
    turn_detector = TurnDetector(threshold=0.8)

    agent = MyVoiceAgent()
    conversation_flow = MyConversationFlow(agent)

    pipeline = CascadingPipeline(
        stt=stt, 
        llm=llm, 
        tts=tts, 
        vad=vad, 
        turn_detector=turn_detector
    )

    session = AgentSession(
        agent=agent,
        pipeline=pipeline,
        conversation_flow=conversation_flow
    )

    try:
        await context.connect()
        await session.start()
        await asyncio.Event().wait()
    finally:
        await session.close()
        await context.shutdown()

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="YOUR_MEETING_ID", # Replace it with your actual meetingID
        # auth_token = "<VIDEOSDK_AUTH_TOKEN>", # When VIDEOSDK_AUTH_TOKEN is set in .env - DON'T include videosdk_auth
        name="Cascading Agent",
        playground=True,
    )

    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start() 