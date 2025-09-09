import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class PendleTool(MCPTool):
    """Pendle MCP tool for accessing Pendle Finance yield protocol data"""
    
    def __init__(self):
        self.session = None
        # Note: Pendle API key will be provided by user
        # Pendle uses different API versions for different endpoints
        self.base_urls = {
            "v1": "https://api-v2.pendle.finance/core/v1",
            "v2": "https://api-v2.pendle.finance/core/v2"
        }
        
    @property
    def name(self) -> str:
        return "pendle"
    
    @property
    def description(self) -> str:
        return "Access Pendle Finance yield protocol data including markets, yields, and liquidity information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_active_markets",
                        "get_market_data",
                        "get_historical_data",
                        "get_protocol_stats",
                        "get_yield_tokens",
                        "get_liquidity_data"
                    ],
                    "description": "Action to perform"
                },
                "chain": {
                    "type": "string",
                    "enum": ["ethereum", "arbitrum", "bsc"],
                    "default": "ethereum",
                    "description": "Blockchain network"
                },
                "market_address": {
                    "type": "string",
                    "description": "Market address for specific market queries"
                },
                "token_address": {
                    "type": "string",
                    "description": "Token address for token-specific queries"
                },
                "limit": {
                    "type": "integer",
                    "default": 20,
                    "description": "Maximum number of results"
                },
                "api_key": {
                    "type": "string",
                    "description": "Pendle API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            chain = arguments.get("chain", "ethereum")
            market_address = arguments.get("market_address")
            token_address = arguments.get("token_address")
            limit = arguments.get("limit", 20)
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Pendle API key is required. Please provide your API key."}]
            
            if action == "get_active_markets":
                result = await self._get_active_markets(chain, api_key)
            elif action == "get_market_data":
                if not market_address:
                    result = {"type": "text", "text": "❌ Error: Market address is required for get_market_data"}
                else:
                    result = await self._get_market_data(market_address, chain, api_key)
            elif action == "get_historical_data":
                if not market_address:
                    result = {"type": "text", "text": "❌ Error: Market address is required for get_historical_data"}
                else:
                    result = await self._get_historical_data(market_address, chain, api_key)
            elif action == "get_protocol_stats":
                result = await self._get_protocol_stats(chain, api_key)
            elif action == "get_yield_tokens":
                result = await self._get_yield_tokens(chain, api_key)
            elif action == "get_liquidity_data":
                result = await self._get_liquidity_data(chain, api_key)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_active_markets(self, chain: str, api_key: str) -> dict:
        """Get active markets on Pendle using v1 API"""
        try:
            # Map chain to Pendle's chain ID (1 = Ethereum, 42161 = Arbitrum, 56 = BSC)
            chain_id = {"ethereum": "1", "arbitrum": "42161", "bsc": "56"}.get(chain, "1")
            url = f"{self.base_urls['v1']}/{chain_id}/markets/active"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    # Read as text first, then parse as JSON (like Meteora)
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        return {
                            "success": True,
                            "data": data,
                            "chain": chain,
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting active markets: {e}")
            return {
                "success": False,
                "error": f"Failed to get active markets: {str(e)}"
            }
    
    async def _get_market_data(self, market_address: str, chain: str, api_key: str) -> dict:
        """Get latest market data using v2 API"""
        try:
            chain_id = {"ethereum": "1", "arbitrum": "42161", "bsc": "56"}.get(chain, "1")
            url = f"{self.base_urls['v2']}/{chain_id}/markets/{market_address}/data"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        return {
                            "success": True,
                            "data": data,
                            "market_address": market_address,
                            "chain": chain,
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting market data: {e}")
            return {
                "success": False,
                "error": f"Failed to get market data: {str(e)}"
            }
    
    async def _get_historical_data(self, market_address: str, chain: str, api_key: str) -> dict:
        """Get historical market data using v1 API"""
        try:
            chain_id = {"ethereum": "1", "arbitrum": "42161", "bsc": "56"}.get(chain, "1")
            url = f"{self.base_urls['v1']}/{chain_id}/markets/{market_address}/historical-data"
            params = {"time_frame": "week"}
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        return {
                            "success": True,
                            "data": data,
                            "market_address": market_address,
                            "chain": chain,
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            return {
                "success": False,
                "error": f"Failed to get historical data: {str(e)}"
            }
    
    async def _get_protocol_stats(self, chain: str, api_key: str) -> dict:
        """Get protocol statistics by aggregating data from active markets"""
        try:
            # Get active markets first to calculate protocol stats
            markets_result = await self._get_active_markets(chain, api_key)
            
            if not markets_result.get("success"):
                return {
                    "success": False,
                    "error": f"Failed to get markets data for protocol stats: {markets_result.get('error', 'Unknown error')}"
                }
            
            markets_data = markets_result.get("data", [])
            
            if not markets_data:
                return {
                    "success": True,
                    "data": {
                        "total_markets": 0,
                        "total_tvl": 0,
                        "average_apy": 0,
                        "total_volume": 0,
                        "chain": chain,
                        "message": "No active markets found"
                    },
                    "chain": chain,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Calculate protocol statistics
            total_markets = len(markets_data)
            total_tvl = 0
            total_volume = 0
            apy_values = []
            
            for market in markets_data:
                # Ensure market is a dictionary
                if not isinstance(market, dict):
                    continue
                    
                # Sum up TVL (assuming liquidity field exists)
                if 'liquidity' in market and market['liquidity']:
                    try:
                        total_tvl += float(market['liquidity'])
                    except (ValueError, TypeError):
                        pass
                
                # Sum up trading volume
                if 'tradingVolume' in market and market['tradingVolume']:
                    try:
                        total_volume += float(market['tradingVolume'])
                    except (ValueError, TypeError):
                        pass
                
                # Collect APY values for average calculation
                if 'apy' in market and market['apy']:
                    try:
                        apy_values.append(float(market['apy']))
                    except (ValueError, TypeError):
                        pass
            
            # Calculate average APY
            average_apy = sum(apy_values) / len(apy_values) if apy_values else 0
            
            protocol_stats = {
                "total_markets": total_markets,
                "total_tvl": round(total_tvl, 2),
                "average_apy": round(average_apy, 2),
                "total_volume": round(total_volume, 2),
                "chain": chain,
                "markets_analyzed": len(markets_data),
                "apy_markets_count": len(apy_values)
            }
            
            return {
                "success": True,
                "data": protocol_stats,
                "chain": chain,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting protocol stats: {e}")
            return {
                "success": False,
                "error": f"Failed to get protocol stats: {str(e)}"
            }
    
    async def _get_yield_tokens(self, chain: str, api_key: str) -> dict:
        """Get yield token information by extracting from active markets"""
        try:
            # Get active markets first to extract yield token information
            markets_result = await self._get_active_markets(chain, api_key)
            
            if not markets_result.get("success"):
                return {
                    "success": False,
                    "error": f"Failed to get markets data for yield tokens: {markets_result.get('error', 'Unknown error')}"
                }
            
            markets_data = markets_result.get("data", [])
            
            if not markets_data:
                return {
                    "success": True,
                    "data": {
                        "yield_tokens": [],
                        "total_tokens": 0,
                        "chain": chain,
                        "message": "No active markets found"
                    },
                    "chain": chain,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Extract unique yield tokens from markets
            yield_tokens = []
            seen_tokens = set()
            
            for market in markets_data:
                # Ensure market is a dictionary
                if not isinstance(market, dict):
                    continue
                    
                # Extract token information from market data
                token_info = {}
                
                if 'underlyingAsset' in market:
                    token_info['symbol'] = market['underlyingAsset']
                
                if 'marketAddress' in market:
                    token_info['market_address'] = market['marketAddress']
                
                if 'apy' in market and market['apy']:
                    try:
                        token_info['apy'] = float(market['apy'])
                    except (ValueError, TypeError):
                        pass
                
                if 'liquidity' in market and market['liquidity']:
                    try:
                        token_info['liquidity'] = float(market['liquidity'])
                    except (ValueError, TypeError):
                        pass
                
                if 'expiry' in market:
                    token_info['expiry'] = market['expiry']
                
                # Use market address as unique identifier
                token_id = market.get('marketAddress', market.get('underlyingAsset', ''))
                if token_id and token_id not in seen_tokens:
                    seen_tokens.add(token_id)
                    yield_tokens.append(token_info)
            
            return {
                "success": True,
                "data": {
                    "yield_tokens": yield_tokens,
                    "total_tokens": len(yield_tokens),
                    "chain": chain
                },
                "chain": chain,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting yield tokens: {e}")
            return {
                "success": False,
                "error": f"Failed to get yield tokens: {str(e)}"
            }
    
    async def _get_liquidity_data(self, chain: str, api_key: str) -> dict:
        """Get liquidity data by aggregating from active markets"""
        try:
            # Get active markets first to extract liquidity information
            markets_result = await self._get_active_markets(chain, api_key)
            
            if not markets_result.get("success"):
                return {
                    "success": False,
                    "error": f"Failed to get markets data for liquidity: {markets_result.get('error', 'Unknown error')}"
                }
            
            markets_data = markets_result.get("data", [])
            
            if not markets_data:
                return {
                    "success": True,
                    "data": {
                        "total_liquidity": 0,
                        "markets_with_liquidity": 0,
                        "average_liquidity": 0,
                        "liquidity_by_market": [],
                        "chain": chain,
                        "message": "No active markets found"
                    },
                    "chain": chain,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Calculate liquidity statistics
            total_liquidity = 0
            markets_with_liquidity = 0
            liquidity_by_market = []
            
            for market in markets_data:
                # Ensure market is a dictionary
                if not isinstance(market, dict):
                    continue
                    
                market_liquidity = 0
                if 'liquidity' in market and market['liquidity']:
                    try:
                        market_liquidity = float(market['liquidity'])
                        total_liquidity += market_liquidity
                        markets_with_liquidity += 1
                    except (ValueError, TypeError):
                        pass
                
                liquidity_by_market.append({
                    'market_address': market.get('marketAddress', 'Unknown'),
                    'underlying_asset': market.get('underlyingAsset', 'Unknown'),
                    'liquidity': market_liquidity,
                    'apy': float(market.get('apy', 0)) if market.get('apy') else 0
                })
            
            # Sort by liquidity (highest first)
            liquidity_by_market.sort(key=lambda x: x['liquidity'], reverse=True)
            
            average_liquidity = total_liquidity / markets_with_liquidity if markets_with_liquidity > 0 else 0
            
            return {
                "success": True,
                "data": {
                    "total_liquidity": round(total_liquidity, 2),
                    "markets_with_liquidity": markets_with_liquidity,
                    "average_liquidity": round(average_liquidity, 2),
                    "liquidity_by_market": liquidity_by_market,
                    "chain": chain
                },
                "chain": chain,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting liquidity data: {e}")
            return {
                "success": False,
                "error": f"Failed to get liquidity data: {str(e)}"
            }