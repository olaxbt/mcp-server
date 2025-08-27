import asyncio
import logging
import aiohttp
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class PumpFunDataTool(MCPTool):
    """PumpFun Data MCP tool for accessing Solana token launch data"""
    
    def __init__(self):
        self.session = None
        # Note: PumpFun Data API key will be provided by user
        self.base_url = "https://api.pumpfun.com"
        
    @property
    def name(self) -> str:
        return "pumpfun_data"
    
    @property
    def description(self) -> str:
        return "Access PumpFun data for Solana token launches, social sentiment, and pump detection"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_pump_detection",
                        "get_social_sentiment",
                        "get_token_launches",
                        "get_market_alerts",
                        "get_trending_coins"
                    ],
                    "description": "Action to perform"
                },
                "symbol": {
                    "type": "string",
                    "description": "Token symbol"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results"
                },
                "api_key": {
                    "type": "string",
                    "description": "PumpFun Data API key (required)"
                }
            },
            "required": ["action", "api_key"]
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
            symbol = arguments.get("symbol")
            limit = arguments.get("limit", 10)
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: PumpFun Data API key is required. Please provide your API key."}]
            
            if action == "get_pump_detection":
                result = await self._get_pump_detection(symbol, limit, **arguments)
            elif action == "get_social_sentiment":
                result = await self._get_social_sentiment(symbol, limit, **arguments)
            elif action == "get_token_launches":
                result = await self._get_token_launches(limit, **arguments)
            elif action == "get_market_alerts":
                result = await self._get_market_alerts(limit, **arguments)
            elif action == "get_trending_coins":
                result = await self._get_trending_coins(limit, **arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_pump_detection(self, symbol: str, limit: int, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/pump-detection"
            params = {"limit": limit}
            if symbol:
                params["symbol"] = symbol
            
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
                        "symbol": symbol,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pump detection: {str(e)}"}
    
    async def _get_social_sentiment(self, symbol: str, limit: int, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/social-sentiment"
            params = {"limit": limit}
            if symbol:
                params["symbol"] = symbol
            
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
                        "symbol": symbol,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get social sentiment: {str(e)}"}
    
    async def _get_token_launches(self, limit: int, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/token-launches"
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
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token launches: {str(e)}"}
    
    async def _get_market_alerts(self, limit: int, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/market-alerts"
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
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get market alerts: {str(e)}"}
    
    async def _get_trending_coins(self, limit: int, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/trending-coins"
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
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get trending coins: {str(e)}"}


class CoinDeskAssetsTool(MCPTool):
    """CoinDesk Assets MCP tool for accessing cryptocurrency asset data"""
    
    def __init__(self):
        self.session = None
        # Note: CoinDesk Assets API key will be provided by user
        self.base_url = "https://api.coindesk.com/v1"
        
    @property
    def name(self) -> str:
        return "coindesk_assets"
    
    @property
    def description(self) -> str:
        return "Access CoinDesk asset data including prices, market data, and cryptocurrency information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_asset_info",
                        "get_asset_prices",
                        "get_market_data",
                        "get_asset_news",
                        "get_asset_metrics"
                    ],
                    "description": "Action to perform"
                },
                "asset": {
                    "type": "string",
                    "description": "Asset symbol (e.g., 'BTC', 'ETH')"
                },
                "currency": {
                    "type": "string",
                    "default": "USD",
                    "description": "Target currency"
                },
                "api_key": {
                    "type": "string",
                    "description": "CoinDesk Assets API key (required)"
                }
            },
            "required": ["action", "asset", "api_key"]
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
            asset = arguments.get("asset")
            currency = arguments.get("currency", "USD")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: CoinDesk Assets API key is required. Please provide your API key."}]
            
            if action == "get_asset_info":
                result = await self._get_asset_info(asset, **arguments)
            elif action == "get_asset_prices":
                result = await self._get_asset_prices(asset, currency, **arguments)
            elif action == "get_market_data":
                result = await self._get_market_data(asset, **arguments)
            elif action == "get_asset_news":
                result = await self._get_asset_news(asset, **arguments)
            elif action == "get_asset_metrics":
                result = await self._get_asset_metrics(asset, **arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_asset_info(self, asset: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/assets/{asset}"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "asset": asset,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get asset info: {str(e)}"}
    
    async def _get_asset_prices(self, asset: str, currency: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/assets/{asset}/prices"
            params = {"currency": currency}
            
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
                        "asset": asset,
                        "currency": currency,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get asset prices: {str(e)}"}
    
    async def _get_market_data(self, asset: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/assets/{asset}/market-data"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "asset": asset,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get market data: {str(e)}"}
    
    async def _get_asset_news(self, asset: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/assets/{asset}/news"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "asset": asset,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get asset news: {str(e)}"}
    
    async def _get_asset_metrics(self, asset: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/assets/{asset}/metrics"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "asset": asset,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get asset metrics: {str(e)}"}


class BNBChainTool(MCPTool):
    """BNB Chain MCP tool for accessing BSC and opBNB data"""
    
    def __init__(self):
        self.session = None
        # Note: BNBChain API key will be provided by user
        self.base_url = "https://api.bnbchain.org"
        
    @property
    def name(self) -> str:
        return "bnbchain"
    
    @property
    def description(self) -> str:
        return "Access BNB Chain data including BSC and opBNB blockchain information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_block_info",
                        "get_transaction",
                        "get_account_balance",
                        "get_token_info",
                        "get_contract_info"
                    ],
                    "description": "Action to perform"
                },
                "network": {
                    "type": "string",
                    "enum": ["bsc", "opbnb"],
                    "default": "bsc",
                    "description": "BNB Chain network"
                },
                "block_number": {
                    "type": "string",
                    "description": "Block number or hash"
                },
                "address": {
                    "type": "string",
                    "description": "Account or contract address"
                },
                "api_key": {
                    "type": "string",
                    "description": "BNBChain API key (required)"
                }
            },
            "required": ["action", "api_key"]
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
            network = arguments.get("network", "bsc")
            block_number = arguments.get("block_number")
            address = arguments.get("address")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: BNBChain API key is required. Please provide your API key."}]
            
            if action == "get_block_info":
                if not block_number:
                    result = {"type": "text", "text": "❌ Error: Block number is required"}
                else:
                    result = await self._get_block_info(network, block_number, **arguments)
            elif action == "get_transaction":
                if not address:
                    result = {"type": "text", "text": "❌ Error: Transaction hash is required"}
                else:
                    result = await self._get_transaction(network, address, **arguments)
            elif action == "get_account_balance":
                if not address:
                    result = {"type": "text", "text": "❌ Error: Account address is required"}
                else:
                    result = await self._get_account_balance(network, address, **arguments)
            elif action == "get_token_info":
                if not address:
                    result = {"type": "text", "text": "❌ Error: Token address is required"}
                else:
                    result = await self._get_token_info(network, address, **arguments)
            elif action == "get_contract_info":
                if not address:
                    result = {"type": "text", "text": "❌ Error: Contract address is required"}
                else:
                    result = await self._get_contract_info(network, address, **arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_block_info(self, network: str, block_number: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/{network}/block/{block_number}"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "network": network,
                        "block_number": block_number,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get block info: {str(e)}"}
    
    async def _get_transaction(self, network: str, tx_hash: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/{network}/transaction/{tx_hash}"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "network": network,
                        "tx_hash": tx_hash,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get transaction: {str(e)}"}
    
    async def _get_account_balance(self, network: str, address: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/{network}/account/{address}/balance"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "network": network,
                        "address": address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get account balance: {str(e)}"}
    
    async def _get_token_info(self, network: str, address: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/{network}/token/{address}"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "network": network,
                        "address": address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token info: {str(e)}"}
    
    async def _get_contract_info(self, network: str, address: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/{network}/contract/{address}"
            
            headers = {}
            api_key = kwargs.get("api_key")
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            session = await self._get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "network": network,
                        "address": address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get contract info: {str(e)}"}


class ChainbaseBasicTool(MCPTool):
    """Chainbase Basic MCP tool for accessing basic blockchain data"""
    
    def __init__(self):
        self.session = None
        # Note: ChainBase API key will be provided by user
        self.base_url = "https://api.chainbase.online/v1"
        
    @property
    def name(self) -> str:
        return "chainbase_basic"
    
    @property
    def description(self) -> str:
        return "Access Chainbase basic blockchain data including blocks, transactions, and network information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_latest_block",
                        "get_block_by_number",
                        "get_block_by_hash",
                        "get_transaction",
                        "get_network_info"
                    ],
                    "description": "Action to perform"
                },
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "block_number": {
                    "type": "string",
                    "description": "Block number"
                },
                "block_hash": {
                    "type": "string",
                    "description": "Block hash"
                },
                "tx_hash": {
                    "type": "string",
                    "description": "Transaction hash"
                },
                "api_key": {
                    "type": "string",
                    "description": "ChainBase API key (required)"
                }
            },
            "required": ["action", "chain_id", "api_key"]
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
            chain_id = arguments.get("chain_id")
            block_number = arguments.get("block_number")
            block_hash = arguments.get("block_hash")
            tx_hash = arguments.get("tx_hash")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: ChainBase API key is required. Please provide your API key."}]
            
            if action == "get_latest_block":
                result = await self._get_latest_block(chain_id, **arguments)
            elif action == "get_block_by_number":
                if not block_number:
                    result = {"type": "text", "text": "❌ Error: Block number is required"}
                else:
                    result = await self._get_block_by_number(chain_id, block_number, **arguments)
            elif action == "get_block_by_hash":
                if not block_hash:
                    result = {"type": "text", "text": "❌ Error: Block hash is required"}
                else:
                    result = await self._get_block_by_hash(chain_id, block_hash, **arguments)
            elif action == "get_transaction":
                if not tx_hash:
                    result = {"type": "text", "text": "❌ Error: Transaction hash is required"}
                else:
                    result = await self._get_transaction(chain_id, tx_hash, **arguments)
            elif action == "get_network_info":
                result = await self._get_network_info(chain_id, **arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_latest_block(self, chain_id: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/block/latest"
            params = {"chain_id": chain_id}
            api_key = kwargs.get("api_key")
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get latest block: {str(e)}"}
    
    async def _get_block_by_number(self, chain_id: str, block_number: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/block/number"
            params = {"chain_id": chain_id, "block_number": block_number}
            api_key = kwargs.get("api_key")
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "block_number": block_number,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get block by number: {str(e)}"}
    
    async def _get_block_by_hash(self, chain_id: str, block_hash: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/block/hash"
            params = {"chain_id": chain_id, "block_hash": block_hash}
            api_key = kwargs.get("api_key")
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "block_hash": block_hash,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get block by hash: {str(e)}"}
    
    async def _get_transaction(self, chain_id: str, tx_hash: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/transaction"
            params = {"chain_id": chain_id, "tx_hash": tx_hash}
            api_key = kwargs.get("api_key")
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "tx_hash": tx_hash,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get transaction: {str(e)}"}
    
    async def _get_network_info(self, chain_id: str, **kwargs) -> dict:
        try:
            url = f"{self.base_url}/network/info"
            params = {"chain_id": chain_id}
            api_key = kwargs.get("api_key")
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get network info: {str(e)}"}
