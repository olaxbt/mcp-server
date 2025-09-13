"""
CoinPaprika MCP Tool
Access comprehensive cryptocurrency data from CoinPaprika API (free, no auth required)
"""

import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class CoinPaprikaTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._name = "coinpaprika"
        self._description = "Access comprehensive cryptocurrency data from CoinPaprika API (free, no authentication required)"
        self.base_url = "https://api.coinpaprika.com/v1"
        self._session = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_global",
                        "get_coins",
                        "get_coin_by_id",
                        "get_coin_twitter",
                        "get_coin_events",
                        "get_coin_exchanges",
                        "get_coin_markets",
                        "get_coin_ohlc",
                        "get_coin_today",
                        "get_coin_tickers",
                        "get_exchanges",
                        "get_exchange_by_id",
                        "get_exchange_markets",
                        "get_people",
                        "get_person_by_id",
                        "get_tags",
                        "get_search"
                    ],
                    "description": "The action to perform"
                },
                "coin_id": {
                    "type": "string",
                    "description": "Coin ID (e.g., btc-bitcoin, eth-ethereum)"
                },
                "exchange_id": {
                    "type": "string",
                    "description": "Exchange ID (e.g., binance, coinbase)"
                },
                "quote": {
                    "type": "string",
                    "description": "Quote currency (e.g., usd, btc, eth)",
                    "default": "usd"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 100
                },
                "timeframe": {
                    "type": "string",
                    "enum": ["1h", "4h", "12h", "1d", "1w", "1m", "3m", "6m", "1y", "2y", "5y"],
                    "description": "Timeframe for OHLC data",
                    "default": "1d"
                },
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "categories": {
                    "type": "string",
                    "description": "Comma-separated categories"
                }
            },
            "required": ["action"]
        }

    async def _get_session(self):
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_global":
                return await self._get_global()
            elif action == "get_coins":
                return await self._get_coins(arguments)
            elif action == "get_coin_by_id":
                return await self._get_coin_by_id(arguments)
            elif action == "get_coin_twitter":
                return await self._get_coin_twitter(arguments)
            elif action == "get_coin_events":
                return await self._get_coin_events(arguments)
            elif action == "get_coin_exchanges":
                return await self._get_coin_exchanges(arguments)
            elif action == "get_coin_markets":
                return await self._get_coin_markets(arguments)
            elif action == "get_coin_ohlc":
                return await self._get_coin_ohlc(arguments)
            elif action == "get_coin_today":
                return await self._get_coin_today(arguments)
            elif action == "get_coin_tickers":
                return await self._get_coin_tickers(arguments)
            elif action == "get_exchanges":
                return await self._get_exchanges(arguments)
            elif action == "get_exchange_by_id":
                return await self._get_exchange_by_id(arguments)
            elif action == "get_exchange_markets":
                return await self._get_exchange_markets(arguments)
            elif action == "get_people":
                return await self._get_people(arguments)
            elif action == "get_person_by_id":
                return await self._get_person_by_id(arguments)
            elif action == "get_tags":
                return await self._get_tags(arguments)
            elif action == "get_search":
                return await self._get_search(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request to CoinPaprika"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"CoinPaprika API request failed: {e}")
            return {"error": f"CoinPaprika API request failed: {e}"}

    async def _get_global(self) -> List[Dict[str, Any]]:
        """Get global cryptocurrency data"""
        try:
            data = await self._make_request("/global")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Global Data:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching global data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching global data: {str(e)}"}]

    async def _get_coins(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all coins"""
        limit = arguments.get("limit", 100)
        categories = arguments.get("categories", "")
        
        try:
            params = {}
            if limit:
                params["limit"] = min(limit, 5000)
            if categories:
                params["categories"] = categories
            
            data = await self._make_request("/coins", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Coins:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coins: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coins: {str(e)}"}]

    async def _get_coin_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin by ID"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        
        try:
            data = await self._make_request(f"/coins/{coin_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Coin {coin_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin by ID: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin by ID: {str(e)}"}]

    async def _get_coin_twitter(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin Twitter data"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        
        try:
            data = await self._make_request(f"/coins/{coin_id}/twitter")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} Twitter:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin Twitter: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin Twitter: {str(e)}"}]

    async def _get_coin_events(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin events"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        limit = arguments.get("limit", 100)
        
        try:
            params = {}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request(f"/coins/{coin_id}/events", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} Events:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin events: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin events: {str(e)}"}]

    async def _get_coin_exchanges(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin exchanges"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        limit = arguments.get("limit", 100)
        
        try:
            params = {}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request(f"/coins/{coin_id}/exchanges", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} Exchanges:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin exchanges: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin exchanges: {str(e)}"}]

    async def _get_coin_markets(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin markets"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        quote = arguments.get("quote", "usd")
        limit = arguments.get("limit", 100)
        
        try:
            params = {"quotes": quote}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request(f"/coins/{coin_id}/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} Markets:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin markets: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin markets: {str(e)}"}]

    async def _get_coin_ohlc(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin OHLC data"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        quote = arguments.get("quote", "usd")
        timeframe = arguments.get("timeframe", "1d")
        
        try:
            data = await self._make_request(f"/coins/{coin_id}/ohlc/latest", {
                "quote": quote,
                "timeframe": timeframe
            })
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} OHLC ({timeframe}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin OHLC: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin OHLC: {str(e)}"}]

    async def _get_coin_today(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin today data"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        quote = arguments.get("quote", "usd")
        
        try:
            data = await self._make_request(f"/coins/{coin_id}/today", {"quotes": quote})
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} Today:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin today: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin today: {str(e)}"}]

    async def _get_coin_tickers(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin tickers"""
        coin_id = arguments.get("coin_id", "btc-bitcoin")
        quote = arguments.get("quote", "usd")
        limit = arguments.get("limit", 100)
        
        try:
            params = {"quotes": quote}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request(f"/coins/{coin_id}/tickers", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {coin_id} Tickers:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching coin tickers: {e}")
            return [{"type": "text", "text": f"❌ Error fetching coin tickers: {str(e)}"}]

    async def _get_exchanges(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all exchanges"""
        limit = arguments.get("limit", 100)
        
        try:
            params = {}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request("/exchanges", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Exchanges:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching exchanges: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchanges: {str(e)}"}]

    async def _get_exchange_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange by ID"""
        exchange_id = arguments.get("exchange_id", "binance")
        
        try:
            data = await self._make_request(f"/exchanges/{exchange_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Exchange {exchange_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching exchange by ID: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchange by ID: {str(e)}"}]

    async def _get_exchange_markets(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange markets"""
        exchange_id = arguments.get("exchange_id", "binance")
        quote = arguments.get("quote", "usd")
        limit = arguments.get("limit", 100)
        
        try:
            params = {"quotes": quote}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request(f"/exchanges/{exchange_id}/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika {exchange_id} Markets:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching exchange markets: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchange markets: {str(e)}"}]

    async def _get_people(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get people in crypto"""
        limit = arguments.get("limit", 100)
        
        try:
            params = {}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request("/people", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika People:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching people: {e}")
            return [{"type": "text", "text": f"❌ Error fetching people: {str(e)}"}]

    async def _get_person_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get person by ID"""
        person_id = arguments.get("person_id", "vitalik-buterin")
        
        try:
            data = await self._make_request(f"/people/{person_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Person {person_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching person by ID: {e}")
            return [{"type": "text", "text": f"❌ Error fetching person by ID: {str(e)}"}]

    async def _get_tags(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get tags/categories"""
        limit = arguments.get("limit", 100)
        
        try:
            params = {}
            if limit:
                params["limit"] = min(limit, 1000)
            
            data = await self._make_request("/tags", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Tags:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching tags: {e}")
            return [{"type": "text", "text": f"❌ Error fetching tags: {str(e)}"}]

    async def _get_search(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search coins, exchanges, and people"""
        query = arguments.get("query", "bitcoin")
        limit = arguments.get("limit", 100)
        categories = arguments.get("categories", "")
        
        try:
            params = {"q": query}
            if limit:
                params["limit"] = min(limit, 1000)
            if categories:
                params["c"] = categories
            
            data = await self._make_request("/search", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinPaprika Search '{query}':\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return [{"type": "text", "text": f"❌ Error searching: {str(e)}"}]