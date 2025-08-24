# OLAXBT MCP Gateway

A modern, modular MCP (Model Context Protocol) server with scalable service architecture, supporting multiple MCP services including DeFi, Gaming, and search tools.

## Features

- **Modular Service Architecture**: Plugin-based service loading and management
- **Service Registry**: Dynamic service discovery, registration, and health monitoring
- **Multiple Connection Types**: HTTP, SSE, WebSocket, and standard MCP protocol
- **Service Management**: Add, remove, enable/disable, and reload services dynamically
- **Built-in Tools**: DuckDuckGo search and enhanced web search
- **FastAPI Backend**: High-performance async web framework

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python run.py
```

## API Endpoints

### Core Endpoints
- `GET /` - Server information and status
- `GET /health` - Health check with service status
- `GET /services` - List all registered services
- `GET /tools` - List all available tools
- `GET /statistics` - Detailed service and tool statistics

### Service Management
- `POST /services/reload/{service_id}` - Reload a specific service
- `POST /services/load` - Load services from configuration
- `POST /services/add` - Add a new service dynamically
- `DELETE /services/{service_id}` - Remove a service
- `POST /services/{service_id}/enable` - Enable a disabled service
- `POST /services/{service_id}/disable` - Disable a service
- `GET /services/{service_id}/status` - Get detailed service status

### MCP Protocol Endpoints
- `POST /mcp` - Standard MCP endpoint (POST)
- `GET /mcp` - Standard MCP endpoint (SSE)
- `GET /sse` - Server-Sent Events endpoint
- `POST /api/mcp/olaxbt-gateway` - Custom MCP endpoint

### Legacy MCP Endpoints
- `POST /mcp/tools/list` - List all available tools
- `POST /mcp/tools/call` - Call a specific tool
- `POST /mcp/services/list` - List all available services

## Usage Examples

### List Services
```bash
curl http://localhost:3000/services
```

### List Tools
```bash
curl http://localhost:3000/tools
```

### Get Service Status
```bash
curl http://localhost:3000/services/meteora/status
```

### MCP Protocol Request
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

### Add New Service
```bash
curl -X POST http://localhost:3000/services/add \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Service",
    "description": "Custom service description",
    "url": "http://localhost:3003",
    "tools": ["my_tool"],
    "metadata": {"category": "custom"}
  }'
```

## Service Configuration

Services can be configured through:
- Configuration files
- Dynamic API calls
- Environment variables

## Architecture

```
Client → MCP Gateway → Service Manager → Service Registry
                    ↓
                Router → Local Tools
```

The server provides:
- **Service Manager**: Handles service lifecycle and configuration
- **Service Registry**: Manages service registration and health monitoring
- **Router**: Routes requests to appropriate services or local tools
- **Local Tools**: Built-in search and utility tools

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
3. **Run the server:** `uvicorn app.mcp.server:app --host 0.0.0.0 --port 3000`
4. **Set environment variables:**
   ```bash
   MCP_HOST=0.0.0.0
   MCP_PORT=3000
   MCP_DEBUG=false
   ```

## VSCode Integration

Add `.vscode/mcp.json` for HTTP or SSE connections:

```json
{
  "servers": {
    "olaxbt-mcp": {
      "url": "http://localhost:3000/mcp",
      "type": "http"
    }
  },
  "inputs": []
}
```

## Available Tools

### Local Tools
- `duckduckgo_search` - Web search using DuckDuckGo
- `web_search` - Enhanced search (text, news, images, videos)

### Service Tools
Tools are dynamically loaded from registered services and can include:
- DeFi protocols (Meteora, etc.)
- Gaming platforms (GMGN, etc.)
- Analytics services
- Custom integrations

## Project Structure

```
app/mcp/
├── server.py           # Main server with FastAPI
├── service_manager.py  # Service lifecycle management
├── router.py           # Request routing and MCP handling
├── config.py           # Configuration management
├── tools.py            # Local tool implementations
└── services/           # Service implementations
    ├── base_service.py # Base service class
    ├── meteora.py      # Meteora DeFi service
    └── gmgn.py         # GMGN Gaming service
```

## Requirements

- Python 3.8+
- FastAPI
- uvicorn
- duckduckgo-search
- aiohttp
- websockets
- pydantic

## License

This project is licensed under the MIT License. 