import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DefiLlamaDexTool(MCPTool):
    """DefiLlama DEX MCP tool for accessing DEX volume and trading data"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.llama.fi"
        
    @property
    def name(self) -> str:
        return "defillama_dex"
    
    @property
    def description(self) -> str:
        return "Access DefiLlama DEX data including trading volumes, DEX rankings, and volume analytics"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_all_dexs_with_volumes",
                        "get_summary_dex_volume",
                        "get_dex_volumes_by_chain",
                        "get_all_options_volumes",
                        "get_options_volumes",
                        "get_summary_options_dex_volume",
                        "get_dex_volume_historical",
                        "get_dex_volume_by_protocol"
                    ],
                    "description": "Action to perform"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network (e.g., ethereum, polygon, bsc)"
                },
                "protocol": {
                    "type": "string",
                    "description": "DEX protocol name (e.g., uniswap, sushiswap, pancakeswap)"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days for historical data (default: 7)"
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
            days = arguments.get("days", 7)
            limit = arguments.get("limit", 100)
            
            # Validate action
            if not action:
                result = {"success": False, "error": "Action is required. Please select an action."}
            elif action == "get_all_dexs_with_volumes":
                result = await self._get_all_dexs_with_volumes(limit)
            elif action == "get_summary_dex_volume":
                result = await self._get_summary_dex_volume()
            elif action == "get_dex_volumes_by_chain":
                if not chain:
                    result = {"success": False, "error": "Chain is required for this action"}
                else:
                    result = await self._get_dex_volumes_by_chain(chain, limit)
            elif action == "get_all_options_volumes":
                result = await self._get_all_options_volumes(limit)
            elif action == "get_options_volumes":
                result = await self._get_options_volumes(limit)
            elif action == "get_summary_options_dex_volume":
                result = await self._get_summary_options_dex_volume()
            elif action == "get_dex_volume_historical":
                result = await self._get_dex_volume_historical(days)
            elif action == "get_dex_volume_by_protocol":
                if not protocol:
                    result = {"success": False, "error": "Protocol is required for this action"}
                else:
                    result = await self._get_dex_volume_by_protocol(protocol, days)
            else:
                result = {"success": False, "error": f"Unknown action: '{action}'. Valid actions are: get_all_dexs_with_volumes, get_summary_dex_volume, get_dex_volumes_by_chain, get_all_options_volumes, get_options_volumes, get_summary_options_dex_volume, get_dex_volume_historical, get_dex_volume_by_protocol"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_all_dexs_with_volumes(self, limit: int) -> dict:
        """Get all DEXs with their volumes - using overview/dexs endpoint"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Extract DEX data from the overview response
                        dex_data = {
                            "total24h": data.get("total24h", 0),
                            "total7d": data.get("total7d", 0),
                            "total30d": data.get("total30d", 0),
                            "change_1d": data.get("change_1d", 0),
                            "change_7d": data.get("change_7d", 0),
                            "change_1m": data.get("change_1m", 0),
                            "protocols": data.get("protocols", []),
                            "allChains": data.get("allChains", []),
                            "totalDataChart": data.get("totalDataChart", []),
                            "totalDataChartBreakdown": data.get("totalDataChartBreakdown", [])
                        }
                        
                        # Apply limit to protocols if needed
                        if limit and "protocols" in dex_data and isinstance(dex_data["protocols"], list):
                            dex_data["protocols"] = dex_data["protocols"][:limit]
                        
                        return {
                            "success": True,
                            "data": dex_data,
                            "limit": limit,
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
            return {"success": False, "error": f"Failed to get all DEXs with volumes: {str(e)}"}
    
    async def _get_summary_dex_volume(self) -> dict:
        """Get summary of DEX volumes - using overview/dexs endpoint"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Extract summary data
                        summary_data = {
                            "total24h": data.get("total24h", 0),
                            "total7d": data.get("total7d", 0),
                            "total30d": data.get("total30d", 0),
                            "total1y": data.get("total1y", 0),
                            "change_1d": data.get("change_1d", 0),
                            "change_7d": data.get("change_7d", 0),
                            "change_1m": data.get("change_1m", 0),
                            "totalAllTime": data.get("totalAllTime", 0),
                            "protocols_count": len(data.get("protocols", [])),
                            "chains_count": len(data.get("allChains", []))
                        }
                        
                        return {
                            "success": True,
                            "data": summary_data,
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
            return {"success": False, "error": f"Failed to get summary DEX volume: {str(e)}"}
    
    async def _get_dex_volumes_by_chain(self, chain: str, limit: int) -> dict:
        """Get DEX volumes by chain - using overview/dexs endpoint filtered by chain"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Filter protocols by chain
                        all_chains = data.get("allChains", [])
                        chain_protocols = []
                        
                        if isinstance(all_chains, list):
                            for chain_data in all_chains:
                                if isinstance(chain_data, dict):
                                    chain_name = chain_data.get("name", "").lower()
                                    if chain.lower() in chain_name:
                                        chain_protocols.append(chain_data)
                        
                        # Apply limit
                        if limit and len(chain_protocols) > limit:
                            chain_protocols = chain_protocols[:limit]
                        
                        return {
                            "success": True,
                            "data": {
                                "chain": chain,
                                "protocols": chain_protocols,
                                "total_protocols": len(chain_protocols)
                            },
                            "chain": chain,
                            "limit": limit,
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
            return {"success": False, "error": f"Failed to get DEX volumes by chain: {str(e)}"}
    
    async def _get_all_options_volumes(self, limit: int) -> dict:
        """Get all options volumes - using overview/dexs endpoint (options data not available)"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Options data is not available in the current API
                        # Return a message indicating this
                        return {
                            "success": True,
                            "data": {
                                "message": "Options volume data is not available in the current DefiLlama API",
                                "available_data": "DEX volume data is available via overview/dexs endpoint",
                                "total24h": data.get("total24h", 0),
                                "total7d": data.get("total7d", 0),
                                "total30d": data.get("total30d", 0)
                            },
                            "limit": limit,
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
            return {"success": False, "error": f"Failed to get all options volumes: {str(e)}"}
    
    async def _get_options_volumes(self, limit: int) -> dict:
        """Get options volumes list - using overview/dexs endpoint (options data not available)"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Options data is not available in the current API
                        return {
                            "success": True,
                            "data": {
                                "message": "Options volume data is not available in the current DefiLlama API",
                                "available_data": "DEX volume data is available via overview/dexs endpoint",
                                "protocols": data.get("protocols", [])[:limit] if limit else data.get("protocols", [])
                            },
                            "limit": limit,
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
            return {"success": False, "error": f"Failed to get options volumes: {str(e)}"}
    
    async def _get_summary_options_dex_volume(self) -> dict:
        """Get summary of options DEX volume - using overview/dexs endpoint (options data not available)"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Options data is not available in the current API
                        return {
                            "success": True,
                            "data": {
                                "message": "Options volume data is not available in the current DefiLlama API",
                                "available_data": "DEX volume data is available via overview/dexs endpoint",
                                "total24h": data.get("total24h", 0),
                                "total7d": data.get("total7d", 0),
                                "total30d": data.get("total30d", 0)
                            },
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
            return {"success": False, "error": f"Failed to get summary options DEX volume: {str(e)}"}
    
    async def _get_dex_volume_historical(self, days: int) -> dict:
        """Get DEX volume historical data - using overview/dexs endpoint with chart data"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Extract historical data from chart
                        historical_data = {
                            "totalDataChart": data.get("totalDataChart", []),
                            "totalDataChartBreakdown": data.get("totalDataChartBreakdown", []),
                            "days": days,
                            "total24h": data.get("total24h", 0),
                            "total7d": data.get("total7d", 0),
                            "total30d": data.get("total30d", 0),
                            "change_1d": data.get("change_1d", 0),
                            "change_7d": data.get("change_7d", 0),
                            "change_1m": data.get("change_1m", 0)
                        }
                        
                        return {
                            "success": True,
                            "data": historical_data,
                            "days": days,
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
            return {"success": False, "error": f"Failed to get DEX volume historical: {str(e)}"}
    
    async def _get_dex_volume_by_protocol(self, protocol: str, days: int) -> dict:
        """Get DEX volume by protocol - using overview/dexs endpoint filtered by protocol"""
        try:
            url = f"{self.base_url}/overview/dexs"
            
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        data = json.loads(text_content)
                        
                        # Filter protocols by name
                        all_protocols = data.get("protocols", [])
                        protocol_data = []
                        
                        if isinstance(all_protocols, list):
                            for p in all_protocols:
                                if isinstance(p, dict):
                                    name = p.get("name", "").lower()
                                    if protocol.lower() in name:
                                        protocol_data.append(p)
                        
                        return {
                            "success": True,
                            "data": {
                                "protocol": protocol,
                                "protocols": protocol_data,
                                "total_protocols": len(protocol_data),
                                "days": days
                            },
                            "protocol": protocol,
                            "days": days,
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
            return {"success": False, "error": f"Failed to get DEX volume by protocol: {str(e)}"}
