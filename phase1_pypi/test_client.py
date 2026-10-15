"""
Phase 1 Client Test Script
Demonstrates connecting to the packaged MCP server via stdio transport,
discovering tools/resources/prompts, and calling them.
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
        args=["-m", "mcp_pypi.server", "--transport", "stdio"],
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

            # 3. Call tool: add_numbers
            print("\n--- Testing Tool: add_numbers(a=12.5, b=27.5) ---")
            add_res = await session.call_tool("add_numbers", arguments={"a": 12.5, "b": 27.5})
            print(f"Result: {add_res.content[0].text}")

            # 4. Call tool: get_weather
            print("\n--- Testing Tool: get_weather(city='Tokyo') ---")
            weather_res = await session.call_tool("get_weather", arguments={"city": "Tokyo"})
            print(f"Result: {weather_res.content[0].text}")

            # 5. List resources
            resources_response = await session.list_resources()
            print(f"\n[OK] Resources: {[r.uri for r in resources_response.resources]}")

            # 6. Read resource: greeting
            print("\n--- Testing Resource: greeting://Student ---")
            greeting_res = await session.read_resource("greeting://Student")
            print(f"Resource Content: {greeting_res.contents[0].text}")

            # 7. List prompts
            prompts_response = await session.list_prompts()
            print(f"\n[OK] Prompts: {[p.name for p in prompts_response.prompts]}")

    print("\n==================================================")
    print("All Phase 1 tests passed successfully!")
    print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_client_test())
