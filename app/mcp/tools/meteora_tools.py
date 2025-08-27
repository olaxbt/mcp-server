import asyncio
import logging
import aiohttp
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class MeteoraTool(MCPTool):
    """Meteora MCP tool for accessing DEX data and dynamic AMM information"""
    
    def __init__(self):
        self.session = None
        # Note: Meteora API key will be provided by user
        self.base_url = "https://api.meteora.ag"
        
    @property
    def name(self) -> str:
        return "meteora"
    
    @property
    def description(self) -> str:
        return "Access Meteora DEX data including pools, tokens, and dynamic AMM analytics"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_pools",
                        "get_pool_info",
                        "get_tokens",
                        "get_trading_pairs",
                        "get_volume_data",
                        "get_liquidity_data"
                    ],
                    "description": "Action to perform"
                },
                "chain": {
                    "type": "string",
                    "enum": ["solana", "ethereum", "polygon"],
                    "default": "solana",
                    "description": "Blockchain network"
                },
                "pool_address": {
                    "type": "string",
                    "description": "Pool address for specific pool queries"
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
                    "description": "Meteora API key (required)"
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
            chain = arguments.get("chain", "solana")
            pool_address = arguments.get("pool_address")
            token_address = arguments.get("token_address")
            limit = arguments.get("limit", 20)
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Meteora API key is required. Please provide your API key."}]
            
            if action == "get_pools":
                result = await self._get_pools(chain, limit)
            elif action == "get_pool_info":
                if not pool_address:
                    result = {"type": "text", "text": "❌ Error: Pool address is required for get_pool_info"}
                else:
                    result = await self._get_pool_info(pool_address, chain)
            elif action == "get_tokens":
                result = await self._get_tokens(chain, limit)
            elif action == "get_trading_pairs":
                result = await self._get_trading_pairs(chain, limit)
            elif action == "get_volume_data":
                result = await self._get_volume_data(chain, limit)
            elif action == "get_liquidity_data":
                result = await self._get_liquidity_data(chain, limit)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_pools(self, chain: str, limit: int, **kwargs) -> dict:
        """Get available pools on Meteora"""
        try:
            url = f"{self.base_url}/pools"
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
            logger.error(f"Error getting pools: {e}")
            return {
                "success": False,
                "error": f"Failed to get pools: {str(e)}"
            }
    
    async def _get_pool_info(self, pool_address: str, chain: str, **kwargs) -> dict:
        """Get specific pool information"""
        try:
            url = f"{self.base_url}/pools/{pool_address}"
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
                        "pool_address": pool_address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting pool info: {e}")
            return {
                "success": False,
                "error": f"Failed to get pool info: {str(e)}"
            }
    
    async def _get_tokens(self, chain: str, limit: int, **kwargs) -> dict:
        """Get available tokens on Meteora"""
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
    
    async def _get_trading_pairs(self, chain: str, limit: int, **kwargs) -> dict:
        """Get trading pairs available on Meteora"""
        try:
            url = f"{self.base_url}/trading-pairs"
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
            logger.error(f"Error getting trading pairs: {e}")
            return {
                "success": False,
                "error": f"Failed to get trading pairs: {str(e)}"
            }
    
    async def _get_volume_data(self, chain: str, limit: int, **kwargs) -> dict:
        """Get volume data for Meteora pools"""
        try:
            url = f"{self.base_url}/volume"
            params = {"limit": limit}
            
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
            logger.error(f"Error getting volume data: {e}")
            return {
                "success": False,
                "error": f"Failed to get volume data: {str(e)}"
            }
    
    async def _get_liquidity_data(self, chain: str, limit: int, **kwargs) -> dict:
        """Get liquidity data for Meteora pools"""
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
            logger.error(f"Error getting liquidity data: {e}")
            return {
                "success": False,
                "error": f"Failed to get liquidity data: {str(e)}"
            }
