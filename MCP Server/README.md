# 🔗 Model Context Protocol (MCP) Integration Example

This directory contains an example MCP server implementation that demonstrates how to integrate the Model Context Protocol with VideoSDK AI agents.

## 📖 What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is an open protocol that standardizes how applications provide context to LLMs. Think of MCP like a USB-C port for AI applications - it provides a standardized way to connect AI models to different data sources and tools.

## 🏗️ Architecture

MCP follows a client-server architecture:

- **MCP Hosts**: VideoSDK AI agents that want to access data through MCP
- **MCP Clients**: Protocol clients that maintain 1:1 connections with servers  
- **MCP Servers**: Lightweight programs that expose specific capabilities through the standardized protocol
- **Data Sources**: Your services, databases, and APIs that MCP servers can access

## 📁 Example Server

The `mcp_stdio_example.py` file demonstrates a simple MCP server that provides current time functionality:

```python
from mcp.server.fastmcp import FastMCP
import datetime

# Create the MCP server
mcp = FastMCP("CurrentTimeServer")

@mcp.tool()
def get_current_time() -> str:
    """Get the current time in the user's location"""
    now = datetime.datetime.now()
    return f"The current time is {now.strftime('%H:%M:%S')} on {now.strftime('%Y-%m-%d')}"

if __name__ == "__main__":
    mcp.run(transport="stdio")  # Use stdio for direct process communication
```

## 🚀 Integration with VideoSDK Agents

VideoSDK agents can connect to MCP servers using two transport methods:

### 1. STDIO Transport (MCPServerStdio)
For local process communication:

```python
from videosdk.agents import MCPServerStdio
import sys
from pathlib import Path

mcp_script = Path(__file__).parent.parent / "MCP Server" / "mcp_stdio_example.py"

mcp_servers=[
    MCPServerStdio(
        executable_path=sys.executable,
        process_arguments=[str(mcp_script)],
        session_timeout=30
    )
]
```

### 2. HTTP Transport (MCPServerHTTP)
For remote service communication:

```python
from videosdk.agents import MCPServerHTTP

mcp_servers=[
    MCPServerHTTP(
        endpoint_url="https://your-mcp-server.com/api/mcp",
        session_timeout=30
    )
]
```

### 3. Multiple MCP Servers
You can use both transport types simultaneously:

```python
mcp_servers=[
    MCPServerStdio(
        executable_path=sys.executable,
        process_arguments=[str(mcp_script)],
        session_timeout=30
    ),
    MCPServerHTTP(
        endpoint_url="https://mcp.zapier.com/api/mcp/s/your-server-id",
        session_timeout=30
    )
]
```

## 🛠️ Usage in Agent Classes

Include MCP servers in your agent initialization:

```python
class MyVoiceAgent(Agent):
    def __init__(self):
        mcp_script = Path(__file__).parent.parent / "MCP Server" / "mcp_stdio_example.py"
        super().__init__(
            instructions="Your agent instructions here",
            tools=[your_custom_tools],
            mcp_servers=[
                MCPServerStdio(
                    executable_path=sys.executable,
                    process_arguments=[str(mcp_script)],
                    session_timeout=30
                )
            ]
        )
```

## 📋 Installation Requirements

To use MCP with VideoSDK agents, ensure you have:

```bash
pip install fastmcp  # For creating MCP servers
pip install videosdk-agents  # VideoSDK agents with MCP support
```

## 🔧 Transport Types

### STDIO Transport
- **Use case**: Local integrations, executable_path-line tools, shell scripts
- **Security**: Process-level isolation
- **Performance**: Low latency, direct process communication
- **Best for**: Development, testing, local services

### HTTP Transport  
- **Use case**: Remote services, web APIs, cloud integrations
- **Security**: Requires proper authentication and HTTPS
- **Performance**: Network dependent
- **Best for**: Production services, third-party integrations

## 🤝 Examples in Action

Check out the working examples in:
- `../OpenAI/openai_agent_quickstart.py`
- `../Google Gemini (LiveAPI)/gemini_agent_quickstart.py` 
- `../AWS Nova Sonic/aws_novasonic_agent_quickstart.py`

Each example demonstrates MCP integration with different Plugins.
For More Infromation, see the [official VideoSDK MCP documentation](https://docs.videosdk.live/ai_agents/mcp-integration).


---

🤝 Need help? Join our [Discord community](https://discord.com/invite/f2WsNDN9S5).

Made with ❤️ by the [VideoSDK](https://videosdk.live) Team 