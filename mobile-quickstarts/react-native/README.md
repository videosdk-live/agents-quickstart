# VideoSDK AI Agent with React Native

<!-- [![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/react-native/guide/video-and-audio-calling-api-sdk/concept-and-architecture) -->
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

This project demonstrates a real-time AI agent integration using VideoSDK with a React Native frontend and Python backend. The agent acts as a high-energy game show host that guides users to guess a secret number.

At Video SDK, we're building tools to help companies create world-class collaborative products with capabilities of live audio/videos, compose cloud recordings/rtmp/hls and interaction APIs

## Features

- **Static Room ID**: Both frontend and backend use the same static meeting room ID for simplicity
- **Real-time Voice Interaction**: AI agent responds with voice using Google Gemini Live API
- **Game Show Experience**: Interactive number guessing game with AI host
- **WebRTC Integration**: Seamless audio communication through VideoSDK
- **Audio-Only Mode**: Microphone input and audio output only (webcam disabled)
- **Cross-Platform**: Works on both Android and iOS devices

## Setup Guide

- Sign up on [VideoSDK](https://app.videosdk.live/) and visit [API Keys](https://app.videosdk.live/api-keys) section to get your API key and Secret key.
- Get familiarized with [Authentication and tokens](https://docs.videosdk.live/react-native/guide/video-and-audio-calling-api-sdk/authentication-and-token)

### Prerequisites

- Node.js 18+ (for React Native development)
- React Native development environment:
  - **Android**: Android Studio 
  - **iOS**: Xcode
- Python 3.12+ (for the AI agent backend)
- Google API Key (for Gemini Live API)
- Valid [Video SDK Account](https://app.videosdk.live/signup)

## Run the Sample App

### Step 1: Clone the sample project

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/agents-quickstart.git
cd mobile-quickstarts/react-native/
```

### Step 2: Environment Configuration

Create a `.env` file in the `react-native/` directory with the following variables:

```env
# Google API Key for Gemini Live API
GOOGLE_API_KEY=your_google_api_key_here

# VideoSDK Authentication Token
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token_here
```

### Step 3: Create Meeting Room

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

### Step 4: Update Configuration Files

#### Update `constants.js`:
```javascript
export const token = "your_videosdk_auth_token_here";
export const meetingId = "YOUR_MEETING_ID";  // Static room ID shared between frontend and backend
export const name = "React Native Agent User";
```

#### Update `agent-react-native.py`:
Update the `room_id` in the agent-react-native.py:
```python
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

### Step 5: Install Dependencies

Install all the dependencies to run the project.

```bash
npm install
```

### Step 6: Run the React Native App

#### For Android Development:

**Option A: Using Command Line (Recommended)**
```bash
npm run android
```

**Option B: Using Android Studio**
1. Open Android Studio
2. Open the `android/` folder from the project directory
3. Build and run the project from Android Studio

**Prerequisites for Android:**
- Android Studio installed
- Android SDK configured
- Android emulator running or physical device connected via USB
- USB debugging enabled on physical device

#### For iOS Development:

**Option A: Using Command Line (Recommended)**
```bash
npm run ios
```

**Option B: Using Xcode**
1. Open Xcode
2. Open `ios/MyApp.xcworkspace` from the project directory
3. Build and run the project from Xcode

**Prerequisites for iOS:**
- Xcode installed (macOS only)
- iOS Simulator or physical device
- Apple Developer account (for physical devices)
- CocoaPods installed: `sudo gem install cocoapods`

### Step 7: Start the AI Agent Backend

1. **Open a new terminal and navigate to the react-native directory:**
   ```bash
   cd mobile-quickstarts/react-native/
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
   python agent-react-native.py
   ```

### Step 8: Connect and Interact

1. **Join the meeting from the React Native app:**
   - Click the "Join" button in your React Native app
   - Allow microphone permissions when prompted

2. **Agent connection:**
   - Once you join, the Python backend will detect your participation
   - You should see "Participant joined" in the terminal
   - The AI agent will greet and initiate the game

3. **Start playing:**
   - The agent will guide you through a number guessing game (1-100)
   - Use your microphone to interact with the AI host
   - The agent will provide hints and encouragement throughout the game


## File Structure

```
react-native/
├── README.md              # This file
├── App.js                 # React Native frontend component
├── constants.js           # Configuration (tokens, room ID)
├── agent-react-native.py  # Python AI agent backend
├── package.json           # Node.js dependencies
├── android/               # Android native code
├── ios/                   # iOS native code
└── .env                   # Environment variables (create this)
```

## Key Components

### Frontend (`App.js`)
- **Static Room Connection**: Automatically connects to the predefined room ID
- **Audio Controls**: Toggle microphone (webcam disabled for AI agent)
- **Real-time Communication**: WebRTC integration through VideoSDK
- **Cross-Platform**: Works on both Android and iOS

### Backend (`agent-react-native.py`)
- **AI Agent**: Game show host personality using Google Gemini Live
- **Voice Interaction**: Real-time audio processing and response
- **Room Management**: Waits for participants and manages the session
- **Game Logic**: Interactive number guessing game (1-100)

### Configuration
- **Static Room ID**: `"YOUR_MEETING_ID"` ensures both frontend and backend connect to the same room
- **Environment Variables**: Secure storage of API keys and tokens

## Troubleshooting

### Common Issues:

1. **"Waiting for participant..." but no connection:**
   - Ensure both frontend and backend are running
   - Check that the room ID matches in both `constants.js` and `agent-react-native.py`
   - Verify your VideoSDK token is valid
   - Make sure you've created the room using the VideoSDK API and copied the correct room ID

2. **Audio not working:**
   - Check device permissions for microphone access
   - Ensure your Google API key has Gemini Live API access enabled
   - Verify microphone permissions in device settings

3. **Agent not responding:**
   - Verify your Google API key is correctly set in the environment
   - Check that the Gemini Live API is enabled in your Google Cloud Console
   - Ensure Python dependencies are installed correctly

4. **React Native build issues:**

   **Android:**
   - Clean and rebuild: `cd android && ./gradlew clean && cd .. && npm run android`
   - Check Android Studio and SDK setup
   - Verify emulator or device connection

   **iOS:**
   - Clean and rebuild: `cd ios && xcodebuild clean && cd .. && npm run ios`
   - Check Xcode and iOS SDK setup
   - Verify simulator or device connection
   - Run `cd ios && pod install` if needed

5. **Metro bundler issues:**
   - Clear Metro cache: `npx react-native start --reset-cache`
   - Restart Metro bundler
   - Check Node.js version compatibility

### Platform Compatibility:
- **Android**: API level 25+ (Android 7.0+)
- **iOS**: iOS 15.1+
- **React Native**: 0.70+


## Security Notes

- Never commit your `.env` file or `constants.js` with real tokens to version control
- Keep your API keys secure and rotate them regularly