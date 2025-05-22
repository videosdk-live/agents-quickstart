# 🚀 AWS Nova Sonic Agent for VideoSDK

This directory contains example code for integrating an AWS Nova Sonic-powered voice agent into VideoSDK meetings.

## Prerequisites

Before using AWS Nova Sonic with the VideoSDK AI Agent, ensure the following:

- **AWS Account**: You have an active AWS account with permissions to access Amazon Bedrock.
- **Model Access**: You've requested and obtained access to the Amazon Nova models (Nova Lite and Nova Canvas) via the Amazon Bedrock console.
- **Region Selection**: You're operating in the US East (N. Virginia) (us-east-1) region, as model access is region-specific.
- **AWS Credentials**: Your AWS credentials (aws_access_key_id and aws_secret_access_key) are configured.

## 🛠️ Installation

Install the AWS-enabled VideoSDK Agents package:

```bash
pip install "videosdk-plugins-aws"
```

## Configuration

Before running the agent, make sure to:

1. Replace the placeholder AWS credentials in `aws_novasonic_agent_quickstart.py` with your actual AWS credentials
   ```python
   model = NovaSonicRealtime(
       model="amazon.nova-sonic-v1:0",
       region="us-east-1",  # Currently, only "us-east-1" is supported for Amazon Nova Sonic
       aws_access_key_id="your-aws-access-key-id",  # Or use environment variable
       aws_secret_access_key="your-aws-secret-access-key",  # Or use environment variable
       # ...
   )
   ```

2. Set your VideoSDK credentials in the context dictionary:
   ```python
   def make_context():
       return {
           "meetingId": "your-meeting-id",               # VideoSDK meeting ID
           "name": "AWS Agent",                          # Name displayed in the meeting
           "videosdk_auth": "your-videosdk-auth-token"   # VideoSDK auth token
       }
   ```

   You can also use environment variables instead:
   ```python
   def make_context():
       return {
           "meetingId": os.environ.get("VIDEOSDK_MEETING_ID"),
           "name": "AWS Agent",
           "videosdk_auth": os.environ.get("VIDEOSDK_AUTH_TOKEN")
       }
   ```

## Running the Example

To run the AWS-powered agent:

```bash
python aws_novasonic_agent_quickstart.py
```

> **Note**: To initiate a conversation with Amazon Nova Sonic, the user must speak first. The model listens for user input to begin the interaction.

## ✨ Key Features

- **Speech-to-Speech AI**: Direct speech interaction without intermediate text conversion
- **Function Calling**: Retrieve weather data and other information
- **Custom Agent Behaviors**: Define agent personality and interaction style
- **Call Control**: Agents can manage call flow and termination

## 🧠 Nova Sonic Configuration

The agent uses Amazon's Nova Sonic model for real-time, speech-to-speech AI interactions. Configuration options include:

- `model`: The Nova Sonic model to use (e.g., `"amazon.nova-sonic-v1:0"`)
- `region`: AWS region where the model is hosted (currently only `"us-east-1"` is supported)
- `aws_access_key_id` and `aws_secret_access_key`: Your AWS credentials
- `config`: Advanced configuration options including voice, temperature, top_p, max_tokens, etc.

For complete configuration options, see the [official VideoSDK AWS Nova Sonic plugin documentation](https://docs.videosdk.live/ai_agents/plugins/aws-nova-sonic).

---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team

