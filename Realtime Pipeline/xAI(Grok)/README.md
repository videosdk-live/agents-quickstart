# 🚀 xAI (Grok) Agent for VideoSDK

This directory contains example code for integrating an xAI Grok-powered voice agent into VideoSDK meetings.

## 🛠️ Installation

Install the xAI-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-xai"
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder API key in `xai_agent_quickstart.py` with your actual xAI API key
   ```python
   model = XAIRealtime(
       model="grok-4-1-fast-non-reasoning",
       api_key="your-xai-api-key",  # Or use environment variable XAI_API_KEY
       config=XAIRealtimeConfig(
           voice="Eve",
           # collection_id="your-collection-id",  # Optional: See Collection Storage section below
           # ... other config options
       )
   )
   ```

   **Optional**: To use collections for additional context, create a collection in the [xAI Console](https://console.x.ai) storage section and pass the collection ID in the config. See the [Collection Storage](#-collection-storage) section below for detailed instructions.

2. Set your VideoSDK credentials in the `make_context` function:
   ```python
   from videosdk.agents import JobContext, RoomOptions

   def make_context() -> JobContext:
       room_options = RoomOptions(
           room_id="your-meeting-id",                 # VideoSDK meeting ID
           auth_token="your-videosdk-auth-token",     # Or use environment variable VIDEOSDK_AUTH_TOKEN
           name="xAI(Grok) Agent",
           playground=True,
       )
       return JobContext(room_options=room_options)
   ```

   You can also use environment variables for `VIDEOSDK_MEETING_ID` and `VIDEOSDK_AUTH_TOKEN`.

## Running the Example

To run the xAI Grok-powered agent:

```bash
python xai_agent_quickstart.py
```

When running in playground mode (`playground=True` in `RoomOptions`), a direct link will be printed to your console. You can open this link in your browser to interact with the agent.

```
Agent started in playground mode
Interact with agent here at:
https://playground.videosdk.live?token=...&meetingId=...
```

## ✨ Key Features

- **Multi-modal Interactions**: Utilize xAI's powerful Grok models
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination
- **Web Search**: Enable real-time web search capabilities with `enable_web_search=True`
- **X Search**: Access X (Twitter) content with `enable_x_search=True` and `allowed_x_handles`


## 🧠 xAI Grok Configuration

The agent uses xAI's Grok models for real-time AI interactions. Configuration options include:

- `model`: The Grok model to use (e.g., `"grok-4-1-fast-non-reasoning"`)
- `api_key`: Your xAI API key (can also be set via environment variable `XAI_API_KEY`)
- `config`: Advanced configuration options including:
  - `voice`: Voice selection (e.g., `"Eve"`, `"Ara"`, `"Rex"`, `"Sal"`, `"Leo"`)
  - `enable_web_search`: Enable web search capabilities
  - `enable_x_search`: Enable X (Twitter) search capabilities
  - `allowed_x_handles`: List of allowed X handles for search
  - `collection_id`: Custom collection ID for context
  - `turn_detection`: Turn detection configuration with VAD settings

For complete configuration options, see the [official VideoSDK xAI (Grok) plugin documentation](https://docs.videosdk.live/ai_agents/plugins/xai).

## 📚 Collection Storage

xAI Grok supports using collections to provide additional context to your agent. To use collections:

1. **Navigate to xAI Console**: Go to [console.x.ai](https://console.x.ai) dashboard
2. **Access Storage Section**: Click on the **Storage** section in the dashboard
3. **Create New Collection**: Click on **"Create New Collection"** button
4. **Upload Files**: Upload your relevant files (documents, data files, etc.) to the collection
5. **Get Collection ID**: Once created, copy the collection ID from the dashboard
6. **Use in Config**: Pass the collection ID in your agent configuration:

```python
model = XAIRealtime(
    model="grok-4-1-fast-non-reasoning",
    api_key="your-xai-api-key",
    config=XAIRealtimeConfig(
        voice="Eve",
        collection_id="your-collection-id",  # Use the collection ID from console.x.ai
        # ... other config options
    )
)
```

The collection will provide additional context to your agent, allowing it to access and reference the uploaded files during conversations.

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team