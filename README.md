# OLAXBT MCP Gateway

The OlaXBT MCP Server features a modular, scalable architecture designed to efficiently support multiple services. This new structure separates concerns, enables plugin-based service loading, and offers comprehensive service management capabilities.

## Features

- **MCP Gateway**: Central management for multiple MCP services
- **DuckDuckGo Integration**: Built-in web search capabilities
- **Service Registry**: Dynamic service discovery and registration
- **Tool Routing**: Automatic routing of tool calls to appropriate services
- **FastAPI Backend**: High-performance async web framework

## Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run locally:**
```bash
python run.py
```

## Deployment

Deploy to any server that supports Python applications:

1. **Upload your code to your server**
2. **Install dependencies:** `pip install -r requirements.txt`
3. **Run the server:** `uvicorn app.mcp.server:app --host 0.0.0.0 --port 8080`
4. **Set environment variables:**
   ```bash
   MCP_HOST=0.0.0.0
   MCP_PORT=8080
   MCP_DEBUG=false
   ```

## Client Connection in vscode

You can add .vscode/mcp.json by adding HTTP or SSE to a remote server, change localhost:3000 to your deployed address,

```json
{
	"servers": {
		"my-mcp-server": {
			"url": "http://localhost:3000/mcp",
			"type": "http"
		}
	},
	"inputs": []
}
```

## Tools for testing

- `duckduckgo_search` - Web search using DuckDuckGo
- `web_search` - Enhanced search (text, news, images, videos)

## Architecture

```
Client → MCP Gateway → [Service 1, Service 2, ..., Service N]
                    → Local Tools (DuckDuckGo, Web Search)
```

The server provides a unified interface for multiple MCP services while maintaining local tool capabilities. 