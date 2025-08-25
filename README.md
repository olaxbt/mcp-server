# OLAXBT MCP Server

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

### Tool Usage Examples

#### **Cryptocurrency Price Tool**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "crypto_price",
    "arguments": {
      "coin_id": "bitcoin",
      "vs_currency": "usd",
      "include_market_data": true,
      "include_24hr_change": true
    }
  }
}
```

#### **Portfolio Tracker Tool**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "portfolio_tracker",
    "arguments": {
      "action": "create",
      "portfolio_id": "my_portfolio",
      "name": "My Crypto Portfolio"
    }
  }
}
```

#### **DeFi Protocol Tool**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "defi_protocol",
    "arguments": {
      "protocol": "meteora",
      "action": "pools"
    }
  }
}
```

#### **Market Analysis Tool**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "market_analysis",
    "arguments": {
      "coin_id": "bitcoin",
      "analysis_type": "technical_indicators",
      "timeframe": "7d"
    }
  }
}
```

#### **APY Calculator Tool**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "apy_calculator",
    "arguments": {
      "calculation_type": "liquidity_pool",
      "protocol": "meteora",
      "principal": 10000,
      "time_period": 365
    }
  }
}
```

#### **NFT Marketplace Tool**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "nft_marketplace",
    "arguments": {
      "action": "collection_stats",
      "collection_slug": "bored-ape-yacht-club",
      "chain": "ethereum"
    }
  }
}
```

#### **NFT Floor Price**
```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "nft_marketplace",
    "arguments": {
      "action": "floor_price",
      "collection_slug": "degen-ape-academy",
      "chain": "solana"
    }
  }
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

3. **Test all tools:**
```bash
python scripts/test_tools.py
```

4. **Test NFT marketplace specifically:**
```bash
python scripts/test_nft_tool.py
```

5. **Test tools with real data implementations:**
```bash
python scripts/test_real_data_tools.py
```

This will run comprehensive tests for all implemented tools including:
- Cryptocurrency price data
- DeFi protocol interactions
- Portfolio tracking and analysis
- Crypto news aggregation
- NFT marketplace data (real API integrations)
- Market analysis and technical indicators (real-time data)
- Notification system (real market integration)
- APY calculations (real protocol data)

### Real Data Implementations

The following tools now use real APIs instead of hardcoded data:

- **MarketAnalysisTool**: Uses CoinGecko API for real-time price data, Fear & Greed Index API for sentiment, and calculates actual technical indicators
- **APYCalculatorTool**: Fetches real DeFi protocol data from CoinGecko and calculates APY with actual market rates
- **NotificationTool**: Integrates with CoinGecko API for real-time price checking and market summaries

All tools include comprehensive error handling and fallback to reasonable defaults when APIs are unavailable.

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

#### **Search & Information Tools**
- `duckduckgo_search` - Web search using DuckDuckGo
- `web_search` - Enhanced search (text, news, images, videos)
- `crypto_news` - Cryptocurrency-specific news aggregation with sentiment analysis

#### **Cryptocurrency & DeFi Tools**
- `crypto_price` - Real-time cryptocurrency prices and market data from CoinGecko
- `defi_protocol` - Interact with DeFi protocols (Meteora liquidity pools, Jupiter swap aggregator)
- `portfolio_tracker` - Track and analyze cryptocurrency portfolios with real-time pricing
- `apy_calculator` - Calculate APY using real DeFi protocol data:
  - Liquidity pool APY with impermanent loss estimates
  - Yield farming APY with compound interest calculations
  - Staking APY with real protocol data
  - Compound interest with monthly breakdowns
  - Real-time DeFi protocol data from CoinGecko

#### **NFT & Gaming Tools**
- `nft_marketplace` - Real-time NFT marketplace data from OpenSea, Magic Eden, and other major marketplaces
  - Collection information and statistics
  - Floor prices with 24h/7d changes
  - Trading volume and sales data
  - Recent sales with transaction details
  - Support for Ethereum, Solana, and Polygon chains

#### **Market Analysis Tools**
- `market_analysis` - Advanced market analysis with real-time data:
  - Technical indicators (RSI, MACD, Bollinger Bands, Moving Averages)
  - Trend analysis with momentum and key levels
  - Market sentiment using Fear & Greed Index and social metrics
  - Volatility analysis with risk metrics (VaR, Sharpe ratio, Sortino ratio)
  - Real-time data from CoinGecko API

#### **Utility Tools**
- `notification` - Set up and manage alerts with real market integration:
  - Price alerts with real-time CoinGecko price checking
  - News alerts for cryptocurrency and DeFi topics
  - Portfolio alerts with market summary data
  - Real-time market data integration for alert testing

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

## Environment Variables

For full functionality, set the following environment variables:

```bash
# NFT Marketplace APIs (optional but recommended)
OPENSEA_API_KEY=your_opensea_api_key_here
RESERVOIR_API_KEY=your_reservoir_api_key_here

# Server Configuration
MCP_HOST=0.0.0.0
MCP_PORT=3000
MCP_DEBUG=false
```

### Getting API Keys

1. **OpenSea API Key**: 
   - Visit [OpenSea API Documentation](https://docs.opensea.io/reference/api-overview)
   - Sign up for an API key at [OpenSea Developer Portal](https://docs.opensea.io/reference/api-overview#api-keys)

2. **Reservoir API Key** (optional):
   - Visit [Reservoir API Documentation](https://docs.reservoir.tools/)
   - Get an API key for enhanced Ethereum/Polygon data

**Note**: The NFT marketplace tool will work without API keys but with rate limits. API keys provide higher rate limits and better reliability.

## License

This project is licensed under the MIT License. 
