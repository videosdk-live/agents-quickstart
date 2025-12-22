# Conversational Graph

The **Conversational Graph** is a powerful tool that allows you to define complex, structured conversation flows for your AI agents. Instead of relying solely on an LLM's inherent reasoning, which can sometimes be unpredictable, you can use a graph-based approach to guide the conversation through specific states and transitions.

## Installation

To use the Conversational Graph, you need to install the `videosdk-conversational-graph` package.

```bash
pip install videosdk-conversational-graph
```

:::note
Check out the latest version of [videosdk-conversational-graph](https://pypi.org/project/videosdk-conversational-graph/) on PyPI.
:::

## Core Concepts

The Conversational Graph is built around a few key concepts:

1.  **ConversationalGraph**: The main object that manages the states and transitions.
2.  **State**: A specific point in the conversation (e.g., "Greeting", "Asking for Name"). Each state has instructions for the agent.
3.  **Transition**: Logic that dictates how the agent moves from one state to another based on user input or collected data.

## Working Example

- [Conversational Graph Example](https://github.com/videosdk-live/agents/blob/main/examples/test_workflow_pipeline.py): Check out the complete working example of a Loan Application agent using Conversational Graph.