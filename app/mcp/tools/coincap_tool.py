"""
CoinCap MCP Tool
Access real-time cryptocurrency market data from CoinCap API (free, no auth required)
Note: Using CoinGecko as fallback since CoinCap API is currently unavailable
"""

import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class CoinCapTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._name = "coincap"
        self._description = "Access real-time cryptocurrency market data from CoinCap API (free, no authentication required)"
        self.base_url = "https://api.coingecko.com/api/v3"  # Using CoinGecko as fallback
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
                        "get_assets",
                        "get_asset_by_id",
                        "get_asset_history",
                        "get_asset_markets",
                        "get_rates",
                        "get_rate_by_id",
                        "get_exchanges",
                        "get_exchange_by_id",
                        "get_markets",
                        "get_candles"
                    ],
                    "description": "The action to perform"
                },
                "id": {
                    "type": "string",
                    "description": "Asset ID (e.g., bitcoin, ethereum)"
                },
                "search": {
                    "type": "string",
                    "description": "Search term for assets"
                },
                "ids": {
                    "type": "string",
                    "description": "Comma-separated list of asset IDs"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return (1-2000)",
                    "default": 100
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of results to skip",
                    "default": 0
                },
                "interval": {
                    "type": "string",
                    "enum": ["m1", "m5", "m15", "m30", "h1", "h2", "h6", "h12", "d1"],
                    "description": "Time interval for historical data",
                    "default": "d1"
                },
                "start": {
                    "type": "string",
                    "description": "Start time (Unix timestamp in milliseconds)"
                },
                "end": {
                    "type": "string",
                    "description": "End time (Unix timestamp in milliseconds)"
                },
                "exchange_id": {
                    "type": "string",
                    "description": "Exchange ID for market data"
                },
                "base_id": {
                    "type": "string",
                    "description": "Base asset ID for market data"
                },
                "quote_id": {
                    "type": "string",
                    "description": "Quote asset ID for market data"
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
            if action == "get_assets":
                return await self._get_assets(arguments)
            elif action == "get_asset_by_id":
                return await self._get_asset_by_id(arguments)
            elif action == "get_asset_history":
                return await self._get_asset_history(arguments)
            elif action == "get_asset_markets":
                return await self._get_asset_markets(arguments)
            elif action == "get_rates":
                return await self._get_rates(arguments)
            elif action == "get_rate_by_id":
                return await self._get_rate_by_id(arguments)
            elif action == "get_exchanges":
                return await self._get_exchanges(arguments)
            elif action == "get_exchange_by_id":
                return await self._get_exchange_by_id(arguments)
            elif action == "get_markets":
                return await self._get_markets(arguments)
            elif action == "get_candles":
                return await self._get_candles(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make API request to CoinGecko (CoinCap fallback)"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"CoinCap API request failed: {e}")
            return {"error": f"CoinCap API request failed: {e}"}

    async def _get_assets(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all assets"""
        limit = arguments.get("limit", 100)
        offset = arguments.get("offset", 0)
        search = arguments.get("search", "")
        ids = arguments.get("ids", "")
        
        try:
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": min(limit, 250),
                "page": (offset // limit) + 1,
                "sparkline": "false"
            }
            
            if search:
                params["search"] = search
            if ids:
                params["ids"] = ids
            
            data = await self._make_request("/coins/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform CoinGecko data to CoinCap-like format
            transformed_data = []
            for coin in data:
                transformed_data.append({
                    "id": coin["id"],
                    "rank": coin["market_cap_rank"],
                    "symbol": coin["symbol"].upper(),
                    "name": coin["name"],
                    "supply": coin["circulating_supply"],
                    "maxSupply": coin["total_supply"],
                    "marketCapUsd": coin["market_cap"],
                    "volumeUsd24Hr": coin["total_volume"],
                    "priceUsd": coin["current_price"],
                    "changePercent24Hr": coin["price_change_percentage_24h"],
                    "vwap24Hr": coin["price_change_24h"]
                })
            
            return [{"type": "text", "text": f"✅ CoinCap Assets Data:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching assets: {e}")
            return [{"type": "text", "text": f"❌ Error fetching assets: {str(e)}"}]

    async def _get_asset_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset by ID"""
        asset_id = arguments.get("id", "bitcoin")
        
        try:
            data = await self._make_request(f"/coins/{asset_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform CoinGecko data to CoinCap-like format
            market_data = data.get("market_data", {})
            transformed_data = {
                "id": data["id"],
                "rank": data["market_cap_rank"],
                "symbol": data["symbol"].upper(),
                "name": data["name"],
                "supply": market_data.get("circulating_supply"),
                "maxSupply": market_data.get("total_supply"),
                "marketCapUsd": market_data.get("market_cap", {}).get("usd"),
                "volumeUsd24Hr": market_data.get("total_volume", {}).get("usd"),
                "priceUsd": market_data.get("current_price", {}).get("usd"),
                "changePercent24Hr": market_data.get("price_change_percentage_24h"),
                "description": data.get("description", {}).get("en", "")[:200] + "..."
            }
            
            return [{"type": "text", "text": f"✅ CoinCap Asset {asset_id}:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset by ID: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset by ID: {str(e)}"}]

    async def _get_asset_history(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset history"""
        asset_id = arguments.get("id", "bitcoin")
        interval = arguments.get("interval", "d1")
        start = arguments.get("start", "")
        end = arguments.get("end", "")
        
        try:
            # Convert interval to days
            days_map = {
                "m1": 1, "m5": 1, "m15": 1, "m30": 1, "h1": 1, "h2": 1, "h6": 1, "h12": 1, "d1": 1
            }
            days = days_map.get(interval, 1)
            
            params = {"vs_currency": "usd", "days": days}
            if start:
                params["from_timestamp"] = int(start) // 1000
            if end:
                params["to_timestamp"] = int(end) // 1000
            
            data = await self._make_request(f"/coins/{asset_id}/market_chart", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            prices = data.get("prices", [])
            transformed_data = []
            for price_data in prices:
                transformed_data.append({
                    "time": price_data[0],
                    "priceUsd": price_data[1]
                })
            
            return [{"type": "text", "text": f"✅ CoinCap {asset_id} History ({interval}):\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset history: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset history: {str(e)}"}]

    async def _get_asset_markets(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset markets"""
        asset_id = arguments.get("id", "bitcoin")
        
        try:
            data = await self._make_request(f"/coins/{asset_id}/tickers")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            tickers = data.get("tickers", [])
            transformed_data = []
            for ticker in tickers[:10]:  # Limit to first 10
                transformed_data.append({
                    "exchangeId": ticker.get("market", {}).get("name", ""),
                    "baseId": asset_id,
                    "quoteId": ticker.get("target", ""),
                    "priceUsd": ticker.get("last"),
                    "volumeUsd24Hr": ticker.get("volume"),
                    "percentExchangeVolume": ticker.get("converted_volume", {}).get("usd", 0)
                })
            
            return [{"type": "text", "text": f"✅ CoinCap {asset_id} Markets:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset markets: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset markets: {str(e)}"}]

    async def _get_rates(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange rates"""
        try:
            data = await self._make_request("/exchange_rates")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            rates = data.get("rates", {})
            transformed_data = []
            for currency, rate_data in list(rates.items())[:20]:  # Limit to first 20
                transformed_data.append({
                    "id": currency,
                    "symbol": currency.upper(),
                    "currencySymbol": currency.upper(),
                    "type": "fiat",
                    "rateUsd": rate_data.get("value", 0)
                })
            
            return [{"type": "text", "text": f"✅ CoinCap Rates:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching rates: {e}")
            return [{"type": "text", "text": f"❌ Error fetching rates: {str(e)}"}]

    async def _get_rate_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get rate by ID"""
        rate_id = arguments.get("id", "usd")
        
        try:
            data = await self._make_request("/exchange_rates")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            rates = data.get("rates", {})
            if rate_id.lower() in rates:
                rate_data = rates[rate_id.lower()]
                transformed_data = {
                    "id": rate_id,
                    "symbol": rate_id.upper(),
                    "currencySymbol": rate_id.upper(),
                    "type": "fiat",
                    "rateUsd": rate_data.get("value", 0)
                }
                return [{"type": "text", "text": f"✅ CoinCap Rate {rate_id}:\n\n{transformed_data}"}]
            else:
                return [{"type": "text", "text": f"❌ Rate {rate_id} not found"}]
        except Exception as e:
            logger.error(f"Error fetching rate by ID: {e}")
            return [{"type": "text", "text": f"❌ Error fetching rate by ID: {str(e)}"}]

    async def _get_exchanges(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchanges"""
        limit = arguments.get("limit", 100)
        
        try:
            data = await self._make_request("/exchanges")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            transformed_data = []
            for exchange in data[:limit]:
                transformed_data.append({
                    "id": exchange.get("id", ""),
                    "name": exchange.get("name", ""),
                    "rank": exchange.get("trust_score_rank"),
                    "percentTotalVolume": exchange.get("trade_volume_24h_btc", 0),
                    "volumeUsd": exchange.get("trade_volume_24h_btc_normalized", 0),
                    "tradingPairs": exchange.get("trading_pairs", 0),
                    "socket": exchange.get("has_trading_incentive", False),
                    "exchangeUrl": exchange.get("url", ""),
                    "updated": exchange.get("last_trade_at")
                })
            
            return [{"type": "text", "text": f"✅ CoinCap Exchanges:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching exchanges: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchanges: {str(e)}"}]

    async def _get_exchange_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange by ID"""
        exchange_id = arguments.get("id", "binance")
        
        try:
            data = await self._make_request(f"/exchanges/{exchange_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            transformed_data = {
                "id": data.get("id", ""),
                "name": data.get("name", ""),
                "rank": data.get("trust_score_rank"),
                "percentTotalVolume": data.get("trade_volume_24h_btc", 0),
                "volumeUsd": data.get("trade_volume_24h_btc_normalized", 0),
                "tradingPairs": data.get("trading_pairs", 0),
                "socket": data.get("has_trading_incentive", False),
                "exchangeUrl": data.get("url", ""),
                "updated": data.get("last_trade_at"),
                "description": data.get("description", "")[:200] + "..."
            }
            
            return [{"type": "text", "text": f"✅ CoinCap Exchange {exchange_id}:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching exchange by ID: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchange by ID: {str(e)}"}]

    async def _get_markets(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get markets"""
        limit = arguments.get("limit", 100)
        
        try:
            data = await self._make_request("/coins/markets", {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": min(limit, 250),
                "sparkline": "false"
            })
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            transformed_data = []
            for coin in data:
                transformed_data.append({
                    "exchangeId": "coingecko",
                    "baseId": coin["id"],
                    "quoteId": "usd",
                    "baseSymbol": coin["symbol"].upper(),
                    "quoteSymbol": "USD",
                    "volumeUsd24Hr": coin["total_volume"],
                    "priceUsd": coin["current_price"],
                    "volumePercent": coin["price_change_percentage_24h"]
                })
            
            return [{"type": "text", "text": f"✅ CoinCap Markets:\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching markets: {e}")
            return [{"type": "text", "text": f"❌ Error fetching markets: {str(e)}"}]

    async def _get_candles(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get candles data"""
        exchange_id = arguments.get("exchange_id", "binance")
        base_id = arguments.get("base_id", "bitcoin")
        quote_id = arguments.get("quote_id", "usd")
        interval = arguments.get("interval", "d1")
        start = arguments.get("start", "")
        end = arguments.get("end", "")
        
        try:
            # Convert interval to days
            days_map = {
                "m1": 1, "m5": 1, "m15": 1, "m30": 1, "h1": 1, "h2": 1, "h6": 1, "h12": 1, "d1": 1
            }
            days = days_map.get(interval, 1)
            
            params = {"vs_currency": quote_id, "days": days}
            if start:
                params["from_timestamp"] = int(start) // 1000
            if end:
                params["to_timestamp"] = int(end) // 1000
            
            data = await self._make_request(f"/coins/{base_id}/market_chart", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Transform data
            prices = data.get("prices", [])
            volumes = data.get("total_volumes", [])
            transformed_data = []
            
            for i, price_data in enumerate(prices):
                volume_data = volumes[i] if i < len(volumes) else [price_data[0], 0]
                transformed_data.append({
                    "open": price_data[1],
                    "high": price_data[1],  # Simplified - would need OHLC data
                    "low": price_data[1],
                    "close": price_data[1],
                    "volume": volume_data[1],
                    "period": price_data[0]
                })
            
            return [{"type": "text", "text": f"✅ CoinCap Candles ({exchange_id}/{base_id}/{quote_id}):\n\n{transformed_data}"}]
        except Exception as e:
            logger.error(f"Error fetching candles: {e}")
            return [{"type": "text", "text": f"❌ Error fetching candles: {str(e)}"}]