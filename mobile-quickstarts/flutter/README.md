# VideoSDK AI Agent with Flutter

<!-- [![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/flutter/guide/video-and-audio-calling-api-sdk/getting-started) -->
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.com/invite/f2WsNDN9S5)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

This project demonstrates a real-time AI agent integration using VideoSDK with a Flutter frontend and Python backend. The agent acts as a high-energy game show host that guides users to guess a secret number.

At Video SDK, we're building tools to help companies create world-class collaborative products with capabilities of live audio/videos, compose cloud recordings/rtmp/hls and interaction APIs.

## Features

- **Static Room ID**: Both frontend and backend use the same static meeting room ID for simplicity
- **Real-time Voice Interaction**: AI agent responds with voice using Google Gemini Live API
- **Game Show Experience**: Interactive number guessing game with AI host
- **WebRTC Integration**: Seamless audio communication through VideoSDK
- **Audio-Only Mode**: Microphone input and audio output only (webcam disabled)
- **Cross-Platform**: Works on both Android and iOS devices

## Setup Guide

- Sign up on [VideoSDK](https://app.videosdk.live/) and visit [API Keys](https://app.videosdk.live/api-keys) section to get your API key and Secret key.
- Get familiarized with [API key and Secret key](https://docs.videosdk.live/flutter/guide/video-and-audio-calling-api-sdk/signup-and-create-api)
- Get familiarized with [Token](https://docs.videosdk.live/flutter/guide/video-and-audio-calling-api-sdk/server-setup)

## Prerequisites

- If your target platform is iOS, your development environment must meet the following requirements:
  - Flutter 2.0 or later
  - Dart 2.12.0 or later
  - macOS
  - Xcode (Latest version recommended)
- If your target platform is Android, your development environment must meet the following requirements:
  - Flutter 2.0 or later
  - Dart 2.12.0 or later
  - macOS or Windows
  - Android Studio (Latest version recommended)
- If your target platform is iOS, you need a real iOS device.
- If your target platform is Android, you need an Android simulator or a real Android device.
- Valid Video SDK [Account](https://app.videosdk.live/)
- Python 3.12+ (for the AI agent backend)
- Google API Key (for Gemini Live API)

## Run the Sample App

### 1. Clone the sample project

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/agents-quickstart.git
cd mobile-quickstarts/flutter/
```

### 2. Environment Configuration

Create a `.env` file in the `flutter/` directory with the following variables:

```env
# Google API Key for Gemini Live API
GOOGLE_API_KEY=your_google_api_key_here

# VideoSDK Authentication Token
VIDEOSDK_AUTH_TOKEN=your_videosdk_auth_token_here
```

### 3. Create Meeting Room

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

### 4. Update Configuration Files

#### Update `lib/api_call.dart`:
Update the auth token in the Flutter app:

```dart
//Auth token we will use to generate a meeting and connect to it
const token = 'YOUR_VIDEOSDK_AUTH_TOKEN';
```

#### Update `lib/join_screen.dart`:
Update the static meeting ID in the Flutter app:

```dart
MeetingScreen(meetingId: "YOUR_MEETING_ID", token: token)
```

#### Update `agent-flutter.py`:
Update the `room_id` in the agent-flutter.py:
```python
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

### 5. Install Dependencies

Install all the dependencies to run the project.

```bash
flutter pub get
```

### 6. Run the Flutter App

#### For Android:
```bash
flutter run -d android
```

#### For iOS:
```bash
flutter run -d ios
```

### 7. Start the AI Agent Backend

1. **Open a new terminal and navigate to the flutter directory:**
   ```bash
   cd mobile-quickstarts/flutter/
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
   python agent-flutter.py
   ```

### 8. Connect and Interact

1. **Join the meeting from the Flutter app:**
   - Tap the "Join" button in your Flutter app
   - Allow microphone permissions when prompted

2. **Agent connection:**
   - Once you join, the Python backend will detect your participation
   - You should see "Participant joined" in the terminal
   - The AI agent will greet and initiate the game

3. **Start playing:**
   - The agent will guide you through a number guessing game (1-100)
   - Use your microphone to interact with the AI host
   - The agent will provide hints and encouragement throughout the game

## Key Concepts

- `Meeting` - A Meeting represents Real time audio and video communication.

  **`Note : Don't confuse with Room and Meeting keyword, both are same thing 😃`**

- `Sessions` - A particular duration you spend in a given meeting is a referred as session, you can have multiple session of a particular meetingId.
- `Participant` - Participant represents someone who is attending the meeting's session, `local partcipant` represents self (You), for this self, other participants are `remote participants`.
- `Stream` - Stream means video or audio media content that is either published by `local participant` or `remote participants`.
- `AI Agent` - An intelligent participant that can interact with human participants using voice and AI capabilities.

## Android Permission

Add all the following permissions to AndroidManifest.xml file.

```xml
<uses-feature android:name="android.hardware.camera" />
<uses-feature android:name="android.hardware.camera.autofocus" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.READ_PHONE_STATE" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.CHANGE_NETWORK_STATE" />
```

## iOS Permission

Add the following entry to your Info.plist file, located at `<project root>/ios/Runner/Info.plist`:

```xml
<key>NSCameraUsageDescription</key>
<string>$(PRODUCT_NAME) Camera Usage!</string>
<key>NSMicrophoneUsageDescription</key>
<string>$(PRODUCT_NAME) Microphone Usage!</string>
```


## File Structure

```
flutter/
├── README.md              # This file
├── lib/                   # Flutter app source code
│   ├── api_call.dart      # Auth token configuration
│   ├── join_screen.dart   # Static meeting ID configuration
│   ├── meeting_screen.dart # Main meeting interface
│   ├── participant_tile.dart # Participant display
│   └── main.dart          # App entry point
├── android/               # Android native code
├── ios/                   # iOS native code
├── agent-flutter.py       # Python AI agent backend
├── pubspec.yaml           # Flutter dependencies
└── .env                   # Environment variables (create this)
```

## Key Components

### Frontend (Flutter App)
- **Static Room Connection**: Automatically connects to the predefined room ID
- **Audio Controls**: Toggle microphone (webcam disabled for AI agent)
- **Real-time Communication**: WebRTC integration through VideoSDK
- **Cross-Platform**: Works on both Android and iOS

### Backend (`agent-flutter.py`)
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
   - Check that the room ID matches in both `lib/join_screen.dart` and `agent-flutter.py`
   - Verify your VideoSDK token is valid in `lib/api_call.dart`
   - Make sure you've created the room using the VideoSDK API and copied the correct room ID

2. **Audio not working:**
   - Check device permissions for microphone access
   - Ensure your Google API key has Gemini Live API access enabled
   - Verify microphone permissions in device settings

3. **Agent not responding:**
   - Verify your Google API key is correctly set in the environment
   - Check that the Gemini Live API is enabled in your Google Cloud Console
   - Ensure Python dependencies are installed correctly

4. **Flutter build issues:**
   - Clean and rebuild: `flutter clean && flutter pub get`
   - Check Flutter environment setup
   - Verify Dart/Flutter version compatibility

5. **Platform-specific issues:**
   - **Android**: Check Android SDK and build tools
   - **iOS**: Check Xcode and iOS deployment target
   - Run `flutter doctor` to diagnose environment issues

## Security Notes

- Never commit your `.env` file with real tokens to version control
- Keep your API keys secure and rotate them regularly
