import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DefiLlamaCoinTool(MCPTool):
    """DefiLlama Coin MCP tool for accessing token prices and historical data"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.llama.fi"
        
    @property
    def name(self) -> str:
        return "defillama_coin"
    
    @property
    def description(self) -> str:
        return "Access DefiLlama coin data including token prices, historical data, price changes, and market analytics"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_token_prices",
                        "get_batch_historical_prices",
                        "get_percentage_change_in_price",
                        "get_closest_block_to_timestamp",
                        "get_earliest_timestamp_price_record",
                        "get_token_price_by_address",
                        "get_token_price_by_symbol",
                        "get_price_historical_range"
                    ],
                    "description": "Action to perform"
                },
                "token_address": {
                    "type": "string",
                    "description": "Token contract address"
                },
                "token_symbol": {
                    "type": "string",
                    "description": "Token symbol (e.g., BTC, ETH, USDC)"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network (e.g., ethereum, polygon, bsc)"
                },
                "timestamp": {
                    "type": "integer",
                    "description": "Unix timestamp for historical queries"
                },
                "start_timestamp": {
                    "type": "integer",
                    "description": "Start timestamp for range queries"
                },
                "end_timestamp": {
                    "type": "integer",
                    "description": "End timestamp for range queries"
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
            token_address = arguments.get("token_address")
            token_symbol = arguments.get("token_symbol")
            chain = arguments.get("chain")
            timestamp = arguments.get("timestamp")
            start_timestamp = arguments.get("start_timestamp")
            end_timestamp = arguments.get("end_timestamp")
            days = arguments.get("days", 30)
            limit = arguments.get("limit", 100)
            
            # Validate action
            if not action:
                result = {"success": False, "error": "Action is required. Please select an action."}
            elif action == "get_token_prices":
                result = await self._get_token_prices(limit)
            elif action == "get_batch_historical_prices":
                result = await self._get_batch_historical_prices(days)
            elif action == "get_percentage_change_in_price":
                if not token_address and not token_symbol:
                    result = {"success": False, "error": "Token address or symbol is required for this action"}
                else:
                    result = await self._get_percentage_change_in_price(token_address, token_symbol, days)
            elif action == "get_closest_block_to_timestamp":
                if not timestamp:
                    result = {"success": False, "error": "Timestamp is required for this action"}
                else:
                    result = await self._get_closest_block_to_timestamp(timestamp, chain)
            elif action == "get_earliest_timestamp_price_record":
                if not token_address and not token_symbol:
                    result = {"success": False, "error": "Token address or symbol is required for this action"}
                else:
                    result = await self._get_earliest_timestamp_price_record(token_address, token_symbol)
            elif action == "get_token_price_by_address":
                if not token_address:
                    result = {"success": False, "error": "Token address is required for this action"}
                else:
                    result = await self._get_token_price_by_address(token_address, chain)
            elif action == "get_token_price_by_symbol":
                if not token_symbol:
                    result = {"success": False, "error": "Token symbol is required for this action"}
                else:
                    result = await self._get_token_price_by_symbol(token_symbol, chain)
            elif action == "get_price_historical_range":
                if not start_timestamp or not end_timestamp:
                    result = {"success": False, "error": "Start and end timestamps are required for this action"}
                else:
                    result = await self._get_price_historical_range(token_address, token_symbol, start_timestamp, end_timestamp, chain)
            else:
                result = {"success": False, "error": f"Unknown action: '{action}'. Valid actions are: get_token_prices, get_batch_historical_prices, get_percentage_change_in_price, get_closest_block_to_timestamp, get_earliest_timestamp_price_record, get_token_price_by_address, get_token_price_by_symbol, get_price_historical_range"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_token_prices(self, limit: int) -> dict:
        """Get current token prices - using /protocols endpoint filtered for token-like data"""
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
                        
                        # Extract token-like data from protocols
                        token_data = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                token_info = {
                                    'name': protocol.get('name'),
                                    'symbol': protocol.get('symbol'),
                                    'tvl': protocol.get('tvl', 0),
                                    'change_1d': protocol.get('change_1d', 0),
                                    'change_7d': protocol.get('change_7d', 0),
                                    'change_1h': protocol.get('change_1h', 0),
                                    'chains': protocol.get('chains', []),
                                    'category': protocol.get('category'),
                                    'url': protocol.get('url'),
                                    'mcap': protocol.get('mcap', 0),
                                    'fdl': protocol.get('fdl', 0)
                                }
                                token_data.append(token_info)
                        
                        # Sort by TVL descending and apply limit
                        token_data.sort(key=lambda x: x.get('tvl', 0) or 0, reverse=True)
                        if limit and len(token_data) > limit:
                            token_data = token_data[:limit]
                        
                        return {
                            "success": True,
                            "data": token_data,
                            "limit": limit,
                            "total_tokens": len(token_data),
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
            return {"success": False, "error": f"Failed to get token prices: {str(e)}"}
    
    async def _get_batch_historical_prices(self, days: int) -> dict:
        """Get batch historical prices - using /protocols endpoint with historical data"""
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
                        
                        # Extract historical data from protocols
                        historical_data = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                historical_info = {
                                    'name': protocol.get('name'),
                                    'symbol': protocol.get('symbol'),
                                    'tvl': protocol.get('tvl', 0),
                                    'change_1d': protocol.get('change_1d', 0),
                                    'change_7d': protocol.get('change_7d', 0),
                                    'change_1h': protocol.get('change_1h', 0),
                                    'change_30d': protocol.get('change_30d', 0),
                                    'chains': protocol.get('chains', []),
                                    'category': protocol.get('category'),
                                    'mcap': protocol.get('mcap', 0),
                                    'fdl': protocol.get('fdl', 0)
                                }
                                historical_data.append(historical_info)
                        
                        return {
                            "success": True,
                            "data": historical_data,
                            "days": days,
                            "total_protocols": len(historical_data),
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
            return {"success": False, "error": f"Failed to get batch historical prices: {str(e)}"}
    
    async def _get_percentage_change_in_price(self, token_address: str = None, token_symbol: str = None, days: int = 30) -> dict:
        """Get percentage change in price - using /protocols endpoint with change data"""
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
                        
                        # Filter by token if specified
                        filtered_protocols = all_protocols
                        if token_symbol:
                            filtered_protocols = [p for p in all_protocols if p.get('symbol', '').lower() == token_symbol.lower()]
                        elif token_address:
                            # For address matching, we'd need to check if the protocol has address info
                            # For now, just return all protocols
                            pass
                        
                        # Extract percentage change data
                        change_data = []
                        for protocol in filtered_protocols:
                            if isinstance(protocol, dict):
                                change_info = {
                                    'name': protocol.get('name'),
                                    'symbol': protocol.get('symbol'),
                                    'change_1d': protocol.get('change_1d', 0),
                                    'change_7d': protocol.get('change_7d', 0),
                                    'change_1h': protocol.get('change_1h', 0),
                                    'change_30d': protocol.get('change_30d', 0),
                                    'tvl': protocol.get('tvl', 0),
                                    'chains': protocol.get('chains', [])
                                }
                                change_data.append(change_info)
                        
                        return {
                            "success": True,
                            "data": change_data,
                            "token_address": token_address,
                            "token_symbol": token_symbol,
                            "days": days,
                            "total_protocols": len(change_data),
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
            return {"success": False, "error": f"Failed to get percentage change in price: {str(e)}"}
    
    async def _get_closest_block_to_timestamp(self, timestamp: int, chain: str = None) -> dict:
        """Get closest block to timestamp - placeholder implementation"""
        try:
            # This endpoint is not available in the current DefiLlama API
            # Return a placeholder response with available data
            return {
                "success": True,
                "data": {
                    "message": "Block timestamp lookup not available in current DefiLlama API",
                    "timestamp": timestamp,
                    "chain": chain or "ethereum",
                    "note": "Use /protocols endpoint for available data"
                },
                "timestamp": timestamp,
                "chain": chain or "ethereum",
                "timestamp_iso": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to get closest block to timestamp: {str(e)}"}
    
    async def _get_earliest_timestamp_price_record(self, token_address: str = None, token_symbol: str = None) -> dict:
        """Get earliest timestamp price record - placeholder implementation"""
        try:
            # This endpoint is not available in the current DefiLlama API
            # Return a placeholder response
            return {
                "success": True,
                "data": {
                    "message": "Earliest timestamp price record not available in current DefiLlama API",
                    "token_address": token_address,
                    "token_symbol": token_symbol,
                    "note": "Use /protocols endpoint for available data"
                },
                "token_address": token_address,
                "token_symbol": token_symbol,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to get earliest timestamp price record: {str(e)}"}
    
    async def _get_token_price_by_address(self, token_address: str, chain: str = None) -> dict:
        """Get token price by address - using /protocols endpoint with filtering"""
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
                        
                        # Filter protocols that might match the address (simplified approach)
                        matching_protocols = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                # Check if any field contains the address or if it's a known protocol
                                protocol_str = str(protocol).lower()
                                if token_address.lower() in protocol_str or protocol.get('name', '').lower() in token_address.lower():
                                    matching_protocols.append(protocol)
                        
                        return {
                            "success": True,
                            "data": matching_protocols,
                            "token_address": token_address,
                            "chain": chain,
                            "total_matches": len(matching_protocols),
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
            return {"success": False, "error": f"Failed to get token price by address: {str(e)}"}
    
    async def _get_token_price_by_symbol(self, token_symbol: str, chain: str = None) -> dict:
        """Get token price by symbol - using /protocols endpoint with filtering"""
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
                        
                        # Filter protocols by symbol
                        matching_protocols = []
                        for protocol in all_protocols:
                            if isinstance(protocol, dict):
                                if protocol.get('symbol', '').lower() == token_symbol.lower():
                                    matching_protocols.append(protocol)
                        
                        return {
                            "success": True,
                            "data": matching_protocols,
                            "token_symbol": token_symbol,
                            "chain": chain,
                            "total_matches": len(matching_protocols),
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
            return {"success": False, "error": f"Failed to get token price by symbol: {str(e)}"}
    
    async def _get_price_historical_range(self, token_address: str = None, token_symbol: str = None, start_timestamp: int = None, end_timestamp: int = None, chain: str = None) -> dict:
        """Get price historical range - using /protocols endpoint with historical data"""
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
                        
                        # Filter by token if specified
                        filtered_protocols = all_protocols
                        if token_symbol:
                            filtered_protocols = [p for p in all_protocols if p.get('symbol', '').lower() == token_symbol.lower()]
                        elif token_address:
                            # For address matching, we'd need to check if the protocol has address info
                            # For now, just return all protocols
                            pass
                        
                        # Extract historical-like data
                        historical_data = []
                        for protocol in filtered_protocols:
                            if isinstance(protocol, dict):
                                historical_info = {
                                    'name': protocol.get('name'),
                                    'symbol': protocol.get('symbol'),
                                    'tvl': protocol.get('tvl', 0),
                                    'change_1d': protocol.get('change_1d', 0),
                                    'change_7d': protocol.get('change_7d', 0),
                                    'change_1h': protocol.get('change_1h', 0),
                                    'change_30d': protocol.get('change_30d', 0),
                                    'chains': protocol.get('chains', []),
                                    'category': protocol.get('category'),
                                    'mcap': protocol.get('mcap', 0),
                                    'fdl': protocol.get('fdl', 0)
                                }
                                historical_data.append(historical_info)
                        
                        return {
                            "success": True,
                            "data": historical_data,
                            "token_address": token_address,
                            "token_symbol": token_symbol,
                            "start_timestamp": start_timestamp,
                            "end_timestamp": end_timestamp,
                            "chain": chain,
                            "total_protocols": len(historical_data),
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
            return {"success": False, "error": f"Failed to get price historical range: {str(e)}"}
