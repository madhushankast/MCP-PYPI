"""
Phase 2: MCP Gateway Server
Demonstrates building an MCP Gateway that aggregates multiple downstream MCP servers
into a unified interface for AI clients (from tutorial timestamp 3:19:15).
"""

import sys
import asyncio
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# Initialize Gateway FastMCP server
gateway = FastMCP(
    name="MCP-Unified-Gateway",
    dependencies=["mcp", "pydantic", "httpx"]
)

# Registry of downstream MCP server configurations
DOWNSTREAM_SERVERS = {
    "core": {
        "command": sys.executable,
        "args": ["-m", "mcp_pypi.server", "--transport", "stdio"],
    }
}


# ============================================================================
# Gateway Native Tools & Routing
# ============================================================================

@gateway.tool()
def gateway_health() -> dict:
    """Check the health status of the Gateway and registered downstream services."""
    return {
        "gateway_status": "ONLINE",
        "registered_downstreams": list(DOWNSTREAM_SERVERS.keys()),
        "architecture": "Unified Multiplexing Gateway"
    }


@gateway.tool()
async def invoke_downstream_tool(server_key: str, tool_name: str, arguments: dict) -> dict:
    """Dynamically route and invoke a tool on a registered downstream MCP server.

    Args:
        server_key: Identifier of the downstream server (e.g. 'core')
        tool_name: The target tool to execute (e.g. 'get_weather', 'add_numbers')
        arguments: JSON dictionary of arguments to pass to the tool
    """
    if server_key not in DOWNSTREAM_SERVERS:
        return {
            "error": f"Downstream server '{server_key}' not found. Available: {list(DOWNSTREAM_SERVERS.keys())}"
        }

    config = DOWNSTREAM_SERVERS[server_key]
    server_params = StdioServerParameters(
        command=config["command"],
        args=config["args"],
        env=None
    )

    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=arguments)
                text_content = [c.text for c in result.content if hasattr(c, "text")]
                return {
                    "server": server_key,
                    "tool": tool_name,
                    "result": text_content[0] if text_content else "No text response",
                    "status": "success"
                }
    except Exception as e:
        return {
            "error": str(e),
            "server": server_key,
            "tool": tool_name,
            "status": "failed"
        }


@gateway.tool()
async def list_all_gateway_tools() -> dict:
    """Query and aggregate all tools from all registered downstream servers."""
    aggregated = {}
    for key, config in DOWNSTREAM_SERVERS.items():
        server_params = StdioServerParameters(
            command=config["command"],
            args=config["args"],
            env=None
        )
        try:
            async with stdio_client(server_params) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    tools_res = await session.list_tools()
                    aggregated[key] = [
                        {"name": t.name, "description": t.description}
                        for t in tools_res.tools
                    ]
        except Exception as e:
            aggregated[key] = f"Failed to connect: {str(e)}"

    return aggregated


# ============================================================================
# Entry Point
# ============================================================================

def main():
    print("Starting MCP Gateway on STDIO...", file=sys.stderr)
    gateway.run(transport="stdio")


if __name__ == "__main__":
    main()
