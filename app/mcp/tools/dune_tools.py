import asyncio
import logging
import aiohttp
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DuneQueryTool(MCPTool):
    """Dune Query MCP tool for accessing blockchain data via Sim APIs"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.sim.dune.com/v1"
        
    @property
    def name(self) -> str:
        return "dune_query"
    
    @property
    def description(self) -> str:
        return "Access blockchain data and analytics via Dune Sim APIs including balances, transactions, and token information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_balances",
                        "get_activity",
                        "get_collectibles",
                        "get_transactions",
                        "get_token_info",
                        "get_token_holders"
                    ],
                    "description": "Action to perform"
                },
                "address": {
                    "type": "string",
                    "description": "Wallet address to query"
                },
                "chain": {
                    "type": "string",
                    "enum": ["ethereum", "polygon", "bsc", "arbitrum", "optimism", "avalanche"],
                    "default": "ethereum",
                    "description": "Blockchain network"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results"
                },
                "offset": {
                    "type": "string",
                    "description": "Pagination offset token"
                },
                "api_key": {
                    "type": "string",
                    "description": "Dune API key (required)"
                }
            },
            "required": ["action", "address", "api_key"]
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
            address = arguments.get("address")
            chain = arguments.get("chain", "ethereum")
            limit = arguments.get("limit", 10)
            offset = arguments.get("offset")
            api_key = arguments.get("api_key")
            
            if not address:
                return [{"success": False, "error": "Address is required"}]
            
            if not api_key:
                return [{"success": False, "error": "Dune API key is required. Please provide your API key."}]
            
            if action == "get_balances":
                result = await self._get_balances(address, chain, limit, offset, api_key)
            elif action == "get_activity":
                result = await self._get_activity(address, chain, limit, offset, api_key)
            elif action == "get_collectibles":
                result = await self._get_collectibles(address, chain, limit, offset, api_key)
            elif action == "get_transactions":
                result = await self._get_transactions(address, chain, limit, offset, api_key)
            elif action == "get_token_info":
                result = await self._get_token_info(address, chain, api_key)
            elif action == "get_token_holders":
                result = await self._get_token_holders(address, chain, limit, offset, api_key)
            else:
                result = {"success": False, "error": f"Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_balances(self, address: str, chain: str, limit: int, offset: str = None, api_key: str = None) -> dict:
        """Get token balances for an address"""
        try:
            if not api_key:
                return {
                    "success": False,
                    "error": "Dune API key is required. Please provide your API key."
                }
            
            url = f"{self.base_url}/evm/balances/{address}"
            params = {"limit": limit}
            if offset:
                params["offset"] = offset
            
            headers = {"X-Sim-Api-Key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "address": address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting balances: {e}")
            return {
                "success": False,
                "error": f"Failed to get balances: {str(e)}"
            }
    
    async def _get_activity(self, address: str, chain: str, limit: int, offset: str = None, api_key: str = None) -> dict:
        """Get activity for an address"""
        try:
            if not api_key:
                return {
                    "success": False,
                    "error": "Dune API key is required. Please provide your API key."
                }
            
            url = f"{self.base_url}/evm/activity/{address}"
            params = {"limit": limit}
            if offset:
                params["offset"] = offset
            
            headers = {"X-Sim-Api-Key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "address": address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting activity: {e}")
            return {
                "success": False,
                "error": f"Failed to get activity: {str(e)}"
            }
    
    async def _get_collectibles(self, address: str, chain: str, limit: int, offset: str = None, api_key: str = None) -> dict:
        """Get NFT collectibles for an address"""
        try:
            if not api_key:
                return {
                    "success": False,
                    "error": "Dune API key is required. Please provide your API key."
                }
            
            url = f"{self.base_url}/evm/collectibles/{address}"
            params = {"limit": limit}
            if offset:
                params["offset"] = offset
            
            headers = {"X-Sim-Api-Key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "address": address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting collectibles: {e}")
            return {
                "success": False,
                "error": f"Failed to get collectibles: {str(e)}"
            }
    
    async def _get_transactions(self, address: str, chain: str, limit: int, offset: str = None, api_key: str = None) -> dict:
        """Get transactions for an address"""
        try:
            if not api_key:
                return {
                    "success": False,
                    "error": "Dune API key is required. Please provide your API key."
                }
            
            url = f"{self.base_url}/evm/transactions/{address}"
            params = {"limit": limit}
            if offset:
                params["offset"] = offset
            
            headers = {"X-Sim-Api-Key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "address": address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting transactions: {e}")
            return {
                "success": False,
                "error": f"Failed to get transactions: {str(e)}"
            }
    
    async def _get_token_info(self, address: str, chain: str, api_key: str = None) -> dict:
        """Get token information"""
        try:
            if not api_key:
                return {
                    "success": False,
                    "error": "Dune API key is required. Please provide your API key."
                }
            
            url = f"{self.base_url}/evm/token/{address}"
            headers = {"X-Sim-Api-Key": api_key}
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "address": address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting token info: {e}")
            return {
                "success": False,
                "error": f"Failed to get token info: {str(e)}"
            }
    
    async def _get_token_holders(self, address: str, chain: str, limit: int, offset: str = None, api_key: str = None) -> dict:
        """Get token holders"""
        try:
            if not api_key:
                return {
                    "success": False,
                    "error": "Dune API key is required. Please provide your API key."
                }
            
            url = f"{self.base_url}/evm/token/{address}/holders"
            params = {"limit": limit}
            if offset:
                params["offset"] = offset
            
            headers = {"X-Sim-Api-Key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "address": address,
                        "chain": chain,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting token holders: {e}")
            return {
                "success": False,
                "error": f"Failed to get token holders: {str(e)}"
            }
