# VideoSDK AI Agent with Unity

[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

Unity example to join a static meeting room with microphone only (camera disabled), plus a Python AI agent that joins the same room and talks using Google Gemini Live.

## Prerequisites

- Unity 2022.3 LTS or later
- A VideoSDK Auth Token (JWT)
- A meeting `ROOM_ID` (create one via API)

### Create a meeting room
```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```
Copy the `roomId` from the response and use it as `YOUR_MEETING_ID`.

## Setup (Unity frontend)

1) Navigate to the project directory:
```bash
cd Unity-quickstart/Unity-VideoSdk-Example
```

2) Install VideoSDK Unity package:
- Open Unity's Package Manager: **Window -> Package Manager**
- Click **+** button and select **Add package from git URL...**
- Paste: `https://github.com/videosdk-live/videosdk-rtc-unity-sdk.git`
- Add `com.unity.nuget.newtonsoft-json` package

3) Configure credentials in `Assets/Scripts/GameManager.cs`:
```csharp
private readonly string _token = "YOUR_VIDEOSDK_AUTH_TOKEN";
private readonly string _meetingId = "YOUR_MEETING_ID";
```

4) Build and run:
- For Android: Build for Android and deploy to device
- For iOS: Build for iOS and open in Xcode

## Setup (Python AI Agent)

1) Navigate to the Unity quickstart directory:
```bash
cd Unity-quickstart
```

2) Install Python dependencies:
```bash
pip install videosdk-agents
pip install "videosdk-plugins-google"
```

3) Set environment variable:
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

4) Ensure the agent uses the same static room ID:
```python
# Unity-quickstart/agent-unity.py
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

5) Run the agent:
```bash
python agent-unity.py
```

## Notes

- Audio-only: camera disabled in Unity (`false` parameter in `Join()`)
- Static room join using `_meetingId` from `GameManager.cs`
- Requires microphone permission on mobile devices
