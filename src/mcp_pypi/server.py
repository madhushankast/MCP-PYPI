"""
Core MCP Server implementation for MCP-PYPI package.
Provides Tools, Resources, and Prompts via STDIO or SSE transports.
"""

import sys
import argparse
import platform
import datetime
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP(
    name="MCP-PYPI-Server",
    dependencies=["httpx", "pydantic"]
)


# ============================================================================
# 1. TOOLS
# ============================================================================

@mcp.tool()
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a + b


@mcp.tool()
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers.

    Args:
        a: First number
        b: Second number
    """
    return a * b


@mcp.tool()
def get_system_info() -> dict:
    """Retrieve current operating system and runtime metadata."""
    return {
        "platform": platform.platform(),
        "python_version": sys.version,
        "machine": platform.machine(),
        "processor": platform.processor(),
        "current_time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }


@mcp.tool()
def format_text(text: str, mode: str = "uppercase") -> str:
    """Format input text according to the selected mode.

    Args:
        text: Input string to format
        mode: Formatting mode ('uppercase', 'lowercase', 'title', 'reverse')
    """
    mode = mode.lower()
    if mode == "uppercase":
        return text.upper()
    elif mode == "lowercase":
        return text.lower()
    elif mode == "title":
        return text.title()
    elif mode == "reverse":
        return text[::-1]
    else:
        return f"Unknown mode '{mode}'. Choose from: uppercase, lowercase, title, reverse."


@mcp.tool()
def get_weather(city: str) -> dict:
    """Simulate getting live weather data for a given city.

    Args:
        city: The name of the city
    """
    city_normalized = city.strip().title()
    # Simulated weather data for demonstration
    mock_data = {
        "New York": {"temperature_c": 18, "condition": "Partly Cloudy", "humidity": "55%"},
        "London": {"temperature_c": 14, "condition": "Light Rain", "humidity": "80%"},
        "Tokyo": {"temperature_c": 22, "condition": "Clear", "humidity": "45%"},
        "Colombo": {"temperature_c": 30, "condition": "Tropical Sunny", "humidity": "78%"},
        "San Francisco": {"temperature_c": 16, "condition": "Foggy", "humidity": "70%"},
    }
    weather = mock_data.get(city_normalized, {
        "temperature_c": 20,
        "condition": "Sunny with clouds",
        "humidity": "60%",
        "note": "Default forecast simulation for this location"
    })
    return {
        "city": city_normalized,
        **weather,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }


# ============================================================================
# 2. RESOURCES
# ============================================================================

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Return a personalized dynamic greeting resource.

    Args:
        name: Name to greet
    """
    return f"Hello, {name}! Welcome to the MCP-PYPI server. The server is active and running."


@mcp.resource("system://metrics")
def get_metrics_resource() -> str:
    """Resource returning system health metrics in plaintext."""
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return f"Status: HEALTHY\nTime: {now}\nPlatform: {platform.system()} {platform.release()}"


# ============================================================================
# 3. PROMPTS
# ============================================================================

@mcp.prompt("code-review")
def code_review_prompt(language: str, code_snippet: str) -> str:
    """Generate a structured code review prompt template."""
    return f"""Please perform an in-depth code review on the following {language} snippet:

```{language}
{code_snippet}
```

Review criteria:
1. Logic correctness and potential bugs
2. Security vulnerabilities
3. Performance and complexity
4. Readability and idiomatic conventions
"""


# ============================================================================
# 4. ENTRY POINT
# ============================================================================

def main():
    """Main CLI entrypoint for MCP-PYPI."""
    parser = argparse.ArgumentParser(description="MCP-PYPI: Model Context Protocol Server")
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
        print(f"Starting MCP-PYPI server over SSE at http://{args.host}:{args.port}...", file=sys.stderr)
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="sse")
    else:
        # Default STDIO transport
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
