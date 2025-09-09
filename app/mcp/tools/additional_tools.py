import asyncio
import logging
import aiohttp
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class SolanaTokenAnalysisTool(MCPTool):
    """Solana Token Analysis MCP tool for accessing Solana token data, trends, and analysis"""
    
    def __init__(self):
        self.session = None
        # Using CoinGecko API for Solana token data
        self.base_url = "https://api.coingecko.com/api/v3"
        
    @property
    def name(self) -> str:
        return "solana_token_analysis"
    
    @property
    def description(self) -> str:
        return "Access Solana token data, trending tokens, market analysis, and pump detection using CoinGecko API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_trending_solana_tokens",
                        "get_token_analysis",
                        "get_pump_detection",
                        "get_market_overview",
                        "get_token_price_history"
                    ],
                    "description": "Action to perform"
                },
                "token_id": {
                    "type": "string",
                    "description": "Token ID (e.g., 'solana', 'usdc', 'ray') for token-specific actions"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results"
                },
                "days": {
                    "type": "integer",
                    "default": 7,
                    "description": "Number of days for price history (1, 7, 14, 30, 90, 365, max)"
                }
            },
            "required": ["action"]
        }
    
    async def _get_session(self):
        if self.session is None:
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)
        return self.session
    
    async def _cleanup_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            token_id = arguments.get("token_id")
            limit = arguments.get("limit", 10)
            days = arguments.get("days", 7)
            
            if action == "get_trending_solana_tokens":
                result = await self._get_trending_solana_tokens(limit)
            elif action == "get_token_analysis":
                if not token_id:
                    return [{"type": "text", "text": "❌ Error: Token ID is required for this action."}]
                result = await self._get_token_analysis(token_id)
            elif action == "get_pump_detection":
                result = await self._get_pump_detection(limit)
            elif action == "get_market_overview":
                result = await self._get_market_overview()
            elif action == "get_token_price_history":
                if not token_id:
                    return [{"type": "text", "text": "❌ Error: Token ID is required for this action."}]
                result = await self._get_token_price_history(token_id, days)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_trending_solana_tokens(self, limit: int) -> dict:
        try:
            # Get trending Solana tokens from CoinGecko
            url = f"{self.base_url}/coins/markets"
            params = {
                "vs_currency": "usd",
                "category": "solana-ecosystem",
                "order": "market_cap_desc",
                "per_page": limit,
                "page": 1,
                "sparkline": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "trending_solana_tokens": data,
                            "analysis": "Top Solana ecosystem tokens by market cap",
                            "note": "Data provided by CoinGecko API"
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get trending Solana tokens: {str(e)}"}
    
    async def _get_token_analysis(self, token_id: str) -> dict:
        try:
            # Get detailed token analysis from CoinGecko
            url = f"{self.base_url}/coins/{token_id}"
            params = {
                "localization": "false",
                "tickers": "false",
                "market_data": "true",
                "community_data": "true",
                "developer_data": "true",
                "sparkline": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "token_analysis": data,
                            "analysis_type": "Comprehensive token analysis including market data, community metrics, and developer activity",
                            "note": "Data provided by CoinGecko API"
                        },
                        "token_id": token_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token analysis: {str(e)}"}
    
    async def _get_pump_detection(self, limit: int) -> dict:
        try:
            # Get coins with highest price changes (potential pumps)
            url = f"{self.base_url}/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "price_change_percentage_24h_desc",
                "per_page": limit,
                "page": 1,
                "sparkline": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # Filter for significant price increases (potential pumps)
                    pump_candidates = [coin for coin in data if coin.get('price_change_percentage_24h', 0) > 10]
                    
                    return {
                        "success": True,
                        "data": {
                            "pump_candidates": pump_candidates,
                            "analysis": "Tokens with significant 24h price increases (potential pump detection)",
                            "note": "Data provided by CoinGecko API - showing tokens with >10% 24h price increase"
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get pump detection: {str(e)}"}
    
    async def _get_market_overview(self) -> dict:
        try:
            # Get global market overview
            url = f"{self.base_url}/global"
            
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "market_overview": data,
                            "analysis": "Global cryptocurrency market overview including total market cap, volume, and market dominance",
                            "note": "Data provided by CoinGecko API"
                        },
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get market overview: {str(e)}"}
    
    async def _get_token_price_history(self, token_id: str, days: int) -> dict:
        try:
            # Get token price history
            url = f"{self.base_url}/coins/{token_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily" if days > 1 else "hourly"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "price_history": data,
                            "analysis": f"Price history for {token_id} over {days} days",
                            "note": "Data provided by CoinGecko API"
                        },
                        "token_id": token_id,
                        "days": days,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get token price history: {str(e)}"}


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
