# VideoSDK AI Agent with Unity

[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/kgAvyxtTxv)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

Unity example to join a static meeting room, plus a Python AI agent that joins the same room and talks using Google Gemini Live.

## Prerequisites

- Unity 2022.3 LTS or later
- Valid VideoSDK [Account](https://app.videosdk.live/)
- Python 3.12+ (for the AI agent backend)
- Google API Key (for Gemini Live API)

## How to install the VideoSDK package?

1. Open Unity's Package Manager by selecting from the top bar:
   **Window -> Package Manager**.

2. Click the **+** button in the top left corner and select **Add package from git URL...**

3. Paste the following URL and click **Add**:

   ```
   https://github.com/videosdk-live/videosdk-rtc-unity-sdk.git
   ```

4. Add the `com.unity.nuget.newtonsoft-json` package by following the instructions provided [here](https://github.com/applejag/Newtonsoft.Json-for-Unity/wiki/Install-official-via-UPM).

## Android Setup

- Add the repository to `settingsTemplate.gradle` file in your project.

```gradle
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.PREFER_SETTINGS)
    repositories {
        **ARTIFACTORYREPOSITORY**
        google()
        mavenCentral()
        jcenter()
         maven {
            url = uri("https://maven.aliyun.com/repository/jcenter")
        }
        flatDir {
            dirs "${project(':unityLibrary').projectDir}/libs"
        }
    }
}
```

- Install our Android SDK in `mainTemplate.gradle`

```gradle
dependencies {
     //...
    implementation 'live.videosdk:rtc-android-sdk:0.1.37'
**DEPS**}
```

- If your project has set `android.useAndroidX=true`, 
then set `android.enableJetifier=true` in the `gradleTemplate.properties` file to migrate your project to AndroidX and avoid duplicate class conflict.

```properties
//...
**ADDITIONAL_PROPERTIES**
android.enableJetifier=true
android.useAndroidX=true
android.suppressUnsupportedCompileSdk=34
```

## iOS Setup

- To run it on iOS, build the project from Unity for iOS.

- After building the project for iOS, open the Xcode project and navigate to the Unity-iPhone target.

- Under Frameworks, Libraries and Embedded Content of the General tab, add the VideoSDK and related frameworks.

## Run the Sample App

### 1. Clone the sample project

Clone the repository to your local environment.

```bash
git clone https://github.com/videosdk-live/agents-quickstart.git
cd Unity-quickstart/
```

### 2. Environment Configuration

Create a `.env` file in the `Unity-quickstart/` directory with the following variables:

```env
VIDEOSDK_AUTH_TOKEN="your_authtoken_here"
GOOGLE_API_KEY="your_google_api_key_here"
```

### 3. Create Meeting Room

Create a meeting room using the VideoSDK API:

```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_VIDEOSDK_AUTH_TOKEN" \
  -H "Content-Type: application/json"
```

Use the returned `roomId` in your configuration files.

### 4. Configuration Files

Update the following files with your credentials:

**GameManager.cs**:
```csharp
private readonly string _token = "YOUR_VIDEOSDK_AUTH_TOKEN";
private readonly string _staticMeetingId = "YOUR_MEETING_ID";
```

**agent-unity.py**:
```python
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

### 5. Step-by-Step Implementation

#### Step 1: Start the AI Agent Backend

1. **Open a new terminal and navigate to the Unity-quickstart directory:**
   ```bash
   cd Unity-quickstart/
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
   python agent-unity.py
   ```

#### Step 2: Run the Unity Frontend

1. **Open Unity Hub and open the project:**
   - Open Unity Hub
   - Click "Open" and select the `Unity/` folder

2. **Configure the project:**
   - Wait for Unity to import all assets
   - Ensure the project builds without errors

3. **Build and run:**
   - Go to `File -> Build Settings`
   - Select your target platform (Android/iOS)
   - Click "Build and Run"

### 6. Connect and Interact

1. **Join the meeting from the Unity app:**
   - Tap the "Join Meeting" button
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
Unity-quickstart/
├── Unity/                          # Unity project folder
│   ├── Assets/
│   │   └── Scripts/
│   │       └── GameManager.cs     # Main Unity script
│   ├── ProjectSettings/           # Unity project settings
│   └── Packages/                  # Unity packages
├── agent-unity.py                 # Python AI agent backend
└── README.md                      # This file
```

## Key Components

### Frontend (Unity App)
- **Static Room Connection**: Automatically connects to the predefined room ID
- **Audio Controls**: Toggle microphone (webcam disabled for AI agent)
- **Real-time Communication**: WebRTC integration through VideoSDK
- **Cross-Platform**: Works on both Android and iOS

### Backend (`agent-unity.py`)
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
   - Check that the room ID matches in both `GameManager.cs` and `agent-unity.py`
   - Verify your VideoSDK token is valid
   - Make sure you've created the room using the VideoSDK API

2. **Audio not working:**
   - Check device permissions for microphone access
   - Ensure your Google API key has Gemini Live API access enabled
   - Verify microphone permissions in device settings

3. **Agent not responding:**
   - Verify your Google API key is correctly set in the environment
   - Check that the Gemini Live API is enabled in your Google Cloud Console
   - Ensure Python dependencies are installed correctly

4. **Unity build issues:**
   - Check Unity version compatibility
   - Verify all packages are imported correctly
   - Check platform-specific build settings

## Security Notes

- Never commit your `.env` file with real tokens to version control
- Keep your API keys secure and rotate them regularly
