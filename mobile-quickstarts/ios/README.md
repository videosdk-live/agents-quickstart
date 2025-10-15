# VideoSDK AI Agent Quickstart for iOS

<!-- ![iOS](https://img.shields.io/badge/iOS-000000?style=for-the-badge&logo=ios&logoColor=white) -->
<!-- ![Swift](https://img.shields.io/badge/Swift-FA7343?style=for-the-badge&logo=swift&logoColor=white) -->
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

A comprehensive iOS application demonstrating how to integrate VideoSDK's AI Agent capabilities using SwiftUI and VideoSDK RTC iOS SDK.

## Features

- **Audio-only Communication**: Focus on voice interaction with AI agent
- **Real-time AI Agent**: Google Gemini Live API integration
- **SwiftUI Interface**: Modern iOS user interface
- **Static Meeting ID**: Predefined room for consistent testing
- **Microphone Controls**: Mute/unmute functionality
- **Participant Management**: View active participants

## Prerequisites

- macOS with Xcode 15.0+
- iOS 13.0+ deployment target
- Valid VideoSDK [Account](https://app.videosdk.live/)
- Python 3.12+ (for the AI agent backend)
- Google API Key (for Gemini Live API)

## Run the Sample App

### 1. Clone the sample project

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/agents-quickstart.git
cd mobile-quickstarts/ios/
```

### 2. Environment Configuration

Create a `.env` file in the `ios/` directory with the following variables:

```env
VIDEOSDK_AUTH_TOKEN="your_authtoken_here"
GOOGLE_API_KEY="your_google_api_key_here"
```

### 3. Create a Meeting Room

Create a meeting room using the VideoSDK API:

```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_VIDEOSDK_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

Use the returned `roomId` in your configuration files.

### 4. Configuration Files

Update the following files with your credentials:

**MeetingViewController.swift** (line 14):
```swift
var token = "YOUR_VIDEOSDK_AUTH_TOKEN" // Add Your token here
```

**JoinScreenView.swift** (line 13):
```swift
let meetingId: String = "YOUR_MEETING_ID"
```

**agent-ios.py**:
```python
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

### 5. Step-by-Step Implementation

#### Step 1: Start the AI Agent Backend

1. **Open a new terminal and navigate to the ios directory:**
   ```bash
   cd mobile-quickstarts/ios/
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
   python agent-ios.py
   ```

#### Step 2: Run the iOS Frontend

1. **Open Xcode:**
   ```bash
   open videosdk-agents-quickstart-ios.xcodeproj
   ```

2. **Configure your development team:**
   - Select the project in Xcode
   - Go to "Signing & Capabilities"
   - Select your development team

3. **Build and run:**
   - Select your target device or simulator
   - Press `Cmd + R` to build and run

### 6. File Structure

```
ios/
├── agent-ios.py                    # Python AI agent backend
├── videosdk-agents-quickstart-ios/ # iOS app source code
│   ├── JoinScreenView.swift       # Entry screen with meeting ID
│   ├── MeetingView.swift          # Main meeting interface
│   ├── MeetingViewController.swift # Meeting logic and controls
│   ├── RoomsStruct.swift          # Data models
│   └── videosdk_agents_quickstart_iosApp.swift # App entry point
├── videosdk-agents-quickstart-ios.xcodeproj/ # Xcode project
└── README.md                      # This file
```

### 7. Key Components

#### AI Agent Backend (`agent-ios.py`)
- **RealtimeAgent**: Game show host AI personality
- **GeminiRealtime**: Google's Live API integration
- **RoomOptions**: Static meeting configuration
- **RealTimePipeline**: Audio processing pipeline

#### iOS Frontend
- **JoinScreenView**: User name input and meeting entry
- **MeetingView**: Main meeting interface with controls
- **MeetingViewController**: Core meeting logic and event handling
- **VideoSDK Integration**: Real-time communication setup

### 8. Troubleshooting

#### Common Issues

1. **Build Errors:**
   - Ensure Xcode 15.0+ is installed
   - Check iOS deployment target (13.0+)
   - Verify VideoSDK package dependency

2. **Authentication Issues:**
   - Verify `VIDEOSDK_AUTH_TOKEN` in `MeetingViewController.swift`
   - Check token permissions include `allow_join`

3. **Meeting Connection Issues:**
   - Ensure `YOUR_MEETING_ID` matches in both frontend and backend
   - Verify network connectivity
   - Check VideoSDK account status

4. **AI Agent Issues:**
   - Verify `GOOGLE_API_KEY` is set correctly
   - Check Python dependencies are installed
   - Ensure agent is running before joining meeting

#### Debug Steps

1. **Check Console Logs:**
   - Xcode console for iOS app logs
   - Terminal for Python agent logs

2. **Verify Configuration:**
   - Token format and permissions
   - Meeting ID consistency
   - API key validity

3. **Test Components:**
   - Join meeting without agent
   - Run agent without frontend
   - Check network connectivity

### 9. Security Notes

- Never commit real tokens or API keys to version control
- Use environment variables for sensitive data
- Regularly rotate authentication tokens
- Follow iOS security best practices for production apps

## Next Steps

- Customize the AI agent personality and responses
- Add video capabilities if needed
- Implement additional meeting features
- Deploy to App Store following Apple guidelines
