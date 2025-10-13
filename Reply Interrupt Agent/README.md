# Reply Interrupt Agent

This example demonstrates how to use external methods, `reply` and `interrupt`, within an agent's session. The agent is designed to handle incoming Pub/Sub messages and trigger specific actions based on the message content.

## How It Works

The agent subscribes to a Pub/Sub topic named "CHAT". It then listens for messages on this topic and performs actions based on the content of the received message:

-   **Reply**: When a message with the payload `{"message": "reply"}` is received, the agent calls the `session.reply()` method. This sends a predefined message to the user, in this case, a request to generate a random number and tell a joke.

-   **Interrupt**: If a message with the payload `{"message": "interrupt"}` is received, the agent calls the `session.interrupt()` method. This immediately stops any ongoing speech or action from the agent.

