from videosdk.agents import AgentSession, Pipeline
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.google import GeminiRealtime, GeminiLiveConfig
import os


def create_pipeline(agent_type: str):
    if agent_type == "customer":
        # Realtime Pipeline Mode for voice-enabled customer-facing agent
        return Pipeline(
            llm=GeminiRealtime(
                model="gemini-3.1-flash-live-preview",
                config=GeminiLiveConfig(
                    voice="Leda",
                    response_modalities=["AUDIO"]
                )
            )
        )
    else:
        # Cascade Pipeline Mode (text-only LLM) for background specialist agent
        return Pipeline(
            llm=OpenAILLM(api_key=os.getenv("OPENAI_API_KEY")),
        )


def create_session(agent, pipeline) -> AgentSession:
    return AgentSession(
        agent=agent,
        pipeline=pipeline,
    )


### Alternative: Cascade Pipeline for both agents

# from videosdk.agents import AgentSession, Pipeline
# from videosdk.plugins.google import GoogleSTT, GoogleLLM, GoogleTTS
# from videosdk.plugins.openai import OpenAILLM
# from videosdk.plugins.silero import SileroVAD
# from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
# import os

# pre_download_model()

# def create_pipeline(agent_type: str):
#     if agent_type == "customer":
#         return Pipeline(
#             stt=GoogleSTT(model="latest_long"),
#             llm=GoogleLLM(api_key=os.getenv("GOOGLE_API_KEY")),
#             tts=GoogleTTS(api_key=os.getenv("GOOGLE_API_KEY")),
#             vad=SileroVAD(),
#             turn_detector=TurnDetector(),
#         )
#     else:
#         return Pipeline(
#             llm=OpenAILLM(api_key=os.getenv("OPENAI_API_KEY")),
#         )

# def create_session(agent, pipeline) -> AgentSession:
#     return AgentSession(agent=agent, pipeline=pipeline)
