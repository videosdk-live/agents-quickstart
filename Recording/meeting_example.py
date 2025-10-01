
import os
import requests

VIDEOSDK_AUTH_TOKEN = os.getenv("VIDEOSDK_AUTH_TOKEN")

# -----------------------------
# Meeting Recording
# (Composite output for entire meeting)
# -----------------------------
def start_meeting_recording(room_id: str, config: dict = None) -> dict:
    url = "https://api.videosdk.live/v2/recordings/start"
    headers = {"Authorization": VIDEOSDK_AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {"roomId": room_id, "config": config or {"layout": "grid"}}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


def stop_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/stop"
    headers = {"Authorization": VIDEOSDK_AUTH_TOKEN, "Content-Type": "application/json"}
    payload = {"roomId": room_id}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()


# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    ROOM_ID = "abcd-efgh-ijkl"  # Replace with your actual room ID

    # Meeting Recording (composite)
    print("Starting meeting recording...")
    meeting_resp = start_meeting_recording(ROOM_ID)
    print("Meeting recording started:", meeting_resp)

    # Stop recordings (for demo purposes, usually triggered later)

    print("Stopping meeting recording...")
    print(stop_meeting_recording(ROOM_ID))