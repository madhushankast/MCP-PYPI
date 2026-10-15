"""
Agentic Terminal: Interactive Terminal Agent powered by MCP Tools.
Connects to the MCP server, discovers tools dynamically, and executes them
interactively from the command line interface.
"""

import os
import sys
import asyncio
from typing import Optional, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class AgenticTerminal:
    def __init__(self, server_script: Optional[str] = None):
        if server_script is None:
            # Default to the packaged mcp_pypi.main module
            self.server_args = ["-m", "mcp_pypi.main", "--transport", "stdio"]
        else:
            self.server_args = [server_script, "--transport", "stdio"]

        self.server_params = StdioServerParameters(
            command=sys.executable,
            args=self.server_args,
            env=None
        )
        self.session: Optional[ClientSession] = None
        self.tools: Dict[str, Any] = {}

    async def initialize(self):
        """Connect to MCP server and fetch available tools."""
        tools_resp = await self.session.list_tools()
        for t in tools_resp.tools:
            self.tools[t.name] = t
        print(f"\n[Agentic Terminal] Connected to MCP Server.")
        print(f"[Agentic Terminal] Available tools ({len(self.tools)}): {list(self.tools.keys())}")

    async def execute_tool(self, tool_name: str, args: dict) -> str:
        """Call a specific tool via MCP."""
        if tool_name not in self.tools:
            return f"[Error] Tool '{tool_name}' not found. Available: {list(self.tools.keys())}"

        try:
            result = await self.session.call_tool(tool_name, arguments=args)
            texts = [c.text for c in result.content if hasattr(c, "text")]
            return "\n".join(texts) if texts else "Success (no text content)"
        except Exception as e:
            return f"[Execution Error]: {str(e)}"

    async def run_repl(self):
        """Interactive Terminal Loop."""
        print("=" * 60)
        print("Welcome to the MCP Agentic Terminal")
        print("=" * 60)
        print("Type commands or tool calls in the format:")
        print("  add 10 25")
        print("  subtract 50 15")
        print("  multiply 6 7")
        print("  divide 100 4")
        print("  greeting <name>")
        print("  tools                     (list all available tools)")
        print("  exit or quit              (to stop)")
        print("=" * 60)

        while True:
            try:
                user_input = input("\nAgenticTerminal >> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting Agentic Terminal.")
                break

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break

            if user_input.lower() == "tools":
                print("\nAvailable Tools:")
                for name, t in self.tools.items():
                    print(f" - {name}: {t.description.strip() if t.description else 'No description'}")
                continue

            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd == "add" and len(parts) >= 3:
                try:
                    res = await self.execute_tool("add", {"a": int(parts[1]), "b": int(parts[2])})
                    print(f"Result: {res}")
                except ValueError:
                    print("[Error] Please provide two valid integers: add <a> <b>")

            elif cmd == "subtract" and len(parts) >= 3:
                try:
                    res = await self.execute_tool("subtract", {"a": int(parts[1]), "b": int(parts[2])})
                    print(f"Result: {res}")
                except ValueError:
                    print("[Error] Please provide two valid integers: subtract <a> <b>")

            elif cmd == "multiply" and len(parts) >= 3:
                try:
                    res = await self.execute_tool("multiply", {"a": int(parts[1]), "b": int(parts[2])})
                    print(f"Result: {res}")
                except ValueError:
                    print("[Error] Please provide two valid integers: multiply <a> <b>")

            elif cmd == "divide" and len(parts) >= 3:
                try:
                    res = await self.execute_tool("divide", {"a": float(parts[1]), "b": float(parts[2])})
                    print(f"Result: {res}")
                except ValueError:
                    print("[Error] Please provide two numbers: divide <a> <b>")

            elif cmd in ["greeting", "greet"] and len(parts) >= 2:
                name = parts[1]
                try:
                    res = await self.session.read_resource(f"greeting://{name}")
                    print(f"Greeting: {res.contents[0].text}")
                except Exception as e:
                    print(f"[Error reading resource]: {e}")

            else:
                print(f"[Unknown Command]: '{user_input}'. Type 'tools' to see available tools or 'exit' to quit.")


async def main():
    terminal = AgenticTerminal()
    async with stdio_client(terminal.server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            terminal.session = session
            await terminal.initialize()
            await terminal.run_repl()


if __name__ == "__main__":
    asyncio.run(main())
