# UtteranceHandle

`UtteranceHandle` is a utility class that allows precise control over an agent's speech lifecycle. It is returned by `session.say()` and can be used to manage sequential speech and handle interruptions gracefully.

## Key Features

- **Awaitable Speech**: `await` an `UtteranceHandle` to ensure a speech segment completes before executing the next line of code.
- **Interruption Detection**: Check the `utterance.interrupted` property to determine if the user has interrupted the agent's speech.
