import requests
from dotenv import load_dotenv

def start_track_recording(participant_id: str, kind="audio"):
    url = "https://api.videosdk.live/v2/recordings/participant/track/start"
    payload = {
        "roomId": ROOM_ID,
        "participantId": participant_id,
        "kind": kind,
        "fileFormat": "webm", #optional
        "webhookUrl": "https://www.example.com/", #optional
        "bucketDirPath": "s3path" #optional
    }
    headers = {
        "Authorization": VIDEOSDK_API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Started {kind} recording for participant {participant_id}: {response.text}")

def stop_track_recording(participant_id: str, kind="audio"):
    url = "https://api.videosdk.live/v2/recordings/participant/track/stop"
    payload = {
        "roomId": ROOM_ID,
        "participantId": participant_id,
        "kind": kind
    }
    headers = {
        "Authorization": VIDEOSDK_API_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Stopped {kind} recording for participant {participant_id}: {response.text}")

##Example usage

class MyVoiceAgent(Agent):

    async def on_enter(self) -> None:
        await self.session.say("Hello, how can I help you today?")
    
    async def on_exit(self) -> None:
        await self.session.say("Goodbye!")
    
    # Called automatically when a participant's stream is enabled
    def on_stream_enabled(self, participant_id: str, kind="audio"):
        start_track_recording(participant_id, kind)

    # Called automatically when a participant's stream is disabled
    def on_stream_disabled(self, participant_id: str, kind="audio"):
        stop_track_recording(participant_id, kind)
        
    