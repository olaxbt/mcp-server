import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DefiLlamaFeesTool(MCPTool):
    """DefiLlama Fees MCP tool for accessing protocol fees and revenue data"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.llama.fi"
        
    @property
    def name(self) -> str:
        return "defillama_fees"
    
    @property
    def description(self) -> str:
        return "Access DefiLlama fees and revenue data including protocol earnings, fee analytics, and revenue tracking"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_fees_and_revenue_overview",
                        "get_fees_overview_by_chain",
                        "get_summary_fees",
                        "get_fees_historical",
                        "get_fees_by_protocol",
                        "get_revenue_by_protocol",
                        "get_fees_breakdown",
                        "get_top_fee_generators"
                    ],
                    "description": "Action to perform"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network (e.g., ethereum, polygon, bsc)"
                },
                "protocol": {
                    "type": "string",
                    "description": "Protocol name (e.g., uniswap, aave, compound)"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days for historical data (default: 30)"
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
            days = arguments.get("days", 30)
            limit = arguments.get("limit", 100)
            
            # Validate action
            if not action:
                result = {"success": False, "error": "Action is required. Please select an action."}
            elif action == "get_fees_and_revenue_overview":
                result = await self._get_fees_and_revenue_overview()
            elif action == "get_fees_overview_by_chain":
                if not chain:
                    result = {"success": False, "error": "Chain is required for this action"}
                else:
                    result = await self._get_fees_overview_by_chain(chain)
            elif action == "get_summary_fees":
                result = await self._get_summary_fees()
            elif action == "get_fees_historical":
                result = await self._get_fees_historical(days)
            elif action == "get_fees_by_protocol":
                if not protocol:
                    result = {"success": False, "error": "Protocol is required for this action"}
                else:
                    result = await self._get_fees_by_protocol(protocol, days)
            elif action == "get_revenue_by_protocol":
                if not protocol:
                    result = {"success": False, "error": "Protocol is required for this action"}
                else:
                    result = await self._get_revenue_by_protocol(protocol, days)
            elif action == "get_fees_breakdown":
                result = await self._get_fees_breakdown(limit)
            elif action == "get_top_fee_generators":
                result = await self._get_top_fee_generators(limit)
            else:
                result = {"success": False, "error": f"Unknown action: '{action}'. Valid actions are: get_fees_and_revenue_overview, get_fees_overview_by_chain, get_summary_fees, get_fees_historical, get_fees_by_protocol, get_revenue_by_protocol, get_fees_breakdown, get_top_fee_generators"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_fees_and_revenue_overview(self) -> dict:
        """Get fees and revenue overview - using overview/fees endpoint"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
                        
                        # Extract fees overview data
                        fees_data = {
                            "total24h": data.get("total24h", 0),
                            "total7d": data.get("total7d", 0),
                            "total30d": data.get("total30d", 0),
                            "total1y": data.get("total1y", 0),
                            "change_1d": data.get("change_1d", 0),
                            "change_7d": data.get("change_7d", 0),
                            "change_1m": data.get("change_1m", 0),
                            "totalAllTime": data.get("totalAllTime", 0),
                            "protocols": data.get("protocols", []),
                            "allChains": data.get("allChains", []),
                            "totalDataChart": data.get("totalDataChart", []),
                            "totalDataChartBreakdown": data.get("totalDataChartBreakdown", [])
                        }
                        
                        return {
                            "success": True,
                            "data": fees_data,
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
            return {"success": False, "error": f"Failed to get fees and revenue overview: {str(e)}"}
    
    async def _get_fees_overview_by_chain(self, chain: str) -> dict:
        """Get fees overview by chain - using overview/fees endpoint filtered by chain"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
                        
                        # Filter chains by name
                        all_chains = data.get("allChains", [])
                        chain_data = []
                        
                        if isinstance(all_chains, list):
                            for c in all_chains:
                                if isinstance(c, dict):
                                    chain_name = c.get("name", "").lower()
                                    if chain.lower() in chain_name:
                                        chain_data.append(c)
                        
                        return {
                            "success": True,
                            "data": {
                                "chain": chain,
                                "chains": chain_data,
                                "total_chains": len(chain_data)
                            },
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
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get fees overview by chain: {str(e)}"}
    
    async def _get_summary_fees(self) -> dict:
        """Get summary of fees - using overview/fees endpoint"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
            return {"success": False, "error": f"Failed to get summary fees: {str(e)}"}
    
    async def _get_fees_historical(self, days: int) -> dict:
        """Get fees historical data - using overview/fees endpoint with chart data"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
            return {"success": False, "error": f"Failed to get fees historical: {str(e)}"}
    
    async def _get_fees_by_protocol(self, protocol: str, days: int) -> dict:
        """Get fees by protocol - using overview/fees endpoint filtered by protocol"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
            return {"success": False, "error": f"Failed to get fees by protocol: {str(e)}"}
    
    async def _get_revenue_by_protocol(self, protocol: str, days: int) -> dict:
        """Get revenue by protocol - using overview/fees endpoint filtered by protocol"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
                        
                        # Filter protocols by name (revenue data is included in fees data)
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
                                "days": days,
                                "note": "Revenue data is included in fees data from DefiLlama API"
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
            return {"success": False, "error": f"Failed to get revenue by protocol: {str(e)}"}
    
    async def _get_fees_breakdown(self, limit: int) -> dict:
        """Get fees breakdown - using overview/fees endpoint with protocols data"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
                        
                        # Get protocols data as breakdown
                        protocols = data.get("protocols", [])
                        if limit and len(protocols) > limit:
                            protocols = protocols[:limit]
                        
                        breakdown_data = {
                            "protocols": protocols,
                            "total_protocols": len(protocols),
                            "total24h": data.get("total24h", 0),
                            "total7d": data.get("total7d", 0),
                            "total30d": data.get("total30d", 0)
                        }
                        
                        return {
                            "success": True,
                            "data": breakdown_data,
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
            return {"success": False, "error": f"Failed to get fees breakdown: {str(e)}"}
    
    async def _get_top_fee_generators(self, limit: int) -> dict:
        """Get top fee generators - using overview/fees endpoint with sorted protocols"""
        try:
            url = f"{self.base_url}/overview/fees"
            
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
                        
                        # Get protocols and sort by 24h fees
                        protocols = data.get("protocols", [])
                        if isinstance(protocols, list):
                            # Sort by total24h descending
                            protocols.sort(key=lambda x: x.get("total24h", 0), reverse=True)
                            if limit and len(protocols) > limit:
                                protocols = protocols[:limit]
                        
                        top_generators = {
                            "protocols": protocols,
                            "total_protocols": len(protocols),
                            "total24h": data.get("total24h", 0),
                            "total7d": data.get("total7d", 0),
                            "total30d": data.get("total30d", 0)
                        }
                        
                        return {
                            "success": True,
                            "data": top_generators,
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
            return {"success": False, "error": f"Failed to get top fee generators: {str(e)}"}
