import asyncio
import logging
import aiohttp
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
        self.base_url = "https://api-v2.pendle.finance/core"
        
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
                        "get_markets",
                        "get_market_info",
                        "get_yields",
                        "get_liquidity",
                        "get_tokens",
                        "get_protocol_stats"
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
            
            if action == "get_markets":
                result = await self._get_markets(chain, limit)
            elif action == "get_market_info":
                if not market_address:
                    result = {"type": "text", "text": "❌ Error: Market address is required for get_market_info"}
                else:
                    result = await self._get_market_info(market_address, chain)
            elif action == "get_yields":
                result = await self._get_yields(chain, limit)
            elif action == "get_liquidity":
                result = await self._get_liquidity(chain, limit)
            elif action == "get_tokens":
                result = await self._get_tokens(chain, limit)
            elif action == "get_protocol_stats":
                result = await self._get_protocol_stats(chain)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_markets(self, chain: str, limit: int, **kwargs) -> dict:
        """Get available markets on Pendle"""
        try:
            url = f"{self.base_url}/markets"
            params = {"chain": chain, "limit": limit}
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting markets: {e}")
            return {
                "success": False,
                "error": f"Failed to get markets: {str(e)}"
            }
    
    async def _get_market_info(self, market_address: str, chain: str, **kwargs) -> dict:
        """Get specific market information"""
        try:
            url = f"{self.base_url}/markets/{market_address}"
            params = {"chain": chain}
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "market_address": market_address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting market info: {e}")
            return {
                "success": False,
                "error": f"Failed to get market info: {str(e)}"
            }
    
    async def _get_yields(self, chain: str, limit: int, **kwargs) -> dict:
        """Get yield data for Pendle markets"""
        try:
            url = f"{self.base_url}/yields"
            params = {"chain": chain, "limit": limit}
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting yields: {e}")
            return {
                "success": False,
                "error": f"Failed to get yields: {str(e)}"
            }
    
    async def _get_liquidity(self, chain: str, limit: int, **kwargs) -> dict:
        """Get liquidity data for Pendle markets"""
        try:
            url = f"{self.base_url}/liquidity"
            params = {"chain": chain, "limit": limit}
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting liquidity: {e}")
            return {
                "success": False,
                "error": f"Failed to get liquidity: {str(e)}"
            }
    
    async def _get_tokens(self, chain: str, limit: int, **kwargs) -> dict:
        """Get available tokens on Pendle"""
        try:
            url = f"{self.base_url}/tokens"
            params = {"chain": chain, "limit": limit}
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting tokens: {e}")
            return {
                "success": False,
                "error": f"Failed to get tokens: {str(e)}"
            }
    
    async def _get_protocol_stats(self, chain: str, **kwargs) -> dict:
        """Get protocol statistics for Pendle"""
        try:
            url = f"{self.base_url}/stats"
            params = {"chain": chain}
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting protocol stats: {e}")
            return {
                "success": False,
                "error": f"Failed to get protocol stats: {str(e)}"
            }
