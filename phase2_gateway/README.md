# Phase 2: Creating an MCP Gateway

> **Author**: Madhushanka ([stmadhushanka067@gmail.com](mailto:stmadhushanka067@gmail.com))  
> **Tutorial Reference**: [MCP Full Course For Beginners](https://www.youtube.com/watch?v=io02ZM0ADqM&t=11955s) (Timestamp `3:19:15`)

This phase implements the architecture covered at **timestamp 3:19:15 ("Creating MCP Gateway")** of the tutorial.

---

## 1. What is an MCP Gateway?

In real-world enterprise or multi-tool setups, an AI client (Claude, Cursor, custom agents) often needs access to tools distributed across dozens of separate MCP servers (database servers, file system servers, weather/API servers, code runners, etc.).

Configuring 10+ separate MCP connections inside client config files leads to:
- High client-side resource consumption
- Cumbersome configuration maintenance
- Potential tool name conflicts
- Lack of centralized logging, access control, and telemetry

An **MCP Gateway** acts as a reverse-proxy and multiplexer:
1. Sits between the AI client and downstream MCP servers
2. Aggregates tool catalogs from all registered downstream servers
3. Routes tool execution calls dynamically to the target backend
4. Provides centralized monitoring and health-checks

```text
+------------------------+
|    AI Client (Claude)  |
+-----------+------------+
            | (STDIO or SSE)
            v
+------------------------+
|      MCP Gateway       |  <--- Aggregates tools & handles routing
+-----+------------+-----+
      |            |
      v            v
+------------+ +------------+
| Downstream | | Downstream |
|   MCP #1   | |   MCP #2   |
+------------+ +------------+
```

---

## 2. Gateway Implementation Details

- **`phase2_gateway/gateway.py`**:
  - Registers downstream MCP servers in `DOWNSTREAM_SERVERS`
  - Exposes `gateway_health`: Returns health status and registered servers
  - Exposes `list_all_gateway_tools`: Queries all downstream servers and returns their tools
  - Exposes `invoke_downstream_tool`: Dynamically connects to the target downstream server and runs the tool

---

## 3. Running and Testing the Gateway

Run the automated test script:
```bash
python phase2_gateway/test_gateway.py
```

This verifies:
1. Gateway startup and handshake
2. Health check inspection
3. Tool aggregation across downstream servers
4. Routing and proxying tool invocation (`core -> add_numbers`)
