# Agentic Terminal for MCP

The **Agentic Terminal** is the interactive command-line environment demonstrated in the video tutorial (around timestamps `1:01:00` to `1:55:07`).

---

## 🎯 Purpose

Instead of relying solely on GUI desktop apps (like Claude Desktop), the **Agentic Terminal** allows you to:
1. Connect directly to your local or deployed MCP server over STDIO.
2. Dynamically introspect all registered tools and resources.
3. Call tools interactively using natural commands or conversational agents.
4. Integrate with frameworks like LangChain for autonomous agent tool execution.

---

## 🚀 How to Run the Agentic Terminal

From the root directory:

```bash
python Agentic_terminal/agentic_terminal.py
```

### Available Commands in the Interactive REPL:
- `add <a> <b>`: Invokes the `add` tool (e.g. `add 15 30`)
- `subtract <a> <b>`: Invokes the `subtract` tool (e.g. `subtract 80 25`)
- `multiply <a> <b>`: Invokes the `multiply` tool (e.g. `multiply 7 8`)
- `divide <a> <b>`: Invokes the `divide` tool (e.g. `divide 100 5`)
- `greeting <name>`: Reads the dynamic greeting resource (e.g. `greeting Developer`)
- `tools`: Lists all discovered tools and their descriptions
- `exit` or `quit`: Closes the terminal session

---

## 🧠 LangChain Agent Integration

To run the LangChain agent demonstration:

```bash
python Agentic_terminal/langchain_agent.py
```
