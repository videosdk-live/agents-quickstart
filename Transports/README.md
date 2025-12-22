# Transports

This example showcases the multi-transport support feature, enabling audio agents to run outside standard VideoSDK rooms using WebRTC (P2P) and WebSocket (raw PCM) transports.

## Features

- **Native support for WebRTC (P2P) and WebSocket (raw PCM) transports:** Provides flexible options for connecting audio agents to various clients.
- **Enables audio agents to run outside standard VideoSDK rooms:** Allows for integration possibilities with custom clients and environments.

## Example Usage

```python
from videosdk.agents import RoomOptions,WebSocketConfig,WebRTCConfig

# Option 1: Using Raw PCM WebSockets (for custom clients)
room_options = RoomOptions(
    transport_mode= "websocket",
    websocket=WebSocketConfig(port=8080, path="/ws")
)

# Option 2: Using Standard WebRTC (P2P)
room_options = RoomOptions(
    transport_mode= "webrtc",
    webrtc=WebRTCConfig(
        signaling_url="ws://localhost:8081",
        ice_servers=[{"urls": "stun:stun.l.google.com:19302"}]
    )
)
```

## Client Compatibility

Both WebRTC and WebSocket transports can be used with various client technologies, including:

- iOS
- Flutter
- Android
- Java Script 
- React
- React Native

## Recommendations

For a better and more scalable audio and video calling experience, it is highly recommended to use **VideoSDK**. VideoSDK provides comprehensive client SDK support for various platforms, ensuring seamless integration and robust performance for your agents.
