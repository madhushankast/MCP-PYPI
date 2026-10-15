# Phase 3: Deploying MCP Server with Docker

This phase implements the deployment workflows demonstrated at **timestamp 3:31:12 ("Deploy MCP Server with Docker")** of the tutorial.

---

## 1. Why Dockerize an MCP Server?

1. **Portability**: Runs uniformly on macOS, Linux, and Windows without requiring local Python / virtual environments.
2. **Isolation & Security**: Tools executed by LLMs are contained inside the container.
3. **Versatility**: A single Docker image can be used either:
   - Interactively via **STDIO** (for Claude Desktop / Cursor)
   - As a continuous **SSE / HTTP microservice** (for web apps, LangChain, or remote gateways)

---

## 2. Building the Docker Image

From the project root (`MCP PYPI`):

```bash
docker build -f phase3_docker/Dockerfile -t mcp-pypi-server:latest .
```

---

## 3. Running with STDIO (Claude Desktop & Cursor)

To connect Claude Desktop to your Dockerized MCP server, add this to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-docker": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "mcp-pypi-server:latest",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

> **Note**: The `-i` (interactive) flag is critical because MCP stdio communication relies on streaming `stdin`/`stdout`.

---

## 4. Running as an SSE Service

### Option A: Using Docker Compose
```bash
cd phase3_docker
docker compose up -d
```
The server will now be live at:
`http://localhost:8000/sse`

To stop:
```bash
docker compose down
```

### Option B: Using Direct Docker Run
```bash
docker run -d --name mcp-sse -p 8000:8000 mcp-pypi-server:latest --transport sse --host 0.0.0.0 --port 8000
```
