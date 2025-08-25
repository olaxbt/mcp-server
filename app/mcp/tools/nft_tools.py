"""
NFT Tools
Contains NFT marketplace and collection analysis tools
"""

import asyncio
import logging
import time
import aiohttp
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class NFTMarketplaceTool(MCPTool):
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
        
        # API endpoints for different chains
        self.api_endpoints = {
            "ethereum": {
                "opensea": "https://api.opensea.io/api/v1",
                "reservoir": "https://api.reservoir.tools"
            },
            "solana": {
                "magic_eden": "https://api-mainnet.magiceden.dev/v2",
                "tensor": "https://api.tensor.so/api/v1"
            },
            "polygon": {
                "opensea": "https://api.opensea.io/api/v1",
                "reservoir": "https://api-polygon.reservoir.tools"
            }
        }
        
        # API keys (should be set via environment variables)
        self.opensea_api_key = os.getenv("OPENSEA_API_KEY")
        self.reservoir_api_key = os.getenv("RESERVOIR_API_KEY")
    
    @property
    def name(self) -> str:
        return "nft_marketplace"
    
    @property
    def description(self) -> str:
        return "Get real-time NFT marketplace data including floor prices, trading volume, and collection analytics from OpenSea, Magic Eden, and other major marketplaces."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "NFT marketplace action to perform",
                    "enum": ["collection_info", "floor_price", "trading_volume", "recent_sales", "collection_stats"],
                    "default": "collection_info"
                },
                "collection_slug": {
                    "type": "string",
                    "description": "NFT collection identifier (e.g., 'bored-ape-yacht-club', 'degen-ape-academy')",
                    "default": None
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network",
                    "enum": ["ethereum", "solana", "polygon"],
                    "default": "ethereum"
                },
                "time_period": {
                    "type": "string",
                    "description": "Time period for data (e.g., '1d', '7d', '30d')",
                    "default": "7d"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of recent sales to return (max 50)",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action", "collection_info")
            collection_slug = arguments.get("collection_slug")
            chain = arguments.get("chain", "ethereum")
            time_period = arguments.get("time_period", "7d")
            limit = min(arguments.get("limit", 10), 50)
            
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            if action == "collection_info":
                return await self._get_collection_info(collection_slug, chain)
            elif action == "floor_price":
                return await self._get_floor_price(collection_slug, chain)
            elif action == "trading_volume":
                return await self._get_trading_volume(collection_slug, chain, time_period)
            elif action == "recent_sales":
                return await self._get_recent_sales(collection_slug, chain, limit)
            elif action == "collection_stats":
                return await self._get_collection_stats(collection_slug, chain)
            else:
                return [{"error": f"Unsupported action: {action}"}]
                
        except Exception as e:
            logger.error(f"NFT marketplace tool error: {e}")
            return [{"error": f"NFT marketplace operation failed: {str(e)}"}]
    
    async def _get_collection_info(self, collection_slug: str, chain: str) -> List[Dict[str, Any]]:
        """Get basic collection information from OpenSea or Magic Eden"""
        if not collection_slug:
            return [{"error": "collection_slug is required for collection_info action"}]
        
        try:
            if chain == "ethereum" or chain == "polygon":
                return await self._get_opensea_collection_info(collection_slug, chain)
            elif chain == "solana":
                return await self._get_magic_eden_collection_info(collection_slug)
            else:
                return [{"error": f"Unsupported chain: {chain}"}]
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return [{"error": f"Failed to get collection info: {str(e)}"}]
    
    async def _get_opensea_collection_info(self, collection_slug: str, chain: str) -> List[Dict[str, Any]]:
        """Get collection info from OpenSea API"""
        try:
            url = f"{self.api_endpoints[chain]['opensea']}/collection/{collection_slug}"
            headers = {}
            
            if self.opensea_api_key:
                headers["X-API-KEY"] = self.opensea_api_key
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    collection = data.get("collection", {})
                    
                    collection_info = {
                        "collection_slug": collection_slug,
                        "chain": chain,
                        "name": collection.get("name", ""),
                        "description": collection.get("description", ""),
                        "total_supply": collection.get("stats", {}).get("total_supply", 0),
                        "owners": collection.get("stats", {}).get("num_owners", 0),
                        "floor_price": collection.get("stats", {}).get("floor_price", 0),
                        "total_volume": collection.get("stats", {}).get("total_volume", 0),
                        "created_date": collection.get("created_date", ""),
                        "external_url": collection.get("external_url", ""),
                        "image_url": collection.get("image_url", ""),
                        "banner_image_url": collection.get("banner_image_url", "")
                    }
                    
                    return [{"collection_info": collection_info}]
                else:
                    return [{"error": f"OpenSea API request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea collection info error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_collection_info(self, collection_slug: str) -> List[Dict[str, Any]]:
        """Get collection info from Magic Eden API"""
        try:
            url = f"{self.api_endpoints['solana']['magic_eden']}/collections/{collection_slug}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    collection_info = {
                        "collection_slug": collection_slug,
                        "chain": "solana",
                        "name": data.get("name", ""),
                        "description": data.get("description", ""),
                        "total_supply": data.get("supply", 0),
                        "owners": data.get("holders", 0),
                        "floor_price": data.get("floorPrice", 0),
                        "total_volume": data.get("volumeAll", 0),
                        "created_date": data.get("createdAt", ""),
                        "image_url": data.get("image", ""),
                        "website": data.get("website", "")
                    }
                    
                    return [{"collection_info": collection_info}]
                else:
                    return [{"error": f"Magic Eden API request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden collection info error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_floor_price(self, collection_slug: str, chain: str) -> List[Dict[str, Any]]:
        """Get current floor price from marketplace APIs"""
        if not collection_slug:
            return [{"error": "collection_slug is required for floor_price action"}]
        
        try:
            if chain == "ethereum" or chain == "polygon":
                return await self._get_opensea_floor_price(collection_slug, chain)
            elif chain == "solana":
                return await self._get_magic_eden_floor_price(collection_slug)
            else:
                return [{"error": f"Unsupported chain: {chain}"}]
        except Exception as e:
            logger.error(f"Error getting floor price: {e}")
            return [{"error": f"Failed to get floor price: {str(e)}"}]
    
    async def _get_opensea_floor_price(self, collection_slug: str, chain: str) -> List[Dict[str, Any]]:
        """Get floor price from OpenSea"""
        try:
            url = f"{self.api_endpoints[chain]['opensea']}/collection/{collection_slug}/stats"
            headers = {}
            
            if self.opensea_api_key:
                headers["X-API-KEY"] = self.opensea_api_key
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data.get("stats", {})
                    
                    floor_data = {
                        "collection_slug": collection_slug,
                        "chain": chain,
                        "floor_price": stats.get("floor_price", 0),
                        "floor_price_usd": stats.get("floor_price", 0),  # OpenSea returns in ETH
                        "last_updated": datetime.now().isoformat(),
                        "change_24h": stats.get("one_day_change", 0),
                        "change_7d": stats.get("seven_day_change", 0),
                        "marketplace": "OpenSea"
                    }
                    
                    return [{"floor_price": floor_data}]
                else:
                    return [{"error": f"OpenSea floor price request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea floor price error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_floor_price(self, collection_slug: str) -> List[Dict[str, Any]]:
        """Get floor price from Magic Eden"""
        try:
            url = f"{self.api_endpoints['solana']['magic_eden']}/collections/{collection_slug}/stats"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    floor_data = {
                        "collection_slug": collection_slug,
                        "chain": "solana",
                        "floor_price": data.get("floorPrice", 0),
                        "floor_price_usd": data.get("floorPrice", 0),  # Magic Eden returns in SOL
                        "last_updated": datetime.now().isoformat(),
                        "change_24h": data.get("floorChange24h", 0),
                        "change_7d": data.get("floorChange7d", 0),
                        "marketplace": "Magic Eden"
                    }
                    
                    return [{"floor_price": floor_data}]
                else:
                    return [{"error": f"Magic Eden floor price request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden floor price error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_trading_volume(self, collection_slug: str, chain: str, time_period: str) -> List[Dict[str, Any]]:
        """Get trading volume data from marketplace APIs"""
        if not collection_slug:
            return [{"error": "collection_slug is required for trading_volume action"}]
        
        try:
            if chain == "ethereum" or chain == "polygon":
                return await self._get_opensea_trading_volume(collection_slug, chain, time_period)
            elif chain == "solana":
                return await self._get_magic_eden_trading_volume(collection_slug, time_period)
            else:
                return [{"error": f"Unsupported chain: {chain}"}]
        except Exception as e:
            logger.error(f"Error getting trading volume: {e}")
            return [{"error": f"Failed to get trading volume: {str(e)}"}]
    
    async def _get_opensea_trading_volume(self, collection_slug: str, chain: str, time_period: str) -> List[Dict[str, Any]]:
        """Get trading volume from OpenSea"""
        try:
            url = f"{self.api_endpoints[chain]['opensea']}/collection/{collection_slug}/stats"
            headers = {}
            
            if self.opensea_api_key:
                headers["X-API-KEY"] = self.opensea_api_key
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data.get("stats", {})
                    
                    # Map time periods to OpenSea stats
                    volume_map = {
                        "1d": stats.get("one_day_volume", 0),
                        "7d": stats.get("seven_day_volume", 0),
                        "30d": stats.get("thirty_day_volume", 0)
                    }
                    
                    volume_data = {
                        "collection_slug": collection_slug,
                        "chain": chain,
                        "time_period": time_period,
                        "volume": volume_map.get(time_period, 0),
                        "volume_usd": volume_map.get(time_period, 0),
                        "sales_count": stats.get("total_sales", 0),
                        "average_price": stats.get("average_price", 0),
                        "marketplace": "OpenSea"
                    }
                    
                    return [{"trading_volume": volume_data}]
                else:
                    return [{"error": f"OpenSea trading volume request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea trading volume error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_trading_volume(self, collection_slug: str, time_period: str) -> List[Dict[str, Any]]:
        """Get trading volume from Magic Eden"""
        try:
            url = f"{self.api_endpoints['solana']['magic_eden']}/collections/{collection_slug}/stats"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Map time periods to Magic Eden stats
                    volume_map = {
                        "1d": data.get("volume24h", 0),
                        "7d": data.get("volume7d", 0),
                        "30d": data.get("volume30d", 0)
                    }
                    
                    volume_data = {
                        "collection_slug": collection_slug,
                        "chain": "solana",
                        "time_period": time_period,
                        "volume": volume_map.get(time_period, 0),
                        "volume_usd": volume_map.get(time_period, 0),
                        "sales_count": data.get("sales24h", 0),
                        "average_price": data.get("avgPrice24h", 0),
                        "marketplace": "Magic Eden"
                    }
                    
                    return [{"trading_volume": volume_data}]
                else:
                    return [{"error": f"Magic Eden trading volume request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden trading volume error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_recent_sales(self, collection_slug: str, chain: str, limit: int) -> List[Dict[str, Any]]:
        """Get recent NFT sales from marketplace APIs"""
        if not collection_slug:
            return [{"error": "collection_slug is required for recent_sales action"}]
        
        try:
            if chain == "ethereum" or chain == "polygon":
                return await self._get_opensea_recent_sales(collection_slug, chain, limit)
            elif chain == "solana":
                return await self._get_magic_eden_recent_sales(collection_slug, limit)
            else:
                return [{"error": f"Unsupported chain: {chain}"}]
        except Exception as e:
            logger.error(f"Error getting recent sales: {e}")
            return [{"error": f"Failed to get recent sales: {str(e)}"}]
    
    async def _get_opensea_recent_sales(self, collection_slug: str, chain: str, limit: int) -> List[Dict[str, Any]]:
        """Get recent sales from OpenSea"""
        try:
            url = f"{self.api_endpoints[chain]['opensea']}/events"
            params = {
                "collection_slug": collection_slug,
                "event_type": "successful",
                "limit": limit
            }
            headers = {}
            
            if self.opensea_api_key:
                headers["X-API-KEY"] = self.opensea_api_key
            
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    events = data.get("asset_events", [])
                    
                    recent_sales = []
                    for event in events:
                        sale_data = {
                            "token_id": event.get("asset", {}).get("token_id", ""),
                            "price": event.get("total_price", 0),
                            "price_usd": event.get("payment_token", {}).get("usd_price", 0),
                            "buyer": event.get("winner_account", {}).get("address", ""),
                            "seller": event.get("seller", {}).get("address", ""),
                            "timestamp": event.get("event_timestamp", ""),
                            "transaction_hash": event.get("transaction", ""),
                            "marketplace": "OpenSea"
                        }
                        recent_sales.append(sale_data)
                    
                    return [{"recent_sales": recent_sales}]
                else:
                    return [{"error": f"OpenSea recent sales request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea recent sales error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_recent_sales(self, collection_slug: str, limit: int) -> List[Dict[str, Any]]:
        """Get recent sales from Magic Eden"""
        try:
            url = f"{self.api_endpoints['solana']['magic_eden']}/collections/{collection_slug}/activities"
            params = {
                "offset": 0,
                "limit": limit,
                "type": "buyNow"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    activities = data.get("activities", [])
                    
                    recent_sales = []
                    for activity in activities:
                        sale_data = {
                            "token_id": activity.get("tokenMint", ""),
                            "price": activity.get("price", 0),
                            "price_usd": activity.get("price", 0),  # Magic Eden returns in SOL
                            "buyer": activity.get("buyer", ""),
                            "seller": activity.get("seller", ""),
                            "timestamp": activity.get("blockTime", ""),
                            "transaction_hash": activity.get("signature", ""),
                            "marketplace": "Magic Eden"
                        }
                        recent_sales.append(sale_data)
                    
                    return [{"recent_sales": recent_sales}]
                else:
                    return [{"error": f"Magic Eden recent sales request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden recent sales error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_collection_stats(self, collection_slug: str, chain: str) -> List[Dict[str, Any]]:
        """Get comprehensive collection statistics"""
        if not collection_slug:
            return [{"error": "collection_slug is required for collection_stats action"}]
        
        try:
            # Get all stats in parallel
            tasks = [
                self._get_collection_info(collection_slug, chain),
                self._get_floor_price(collection_slug, chain),
                self._get_trading_volume(collection_slug, chain, "7d")
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            stats = {
                "collection_slug": collection_slug,
                "chain": chain,
                "last_updated": datetime.now().isoformat()
            }
            
            # Combine results
            if not isinstance(results[0], Exception) and results[0]:
                stats.update(results[0][0].get("collection_info", {}))
            
            if not isinstance(results[1], Exception) and results[1]:
                stats.update(results[1][0].get("floor_price", {}))
            
            if not isinstance(results[2], Exception) and results[2]:
                stats.update(results[2][0].get("trading_volume", {}))
            
            return [{"collection_stats": stats}]
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return [{"error": f"Failed to get collection stats: {str(e)}"}]
