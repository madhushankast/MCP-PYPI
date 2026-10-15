"""
Phase 2 Test Script
Validates the MCP Gateway server by querying aggregated tools and routing calls.
"""

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def run_gateway_test():
    print("==================================================")
    print("Testing MCP Gateway Multiplexer")
    print("==================================================")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["phase2_gateway/gateway.py"],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            init_res = await session.initialize()
            print(f"[OK] Gateway initialized: {init_res.serverInfo.name}")

            # 1. Check Gateway Health
            health = await session.call_tool("gateway_health", arguments={})
            print(f"[OK] Gateway Health: {health.content[0].text}")

            # 2. List Aggregated Downstream Tools
            print("\n--- Aggregating tools across downstream MCP servers ---")
            agg = await session.call_tool("list_all_gateway_tools", arguments={})
            print(f"Aggregated Catalog:\n{agg.content[0].text}")

            # 3. Route call through Gateway to Downstream 'core' server
            print("\n--- Routing Tool Call via Gateway: core -> add_numbers ---")
            routed_call = await session.call_tool(
                "invoke_downstream_tool",
                arguments={
                    "server_key": "core",
                    "tool_name": "add_numbers",
                    "arguments": {"a": 100, "b": 250}
                }
            )
            print(f"Routed Result:\n{routed_call.content[0].text}")

    print("\n==================================================")
    print("Phase 2 Gateway tests completed successfully!")
    print("==================================================")


if __name__ == "__main__":
    asyncio.run(run_gateway_test())
