import asyncio
import logging
import aiohttp
import json
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DefiLlamaTool(MCPTool):
    """DefiLlama MCP tool for accessing TVL, revenue, and price data"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.llama.fi"
        
    @property
    def name(self) -> str:
        return "defillama"
    
    @property
    def description(self) -> str:
        return "Access DefiLlama data including TVL, revenue, fees, and token prices across DeFi protocols"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_protocols",
                        "get_protocol_tvl",
                        "get_token_prices",
                        "get_chains",
                        "get_historical_tvl"
                    ],
                    "description": "Action to perform"
                },
                "protocol": {
                    "type": "string",
                    "description": "Protocol name (e.g., 'aave', 'uniswap')"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network"
                },
                "token_address": {
                    "type": "string",
                    "description": "Token contract address"
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
            protocol = arguments.get("protocol")
            chain = arguments.get("chain")
            token_address = arguments.get("token_address")
            
            # Validate action
            if not action:
                result = {"success": False, "error": "Action is required. Please select an action."}
            elif action == "get_protocols":
                result = await self._get_protocols()
            elif action == "get_protocol_tvl":
                if not protocol:
                    result = {"success": False, "error": "Protocol name is required"}
                else:
                    result = await self._get_protocol_tvl(protocol)
            elif action == "get_token_prices":
                if not token_address:
                    result = {"success": False, "error": "Token address is required"}
                else:
                    result = await self._get_token_prices(token_address)
            elif action == "get_chains":
                result = await self._get_chains()
            elif action == "get_historical_tvl":
                if not protocol:
                    result = {"success": False, "error": "Protocol name is required"}
                else:
                    result = await self._get_historical_tvl(protocol)
            else:
                result = {"success": False, "error": f"Unknown action: '{action}'. Valid actions are: get_protocols, get_protocol_tvl, get_token_prices, get_chains, get_historical_tvl"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_protocols(self) -> dict:
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
                        data = json.loads(text_content)
                        return {
                            "success": True,
                            "data": data,
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
            return {"success": False, "error": f"Failed to get protocols: {str(e)}"}
    
    async def _get_protocol_tvl(self, protocol: str) -> dict:
        try:
            url = f"{self.base_url}/protocol/{protocol}"
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
                        return {
                            "success": True,
                            "data": data,
                            "protocol": protocol,
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
            return {"success": False, "error": f"Failed to get protocol TVL: {str(e)}"}
    
    async def _get_token_prices(self, token_address: str) -> dict:
        try:
            url = f"{self.base_url}/prices/current/{token_address}"
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
                        return {
                            "success": True,
                            "data": data,
                            "token_address": token_address,
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
    
    async def _get_chains(self) -> dict:
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
                        data = json.loads(text_content)
                        return {
                            "success": True,
                            "data": data,
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
            return {"success": False, "error": f"Failed to get chains: {str(e)}"}
    
    async def _get_historical_tvl(self, protocol: str) -> dict:
        try:
            url = f"{self.base_url}/protocol/{protocol}/historical"
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
                        return {
                            "success": True,
                            "data": data,
                            "protocol": protocol,
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
            return {"success": False, "error": f"Failed to get historical TVL: {str(e)}"}


class DeribitTool(MCPTool):
    """Deribit MCP tool for accessing cryptocurrency derivatives data"""
    
    def __init__(self):
        self.session = None
        # Note: Deribit API key will be provided by user
        self.base_url = "https://www.deribit.com/api/v2"
        
    @property
    def name(self) -> str:
        return "deribit"
    
    @property
    def description(self) -> str:
        return "Access Deribit cryptocurrency derivatives data including options, futures, and trading information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_instruments",
                        "get_ticker",
                        "get_orderbook",
                        "get_trades",
                        "get_index_price"
                    ],
                    "description": "Action to perform"
                },
                "instrument_name": {
                    "type": "string",
                    "description": "Instrument name (e.g., 'BTC-PERPETUAL')"
                },
                "currency": {
                    "type": "string",
                    "enum": ["BTC", "ETH", "SOL"],
                    "default": "BTC",
                    "description": "Currency for the instrument"
                },
                "api_key": {
                    "type": "string",
                    "description": "Deribit API key (optional for public data)"
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
            api_key = arguments.get("api_key")
            instrument_name = arguments.get("instrument_name")
            currency = arguments.get("currency", "BTC")
            
            # Note: Most Deribit public endpoints don't require API key
            # API key is optional for public data access
            
            if action == "get_instruments":
                result = await self._get_instruments(currency)
            elif action == "get_ticker":
                if not instrument_name:
                    result = {"type": "text", "text": "❌ Error: Instrument name is required"}
                else:
                    result = await self._get_ticker(instrument_name)
            elif action == "get_orderbook":
                if not instrument_name:
                    result = {"type": "text", "text": "❌ Error: Instrument name is required"}
                else:
                    result = await self._get_orderbook(instrument_name)
            elif action == "get_trades":
                if not instrument_name:
                    result = {"type": "text", "text": "❌ Error: Instrument name is required"}
                else:
                    result = await self._get_trades(instrument_name)
            elif action == "get_index_price":
                result = await self._get_index_price(currency)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_instruments(self, currency: str) -> dict:
        try:
            url = f"{self.base_url}/public/get_instruments"
            params = {"currency": currency}
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "currency": currency,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get instruments: {str(e)}"}
    
    async def _get_ticker(self, instrument_name: str) -> dict:
        try:
            url = f"{self.base_url}/public/ticker"
            params = {"instrument_name": instrument_name}
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "instrument_name": instrument_name,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get ticker: {str(e)}"}
    
    async def _get_orderbook(self, instrument_name: str) -> dict:
        try:
            url = f"{self.base_url}/public/get_orderbook"
            params = {"instrument_name": instrument_name, "depth": 20}
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "instrument_name": instrument_name,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get orderbook: {str(e)}"}
    
    async def _get_trades(self, instrument_name: str) -> dict:
        try:
            url = f"{self.base_url}/public/get_last_trades_by_instrument"
            params = {"instrument_name": instrument_name, "count": 20}
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "instrument_name": instrument_name,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get trades: {str(e)}"}
    
    async def _get_index_price(self, currency: str) -> dict:
        try:
            url = f"{self.base_url}/public/get_index"
            params = {"index_name": f"{currency}_USDC"}
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "currency": currency,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get index price: {str(e)}"}


class ChainbaseTokenMetadataTool(MCPTool):
    """Tool for getting Chainbase token metadata"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.chainbase.online/v1"
        self.session = None
    
    @property
    def name(self) -> str:
        return "chainbase_token_metadata"
    
    @property
    def description(self) -> str:
        return "Get token metadata from Chainbase API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "contract_address": {
                    "type": "string",
                    "description": "Token contract address"
                },
                "api_key": {
                    "type": "string",
                    "description": "Chainbase API key (required)"
                }
            },
            "required": ["chain_id", "contract_address", "api_key"]
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
            chain_id = arguments.get("chain_id")
            contract_address = arguments.get("contract_address")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"success": False, "error": "Chainbase API key is required. Please provide your API key."}]
            
            result = await self._get_token_metadata(chain_id, contract_address, api_key)
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_token_metadata(self, chain_id: str, contract_address: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/token/metadata"
            params = {"chain_id": chain_id, "contract_address": contract_address}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Handle ChainBase API response format
                    if data.get("code") == 0 and data.get("message") == "ok":
                        return {
                            "success": True,
                            "data": data.get("data", {}),
                            "chain_id": chain_id,
                            "contract_address": contract_address,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"API Error: {data.get('message', 'Unknown error')} (Code: {data.get('code', 'N/A')})"
                        }
                else:
                    error_data = await response.text()
                    return {"success": False, "error": f"API request failed with status {response.status}: {error_data}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token metadata: {str(e)}"}


class ChainbaseTokenTopHoldersTool(MCPTool):
    """Tool for getting Chainbase top token holders"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.chainbase.online/v1"
        self.session = None
    
    @property
    def name(self) -> str:
        return "chainbase_token_top_holders"
    
    @property
    def description(self) -> str:
        return "Get top token holders from Chainbase API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "contract_address": {
                    "type": "string",
                    "description": "Token contract address"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results"
                },
                "api_key": {
                    "type": "string",
                    "description": "Chainbase API key (required)"
                }
            },
            "required": ["chain_id", "contract_address", "api_key"]
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
            chain_id = arguments.get("chain_id")
            contract_address = arguments.get("contract_address")
            limit = arguments.get("limit", 10)
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"success": False, "error": "Chainbase API key is required. Please provide your API key."}]
            
            result = await self._get_top_holders(chain_id, contract_address, limit, api_key)
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_top_holders(self, chain_id: str, contract_address: str, limit: int, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/token/holders"
            params = {"chain_id": chain_id, "contract_address": contract_address, "limit": limit}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Handle ChainBase API response format
                    if data.get("code") == 0 and data.get("message") == "ok":
                        return {
                            "success": True,
                            "data": data.get("data", {}),
                            "chain_id": chain_id,
                            "contract_address": contract_address,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"API Error: {data.get('message', 'Unknown error')} (Code: {data.get('code', 'N/A')})"
                        }
                else:
                    error_data = await response.text()
                    return {"success": False, "error": f"API request failed with status {response.status}: {error_data}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get top holders: {str(e)}"}


class ChainbaseTokenHoldersTool(MCPTool):
    """Tool for getting Chainbase token holders"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.chainbase.online/v1"
        self.session = None
    
    @property
    def name(self) -> str:
        return "chainbase_token_holders"
    
    @property
    def description(self) -> str:
        return "Get token holders from Chainbase API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "contract_address": {
                    "type": "string",
                    "description": "Token contract address"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results"
                },
                "api_key": {
                    "type": "string",
                    "description": "Chainbase API key (required)"
                }
            },
            "required": ["chain_id", "contract_address", "api_key"]
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
            chain_id = arguments.get("chain_id")
            contract_address = arguments.get("contract_address")
            limit = arguments.get("limit", 10)
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"success": False, "error": "Chainbase API key is required. Please provide your API key."}]
            
            result = await self._get_token_holders(chain_id, contract_address, limit, api_key)
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_token_holders(self, chain_id: str, contract_address: str, limit: int, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/token/holders"
            params = {"chain_id": chain_id, "contract_address": contract_address, "limit": limit}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Handle ChainBase API response format
                    if data.get("code") == 0 and data.get("message") == "ok":
                        return {
                            "success": True,
                            "data": data.get("data", {}),
                            "chain_id": chain_id,
                            "contract_address": contract_address,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"API Error: {data.get('message', 'Unknown error')} (Code: {data.get('code', 'N/A')})"
                        }
                else:
                    error_data = await response.text()
                    return {"success": False, "error": f"API request failed with status {response.status}: {error_data}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token holders: {str(e)}"}


class ChainbaseTokenPriceTool(MCPTool):
    """Tool for getting Chainbase token price"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.chainbase.online/v1"
        self.session = None
    
    @property
    def name(self) -> str:
        return "chainbase_token_price"
    
    @property
    def description(self) -> str:
        return "Get token price from Chainbase API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "contract_address": {
                    "type": "string",
                    "description": "Token contract address"
                },
                "api_key": {
                    "type": "string",
                    "description": "Chainbase API key (required)"
                }
            },
            "required": ["chain_id", "contract_address", "api_key"]
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
            chain_id = arguments.get("chain_id")
            contract_address = arguments.get("contract_address")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"success": False, "error": "Chainbase API key is required. Please provide your API key."}]
            
            result = await self._get_token_price(chain_id, contract_address, api_key)
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_token_price(self, chain_id: str, contract_address: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/token/price"
            params = {"chain_id": chain_id, "contract_address": contract_address}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Handle ChainBase API response format
                    if data.get("code") == 0 and data.get("message") == "ok":
                        return {
                            "success": True,
                            "data": data.get("data", {}),
                            "chain_id": chain_id,
                            "contract_address": contract_address,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"API Error: {data.get('message', 'Unknown error')} (Code: {data.get('code', 'N/A')})"
                        }
                else:
                    error_data = await response.text()
                    return {"success": False, "error": f"API request failed with status {response.status}: {error_data}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token price: {str(e)}"}


class ChainbaseTokenPriceHistoryTool(MCPTool):
    """Tool for getting Chainbase token price history"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.chainbase.online/v1"
        self.session = None
    
    @property
    def name(self) -> str:
        return "chainbase_token_price_history"
    
    @property
    def description(self) -> str:
        return "Get token price history from Chainbase API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "contract_address": {
                    "type": "string",
                    "description": "Token contract address"
                },
                "api_key": {
                    "type": "string",
                    "description": "Chainbase API key (required)"
                }
            },
            "required": ["chain_id", "contract_address", "api_key"]
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
            chain_id = arguments.get("chain_id")
            contract_address = arguments.get("contract_address")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"success": False, "error": "Chainbase API key is required. Please provide your API key."}]
            
            result = await self._get_token_price_history(chain_id, contract_address, api_key)
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_token_price_history(self, chain_id: str, contract_address: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/token/price/history"
            params = {"chain_id": chain_id, "contract_address": contract_address}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    # Handle ChainBase API response format
                    if data.get("code") == 0 and data.get("message") == "ok":
                        return {
                            "success": True,
                            "data": data.get("data", {}),
                            "chain_id": chain_id,
                            "contract_address": contract_address,
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"API Error: {data.get('message', 'Unknown error')} (Code: {data.get('code', 'N/A')})"
                        }
                else:
                    error_data = await response.text()
                    return {"success": False, "error": f"API request failed with status {response.status}: {error_data}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token price history: {str(e)}"}
