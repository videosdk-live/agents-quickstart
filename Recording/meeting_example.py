
import os
import requests
import aiohttp

# Meeting Recording (Composite output for entire meeting)

async def start_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/start"
    headers = {
        "Authorization": VIDEOSDK_AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "roomId": room_id,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Failed to start meeting recording: {response.status}, {text}")
            return await response.json()



async def stop_meeting_recording(room_id: str) -> dict:
    url = "https://api.videosdk.live/v2/recordings/end"
    headers = {
        "Authorization": VIDEOSDK_AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "roomId": room_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status != 200:
                text = await response.text()
                raise Exception(f"Failed to stop meeting recording: {response.status}, {text}")
            return await response.json()


# Example usage

async def on_enter(self) -> None:
    await self.session.say("Hello! I will start recording this meeting.")
    try:
        await start_meeting_recording(room_id)
        print("Meeting recording started")
    except Exception as e:
        print(f"Failed to start meeting recording: {e}")

async def on_exit(self) -> None:
    await self.session.say("Goodbye! Stopping the recording now.")
    try:
        await stop_meeting_recording(room_id)
        print("Meeting recording stopped")
    except Exception as e:
        print(f"Failed to stop meeting recording: {e}")