# VideoSDK AI Agent with JavaScript

<!-- [![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/react/guide/video-and-audio-calling-api-sdk/getting-started) -->
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

This project demonstrates a real-time AI agent integration using VideoSDK with a JavaScript frontend and Python backend. The agent acts as a high-energy game show host that guides users to guess a secret number.

## Features

- **Static Room ID**: Both frontend and backend use the same static meeting room ID for simplicity
- **Real-time Voice Interaction**: AI agent responds with voice using Google Gemini Live API
- **Game Show Experience**: Interactive number guessing game with AI host
- **WebRTC Integration**: Seamless video/audio communication through VideoSDK

## Prerequisites

- Node.js (for serving the frontend)
- Python 3.12+ (for the AI agent backend)
- Google API Key (for Gemini Live API)
- VideoSDK Auth Token

## Cloning Repository

git clone https://github.com/videosdk-live/agents-quickstart.git
cd mobile-quickstarts/js/

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the `js/` directory with the following variables:

```env
# Google API Key for Gemini Live API
GOOGLE_API_KEY=your_google_api_key_here

# VideoSDK Authentication Token
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token_here
```

### 2. Create Meeting Room

Before configuring the application, you need to create a meeting room using the VideoSDK API:

```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```

**Replace `YOUR_JWT_TOKEN_HERE` with your actual VideoSDK auth token.**

The response will contain a `roomId` that you'll use in the configuration files:

```json
{
  "roomId": "your-generated-room-id-here"
}
```

Copy this `roomId` and use it as `YOUR_MEETING_ID` in the configuration files below.

### 3. Configuration Files

#### Create `config.js`:
```javascript
TOKEN = "your_videosdk_auth_token_here";
ROOM_ID = "YOUR_MEETING_ID";  // Static room ID shared between frontend and backend
```

#### `agent-js.py`:
The Python backend is already configured to use the same static room ID:
```python
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

## Step-by-Step Implementation

### Step 1: Start the Frontend

1. **Navigate to the js directory:**
   ```bash
   cd mobile-quickstarts/js/
   ```

2. **Serve the frontend files:**
   You can use any static file server. Here are a few options:

   **Option A: Using Python's built-in server:**
   ```bash
   python3 -m http.server 8000
   ```

   **Option B: Using Node.js http-server:**
   ```bash
   npx http-server -p 8000
   ```

   **Option C: Using Live Server (VS Code extension):**
   - Install the Live Server extension in VS Code
   - Right-click on `index.html` and select "Open with Live Server"

3. **Open the application:**
   - Navigate to `http://localhost:8000` in your web browser
   - You should see the "Join Agent Meeting" button

### Step 2: Start the AI Agent Backend

1. **Open a new terminal and navigate to the js directory:**
   ```bash
   cd mobile-quickstarts/js/
   ```

2. **Install Python dependencies:**
   ```bash
   pip install videosdk-agents
   pip install "videosdk-plugins-google"
   ```

3. **Set up environment variables:**
   ```bash
   export GOOGLE_API_KEY="your_google_api_key_here"
   ```

4. **Run the AI agent:**
   ```bash
   python agent-js.py
   ```

### Step 3: Connect and Interact

1. **Join the meeting from the frontend:**
   - Click the "Join Agent Meeting" button in your browser
   - Allow microphone and camera permissions when prompted

2. **Agent connection:**
   - Once you join, the Python backend will detect your participation
   - You should see "Participant joined" in the terminal
   - The AI agent will greet and initiate the game"

3. **Start playing:**
   - The agent will guide you through a number guessing game (1-100)
   - Use your microphone to interact with the AI host
   - The agent will provide hints and encouragement throughout the game

## File Structure

```
js/
├── README.md              # This file
├── index.html             # Frontend HTML interface
├── index.js               # Frontend JavaScript logic
├── config.js              # Configuration (tokens, room ID) (create this - refer config.example.js)
├── agent-js.py            # Python AI agent backend
└── .env                   # Environment variables (create this)
```

## Key Components

### Frontend (`index.html` + `index.js`)
- **Static Room Connection**: Automatically connects to the predefined room ID
- **Video/Audio Controls**: Toggle microphone and camera
- **Real-time Communication**: WebRTC integration through VideoSDK

### Backend (`agent-js.py`)
- **AI Agent**: Game show host personality using Google Gemini Live
- **Voice Interaction**: Real-time audio processing and response
- **Room Management**: Waits for participants and manages the session

### Configuration
- **Static Room ID**: `"YOUR_MEETING_ID"` ensures both frontend and backend connect to the same room
- **Environment Variables**: Secure storage of API keys and tokens

## Troubleshooting

### Common Issues:

1. **"Waiting for participant..." but no connection:**
   - Ensure both frontend and backend are running
   - Check that the room ID matches in both `config.js` and `agent-js.py`
   - Verify your VideoSDK token is valid
   - Make sure you've created the room using the VideoSDK API and copied the correct room ID

2. **Audio not working:**
   - Check browser permissions for microphone access
   - Ensure your Google API key has Gemini Live API access enabled

3. **Agent not responding:**
   - Verify your Google API key is correctly set in the environment
   - Check that the Gemini Live API is enabled in your Google Cloud Console

## Security Notes

- Never commit your `.env` file or `config.js` with real tokens to version control
- Use the `config.example.js` as a template for others
- Keep your API keys secure and rotate them regularly

## Next Steps

- Customize the agent's personality and instructions in `agent-js.py`
- Add more interactive features to the frontend
- Implement additional game mechanics or conversation flows
- Deploy to a production environment with proper security measures

