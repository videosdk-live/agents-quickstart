import aiohttp
from videosdk.agents import Agent, AgentSession, RealTimePipeline, function_tool, JobContext, RoomOptions, WorkerJob
from videosdk.plugins.openai import OpenAIRealtime, OpenAIRealtimeConfig
from openai.types.beta.realtime.session import InputAudioTranscription, TurnDetection

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
        super().__init__(
            instructions="You Are VideoSDK's Voice Agent.You are a helpful voice assistant that can answer questions and help with tasks.",
            tools=[get_weather])

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

async def start_session(context: JobContext):
    model = OpenAIRealtime(
        model="gpt-realtime-2025-08-28",
        # When OPENAI_API_KEY is set in .env - DON'T pass api_key parameter
        # api_key="sk-proj-XXXXXXXXXXXXXXXXXXXX",
        config=OpenAIRealtimeConfig(
            voice="alloy", # alloy, ash, ballad, coral, echo, fable, onyx, nova, sage, shimmer, and verse
            modalities=["text", "audio"],
            input_audio_transcription=InputAudioTranscription(model="whisper-1"),
            turn_detection=TurnDetection(
                type="server_vad",
                threshold=0.5,
                prefix_padding_ms=300,
                silence_duration_ms=200,
            ),
            tool_choice="auto",
        )
    )
    pipeline = RealTimePipeline(model=model)
    session = AgentSession(
        agent=MyVoiceAgent(),
        pipeline=pipeline
    )

    await context.run_until_shutdown(session=session,wait_for_participant=True)

def make_context() -> JobContext:
    room_options = RoomOptions(
        room_id="<room_id>", # Replace it with your actual room_id
        # auth_token = "<VIDEOSDK_AUTH_TOKEN>", # When VIDEOSDK_AUTH_TOKEN is set in .env - DON'T include videosdk_auth
        name="OpenAI Agent", 
        playground=True,
    )
    
    return JobContext(room_options=room_options)

if __name__ == "__main__":
    job = WorkerJob(entrypoint=start_session, jobctx=make_context)
    job.start()
