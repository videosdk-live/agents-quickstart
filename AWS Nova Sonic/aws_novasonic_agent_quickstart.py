import asyncio
import aiohttp
from videosdk.agents import Agent, AgentSession, RealTimePipeline, function_tool, MCPServerStdio, MCPServerHTTP, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.aws import NovaSonicRealtime, NovaSonicConfig
from pathlib import Path
import sys



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
        # logger.info(f"getting weather for {latitude}, {longitude}")
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
            instructions="You Are VideoSDK's Voice Agent. You are a helpful voice assistant that can answer questions and help with tasks.",
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
        
    # Static test function
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


    pipeline = RealTimePipeline(model=model)
    session = AgentSession(
        agent=MyVoiceAgent(),
        pipeline=pipeline
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
        name="AWS Agent",
        playground=True,
    )

    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
