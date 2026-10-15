"""
Server module for backward compatibility and additional tools.
Re-exports the core FastMCP server and tools from main.py.
"""

from mcp_pypi.main import mcp, add, subtract, multiply, divide, greeting, main

__all__ = ["mcp", "add", "subtract", "multiply", "divide", "greeting", "main"]

if __name__ == "__main__":
    main()
