# Human in the Loop (HITL)

Human in the Loop enables AI agents to escalate specific queries to human operators for review and approval. This example uses Discord as the human interface, enabling seamless handoffs between AI automation and human oversight.

## Overview

- Handle routine inquiries autonomously
- Escalate special cases (e.g., discounts) to human operators via Discord
- Receive human responses and relay them back to users
- Maintain conversation flow while waiting for human input

## Example Overview

- Customer Agent: VideoSDK AI agent that handles customer interactions and escalates specific queries
- Discord MCP Server: MCP server that creates Discord threads for human operator responses

## Customer Agent Setup

```python
from videosdk.agents import Agent, MCPServerStdio
import pathlib
import sys

class CustomerAgent(Agent):
    def __init__(self, ctx: Optional[JobContext] = None):
        current_dir = pathlib.Path(__file__).parent
        discord_mcp_server_path = current_dir / "discord_mcp_server.py"

        super().__init__(
            instructions=(
                "You are a customer-facing agent for VideoSDK. You have access to various tools to assist with customer inquiries, provide support, and handle tasks. "
                "When a user asks for a discount percentage, always use the appropriate tool to retrieve and provide the accurate answer from your superior human agent."
            ),
            mcp_servers=[
                MCPServerStdio(
                    executable_path=sys.executable,
                    process_arguments=[str(discord_mcp_server_path)],
                    session_timeout=30
                ),
            ]
        )
        self.ctx = ctx
```

## Discord MCP Server

```python
from mcp.server.fastmcp import FastMCP
import discord
from discord.ext import commands

class DiscordHuman:
    def __init__(self, user_id: int, channel_id: int):
        self.user_id = user_id
        self.channel_id = channel_id
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        self.response_future = None

    async def ask(self, question: str) -> str:
        channel = self.bot.get_channel(self.channel_id)
        thread = await channel.create_thread(
            name=question[:100],
            type=discord.ChannelType.public_thread
        )
        await thread.send(f"<@{self.user_id}> {question}")

        self.response_future = self.loop.create_future()
        try:
            return await asyncio.wait_for(self.response_future, timeout=600)
        except asyncio.TimeoutError:
            return "⏱️ Timed out waiting for a human response"

# MCP Server Setup
mcp = FastMCP("HumanInTheLoopServer")

@mcp.tool(description="Ask a human agent via Discord for a specific user query such as discount percentage, etc.")
async def ask_human(question: str) -> str:
    return await discord_human.ask(question)
```

## Environment Variables

```bash
DISCORD_TOKEN=your_discord_bot_token
DISCORD_USER_ID=human_operator_user_id
DISCORD_CHANNEL_ID=channel_id_for_escalations
```

See `DISCORD_BOT.md` for bot setup and permissions.
