# VideoSDK Agent React 

Minimal React example to join a static meeting room with microphone only (webcam disabled). Uses `@videosdk.live/react-sdk`.

## Prerequisites
- Node.js 16+
- A VideoSDK Auth Token (JWT)
- A meeting `ROOM_ID` (create one via API)

Create a meeting room:
```bash
curl -X POST https://api.videosdk.live/v2/rooms \
  -H "Authorization: YOUR_JWT_TOKEN_HERE" \
  -H "Content-Type: application/json"
```
Copy the `roomId` from the response and use it as `YOUR_MEETING_ID`.

## Setup
1. Navigate to project directory:
```bash
cd mobile-quickstarts/react
```
2. Install deps:
```bash
npm install
```
2. Configure credentials:
- Copy `src/config.example.js` to `src/config.js` and set:
```js
export const TOKEN = "YOUR_VIDEOSDK_AUTH_TOKEN";
export const ROOM_ID = "YOUR_MEETING_ID"; // from the curl response
```

## Run
```bash
npm start
```
Open the app at `http://localhost:3000`, click Join.

## Notes
- Audio-only: `webcamEnabled: false`
- Static room join using `ROOM_ID` from `src/config.js`
