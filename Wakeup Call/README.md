# Wake Up Call

Wake Up Call enables AI agents to automatically trigger actions when users remain inactive for a specified duration. This helps maintain engagement and provide proactive assistance during sessions.

## Overview

- Monitor user inactivity during conversations
- Automatically trigger custom callback functions after timeouts
- Re-engage users with proactive messages or actions

## Key Components

### Wake Up Configuration

Set the inactivity timeout in the `AgentSession` using the `wake_up` parameter:

```python
session = AgentSession(
    agent=agent,
    pipeline=pipeline,
    conversation_flow=conversation_flow,
    wake_up=10  # seconds
)
```

Important: If a `wake_up` time is provided, you must set a callback function before starting the session. If no `wake_up` time is specified, no timer or callback will be activated.

### Callback Function

Define a custom async function that runs when the inactivity threshold is reached:

```python
async def on_wake_up():
    print("Wake up triggered - user inactive for 10 seconds")
    session.say("Hello, how can I help you today?")

session.on_wake_up = on_wake_up
```

## Example

See `wakeup_call.py` in this directory for a complete runnable example.
