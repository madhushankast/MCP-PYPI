"""
Phase 1 Client Test Script
Demonstrates connecting to the packaged MCP server via stdio transport,
discovering tools/resources, and calling them (matching the 2:36:51 tutorial).
"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_client_test():
    print("==================================================")
    print("Testing MCP-PYPI Server via stdio client")
    print("==================================================")

    # Launch server as a subprocess via standard input/output
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_pypi.main", "--transport", "stdio"],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # 1. Initialize session
            init_result = await session.initialize()
            print(f"[OK] Server initialized: {init_result.serverInfo.name} (version: {init_result.serverInfo.version})")

            # 2. List tools
            tools_response = await session.list_tools()
            tool_names = [t.name for t in tools_response.tools]
            print(f"[OK] Tools discovered ({len(tool_names)}): {tool_names}")

            # 3. Call tool: add(a=12, b=28)
            print("\n--- Testing Tool: add(a=12, b=28) ---")
            add_res = await session.call_tool("add", arguments={"a": 12, "b": 28})
            print(f"Result: {add_res.content[0].text}")

            # 4. Call tool: subtract(a=50, b=20)
            print("\n--- Testing Tool: subtract(a=50, b=20) ---")
            sub_res = await session.call_tool("subtract", arguments={"a": 50, "b": 20})
            print(f"Result: {sub_res.content[0].text}")

            # 5. Call tool: multiply(a=6, b=7)
            print("\n--- Testing Tool: multiply(a=6, b=7) ---")
            mul_res = await session.call_tool("multiply", arguments={"a": 6, "b": 7})
            print(f"Result: {mul_res.content[0].text}")

            # 6. Call tool: divide(a=100.0, b=4.0)
            print("\n--- Testing Tool: divide(a=100.0, b=4.0) ---")
            div_res = await session.call_tool("divide", arguments={"a": 100.0, "b": 4.0})
            print(f"Result: {div_res.content[0].text}")

            # 7. Read resource: greeting
            print("\n--- Testing Resource: greeting://Alice ---")
            greeting_res = await session.read_resource("greeting://Alice")
            print(f"Resource Content: {greeting_res.contents[0].text}")

    print("\n==================================================")
    print("All Phase 1 tests passed successfully!")
    print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_client_test())
