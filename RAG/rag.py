import asyncio
from videosdk.agents import Agent, AgentSession, Pipeline, WorkerJob, JobContext, RoomOptions
from videosdk.plugins.openai import OpenAILLM
from videosdk.plugins.deepgram import DeepgramSTT
from videosdk.plugins.silero import SileroVAD
from videosdk.plugins.turn_detector import TurnDetector, pre_download_model
from videosdk.plugins.elevenlabs import ElevenLabsTTS
from openai import AsyncOpenAI
import chromadb
import numpy as np
import os

pre_download_model()


class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="You are a helpful voice assistant that answers questions based on provided context. Use the retrieved documents to ground your answers. If no relevant context is found, say so."
        )
        # Initialize OpenAI client for embeddings
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # FAQ documents from VideoSDK Integration FAQ
        self.documents = [
            "What is VideoSDK? VideoSDK is a comprehensive video calling and live streaming platform supporting Web (JavaScript), Mobile (React Native, Flutter, Android, iOS), and Server-side REST APIs.",
            "How do I authenticate with VideoSDK? Use JWT tokens generated with your API key and secret from the VideoSDK dashboard, including permissions and expiration time.",
            "How do I create a video meeting room? Call the VideoSDK REST API or use VideoSDK.createMeeting() to generate a meeting ID for participants to join.",
            "How do I implement screen sharing in VideoSDK? Use enableScreenShare() to start and disableScreenShare() to stop, listening to screen-share-started and screen-share-stopped events.",
            "How do I record video meetings? Start recording with startRecording(), configure mode (video-and-audio or audio-only) and quality, and stop with stopRecording().",
            "Can I live stream VideoSDK meetings to social media? Yes, use startLivestream() with RTMP URLs for platforms like YouTube or Facebook, supporting multiple platforms simultaneously."
        ]
        """
        List[str]: The ultimate guidebook for our VideoSDK integration guru! This collection of FAQ entries powers the RAG pipeline, embedding VideoSDK's integration secrets into vectors via OpenAI's `text-embedding-ada-002` and storing them in Chroma DB's digital vault. From creating meetings to live streaming, these nuggets of wisdom enable the assistant to deliver precise answers, transcribed by Deepgram's audio wizardry and voiced through ElevenLabs' sonic brilliance. Swap with your own VideoSDK FAQs or expand with custom docs to make this assistant the go-to expert for video integration queries!
        """

        # Set up Chroma DB
        self.chroma_client = chromadb.Client()  # In-memory client; use PersistentClient for disk storage
        self.collection = self.chroma_client.create_collection(name="videosdk_faq_collection")

        # Generate embeddings and add to Chroma
        embeddings = [self._get_embedding_sync(doc) for doc in self.documents]
        self.collection.add(
            documents=self.documents,
            embeddings=embeddings,
            ids=[f"doc_{i}" for i in range(len(self.documents))]
        )

    def _get_embedding_sync(self, text: str) -> np.ndarray:
        """Synchronous embedding for initialization (since __init__ can't be async)."""
        import openai  # Use sync client for init
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding

    async def get_embedding(self, text: str) -> np.ndarray:
        """Async embedding for queries."""
        response = await self.openai_client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding

    async def retrieve(self, query: str, k: int = 2) -> list[str]:
        """Retrieve top-k documents from Chroma DB."""
        query_emb = await self.get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=k
        )
        return results["documents"][0]  # List of matching documents

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")

    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")


async def entrypoint(ctx: JobContext):
    agent = VoiceAgent()

    pipeline = Pipeline(
        stt=DeepgramSTT(),
        llm=OpenAILLM(),
        tts=ElevenLabsTTS(),
        vad=SileroVAD(),
        turn_detector=TurnDetector()
    )

    # Pipeline hook: retrieve relevant documents at the start of each user turn
    # and inject them into the agent's context before the LLM responds
    @pipeline.on("user_turn_start")
    async def on_user_turn_start(transcript: str):
        context_docs = await agent.retrieve(transcript)
        if context_docs:
            context_str = "\n\n".join(f"Document {i + 1}: {doc}" for i, doc in enumerate(context_docs))
            agent.chat_context.add_message(
                role="system",
                content=f"Retrieved Context:\n{context_str}\n\nUse this context to answer the user's question."
            )

    session = AgentSession(agent=agent, pipeline=pipeline)

    await session.start(wait_for_participant=True, run_until_shutdown=True)


def make_context() -> JobContext:
    room_options = RoomOptions(name="Agent", playground=True)
    return JobContext(room_options=room_options)


if __name__ == "__main__":
    job = WorkerJob(entrypoint=entrypoint, jobctx=make_context)
    job.start()
