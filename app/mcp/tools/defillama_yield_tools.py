import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DefiLlamaYieldTool(MCPTool):
    """DefiLlama Yield MCP tool for accessing yield farming data"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://yields.llama.fi"
        
    @property
    def name(self) -> str:
        return "defillama_yield"
    
    @property
    def description(self) -> str:
        return "Access DefiLlama yield farming data including pools, APY rates, and yield opportunities"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_all_pools",
                        "get_pools_by_chain",
                        "get_pools_by_protocol",
                        "get_pool_history",
                        "get_pools_by_category",
                        "get_pools_by_token"
                    ],
                    "description": "Action to perform"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network (e.g., ethereum, polygon, bsc)"
                },
                "protocol": {
                    "type": "string",
                    "description": "Protocol name (e.g., aave, compound, curve)"
                },
                "category": {
                    "type": "string",
                    "description": "Pool category (e.g., lending, dex, liquid-staking)"
                },
                "token": {
                    "type": "string",
                    "description": "Token symbol or address"
                },
                "min_apy": {
                    "type": "number",
                    "description": "Minimum APY filter"
                },
                "max_apy": {
                    "type": "number",
                    "description": "Maximum APY filter"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results (default: 100)"
                }
            },
            "required": ["action"]
        }
    
    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            chain = arguments.get("chain")
            protocol = arguments.get("protocol")
            category = arguments.get("category")
            token = arguments.get("token")
            
            # Handle empty strings from frontend - convert to None
            min_apy = arguments.get("min_apy")
            if min_apy == "" or min_apy is None:
                min_apy = None
            else:
                try:
                    min_apy = float(min_apy)
                except (ValueError, TypeError):
                    min_apy = None
                    
            max_apy = arguments.get("max_apy")
            if max_apy == "" or max_apy is None:
                max_apy = None
            else:
                try:
                    max_apy = float(max_apy)
                except (ValueError, TypeError):
                    max_apy = None
                    
            limit = arguments.get("limit", 100)
            
            # Validate action
            if not action:
                result = {"success": False, "error": "Action is required. Please select an action."}
            elif action == "get_all_pools":
                result = await self._get_all_pools(limit, min_apy, max_apy)
            elif action == "get_pools_by_chain":
                if not chain:
                    result = {"success": False, "error": "Chain is required for this action"}
                else:
                    result = await self._get_pools_by_chain(chain, limit, min_apy, max_apy)
            elif action == "get_pools_by_protocol":
                if not protocol:
                    result = {"success": False, "error": "Protocol is required for this action"}
                else:
                    result = await self._get_pools_by_protocol(protocol, limit, min_apy, max_apy)
            elif action == "get_pool_history":
                result = await self._get_pool_history(limit)
            elif action == "get_pools_by_category":
                if not category:
                    result = {"success": False, "error": "Category is required for this action"}
                else:
                    result = await self._get_pools_by_category(category, limit, min_apy, max_apy)
            elif action == "get_pools_by_token":
                if not token:
                    result = {"success": False, "error": "Token is required for this action"}
                else:
                    result = await self._get_pools_by_token(token, limit, min_apy, max_apy)
            else:
                result = {"success": False, "error": f"Unknown action: '{action}'. Valid actions are: get_all_pools, get_pools_by_chain, get_pools_by_protocol, get_pool_history, get_pools_by_category, get_pools_by_token"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_all_pools(self, limit: int, min_apy: float = None, max_apy: float = None) -> dict:
        """Get all yield pools - using yields API"""
        try:
            url = f"{self.base_url}/pools"
            params = {}
            if limit:
                params["limit"] = limit
            if min_apy is not None:
                params["minApy"] = min_apy
            if max_apy is not None:
                params["maxApy"] = max_apy
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # The yields API returns {status: "success", data: [...]}
                        if isinstance(data, dict) and "data" in data:
                            pools = data["data"]
                        else:
                            pools = data
                        
                        # Ensure pools is a list and normalize all APY values to prevent comparison errors
                        if not isinstance(pools, list):
                            pools = []
                        
                        # Normalize APY values in the original data to prevent comparison errors
                        for pool in pools:
                            if isinstance(pool, dict):
                                apy = pool.get('apy')
                                if apy is not None:
                                    try:
                                        pool['apy'] = float(apy)
                                    except (ValueError, TypeError):
                                        pool['apy'] = 0.0
                        
                        # Apply additional filtering if needed
                        filtered_pools = []
                        for pool in pools:
                            if isinstance(pool, dict):
                                apy = pool.get('apy', 0)
                                
                                # Convert apy to float safely
                                try:
                                    apy_float = float(apy) if apy is not None else 0
                                except (ValueError, TypeError):
                                    apy_float = 0
                                
                                # Apply APY filters (API should handle this, but double-check)
                                if min_apy is not None and apy_float < min_apy:
                                    continue
                                if max_apy is not None and apy_float > max_apy:
                                    continue
                                
                                filtered_pools.append(pool)
                        
                        # Apply limit if not handled by API
                        if limit and len(filtered_pools) > limit:
                            filtered_pools = filtered_pools[:limit]
                        
                        return {
                            "success": True,
                            "data": filtered_pools,
                            "limit": limit,
                            "min_apy": min_apy,
                            "max_apy": max_apy,
                            "total_pools": len(filtered_pools),
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get all pools: {str(e)}"}
    
    async def _get_pools_by_chain(self, chain: str, limit: int, min_apy: float = None, max_apy: float = None) -> dict:
        """Get yield pools by chain - using yields API filtered by chain"""
        try:
            url = f"{self.base_url}/pools"
            params = {}
            if limit:
                params["limit"] = limit
            if min_apy is not None:
                params["minApy"] = min_apy
            if max_apy is not None:
                params["maxApy"] = max_apy
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # The yields API returns {status: "success", data: [...]}
                        if isinstance(data, dict) and "data" in data:
                            all_pools = data["data"]
                        else:
                            all_pools = data
                        
                        # Filter by chain
                        chain_pools = []
                        for pool in all_pools:
                            if isinstance(pool, dict):
                                pool_chain = pool.get('chain', '').lower()
                                if chain.lower() in pool_chain:
                                    apy = pool.get('apy', 0)
                                    
                                    # Convert apy to float safely
                                    try:
                                        apy_float = float(apy) if apy is not None else 0
                                    except (ValueError, TypeError):
                                        apy_float = 0
                                    
                                    # Apply APY filters
                                    if min_apy is not None and apy_float < min_apy:
                                        continue
                                    if max_apy is not None and apy_float > max_apy:
                                        continue
                                    
                                    chain_pools.append(pool)
                        
                        # Apply limit
                        if limit and len(chain_pools) > limit:
                            chain_pools = chain_pools[:limit]
                        
                        return {
                            "success": True,
                            "data": chain_pools,
                            "chain": chain,
                            "limit": limit,
                            "total_pools": len(chain_pools),
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pools by chain: {str(e)}"}
    
    async def _get_pools_by_protocol(self, protocol: str, limit: int, min_apy: float = None, max_apy: float = None) -> dict:
        """Get yield pools by protocol - using yields API filtered by project name"""
        try:
            url = f"{self.base_url}/pools"
            params = {}
            if limit:
                params["limit"] = limit
            if min_apy is not None:
                params["minApy"] = min_apy
            if max_apy is not None:
                params["maxApy"] = max_apy
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # The yields API returns {status: "success", data: [...]}
                        if isinstance(data, dict) and "data" in data:
                            all_pools = data["data"]
                        else:
                            all_pools = data
                        
                        # Filter by protocol/project
                        protocol_pools = []
                        for pool in all_pools:
                            if isinstance(pool, dict):
                                project = pool.get('project', '').lower()
                                if protocol.lower() in project:
                                    apy = pool.get('apy', 0)
                                    
                                    # Convert apy to float safely
                                    try:
                                        apy_float = float(apy) if apy is not None else 0
                                    except (ValueError, TypeError):
                                        apy_float = 0
                                    
                                    # Apply APY filters
                                    if min_apy is not None and apy_float < min_apy:
                                        continue
                                    if max_apy is not None and apy_float > max_apy:
                                        continue
                                    
                                    protocol_pools.append(pool)
                        
                        # Apply limit
                        if limit and len(protocol_pools) > limit:
                            protocol_pools = protocol_pools[:limit]
                        
                        return {
                            "success": True,
                            "data": protocol_pools,
                            "protocol": protocol,
                            "limit": limit,
                            "total_pools": len(protocol_pools),
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pools by protocol: {str(e)}"}
    
    async def _get_pool_history(self, limit: int) -> dict:
        """Get pool historical data - using yields API with historical data"""
        try:
            url = f"{self.base_url}/pools"
            params = {}
            if limit:
                params["limit"] = limit
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # The yields API returns {status: "success", data: [...]}
                        if isinstance(data, dict) and "data" in data:
                            pools = data["data"]
                        else:
                            pools = data
                        
                        # Extract historical data from pools
                        historical_data = []
                        for pool in pools:
                            if isinstance(pool, dict):
                                history_item = {
                                    'pool': pool.get('pool'),
                                    'chain': pool.get('chain'),
                                    'project': pool.get('project'),
                                    'symbol': pool.get('symbol'),
                                    'tvlUsd': pool.get('tvlUsd', 0),
                                    'apy': pool.get('apy', 0),
                                    'apyBase': pool.get('apyBase', 0),
                                    'apyReward': pool.get('apyReward', 0),
                                    'apyPct1D': pool.get('apyPct1D', 0),
                                    'apyPct7D': pool.get('apyPct7D', 0),
                                    'apyPct30D': pool.get('apyPct30D', 0),
                                    'apyMean30d': pool.get('apyMean30d', 0),
                                    'stablecoin': pool.get('stablecoin', False),
                                    'ilRisk': pool.get('ilRisk'),
                                    'exposure': pool.get('exposure'),
                                    'predictions': pool.get('predictions', {}),
                                    'mu': pool.get('mu'),
                                    'sigma': pool.get('sigma'),
                                    'count': pool.get('count'),
                                    'outlier': pool.get('outlier', False)
                                }
                                historical_data.append(history_item)
                        
                        # Apply limit
                        if limit and len(historical_data) > limit:
                            historical_data = historical_data[:limit]
                        
                        return {
                            "success": True,
                            "data": historical_data,
                            "limit": limit,
                            "total_pools": len(historical_data),
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pool history: {str(e)}"}
    
    async def _get_pools_by_category(self, category: str, limit: int, min_apy: float = None, max_apy: float = None) -> dict:
        """Get yield pools by category - using yields API with category filtering"""
        try:
            url = f"{self.base_url}/pools"
            params = {"category": category}
            if limit:
                params["limit"] = limit
            if min_apy is not None:
                params["minApy"] = min_apy
            if max_apy is not None:
                params["maxApy"] = max_apy
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # The yields API returns {status: "success", data: [...]}
                        if isinstance(data, dict) and "data" in data:
                            pools = data["data"]
                        else:
                            pools = data
                        
                        # Apply additional filtering if needed
                        filtered_pools = []
                        for pool in pools:
                            if isinstance(pool, dict):
                                apy = pool.get('apy', 0)
                                
                                # Convert apy to float safely
                                try:
                                    apy_float = float(apy) if apy is not None else 0
                                except (ValueError, TypeError):
                                    apy_float = 0
                                
                                # Apply APY filters (API should handle this, but double-check)
                                if min_apy is not None and apy_float < min_apy:
                                    continue
                                if max_apy is not None and apy_float > max_apy:
                                    continue
                                
                                filtered_pools.append(pool)
                        
                        # Apply limit if not handled by API
                        if limit and len(filtered_pools) > limit:
                            filtered_pools = filtered_pools[:limit]
                        
                        return {
                            "success": True,
                            "data": filtered_pools,
                            "category": category,
                            "limit": limit,
                            "total_pools": len(filtered_pools),
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pools by category: {str(e)}"}
    
    async def _get_pools_by_token(self, token: str, limit: int, min_apy: float = None, max_apy: float = None) -> dict:
        """Get yield pools by token - using yields API with token filtering"""
        try:
            url = f"{self.base_url}/pools"
            params = {"token": token}
            if limit:
                params["limit"] = limit
            if min_apy is not None:
                params["minApy"] = min_apy
            if max_apy is not None:
                params["maxApy"] = max_apy
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # The yields API returns {status: "success", data: [...]}
                        if isinstance(data, dict) and "data" in data:
                            pools = data["data"]
                        else:
                            pools = data
                        
                        # Apply additional filtering if needed
                        filtered_pools = []
                        for pool in pools:
                            if isinstance(pool, dict):
                                apy = pool.get('apy', 0)
                                
                                # Convert apy to float safely
                                try:
                                    apy_float = float(apy) if apy is not None else 0
                                except (ValueError, TypeError):
                                    apy_float = 0
                                
                                # Apply APY filters (API should handle this, but double-check)
                                if min_apy is not None and apy_float < min_apy:
                                    continue
                                if max_apy is not None and apy_float > max_apy:
                                    continue
                                
                                filtered_pools.append(pool)
                        
                        # Apply limit if not handled by API
                        if limit and len(filtered_pools) > limit:
                            filtered_pools = filtered_pools[:limit]
                        
                        return {
                            "success": True,
                            "data": filtered_pools,
                            "token": token,
                            "limit": limit,
                            "total_pools": len(filtered_pools),
                            "timestamp": datetime.now().isoformat()
                        }
                    except Exception as json_error:
                        content_type = response.headers.get('content-type', 'Not specified')
                        return {
                            "success": False,
                            "error": f"Failed to parse JSON response (type: {content_type}). Error: {str(json_error)}. Response: {text_content[:200]}..."
                        }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pools by token: {str(e)}"}
