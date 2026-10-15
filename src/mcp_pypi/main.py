"""
Main MCP Server implementation as demonstrated at 2:36:51 ("Deploy MCP to PyPI").
Provides FastMCP tools, resources, and CLI entrypoint for PyPI distribution.
"""

import sys
import argparse
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("mcp-pypi-server")


# ============================================================================
# Tools (Tutorial Implementation)
# ============================================================================

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers together.

    Args:
        a: First number
        b: Second number
    """
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a.

    Args:
        a: First number
        b: Second number to subtract
    """
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: First number
        b: Second number
    """
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide a by b.

    Args:
        a: Numerator
        b: Denominator (non-zero)
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b


# ============================================================================
# Resources
# ============================================================================

@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Personalized dynamic greeting resource.

    Args:
        name: Name to greet
    """
    return f"Hello, {name}! Welcome to the MCP server."


# ============================================================================
# CLI Entrypoint for PyPI
# ============================================================================

def main():
    """Main CLI entrypoint executed when running 'mcp-pypi'."""
    parser = argparse.ArgumentParser(description="MCP PyPI Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol (stdio or sse). Default is stdio."
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address for SSE transport (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for SSE transport (default: 8000)"
    )

    args = parser.parse_args()

    if args.transport == "sse":
        print(f"Starting MCP server on SSE at http://{args.host}:{args.port}...", file=sys.stderr)
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="sse")
    else:
        # Runs on STDIO by default (for Claude Desktop, Cursor, uvx, etc.)
        mcp.run()


if __name__ == "__main__":
    main()
