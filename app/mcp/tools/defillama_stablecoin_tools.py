import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DefiLlamaStablecoinTool(MCPTool):
    """DefiLlama Stablecoin MCP tool for accessing stablecoin data"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.llama.fi"
        
    @property
    def name(self) -> str:
        return "defillama_stablecoin"
    
    @property
    def description(self) -> str:
        return "Access DefiLlama stablecoin data including prices, market cap, historical data, and chain distribution"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_stablecoins",
                        "get_stablecoin_prices",
                        "get_stablecoin_chains",
                        "get_stablecoin_history",
                        "get_stablecoin_mcap_sum",
                        "get_stablecoin_historical_mcap"
                    ],
                    "description": "Action to perform"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network (for chain-specific queries)"
                },
                "stablecoin": {
                    "type": "string",
                    "description": "Stablecoin symbol or address (for specific stablecoin queries)"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days for historical data (default: 30)"
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
            stablecoin = arguments.get("stablecoin")
            days = arguments.get("days", 30)
            
            # Validate action
            if not action:
                result = {"success": False, "error": "Action is required. Please select an action."}
            elif action == "get_stablecoins":
                result = await self._get_stablecoins()
            elif action == "get_stablecoin_prices":
                result = await self._get_stablecoin_prices()
            elif action == "get_stablecoin_chains":
                result = await self._get_stablecoin_chains()
            elif action == "get_stablecoin_history":
                result = await self._get_stablecoin_history(days)
            elif action == "get_stablecoin_mcap_sum":
                result = await self._get_stablecoin_mcap_sum()
            elif action == "get_stablecoin_historical_mcap":
                result = await self._get_stablecoin_historical_mcap(days)
            else:
                result = {"success": False, "error": f"Unknown action: '{action}'. Valid actions are: get_stablecoins, get_stablecoin_prices, get_stablecoin_chains, get_stablecoin_history, get_stablecoin_mcap_sum, get_stablecoin_historical_mcap"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_stablecoins(self) -> dict:
        """Get all stablecoins data - using protocols endpoint filtered for stablecoins"""
        try:
            url = f"{self.base_url}/protocols"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        all_protocols = json.loads(text_content)
                        
                        # Filter for stablecoin-related protocols
                        stablecoin_protocols = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                name = protocol.get('name', '').lower()
                                category = protocol.get('category', '').lower()
                                if any(keyword in name or keyword in category for keyword in ['stablecoin', 'usd', 'usdc', 'usdt', 'dai', 'frax', 'lusd']):
                                    stablecoin_protocols.append(protocol)
                        
                        return {
                            "success": True,
                            "data": stablecoin_protocols,
                            "total_protocols": len(all_protocols),
                            "stablecoin_protocols": len(stablecoin_protocols),
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
            return {"success": False, "error": f"Failed to get stablecoins: {str(e)}"}
    
    async def _get_stablecoin_prices(self) -> dict:
        """Get stablecoin prices - using protocols endpoint with price data"""
        try:
            url = f"{self.base_url}/protocols"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        all_protocols = json.loads(text_content)
                        
                        # Filter for stablecoin-related protocols and extract price data
                        stablecoin_prices = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                name = protocol.get('name', '').lower()
                                category = protocol.get('category', '').lower()
                                if any(keyword in name or keyword in category for keyword in ['stablecoin', 'usd', 'usdc', 'usdt', 'dai', 'frax', 'lusd']):
                                    price_data = {
                                        'name': protocol.get('name'),
                                        'symbol': protocol.get('symbol'),
                                        'tvl': protocol.get('tvl', 0),
                                        'change_1d': protocol.get('change_1d', 0),
                                        'change_7d': protocol.get('change_7d', 0),
                                        'mcap': protocol.get('mcap', 0)
                                    }
                                    stablecoin_prices.append(price_data)
                        
                        return {
                            "success": True,
                            "data": stablecoin_prices,
                            "total_stablecoins": len(stablecoin_prices),
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
            return {"success": False, "error": f"Failed to get stablecoin prices: {str(e)}"}
    
    async def _get_stablecoin_chains(self) -> dict:
        """Get stablecoin distribution by chains - using chains endpoint"""
        try:
            url = f"{self.base_url}/chains"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        all_chains = json.loads(text_content)
                        
                        # Filter for chains that might have stablecoin activity
                        stablecoin_chains = []
                        for chain in all_chains:
                            if isinstance(chain, dict):
                                name = chain.get('name', '').lower()
                                tvl = chain.get('tvl', 0)
                                if tvl > 0:  # Only include chains with TVL
                                    chain_data = {
                                        'name': chain.get('name'),
                                        'tvl': tvl,
                                        'tokenSymbol': chain.get('tokenSymbol'),
                                        'gecko_id': chain.get('gecko_id')
                                    }
                                    stablecoin_chains.append(chain_data)
                        
                        # Sort by TVL descending
                        stablecoin_chains.sort(key=lambda x: x.get('tvl', 0), reverse=True)
                        
                        return {
                            "success": True,
                            "data": stablecoin_chains,
                            "total_chains": len(stablecoin_chains),
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
            return {"success": False, "error": f"Failed to get stablecoin chains: {str(e)}"}
    
    async def _get_stablecoin_history(self, days: int) -> dict:
        """Get stablecoin historical data - using protocols endpoint with historical data"""
        try:
            url = f"{self.base_url}/protocols"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        all_protocols = json.loads(text_content)
                        
                        # Filter for stablecoin-related protocols and extract historical data
                        stablecoin_history = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                name = protocol.get('name', '').lower()
                                category = protocol.get('category', '').lower()
                                if any(keyword in name or keyword in category for keyword in ['stablecoin', 'usd', 'usdc', 'usdt', 'dai', 'frax', 'lusd']):
                                    historical_data = {
                                        'name': protocol.get('name'),
                                        'symbol': protocol.get('symbol'),
                                        'tvl': protocol.get('tvl', 0),
                                        'change_1d': protocol.get('change_1d', 0),
                                        'change_7d': protocol.get('change_7d', 0),
                                        'change_1h': protocol.get('change_1h', 0),
                                        'mcap': protocol.get('mcap', 0),
                                        'chains': protocol.get('chains', [])
                                    }
                                    stablecoin_history.append(historical_data)
                        
                        return {
                            "success": True,
                            "data": stablecoin_history,
                            "days": days,
                            "total_stablecoins": len(stablecoin_history),
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
            return {"success": False, "error": f"Failed to get stablecoin history: {str(e)}"}
    
    async def _get_stablecoin_mcap_sum(self) -> dict:
        """Get total stablecoin market cap sum - calculated from protocols data"""
        try:
            url = f"{self.base_url}/protocols"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        all_protocols = json.loads(text_content)
                        
                        # Calculate total market cap for stablecoin-related protocols
                        total_mcap = 0
                        stablecoin_count = 0
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                name = protocol.get('name', '').lower()
                                category = protocol.get('category', '').lower()
                                if any(keyword in name or keyword in category for keyword in ['stablecoin', 'usd', 'usdc', 'usdt', 'dai', 'frax', 'lusd']):
                                    mcap = protocol.get('mcap', 0)
                                    if mcap and mcap > 0:
                                        total_mcap += mcap
                                        stablecoin_count += 1
                        
                        return {
                            "success": True,
                            "data": {
                                "total_market_cap": total_mcap,
                                "stablecoin_count": stablecoin_count,
                                "average_mcap": total_mcap / stablecoin_count if stablecoin_count > 0 else 0
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
            return {"success": False, "error": f"Failed to get stablecoin mcap sum: {str(e)}"}
    
    async def _get_stablecoin_historical_mcap(self, days: int) -> dict:
        """Get stablecoin historical market cap data - using protocols endpoint"""
        try:
            url = f"{self.base_url}/protocols"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    try:
                        text_content = await response.text()
                        all_protocols = json.loads(text_content)
                        
                        # Filter for stablecoin-related protocols and extract market cap data
                        stablecoin_mcap_data = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                name = protocol.get('name', '').lower()
                                category = protocol.get('category', '').lower()
                                if any(keyword in name or keyword in category for keyword in ['stablecoin', 'usd', 'usdc', 'usdt', 'dai', 'frax', 'lusd']):
                                    mcap_data = {
                                        'name': protocol.get('name'),
                                        'symbol': protocol.get('symbol'),
                                        'mcap': protocol.get('mcap', 0),
                                        'tvl': protocol.get('tvl', 0),
                                        'change_1d': protocol.get('change_1d', 0),
                                        'change_7d': protocol.get('change_7d', 0),
                                        'chains': protocol.get('chains', [])
                                    }
                                    stablecoin_mcap_data.append(mcap_data)
                        
                        # Sort by market cap descending
                        stablecoin_mcap_data.sort(key=lambda x: x.get('mcap', 0), reverse=True)
                        
                        return {
                            "success": True,
                            "data": stablecoin_mcap_data,
                            "days": days,
                            "total_stablecoins": len(stablecoin_mcap_data),
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
            return {"success": False, "error": f"Failed to get stablecoin historical mcap: {str(e)}"}
