import asyncio
import logging
import aiohttp
import json
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
        # Meteora uses different API endpoints for different services
        self.base_urls = {
            "damm": "https://damm-api.meteora.ag",
            "dammv2": "https://dammv2-api.meteora.ag", 
            "dlmm": "https://dlmm-api.meteora.ag",
            "merv2": "https://merv2-api.meteora.ag",
            "stake": "https://stake-for-fee-api.meteora.ag"
        }
        
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
                        "get_pool_metrics",
                        "get_pool_vesting",
                        "get_all_pairs",
                        "get_pair_swap_records",
                        "get_vaults",
                        "get_vault_info",
                        "get_apy_data",
                        "get_virtual_price"
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
                result = await self._get_pools(chain, limit, api_key)
            elif action == "get_pool_metrics":
                result = await self._get_pool_metrics(api_key)
            elif action == "get_pool_vesting":
                result = await self._get_pool_vesting(api_key)
            elif action == "get_all_pairs":
                result = await self._get_all_pairs(limit, api_key)
            elif action == "get_pair_swap_records":
                if not pool_address:
                    result = {"type": "text", "text": "❌ Error: Pair address is required for get_pair_swap_records"}
                else:
                    result = await self._get_pair_swap_records(pool_address, api_key)
            elif action == "get_vaults":
                result = await self._get_vaults(api_key)
            elif action == "get_vault_info":
                result = await self._get_vault_info(api_key)
            elif action == "get_apy_data":
                if not token_address:
                    result = {"type": "text", "text": "❌ Error: Token mint address is required for get_apy_data"}
                else:
                    result = await self._get_apy_data(token_address, api_key)
            elif action == "get_virtual_price":
                if not token_address:
                    result = {"type": "text", "text": "❌ Error: Token mint address is required for get_virtual_price"}
                else:
                    result = await self._get_virtual_price(token_address, api_key)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_pools(self, chain: str, limit: int, api_key: str) -> dict:
        """Get available pools on Meteora using DAMM API"""
        try:
            url = f"{self.base_urls['damm']}/pools"
            params = {"limit": limit}
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    # Read as text first, then parse as JSON
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
                        # If JSON parsing fails, return error with content preview
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
            logger.error(f"Error getting pools: {e}")
            return {
                "success": False,
                "error": f"Failed to get pools: {str(e)}"
            }
    
    async def _get_pool_metrics(self, api_key: str) -> dict:
        """Get pools metrics using DAMM API"""
        try:
            url = f"{self.base_urls['damm']}/pools-metrics"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting pool metrics: {e}")
            return {
                "success": False,
                "error": f"Failed to get pool metrics: {str(e)}"
            }
    
    async def _get_pool_vesting(self, api_key: str) -> dict:
        """Get pool vesting list using DAMM v2 API"""
        try:
            url = f"{self.base_urls['dammv2']}/pools/vesting"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting pool vesting: {e}")
            return {
                "success": False,
                "error": f"Failed to get pool vesting: {str(e)}"
            }
    
    async def _get_all_pairs(self, limit: int, api_key: str) -> dict:
        """Get all pairs with pagination using DLMM API"""
        try:
            url = f"{self.base_urls['dlmm']}/pair/all_with_pagination"
            params = {"limit": limit}
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting all pairs: {e}")
            return {
                "success": False,
                "error": f"Failed to get all pairs: {str(e)}"
            }
    
    async def _get_pair_swap_records(self, pair_address: str, api_key: str) -> dict:
        """Get pair swap records using DLMM API"""
        try:
            url = f"{self.base_urls['dlmm']}/pair/{pair_address}/analytic/swap_history"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "pair_address": pair_address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting pair swap records: {e}")
            return {
                "success": False,
                "error": f"Failed to get pair swap records: {str(e)}"
            }
    
    async def _get_vaults(self, api_key: str) -> dict:
        """Get all vaults using Stake API"""
        try:
            url = f"{self.base_urls['stake']}/vault/all"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting vaults: {e}")
            return {
                "success": False,
                "error": f"Failed to get vaults: {str(e)}"
            }
    
    async def _get_vault_info(self, api_key: str) -> dict:
        """Get vault info using MERV2 API"""
        try:
            url = f"{self.base_urls['merv2']}/vault_info"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    # Read as text first, then parse as JSON
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        return {
                            "success": True,
                            "data": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        # If JSON parsing fails, return error with content preview
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
            logger.error(f"Error getting vault info: {e}")
            return {
                "success": False,
                "error": f"Failed to get vault info: {str(e)}"
            }
    
    async def _get_apy_data(self, token_mint: str, api_key: str) -> dict:
        """Get APY data by time range using MERV2 API"""
        try:
            # For now, use current time and 24 hours ago as default range
            end_timestamp = int(datetime.now().timestamp())
            start_timestamp = end_timestamp - 86400  # 24 hours ago
            
            url = f"{self.base_urls['merv2']}/apy_filter/{token_mint}/{start_timestamp}/{end_timestamp}"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "token_mint": token_mint,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting APY data: {e}")
            return {
                "success": False,
                "error": f"Failed to get APY data: {str(e)}"
            }
    
    async def _get_virtual_price(self, token_mint: str, api_key: str) -> dict:
        """Get virtual price using MERV2 API"""
        try:
            # Use default strategy for now
            strategy = "default"
            url = f"{self.base_urls['merv2']}/virtual_price/{token_mint}/{strategy}"
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "token_mint": token_mint,
                        "strategy": strategy,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"API request failed with status {response.status}"
                    }
        except Exception as e:
            logger.error(f"Error getting virtual price: {e}")
            return {
                "success": False,
                "error": f"Failed to get virtual price: {str(e)}"
            }
