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

    Create a `.env` file in the root of the project and add the following:

    ```
    DEEPGRAM_API_KEY=<your_deepgram_api_key>
    GOOGLE_API_KEY=<your_google_api_key>
    CARTESIA_API_KEY=<your_cartesia_api_key>
    VIDEOSDK_AUTH_TOKEN=<your_videosdk_auth_token>
    CALL_TRANSFER_TO=<phone_number_or_sip_uri_to_transfer_to>
    ```

3.  **Run the agent**:
    ```bash
    python "Call Transfer/call_transfer.py"
    ```
