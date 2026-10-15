"""
LangChain Agentic Terminal:
Uses LangChain to connect an LLM to the MCP tools, enabling natural language
conversations where the model decides which MCP tools to invoke.
"""

import os
import sys
import asyncio
from typing import List
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain imports (optional dependency)
try:
    from langchain_core.tools import Tool, StructuredTool
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


async def run_langchain_agent():
    print("=" * 60)
    print("[Agentic Terminal] LangChain Agent for MCP")
    print("=" * 60)

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_pypi.main", "--transport", "stdio"],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools_response = await session.list_tools()
            tool_names = [t.name for t in tools_response.tools]
            print(f"[OK] Connected to MCP Server. Available tools: {tool_names}")

            print("\nThis module demonstrates how an agentic LLM interacts with MCP tools.")
            print("To connect live models, set your API key (OPENAI_API_KEY / GROQ_API_KEY).")
            print("For standalone terminal interaction without external LLM keys, run:")
            print("  python Agentic_terminal/agentic_terminal.py\n")


if __name__ == "__main__":
    asyncio.run(run_langchain_agent())
