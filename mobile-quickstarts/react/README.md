# VideoSDK AI Agent with React

<!-- [![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/react/guide/video-and-audio-calling-api-sdk/concept-and-architecture) -->
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

React example to join a static meeting room with microphone only (webcam disabled), a Python AI agent that joins the same room and talks using Google Gemini Live.

## Prerequisites
- Node.js 16+
- A VideoSDK Auth Token (JWT)
- A meeting `ROOM_ID` (create one via API)

### Create a meeting room
```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```
Copy the `roomId` from the response and use it as `YOUR_MEETING_ID`.

## Setup (React frontend)
1) Navigate to the project directory:
```bash
cd mobile-quickstarts/react
```

2) Install dependencies:
```bash
npm install
```

3) Configure credentials:
- Copy `src/config.example.js` to `src/config.js` and set:
```js
export const TOKEN = "YOUR_VIDEOSDK_AUTH_TOKEN";
export const ROOM_ID = "YOUR_MEETING_ID"; // from the curl response
```

4) Run the app:
```bash
npm start
```
Open `http://localhost:3000` and click Join.

## Setup (Python AI Agent)
1) Navigate to the React quickstart directory:
```bash
cd mobile-quickstarts/react
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
# mobile-quickstarts/react/agent-react.py
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

5) Run the agent:
```bash
python agent-react.py
```

## Notes
- Audio-only: `webcamEnabled: false`
- Static room join using `ROOM_ID` from `src/config.js`
