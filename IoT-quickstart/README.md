# VideoSDK AI Agent with IoT

<!-- [![Documentation](https://img.shields.io/badge/Read-Documentation-blue)](https://docs.videosdk.live/iot/guide/video-and-audio-calling-api-sdk/concept-and-architecture) -->
[![Discord](https://img.shields.io/discord/876774498798551130?label=Join%20on%20Discord)](https://discord.gg/Gpmj6eCq5u)
[![Register](https://img.shields.io/badge/Contact-Know%20More-blue)](https://app.videosdk.live/signup)

At Video SDK, we’re building tools to help developers bring real-time collaboration to IoT and embedded devices. With the IoT SDK, you can integrate live audio communication, meeting management, device-to-cloud connectivity, and session handling directly into ESP32. This quickstart adds an AI Agent (Python) that joins the same room and speaks using Google Gemini Live API.

### Get 10,000 minutes free every month! [Try it now](https://app.videosdk.live/signup)

## Table of Contents

- ⚡ Quick Setup
- 🔧 Prerequisites
- 📦 Running the Quick Start example (ESP-IDF firmware)
- 🤖 Running the AI Agent (Python)
- 🧠 Key Concepts
- 🔑 Token Generation
- 📖 Documentation
- 💬 Join Our Community

## ⚡ Quick Setup

1. Sign up on VideoSDK to grab your API Key and Secret: `https://app.videosdk.live/`
2. Create a meeting room ID via API (used by both device and agent):
```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```
Copy the `roomId` from the response and use it as `YOUR_MEETING_ID` below.

## 🔧 Prerequisites

- ESP-IDF installed and environment set up (ESP32-S3 recommended)
- Python >= 3.12
- A valid VideoSDK account and auth token (JWT)
- Google API Key for Gemini Live API (for the Agent)

## 📦 Running the Quick Start example (ESP32 firmware)

### 1) Configure ESP-IDF environment

Follow Step 1 of the VideoSDK IoT Quickstart to install ESP-IDF tools and set up your environment. You do NOT need to run project-creation commands since this repo already contains the project.

Docs: `https://docs.videosdk.live/iot/guide/video-and-audio-calling-api-sdk/quickstart/quick-start#step-1-setup-for-esp-idf`

### 2) Clone the sample project

```bash
git clone https://github.com/videosdk-live/agents-quickstart.git
cd agents-quickstart/IoT-quickstart
```

### 3) Add IoT SDK component

Clone the IoT SDK locally:
```bash
git clone https://github.com/videosdk-live/IoTSdk
```
Then set its local path inside `main/idf_component.yml` (or at project-level `idf_component.yml` if you keep dependencies there). Example:
```yaml
dependencies:
  iot-sdk:
    path: /absolute/path/to/IoTSdk
  protocol_examples_common:
    path: ${IDF_PATH}/examples/common_components/protocol_examples_common
  idf:
    version: =5.3.0
```

If your ESP-IDF version or module names differ, adjust accordingly.

### 4) Configure additional dependencies (if not present)

Append the following dependencies to your `idf_component.yml` (versions may vary by ESP-IDF version):
```yaml
  mdns: '*'
  espressif/esp_audio_codec: ~2.3.0
  espressif/esp_codec_dev: ~1.3.4
  espressif/esp_audio_effects: ~1.1.0
  sepfy/srtp: ^2.3.0
```

### 5) Set VideoSDK Token and Meeting ID in firmware

Open `main/ai-demo.c` and set your auth token and meeting ID:
```c
const char *token = "YOUR_VIDEOSDK_AUTH_TOKEN"; // Replace with your VideoSDK auth token

init_config_t init_cfg = {
    .meetingID = "YOUR_MEETING_ID", // From the curl response
    .token = token,
    .displayName = "ESP32-Device",
    .audioCodec = AUDIO_CODEC_OPUS,
};
```

Optionally, the example shows how to create a room on-device using `create_meeting(token)`. For a static room, prefer pre-creating it via the API and using `.meetingID`.

### 6) WiFi and board configuration (menuconfig)

Run menuconfig and set WiFi credentials, partition table, board, and TLS/DTLS support:
```bash
idf.py set-target esp32s3
idf.py menuconfig
```
Inside menuconfig:
- Component config → mbedtls → Enable Support DTLS; Enable Support TLS
- Example Connection Configuration → WIFI SSID / WIFI Password
- Partition table → Enable Custom partition table CSV (if using a custom one)
- Serial flasher config → Adjust flash size for your board
- Set Microcontroller → Select your audio hardware board (e.g., ESP32-S3-Korvo-2 or ESP32-S3-XIAO)

### 7) Build & Flash

```bash
idf.py build
idf.py flash monitor
```

On boot, the device will initialize VideoSDK, publish microphone audio, and (optionally) subscribe to audio streams.

## 🤖 Running the AI Agent (Python)

The AI Agent joins the same meeting room and talks using Google Gemini Live API.

### 1) Set the meeting ID for the Agent

Open `agent-iot.py` and ensure the room is set to your static room:
```python
room_options = RoomOptions(room_id="YOUR_MEETING_ID", name="Sandbox Agent", playground=True)
```

### 2) Install dependencies and set environment

```bash
cd agents-quickstart/IoT-quickstart
pip install videosdk-agents
pip install "videosdk-plugins-google"
```

```.env
VIDEOSDK_AUTH_TOKEN="your_authtoken_here"
GOOGLE_API_KEY="your_google_api_key_here"
```

### 3) Run the agent

```bash
python agent-iot.py
```

When the device joins the meeting, the agent will detect the participant and start the session. The agent will speak and interact via audio.

## Notes

- Keep tokens and API keys out of source control.
- Ensure both device and agent use the exact same `YOUR_MEETING_ID`.
- For best results, test with stable WiFi and power the ESP32 via a reliable source.

