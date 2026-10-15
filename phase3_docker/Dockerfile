# ============================================================================
# Phase 3: Production Dockerfile for MCP Server
# Supports both STDIO (interactive container for Claude Desktop) and SSE transports
# ============================================================================

FROM python:3.12-slim

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1

# Copy dependency definition
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install the package and its dependencies using uv
RUN uv pip install --system -e .

# Expose port for SSE transport
EXPOSE 8000

# Default command: STDIO transport
# Can be overridden at runtime, e.g.:
#   docker run -p 8000:8000 mcp-pypi-server mcp-pypi --transport sse --host 0.0.0.0 --port 8000
ENTRYPOINT ["mcp-pypi"]
CMD ["--transport", "stdio"]
