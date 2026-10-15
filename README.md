# MCP-PYPI: Model Context Protocol Server (Deployment & Packaging Masterclass)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.30+-purple.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Implementation of the advanced deployment phases of the Model Context Protocol (MCP):
- **Phase 1: Deploy MCP to PyPI**
- **Phase 2: Creating an MCP Gateway**
- **Phase 3: Deploy MCP Server with Docker**

---

## 📁 Repository Structure

```text
MCP-PYPI/
├── pyproject.toml                     # PEP 621 packaging metadata & CLI entrypoint
├── README.md                          # Project documentation
├── .dockerignore
├── .github/
│   └── workflows/
│       └── publish.yml                # Automated CI/CD PyPI publishing workflow
├── src/
│   └── mcp_pypi/
│       ├── __init__.py                # Package version and exports
│       └── server.py                  # Production FastMCP server (Tools, Resources, Prompts)
├── phase1_pypi/
│   ├── test_client.py                 # Client test script for verifying STDIO server
│   ├── publish.py                     # Interactive publishing helper for PyPI/TestPyPI
│   └── README.md                      # Comprehensive PyPI guide
├── phase2_gateway/
│   ├── gateway.py                     # MCP Gateway multiplexer implementation
│   ├── test_gateway.py                # Gateway aggregation and routing test client
│   └── README.md                      # Architecture and usage guide for Gateways
└── phase3_docker/
    ├── Dockerfile                     # Multi-stage production container
    ├── docker-compose.yml             # Service orchestration for SSE transport
    └── README.md                      # Docker STDIO and SSE execution guide
```

---

## ⚡ Quickstart

### 1. Prerequisites
- [uv](https://github.com/astral-sh/uv) (recommended) or Python 3.10+
- Git

### 2. Setup Virtual Environment & Dependencies
```powershell
uv venv --python 3.13
.venv\Scripts\activate
uv pip install -e .
```

---

## 🚀 Phase-by-Phase Implementation

### [Phase 1: PyPI Packaging & Deployment](phase1_pypi/README.md)
*Covers packaging into wheels, defining CLI entry points, and uploading to PyPI.*

1. **Test Server locally via client:**
   ```powershell
   python phase1_pypi/test_client.py
   ```
2. **Build Distribution Archives:**
   ```powershell
   uv build
   ```
3. **Publish to TestPyPI / PyPI:**
   ```powershell
   python phase1_pypi/publish.py --target testpypi
   ```

---

### [Phase 2: MCP Gateway Multiplexer](phase2_gateway/README.md)
*Covers proxying, aggregating catalogs across multiple downstream MCP servers, and dynamic routing.*

1. **Run and Test the Gateway:**
   ```powershell
   python phase2_gateway/test_gateway.py
   ```
   *Aggregates tools across downstream servers and dispatches execution calls centrally.*

---

### [Phase 3: Docker Deployment](phase3_docker/README.md)
*Covers containerizing the MCP server for both STDIO streaming and HTTP/SSE.*

1. **Build the container:**
   ```powershell
   docker build -f phase3_docker/Dockerfile -t mcp-pypi-server:latest .
   ```
2. **Run interactively via STDIO (for Claude Desktop / Cursor):**
   ```powershell
   docker run -i --rm mcp-pypi-server:latest --transport stdio
   ```
3. **Run as background SSE microservice:**
   ```powershell
   cd phase3_docker
   docker compose up -d
   ```

---

## 🤖 Connecting to Claude Desktop / Cursor

Add the following to your `claude_desktop_config.json`:

### Local Installation:
```json
{
  "mcpServers": {
    "mcp-pypi-local": {
      "command": "mcp-pypi",
      "args": ["--transport", "stdio"]
    }
  }
}
```

### Direct via `uvx` (Once published to PyPI):
```json
{
  "mcpServers": {
    "mcp-pypi": {
      "command": "uvx",
      "args": ["mcp-pypi-server"]
    }
  }
}
```

### Via Docker:
```json
{
  "mcpServers": {
    "mcp-docker": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-pypi-server:latest", "--transport", "stdio"]
    }
  }
}
```

---

## 🛠️ Provided Tools & Resources

### Available Tools:
- `add_numbers(a, b)`: Adds two numbers.
- `multiply_numbers(a, b)`: Multiplies two numbers.
- `get_system_info()`: Retrieves OS, CPU, platform, and runtime metadata.
- `format_text(text, mode)`: Formats strings (`uppercase`, `lowercase`, `title`, `reverse`).
- `get_weather(city)`: Simulates real-time weather lookup.

### Available Resources:
- `greeting://{name}`: Personalized dynamic greeting resource.
- `system://metrics`: Real-time system health and platform status.

### Available Prompts:
- `code-review`: Configured multi-point code audit prompt template.

---

## 📝 License & Author
- **Author**: Madhushanka (<stmadhushanka067@gmail.com>)
- **License**: MIT
