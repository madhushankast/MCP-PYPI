# MCP PyPI: Model Context Protocol Server Package

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.30+-purple.svg)](https://modelcontextprotocol.io/)
[![Build System](https://img.shields.io/badge/build-hatchling-orange.svg)](https://github.com/pypa/hatch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol (MCP) server packaged and structured for distribution on the Python Package Index (**PyPI**), as covered in the tutorial section **[2:36:51 - Deploy MCP to PyPI](https://www.youtube.com/watch?v=io02ZM0ADqM&t=9411s)**.

---

## 📁 Project Structure

```text
MCP-PYPI/
├── pyproject.toml              # PEP 621 packaging metadata & CLI executable definition
├── README.md                   # Package documentation (displayed on PyPI)
├── .gitignore                  # Git ignore rules
├── .github/
│   └── workflows/
│       └── publish.yml         # Automated GitHub Actions workflow to publish on release
└── src/
    └── mcp_pypi/
        ├── __init__.py         # Package exports & version
        ├── main.py             # FastMCP server with tools, resources, and CLI entrypoint
        └── server.py           # Module alias
```

---

## 🛠️ Implemented Tools & Resources

### Tools
- `add(a: int, b: int) -> int`: Adds two integers together.
- `subtract(a: int, b: int) -> int`: Subtracts `b` from `a`.
- `multiply(a: int, b: int) -> int`: Multiplies two integers.
- `divide(a: float, b: float) -> float`: Divides `a` by `b` (with zero division check).

### Resources
- `greeting://{name}`: Dynamic personalized greeting resource.

---

## 🚀 Quickstart: Local Setup & Testing

### 1. Clone the Repository
```bash
git clone https://github.com/madhushankast/MCP-PYPI.git
cd MCP-PYPI
```

### 2. Create Virtual Environment & Install Locally
Using [`uv`](https://github.com/astral-sh/uv) (recommended):
```powershell
uv venv --python 3.13
.venv\Scripts\activate
uv pip install -e .
```

Or using standard `pip`:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -e .
```

### 3. Verify the CLI Command
The command `mcp-pypi` is installed directly into your environment:
```bash
mcp-pypi --help
```

### 4. Test with the MCP Inspector
To test tools and resources visually in your browser:
```bash
uv run mcp dev src/mcp_pypi/main.py
```

---

## 📦 How to Build and Deploy to PyPI (2:36:51 Tutorial Workflow)

### Step 1: Configure Package Name
In `pyproject.toml`, make sure the `name` field is unique on PyPI:
```toml
[project]
name = "mcp-pypi-madhushankast"
version = "0.1.0"
```

### Step 2: Build the Distribution Archives
Run the build command from the project root:
```bash
uv build
```
*(Or with pip: `python -m build`)*

This compiles your package into two files in `dist/`:
- `dist/mcp_pypi_madhushankast-0.1.0-py3-none-any.whl` (built wheel)
- `dist/mcp_pypi_madhushankast-0.1.0.tar.gz` (source tarball)

### Step 3: Publish to TestPyPI (Recommended First)
1. Create an account and API token on [https://test.pypi.org/](https://test.pypi.org/).
2. Upload using `uv`:
   ```bash
   uv publish --publish-url https://test.pypi.org/legacy/
   ```
   - **Username**: `__token__`
   - **Password**: `<your-testpypi-api-token>`

*(Or using Twine: `twine upload --repository testpypi dist/*`)*

### Step 4: Publish to Production PyPI
1. Create an account and API token on [https://pypi.org/](https://pypi.org/).
2. Upload using `uv`:
   ```bash
   uv publish
   ```
   - **Username**: `__token__`
   - **Password**: `<your-pypi-api-token>`

*(Or using Twine: `twine upload dist/*`)*

---

## ⚡ Using Your Published MCP Server

### 1. Instant Run with `uvx` (Zero Install)
Once published on PyPI, anyone can run your server with a single command without cloning:
```bash
uvx mcp-pypi-madhushankast
```

### 2. Configure in Claude Desktop or Cursor
Add the server to your `claude_desktop_config.json`:

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

Or for local development:
```json
{
  "mcpServers": {
    "mcp-pypi-local": {
      "command": "mcp-pypi"
    }
  }
}
```

---

## 📝 License & Author
- **Author**: Madhushanka (<stmadhushanka067@gmail.com>)
- **Repository**: [https://github.com/madhushankast/MCP-PYPI](https://github.com/madhushankast/MCP-PYPI)
- **Tutorial Reference**: [MCP Full Course For Beginners](https://www.youtube.com/watch?v=io02ZM0ADqM&t=9411s) (Timestamp `2:36:51`)
- **License**: MIT
