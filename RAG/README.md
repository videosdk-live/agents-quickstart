# RAG — Retrieval-Augmented Generation Voice Agent

This example demonstrates how to build a voice agent that answers questions using **Retrieval-Augmented Generation (RAG)**. Instead of relying solely on the LLM's training data, the agent retrieves relevant documents from a local vector store at the start of each user turn and injects them into the conversation context before the LLM generates a response.

## What is RAG?

Retrieval-Augmented Generation is a technique that enhances an LLM's responses by supplying it with relevant, up-to-date, or proprietary documents at query time. Rather than fine-tuning the model, you:

1. Embed your documents into a vector store
2. At query time, embed the user's question and find the most similar documents
3. Inject those documents into the LLM's context (system prompt or chat history)
4. Let the LLM answer using both its training knowledge and your retrieved documents

This approach keeps your knowledge base up-to-date without retraining, and works well for domain-specific Q&A over internal documents, product manuals, support knowledge bases, and more.

## How It Works in This Example

The RAG pipeline hook pattern uses `@pipeline.on("user_turn_start")` to retrieve documents and inject them into `agent.chat_context` before the LLM processes the user's message:

```python
@pipeline.on("user_turn_start")
async def on_user_turn_start(agent, transcript: str, **kwargs):
    # 1. Embed the user's question and query the vector store
    results = vector_store.query(transcript, n_results=3)

    # 2. Format the retrieved documents
    context = "\n\n".join(results["documents"][0])

    # 3. Inject them into the agent's chat context
    agent.chat_context.append({
        "role": "system",
        "content": f"Relevant context:\n{context}"
    })
```

## Components

| Component | Purpose |
| :-------- | :------ |
| **ChromaDB** | Local vector store — stores and queries document embeddings |
| **OpenAI Embeddings** (`text-embedding-ada-002`) | Converts text chunks into vector embeddings for similarity search |
| **Deepgram STT** | Converts user speech to text |
| **OpenAI LLM** | Generates responses grounded in retrieved documents |
| **ElevenLabs TTS** | Converts agent responses back to speech |

## How to Add Your Own Documents

Open `rag.py` and locate the document ingestion section. Add your documents as plain text strings or load them from files:

```python
# Add your documents here
documents = [
    "Your first document text...",
    "Your second document text...",
    # Load from file:
    open("my_knowledge_base.txt").read(),
]

# Ingest into ChromaDB
collection.add(
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]
)
```

Documents are chunked and embedded automatically. The vector store persists locally so you only need to ingest once unless your documents change.

## Required Environment Variables

```
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

## Running the Example

```bash
uv run python "RAG/rag.py"
```

The agent will start and print a playground link to your console. Ask it questions that relate to the documents you have ingested — it will retrieve the most relevant passages and use them to answer.

## File Structure

```
RAG/
├── rag.py       # Main agent with RAG pipeline hook
└── README.md    # This file
```
