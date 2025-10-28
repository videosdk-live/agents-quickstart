# Background Audio for Agents

The VideoSDK AI Agent SDK allows you to play background audio to create more natural conversational experiences. You can configure automatic "thinking" sounds and play on-demand audio.

To enable this feature, set `background_audio=True` in `RoomOptions`.

The `Agent` class provides three main methods for controlling audio:
- `set_thinking_audio()`: Sets a default sound that plays automatically when the agent is processing.
- `play_background_audio()`: Plays an audio file on demand. Can be looped.
- `stop_background_audio()`: Stops any currently playing background audio.
