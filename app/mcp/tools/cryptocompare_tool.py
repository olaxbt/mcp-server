"""
CryptoCompare MCP Tool
Access cryptocurrency data, historical prices, and social sentiment from CryptoCompare API
"""

import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class CryptoCompareTool(MCPTool):
    def __init__(self):
        super().__init__()
        self.base_url = "https://min-api.cryptocompare.com/data"
    
    @property
    def name(self) -> str:
        return "cryptocompare"
    
    @property
    def description(self) -> str:
        return "Access cryptocurrency data, historical prices, and social sentiment from CryptoCompare API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_price",
                        "get_historical_daily",
                        "get_historical_hourly",
                        "get_historical_minute",
                        "get_social_sentiment",
                        "get_news",
                        "get_top_list",
                        "get_exchanges",
                        "get_mining_equipment",
                        "get_coin_snapshot"
                    ],
                    "description": "The action to perform"
                },
                "fsym": {
                    "type": "string",
                    "description": "From symbol (e.g., BTC, ETH)",
                    "default": "BTC"
                },
                "tsyms": {
                    "type": "string",
                    "description": "To symbols (e.g., USD,EUR,JPY)",
                    "default": "USD"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of data points to return",
                    "default": 30
                },
                "toTs": {
                    "type": "integer",
                    "description": "Unix timestamp to get data before"
                },
                "aggregate": {
                    "type": "integer",
                    "description": "Data aggregation time (minutes)",
                    "default": 1
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_price":
                return await self._get_price(arguments)
            elif action == "get_historical_daily":
                return await self._get_historical_daily(arguments)
            elif action == "get_historical_hourly":
                return await self._get_historical_hourly(arguments)
            elif action == "get_historical_minute":
                return await self._get_historical_minute(arguments)
            elif action == "get_social_sentiment":
                return await self._get_social_sentiment(arguments)
            elif action == "get_news":
                return await self._get_news(arguments)
            elif action == "get_top_list":
                return await self._get_top_list(arguments)
            elif action == "get_exchanges":
                return await self._get_exchanges(arguments)
            elif action == "get_mining_equipment":
                return await self._get_mining_equipment(arguments)
            elif action == "get_coin_snapshot":
                return await self._get_coin_snapshot(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"CryptoCompare API error: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request to CryptoCompare"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"CryptoCompare API request failed: {e}")
            return {"error": f"CryptoCompare API request failed: {e}"}

    async def _get_price(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get current price for cryptocurrencies"""
        fsym = args.get("fsym", "BTC")
        tsyms = args.get("tsyms", "USD")
        
        try:
            data = await self._make_request("/price", {"fsym": fsym, "tsyms": tsyms})
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Current Prices ({fsym} to {tsyms}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching price: {e}")
            return [{"type": "text", "text": f"❌ Error fetching price: {str(e)}"}]
    
    async def _get_historical_daily(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get historical daily data"""
        fsym = args.get("fsym", "BTC")
        tsym = args.get("tsyms", "USD").split(",")[0]
        limit = args.get("limit", 30)
        toTs = args.get("toTs")
        
        try:
            params = {"fsym": fsym, "tsym": tsym, "limit": limit}
            if toTs:
                params["toTs"] = toTs
                
            data = await self._make_request("/v2/histoday", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Historical Daily Data ({fsym}/{tsym}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching historical daily data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching historical daily data: {str(e)}"}]
    
    async def _get_historical_hourly(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get historical hourly data"""
        fsym = args.get("fsym", "BTC")
        tsym = args.get("tsyms", "USD").split(",")[0]
        limit = args.get("limit", 24)
        toTs = args.get("toTs")
        
        try:
            params = {"fsym": fsym, "tsym": tsym, "limit": limit}
            if toTs:
                params["toTs"] = toTs
                
            data = await self._make_request("/v2/histohour", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Historical Hourly Data ({fsym}/{tsym}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching historical hourly data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching historical hourly data: {str(e)}"}]

    async def _get_historical_minute(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get historical minute data"""
        fsym = args.get("fsym", "BTC")
        tsym = args.get("tsyms", "USD").split(",")[0]
        limit = args.get("limit", 60)
        aggregate = args.get("aggregate", 1)
        toTs = args.get("toTs")
        
        try:
            params = {"fsym": fsym, "tsym": tsym, "limit": limit, "aggregate": aggregate}
            if toTs:
                params["toTs"] = toTs
                
            data = await self._make_request("/v2/histominute", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Historical Minute Data ({fsym}/{tsym}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching historical minute data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching historical minute data: {str(e)}"}]

    async def _get_social_sentiment(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get social sentiment data"""
        fsym = args.get("fsym", "bitcoin")
        
        try:
            data = await self._make_request("/social/coin/histo/day", {"coin": fsym, "limit": 7})
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Social Sentiment for {fsym}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching social sentiment: {e}")
            return [{"type": "text", "text": f"❌ Error fetching social sentiment: {str(e)}"}]
    
    async def _get_news(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get latest cryptocurrency news"""
        limit = args.get("limit", 10)
        
        try:
            data = await self._make_request("/v2/news/", {"lang": "EN", "sortOrder": "latest", "limit": limit})
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Latest News:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return [{"type": "text", "text": f"❌ Error fetching news: {str(e)}"}]
    
    async def _get_top_list(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top cryptocurrency list"""
        tsym = args.get("tsyms", "USD").split(",")[0]
        limit = args.get("limit", 50)
        
        try:
            data = await self._make_request("/top/totalvolfull", {"tsym": tsym, "limit": limit})
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Top List ({tsym}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching top list: {e}")
            return [{"type": "text", "text": f"❌ Error fetching top list: {str(e)}"}]

    async def _get_exchanges(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange information"""
        try:
            data = await self._make_request("/exchanges/general")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Exchanges:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching exchanges: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchanges: {str(e)}"}]

    async def _get_mining_equipment(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get mining equipment data"""
        try:
            data = await self._make_request("/mining/equipment")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Mining Equipment:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching mining equipment: {e}")
            return [{"type": "text", "text": f"❌ Error fetching mining equipment: {str(e)}"}]

    async def _get_coin_snapshot(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get detailed coin snapshot"""
        fsym = args.get("fsym", "BTC")
        tsym = args.get("tsyms", "USD").split(",")[0]
        
        try:
            data = await self._make_request("/coinsnapshot", {"fsym": fsym, "tsym": tsym})
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CryptoCompare Coin Snapshot ({fsym}/{tsym}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin snapshot: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin snapshot: {str(e)}"}]