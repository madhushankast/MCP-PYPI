# Phase 1: Deploying MCP Server to PyPI

> **Author**: Madhushanka ([stmadhushanka067@gmail.com](mailto:stmadhushanka067@gmail.com))  
> **Tutorial Reference**: [MCP Full Course For Beginners](https://www.youtube.com/watch?v=io02ZM0ADqM&t=9411s) (Timestamp `2:36:51`)

This phase covers everything demonstrated in the tutorial from **timestamp 2:36:51 ("Deploy MCP to PyPI")**:

1. Package Architecture and `pyproject.toml`
2. CLI Executable Entrypoints (`[project.scripts]`)
3. Building Wheels & Source Tarballs
4. Publishing to PyPI and TestPyPI
5. Configuring AI Clients (Claude Desktop, Cursor, Antigravity) with the published package

---

## 1. Project Architecture

To make an MCP server installable and executable anywhere via `uvx` or `pip`, it uses the standard `src/` layout:

```text
MCP-PYPI/
├── pyproject.toml              # Build config, package metadata, dependencies
├── README.md                   # Long description shown on PyPI page
├── src/
│   └── mcp_pypi/
│       ├── __init__.py         # Package version and exports
│       └── server.py           # FastMCP server, tools, resources, prompts, CLI
└── phase1_pypi/
    ├── test_client.py          # Native client test
    ├── publish.py              # Publishing helper
    └── README.md               # Phase guide
```

---

## 2. Key `pyproject.toml` Configuration

Notice how the command `mcp-pypi` is registered:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "mcp-pypi-server"        # Note: If publishing to PyPI, choose a globally unique name!
version = "0.1.0"
dependencies = [
    "mcp[cli]>=1.3.0,<2.0.0",
    "httpx>=0.27.0",
    "pydantic>=2.0.0",
]

[project.scripts]
mcp-pypi = "mcp_pypi.server:main"

[tool.hatch.build.targets.wheel]
packages = ["src/mcp_pypi"]
```

When a user runs `uvx mcp-pypi-server` or `pip install mcp-pypi-server`, the binary `mcp-pypi` is placed directly in their PATH.

---

## 3. Step-by-Step Build & Test

### Step A: Test Local Installation in Editable Mode
```bash
uv pip install -e .
mcp-pypi --help
```

### Step B: Test the MCP Server with the Native Client
```bash
python phase1_pypi/test_client.py
```

### Step C: Build Distribution Artifacts
```bash
uv build
```
This generates `dist/mcp_pypi_server-0.1.0-py3-none-any.whl` and `.tar.gz`.

---

## 4. Publishing to PyPI

### Option 1: Test on TestPyPI First (Recommended)
1. Register an account on [https://test.pypi.org/](https://test.pypi.org/)
2. Create an API token under **Account Settings -> API tokens**
3. Run the helper:
   ```bash
   python phase1_pypi/publish.py --target testpypi
   ```
   Or directly via `uv`:
   ```bash
   uv publish --publish-url https://test.pypi.org/legacy/
   ```
   - Username: `__token__`
   - Password: `<your-testpypi-token>`

### Option 2: Publish to Official PyPI
1. Register on [https://pypi.org/](https://pypi.org/)
2. In `pyproject.toml`, ensure your package name is unique (e.g. `mcp-pypi-server-<your-username>`).
3. Run:
   ```bash
   python phase1_pypi/publish.py --target pypi
   ```
   Or directly:
   ```bash
   uv publish
   ```

---

## 5. Integrating with Claude Desktop / Cursor

Once published, you and anyone else can add the server to `claude_desktop_config.json`:

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

Or for local development:
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
