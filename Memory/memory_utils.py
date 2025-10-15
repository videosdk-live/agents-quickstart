import os
from typing import List, Optional
from mem0.client.main import AsyncMemoryClient
from videosdk.agents import Agent, ConversationFlow

class Mem0MemoryManager:
    def __init__(self, api_key: str, user_id: str, agent_id: str = "voice_concierge"):
        self.user_id = user_id
        self.agent_id = agent_id
        self._client = AsyncMemoryClient(api_key=api_key)

    async def fetch_recent_memories(self, limit: int = 5) -> List[str]:
        try:
            response = await self._client.get_all(
                version="v2", filters={"user_id": self.user_id}, page_size=limit, page=1
            )
            results = response.get("results", []) if isinstance(response, dict) else response
            return [entry.get("memory") or entry.get("text", "") for entry in results if isinstance(entry, dict)][:limit]
        except:
            return []

    def should_store(self, user_message: str) -> bool:
        keywords = ("remember", "preference", "favorite", "likes", "dislike", "call me", "my name", "birthday")
        return any(keyword in user_message.lower() for keyword in keywords)

    async def record_memory(self, user_message: str, assistant_message: Optional[str] = None):
        messages = [{"role": "user", "content": user_message}]
        if assistant_message:
            messages.append({"role": "assistant", "content": assistant_message})
        try:
            await self._client.add(messages, user_id=self.user_id, metadata={"source": "voice-agent"})
        except:
            pass

    async def close(self):
        await self._client.async_client.aclose()

class Mem0ConversationFlow(ConversationFlow):
    def __init__(self, agent: Agent, memory_manager: Mem0MemoryManager, **kwargs):
        super().__init__(agent=agent, **kwargs)
        self._memory_manager = memory_manager
        self._pending_user_message: Optional[str] = None

    async def on_turn_start(self, transcript: str):
        self._pending_user_message = transcript

    async def run(self, transcript: str):
        collected_chunks = []
        async for chunk in super().run(transcript):
            collected_chunks.append(chunk)
            yield chunk
        
        full_response = "".join(collected_chunks).strip()
        user_text = transcript or self._pending_user_message
        if user_text and self._memory_manager.should_store(user_text):
            await self._memory_manager.record_memory(user_text, full_response or None)
        self._pending_user_message = None

async def build_agent_instructions(memory_manager: Optional[Mem0MemoryManager]) -> tuple[str, List[str]]:
    base_instructions = "You are a helpful voice concierge that remembers returning callers. Use any known preferences to personalize your responses, but keep the conversation natural."
    
    if not memory_manager:
        return base_instructions, []
    
    remembered = await memory_manager.fetch_recent_memories(limit=int(os.getenv("MEM0_MEMORY_LIMIT", "5")))
    if not remembered:
        return base_instructions, []
    
    memory_lines = "\n".join(f"- {fact}" for fact in remembered)
    enriched_instructions = f"{base_instructions}\n\nKnown details about this caller:\n{memory_lines}\n\nGreet them warmly, weave these facts in when useful, and avoid repeating questions you already know."
    return enriched_instructions, remembered