# Call Transfer

This example demonstrates how to transfer an ongoing SIP call to a phone number or another SIP endpoint.

## Key Features

- **SIP Call Transfer**: Transfer a live call to a different phone number or SIP endpoint.
- **Agent Handoff**: The agent leaves the call automatically after the transfer.

## How It Works

The `call_transfer.py` script shows an agent that can transfer a call using the `call_transfer` method on the session object. When invoked, the agent disconnects, and the call is transferred to the specified destination.

You will need to provide the destination (phone number or SIP URI) and a VideoSDK Auth Token.

## How to Run

1.  **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set up your environment variables**:

    Copy [`.env.example`](../.env.example) at the repo root to `.env` and fill in: `DEEPGRAM_API_KEY`, `GOOGLE_API_KEY`, `CARTESIA_API_KEY`. Also set `CALL_TRANSFER_TO=<phone_number_or_sip_uri_to_transfer_to>`.

    For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime). **Note**: the `transfer_call()` tool in `call_transfer.py` calls the VideoSDK Call Transfer REST API directly with a JWT, so it still reads `VIDEOSDK_AUTH_TOKEN` explicitly — set that one if you want to use the transfer tool.

3.  **Run the agent**:
    ```bash
    python "Call Transfer/call_transfer.py"
    ```
