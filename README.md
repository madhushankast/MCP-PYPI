# Model Context Protocol (MCP) Server & PyPI Deployment

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.30+-purple.svg)](https://modelcontextprotocol.io/)
[![Build System](https://img.shields.io/badge/build-uv%20%2F%20hatchling-orange.svg)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready Model Context Protocol (MCP) server package demonstrating end-to-end building, testing, packaging for PyPI, gateway multiplexing, and Docker containerization.

---

## 📑 Table of Contents
- [Project Architecture](#-project-architecture)
- [Tools & Resources Catalog](#-tools--resources-catalog)
- [Step 1: Clone the Repository](#step-1-clone-the-repository)
- [Step 2: Environment Setup with uv](#step-2-environment-setup-with-uv)
- [Step 3: Run & Test Locally](#step-3-run--test-locally)
- [Step 4: Package & Deploy to PyPI (Phase 1)](#step-4-package--deploy-to-pypi-phase-1)
- [Step 5: Run the MCP Gateway (Phase 2)](#step-5-run-the-mcp-gateway-phase-2)
- [Step 6: Deploy with Docker (Phase 3)](#step-6-deploy-with-docker-phase-3)
- [Step 7: Connect to AI Clients (Claude Desktop / Cursor)](#step-7-connect-to-ai-clients-claude-desktop--cursor)
- [Troubleshooting & FAQs](#-troubleshooting--faqs)
- [License & Author](#-license--author)

---

## 📁 Project Architecture

```text
MCP-PYPI/
├── pyproject.toml                     # PEP 621 packaging metadata & CLI executable
├── README.md                          # Complete setup and user guide
├── .dockerignore
├── .gitignore
├── .github/
│   └── workflows/
│       └── publish.yml                # Automated CI/CD GitHub Actions PyPI publishing
├── src/
│   └── mcp_pypi/
│       ├── __init__.py                # Package exports and version
│       ├── main.py                    # Core FastMCP Server (Tools, Resources, CLI)
│       └── server.py                  # Module re-export
├── phase1_pypi/
│   ├── test_client.py                 # Automated stdio client test script
│   ├── publish.py                     # Interactive publishing helper for TestPyPI / PyPI
│   └── README.md                      # PyPI packaging deep-dive
├── phase2_gateway/
│   ├── gateway.py                     # MCP Gateway multiplexer implementation
│   ├── test_gateway.py                # Gateway test client validating routing
│   └── README.md                      # Gateway architecture explanation
├── phase3_docker/
│   ├── Dockerfile                     # Multi-stage production container
│   ├── docker-compose.yml             # Orchestration for background SSE service
│   └── README.md                      # Docker STDIO and SSE execution guide
└── Agentic_terminal/
    ├── agentic_terminal.py            # Interactive CLI agent executing MCP tools
    ├── langchain_agent.py             # LangChain agent integration
    └── README.md                      # Agentic Terminal user guide
```

---

## 🛠️ Tools & Resources Catalog

### Tools
| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `add` | `a: int, b: int` | Adds two integers together |
| `subtract` | `a: int, b: int` | Subtracts `b` from `a` |
| `multiply` | `a: int, b: int` | Multiplies two integers |
| `divide` | `a: float, b: float` | Divides `a` by `b` (with zero-division validation) |

### Resources
| Resource URI | Description |
| :--- | :--- |
| `greeting://{name}` | Returns a personalized dynamic greeting message |

---

## Step 1: Clone the Repository

Clone the project to your local machine:

```bash
git clone https://github.com/madhushankast/MCP-PYPI.git
cd MCP-PYPI
```

---

## Step 2: Environment Setup with uv

We recommend using [uv](https://github.com/astral-sh/uv) for fast, reproducible Python dependency management.

### Windows (PowerShell):
```powershell
# 1. Create a virtual environment using Python 3.10+
uv venv --python 3.13

# 2. Activate the virtual environment
.venv\Scripts\activate

# 3. Install the package in editable mode with dependencies
uv pip install -e .
```

### macOS / Linux (Bash):
```bash
# 1. Create a virtual environment
uv venv --python 3.12

# 2. Activate the virtual environment
source .venv/bin/activate

# 3. Install the package in editable mode
uv pip install -e .
```

---

## Step 3: Run & Test Locally

### 1. Verify the CLI Command
Once installed, the CLI command `mcp-pypi` is available in your environment:
```bash
mcp-pypi --help
```

### 2. Inspect with the MCP Inspector
To interactively test your tools and resources in a browser UI:
```bash
uv run mcp dev src/mcp_pypi/main.py
```
This opens the official MCP Inspector web dashboard to call tools and inspect payloads.

### 3. Run the Automated Python Client Test
Run the client test script to verify STDIO communication, tool execution, and resource reading:
```bash
python phase1_pypi/test_client.py
```
**Expected Output:**
```text
==================================================
Testing MCP-PYPI Server via stdio client
==================================================
[OK] Server initialized: mcp-pypi-server (version: 1.30.0)
[OK] Tools discovered (4): ['add', 'subtract', 'multiply', 'divide']

--- Testing Tool: add(a=12, b=28) ---
Result: 40

--- Testing Tool: subtract(a=50, b=20) ---
Result: 30

--- Testing Tool: multiply(a=6, b=7) ---
Result: 42

--- Testing Tool: divide(a=100.0, b=4.0) ---
Result: 25.0

--- Testing Resource: greeting://Alice ---
Resource Content: Hello, Alice! Welcome to the MCP server.

==================================================
All Phase 1 tests passed successfully!
==================================================
```

---

## Step 4: Package & Deploy to PyPI (Phase 1)

### 1. Build Distribution Packages
Build standard Python wheel (`.whl`) and source tarball (`.tar.gz`):
```bash
uv build
```
The output artifacts are saved in `dist/`:
- `dist/mcp_pypi_madhushankast-0.1.0-py3-none-any.whl`
- `dist/mcp_pypi_madhushankast-0.1.0.tar.gz`

### 2. Publish to TestPyPI (Recommended First Step)
Test your package upload without affecting production PyPI:
```bash
uv publish --publish-url https://test.pypi.org/legacy/
```
- **Username**: `__token__`
- **Password**: `<your-testpypi-api-token>`

Or run the interactive helper:
```bash
python phase1_pypi/publish.py --target testpypi
```

### 3. Publish to Official PyPI
```bash
uv publish
```
- **Username**: `__token__`
- **Password**: `<your-pypi-api-token>`

### 4. Run Directly via `uvx` (Zero-Install Execution)
Once published to PyPI, anyone can run your MCP server without manually cloning or installing:
```bash
uvx mcp-pypi-madhushankast
```

---

## Step 5: Run the MCP Gateway (Phase 2)

An **MCP Gateway** acts as a central proxy and multiplexer. Instead of connecting an AI client to 10 separate servers, the client connects to a single Gateway that aggregates and routes tool calls to downstream backends.

### Run the Gateway Test:
```bash
python phase2_gateway/test_gateway.py
```
This demonstrates:
1. Health-checking registered downstream servers.
2. Aggregating tool catalogs from multiple backends into a unified schema.
3. Dynamically routing tool execution (e.g. `gateway -> core -> add`).

---

## Step 6: Deploy with Docker (Phase 3)

### 1. Build the Docker Image
```bash
docker build -f phase3_docker/Dockerfile -t mcp-pypi-server:latest .
```

### 2. Interactive STDIO Mode (For Claude Desktop / Cursor)
```bash
docker run -i --rm mcp-pypi-server:latest --transport stdio
```

### 3. SSE Background Service (With Docker Compose)
To run the server as a persistent HTTP/SSE microservice on port 8000:
```bash
cd phase3_docker
docker compose up -d
```
The SSE endpoint will be active at:
`http://localhost:8000/sse`

To stop:
```bash
docker compose down
```

---

## Step 7: Connect to AI Clients (Claude Desktop / Cursor)

Add the server configuration to your `claude_desktop_config.json` (located at `%APPDATA%\Claude\claude_desktop_config.json` on Windows or `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

### Option A: Local Cloned Repository (Using `uv`)
```json
{
  "mcpServers": {
    "mcp-pypi-local": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\Projects\\MCP PYPI",
        "run",
        "mcp-pypi"
      ]
    }
  }
}
```

### Option B: PyPI Package via `uvx` (Once Published)
```json
{
  "mcpServers": {
    "mcp-pypi": {
      "command": "uvx",
      "args": ["mcp-pypi-madhushankast"]
    }
  }
}
```

### Option C: Docker Container
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

---

## ❓ Troubleshooting & FAQs

### 1. `Cannot find module mcp.server.mcpserver`
- **Cause**: MCP 2.x renamed `FastMCP` to `MCPServer`.
- **Solution**: This project pins `mcp>=1.3.0,<2.0.0` where `from mcp.server.fastmcp import FastMCP` is standard. Always install using `uv pip install -e .`.

### 2. Docker container terminates immediately in Claude Desktop
- **Cause**: Missing `-i` (interactive) flag.
- **Solution**: Ensure your args include `"-i"`, as MCP relies on standard input/output streaming.

### 3. 403 Forbidden when uploading to PyPI
- **Cause**: The package name is already claimed by someone else on PyPI.
- **Solution**: Update the `name` field in `pyproject.toml` to a globally unique name (e.g. `mcp-pypi-<your-username>`).

---

## 📝 License & Author
- **Author**: Madhushanka (<stmadhushanka067@gmail.com>)
- **Repository**: [https://github.com/madhushankast/MCP-PYPI](https://github.com/madhushankast/MCP-PYPI)
- **License**: MIT
