"""
Polygon.io MCP Tool
Access real-time market data, news, and financial information from Polygon.io API
"""

import aiohttp
import json
import asyncio
from typing import Dict, Any, List, Optional
from .mcp_tool import MCPTool
import logging

logger = logging.getLogger(__name__)

class PolygonTool(MCPTool):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.polygon.io"
        self._session = None
    
    @property
    def name(self) -> str:
        return "polygon"
    
    @property
    def description(self) -> str:
        return "Access real-time market data, news, and financial information from Polygon.io API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_crypto_aggregates",
                        "get_crypto_previous_close",
                        "get_crypto_grouped_daily",
                        "get_crypto_trades",
                        "get_crypto_quotes",
                        "get_crypto_snapshot",
                        "get_crypto_news",
                        "get_stock_aggregates",
                        "get_stock_previous_close",
                        "get_stock_trades",
                        "get_stock_quotes",
                        "get_stock_snapshot",
                        "get_news"
                    ],
                    "description": "The action to perform"
                },
                "ticker": {
                    "type": "string",
                    "description": "Ticker symbol (e.g., X:BTCUSD, AAPL)",
                    "default": "X:BTCUSD"
                },
                "timespan": {
                    "type": "string",
                    "enum": ["minute", "hour", "day", "week", "month", "quarter", "year"],
                    "description": "Timespan for aggregates",
                    "default": "day"
                },
                "multiplier": {
                    "type": "integer",
                    "description": "Size of the timespan multiplier",
                    "default": 1
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD)",
                    "default": "2024-01-01"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date (YYYY-MM-DD)",
                    "default": "2024-01-15"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 100
                },
                "api_key": {
                    "type": "string",
                    "description": "Polygon.io API key (required for all endpoints)",
                    "default": ""
                }
            },
            "required": ["action"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:
        """Make API request to Polygon.io"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        
        # Add API key to params
        if params is None:
            params = {}
        if api_key and api_key.strip():
            params['apikey'] = api_key.strip()
        else:
            return {"error": "API key is required for Polygon.io API"}
            
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Polygon.io API request failed: {e}")
            return {"error": f"Polygon.io API request failed: {e}"}
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_crypto_aggregates":
                return await self._get_crypto_aggregates(arguments)
            elif action == "get_crypto_previous_close":
                return await self._get_crypto_previous_close(arguments)
            elif action == "get_crypto_grouped_daily":
                return await self._get_crypto_grouped_daily(arguments)
            elif action == "get_crypto_trades":
                return await self._get_crypto_trades(arguments)
            elif action == "get_crypto_quotes":
                return await self._get_crypto_quotes(arguments)
            elif action == "get_crypto_snapshot":
                return await self._get_crypto_snapshot(arguments)
            elif action == "get_crypto_news":
                return await self._get_crypto_news(arguments)
            elif action == "get_stock_aggregates":
                return await self._get_stock_aggregates(arguments)
            elif action == "get_stock_previous_close":
                return await self._get_stock_previous_close(arguments)
            elif action == "get_stock_trades":
                return await self._get_stock_trades(arguments)
            elif action == "get_stock_quotes":
                return await self._get_stock_quotes(arguments)
            elif action == "get_stock_snapshot":
                return await self._get_stock_snapshot(arguments)
            elif action == "get_news":
                return await self._get_news(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_crypto_aggregates(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto aggregates"""
        ticker = args.get("ticker", "X:BTCUSD")
        timespan = args.get("timespan", "day")
        multiplier = args.get("multiplier", 1)
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto Aggregates ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto aggregates: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto aggregates: {str(e)}"}]
    
    async def _get_crypto_previous_close(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto previous close"""
        ticker = args.get("ticker", "X:BTCUSD")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/v2/aggs/ticker/{ticker}/prev", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto Previous Close ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto previous close: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto previous close: {str(e)}"}]
    
    async def _get_crypto_grouped_daily(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto grouped daily"""
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        api_key = args.get("api_key")
        
        try:
            params = {"from": from_date, "to": to_date}
            data = await self._make_request("/v2/aggs/grouped/locale/global/market/crypto/2024-01-01", params=params, api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto Grouped Daily:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto grouped daily: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto grouped daily: {str(e)}"}]
    
    async def _get_crypto_trades(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto trades"""
        ticker = args.get("ticker", "X:BTCUSD")
        limit = args.get("limit", 100)
        api_key = args.get("api_key")
        
        try:
            params = {"limit": limit}
            data = await self._make_request(f"/v3/trades/{ticker}", params=params, api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto Trades ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto trades: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto trades: {str(e)}"}]
    
    async def _get_crypto_quotes(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto quotes"""
        ticker = args.get("ticker", "X:BTCUSD")
        limit = args.get("limit", 100)
        api_key = args.get("api_key")
        
        try:
            params = {"limit": limit}
            data = await self._make_request(f"/v3/quotes/{ticker}", params=params, api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto Quotes ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto quotes: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto quotes: {str(e)}"}]
    
    async def _get_crypto_snapshot(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto snapshot"""
        ticker = args.get("ticker", "X:BTCUSD")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/v2/snapshot/locale/global/markets/crypto/tickers/{ticker}", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto Snapshot ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto snapshot: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto snapshot: {str(e)}"}]
    
    async def _get_crypto_news(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get crypto news"""
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request("/v2/reference/news", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Crypto News:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching crypto news: {e}")
            return [{"type": "text", "text": f"❌ Error fetching crypto news: {str(e)}"}]
    
    async def _get_stock_aggregates(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get stock aggregates"""
        ticker = args.get("ticker", "AAPL")
        timespan = args.get("timespan", "day")
        multiplier = args.get("multiplier", 1)
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Stock Aggregates ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching stock aggregates: {e}")
            return [{"type": "text", "text": f"❌ Error fetching stock aggregates: {str(e)}"}]
    
    async def _get_stock_previous_close(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get stock previous close"""
        ticker = args.get("ticker", "AAPL")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/v2/aggs/ticker/{ticker}/prev", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Stock Previous Close ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching stock previous close: {e}")
            return [{"type": "text", "text": f"❌ Error fetching stock previous close: {str(e)}"}]
    
    async def _get_stock_trades(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get stock trades"""
        ticker = args.get("ticker", "AAPL")
        limit = args.get("limit", 100)
        api_key = args.get("api_key")
        
        try:
            params = {"limit": limit}
            data = await self._make_request(f"/v3/trades/{ticker}", params=params, api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Stock Trades ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching stock trades: {e}")
            return [{"type": "text", "text": f"❌ Error fetching stock trades: {str(e)}"}]
    
    async def _get_stock_quotes(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get stock quotes"""
        ticker = args.get("ticker", "AAPL")
        limit = args.get("limit", 100)
        api_key = args.get("api_key")
        
        try:
            params = {"limit": limit}
            data = await self._make_request(f"/v3/quotes/{ticker}", params=params, api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Stock Quotes ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching stock quotes: {e}")
            return [{"type": "text", "text": f"❌ Error fetching stock quotes: {str(e)}"}]
    
    async def _get_stock_snapshot(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get stock snapshot"""
        ticker = args.get("ticker", "AAPL")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io Stock Snapshot ({ticker}):\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching stock snapshot: {e}")
            return [{"type": "text", "text": f"❌ Error fetching stock snapshot: {str(e)}"}]
    
    async def _get_news(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get general news"""
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request("/v2/reference/news", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Polygon.io News:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return [{"type": "text", "text": f"❌ Error fetching news: {str(e)}"}]