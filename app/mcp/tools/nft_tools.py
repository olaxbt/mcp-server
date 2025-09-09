"""
NFT Tools
Contains tools for interacting with NFT marketplaces and collections
"""

import asyncio
import logging
import aiohttp
from datetime import datetime
from typing import Any, Dict, List

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
                },
                "opensea_api_key": {
                    "type": "string",
                    "description": "OpenSea API key (required for Ethereum/Polygon)"
                },
                "reservoir_api_key": {
                    "type": "string",
                    "description": "Reservoir API key (required for Ethereum/Polygon)"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            logger.info(f"NFT marketplace tool called with arguments: {arguments}")
            
            action = arguments.get("action", "collection_info")
            collection_slug = arguments.get("collection_slug")
            chain = arguments.get("chain", "ethereum")
            time_period = arguments.get("time_period", "7d")
            limit = min(arguments.get("limit", 10), 50)
            
            logger.info(f"Parsed parameters - action: '{action}' (type: {type(action)}), collection_slug: {collection_slug}, chain: {chain}")
            
            # Get API keys from user input (optional)
            opensea_api_key = arguments.get("opensea_api_key")
            reservoir_api_key = arguments.get("reservoir_api_key")
            
            # Store API keys as instance variables for use in other methods
            self.opensea_api_key = opensea_api_key
            self.reservoir_api_key = reservoir_api_key
            
            # Check if we have at least one API key for real data
            has_api_keys = bool(opensea_api_key or reservoir_api_key)
            
            logger.info(f"API keys check - has_api_keys: {has_api_keys}, opensea: {bool(opensea_api_key)}, reservoir: {bool(reservoir_api_key)}")
            
            if not has_api_keys:
                return [{"type": "text", "text": "❌ Error: At least one API key (OpenSea or Reservoir) is required for real NFT data."}]
            
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
                logger.error(f"Unsupported action: '{action}' (type: {type(action)})")
                return [{"type": "text", "text": f"❌ Error: Unsupported action: '{action}'"}]
                
        except Exception as e:
            logger.error(f"NFT marketplace tool error: {e}")
            return [{"type": "text", "text": f"❌ Error: NFT marketplace operation failed: {str(e)}"}]
    
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
        """Get collection info from OpenSea API (with fallback to Reservoir)"""
        try:
            # Try Reservoir API first (more reliable)
            reservoir_url = f"{self.api_endpoints[chain]['reservoir']}/collections/v5?slug={collection_slug}"
            headers = {}
            
            reservoir_api_key = getattr(self, 'reservoir_api_key', None)
            if reservoir_api_key:
                headers["x-api-key"] = reservoir_api_key
            
            async with self.session.get(reservoir_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    collections = data.get("collections", [])
                    
                    if collections:
                        collection = collections[0]
                        collection_info = {
                            "collection_slug": collection_slug,
                            "chain": chain,
                            "name": collection.get("name", ""),
                            "description": collection.get("description", ""),
                            "total_supply": collection.get("tokenCount", 0),
                            "owners": collection.get("ownerCount", 0),
                            "floor_price": collection.get("floor", {}).get("value", 0),
                            "total_volume": collection.get("volume", {}).get("allTime", 0),
                            "created_date": collection.get("createdAt", ""),
                            "external_url": collection.get("externalUrl", ""),
                            "image_url": collection.get("image", ""),
                            "banner_image_url": collection.get("banner", ""),
                            "note": "Data via Reservoir API"
                        }
                        return [{"collection_info": collection_info}]
            
            # Fallback to OpenSea API
            url = f"{self.api_endpoints[chain]['opensea']}/collection/{collection_slug}"
            headers = {}
            
            opensea_api_key = getattr(self, 'opensea_api_key', None)
            if opensea_api_key:
                headers["X-API-KEY"] = opensea_api_key
            
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
                        "external_url": collection.get("external_url", ""),
                        "image_url": collection.get("image_url", ""),
                        "note": "Data via OpenSea API"
                    }
                    return [{"collection_info": collection_info}]
                else:
                    return [{"error": f"OpenSea API request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea collection info error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_collection_info(self, collection_slug: str) -> List[Dict[str, Any]]:
        """Get collection info from Magic Eden"""
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
                        "floor_price": data.get("floorPrice", 0),
                        "total_volume": data.get("volumeAll", 0),
                        "image_url": data.get("image", ""),
                        "note": "Data via Magic Eden API"
                    }
                    return [{"collection_info": collection_info}]
                else:
                    return [{"error": f"Magic Eden API request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden collection info error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_floor_price(self, collection_slug: str, chain: str) -> List[Dict[str, Any]]:
        """Get current floor price for a collection"""
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
        """Get floor price from OpenSea API"""
        try:
            # Try Reservoir API first
            reservoir_url = f"{self.api_endpoints[chain]['reservoir']}/collections/v5?slug={collection_slug}"
            headers = {}
            
            # Get API keys from the execute method's arguments
            reservoir_api_key = getattr(self, 'reservoir_api_key', None)
            if reservoir_api_key:
                headers["x-api-key"] = reservoir_api_key
            
            async with self.session.get(reservoir_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    collections = data.get("collections", [])
                    
                    if collections:
                        collection = collections[0]
                        floor_data = collection.get("floor", {})
                        
                        floor_price_info = {
                            "collection_slug": collection_slug,
                            "chain": chain,
                            "floor_price": floor_data.get("value", 0),
                            "floor_price_usd": floor_data.get("usd", 0),
                            "note": "Data via Reservoir API"
                        }
                        return [{"floor_price": floor_price_info}]
            
            # Fallback to OpenSea API
            url = f"{self.api_endpoints[chain]['opensea']}/collection/{collection_slug}/stats"
            headers = {}
            
            opensea_api_key = getattr(self, 'opensea_api_key', None)
            if opensea_api_key:
                headers["X-API-KEY"] = opensea_api_key
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data.get("stats", {})
                    
                    floor_price_info = {
                        "collection_slug": collection_slug,
                        "chain": chain,
                        "floor_price": stats.get("floor_price", 0),
                        "note": "Data via OpenSea API"
                    }
                    return [{"floor_price": floor_price_info}]
                else:
                    return [{"error": f"OpenSea floor price request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea floor price error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_floor_price(self, collection_slug: str) -> List[Dict[str, Any]]:
        """Get floor price from Magic Eden"""
        try:
            url = f"{self.api_endpoints['solana']['magic_eden']}/collections/{collection_slug}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    floor_price_info = {
                        "collection_slug": collection_slug,
                        "chain": "solana",
                        "floor_price": data.get("floorPrice", 0),
                        "note": "Data via Magic Eden API"
                    }
                    return [{"floor_price": floor_price_info}]
                else:
                    return [{"error": f"Magic Eden floor price request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden floor price error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_trading_volume(self, collection_slug: str, chain: str, time_period: str) -> List[Dict[str, Any]]:
        """Get trading volume for a collection"""
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
        """Get trading volume from OpenSea API"""
        try:
            # Try Reservoir API first
            reservoir_url = f"{self.api_endpoints[chain]['reservoir']}/collections/v5?slug={collection_slug}"
            headers = {}
            
            reservoir_api_key = getattr(self, 'reservoir_api_key', None)
            if reservoir_api_key:
                headers["x-api-key"] = reservoir_api_key
            
            async with self.session.get(reservoir_url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    collections = data.get("collections", [])
                    
                    if collections:
                        collection = collections[0]
                        volume_data = collection.get("volume", {})
                        
                        trading_volume_info = {
                            "collection_slug": collection_slug,
                            "chain": chain,
                            "time_period": time_period,
                            "volume": volume_data.get("1d" if time_period == "1d" else "7d" if time_period == "7d" else "30d", 0),
                            "volume_usd": volume_data.get("1d" if time_period == "1d" else "7d" if time_period == "7d" else "30d", 0),
                            "note": "Data via Reservoir API"
                        }
                        return [{"trading_volume": trading_volume_info}]
            
            # Fallback to OpenSea API
            url = f"{self.api_endpoints[chain]['opensea']}/collection/{collection_slug}/stats"
            headers = {}
            
            opensea_api_key = getattr(self, 'opensea_api_key', None)
            if opensea_api_key:
                headers["X-API-KEY"] = opensea_api_key
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data.get("stats", {})
                    
                    trading_volume_info = {
                        "collection_slug": collection_slug,
                        "chain": chain,
                        "time_period": time_period,
                        "volume": stats.get("total_volume", 0),
                        "note": "Data via OpenSea API"
                    }
                    return [{"trading_volume": trading_volume_info}]
                else:
                    return [{"error": f"OpenSea trading volume request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"OpenSea trading volume error: {e}")
            return [{"error": f"OpenSea API error: {str(e)}"}]
    
    async def _get_magic_eden_trading_volume(self, collection_slug: str, time_period: str) -> List[Dict[str, Any]]:
        """Get trading volume from Magic Eden"""
        try:
            url = f"{self.api_endpoints['solana']['magic_eden']}/collections/{collection_slug}"
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    trading_volume_info = {
                        "collection_slug": collection_slug,
                        "chain": "solana",
                        "time_period": time_period,
                        "volume": data.get("volumeAll", 0),
                        "note": "Data via Magic Eden API"
                    }
                    return [{"trading_volume": trading_volume_info}]
                else:
                    return [{"error": f"Magic Eden trading volume request failed: {response.status}"}]
        except Exception as e:
            logger.error(f"Magic Eden trading volume error: {e}")
            return [{"error": f"Magic Eden API error: {str(e)}"}]
    
    async def _get_recent_sales(self, collection_slug: str, chain: str, limit: int) -> List[Dict[str, Any]]:
        """Get recent sales for a collection"""
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
        """Get recent sales from OpenSea API"""
        try:
            url = f"{self.api_endpoints[chain]['opensea']}/events"
            params = {
                "collection_slug": collection_slug,
                "event_type": "successful",
                "limit": limit
            }
            headers = {}
            
            opensea_api_key = getattr(self, 'opensea_api_key', None)
            if opensea_api_key:
                headers["X-API-KEY"] = opensea_api_key
            
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
