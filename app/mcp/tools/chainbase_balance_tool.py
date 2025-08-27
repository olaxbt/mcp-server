import os
import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class ChainBaseBalanceTool(MCPTool):
    """Tool for fetching real wallet balances using ChainBase API"""

    @property
    def name(self) -> str:
        return "chainbase_balance"

    @property
    def description(self) -> str:
        return "Fetch real wallet balances, token holdings, and portfolio data across multiple blockchain networks using ChainBase API"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_balance", "get_token_holdings", "get_nft_holdings", "get_transaction_history", "get_portfolio_summary"]
                },
                "address": {
                    "type": "string",
                    "description": "Wallet address to query"
                },
                "chain_id": {
                    "type": "string",
                    "description": "Chain ID to query (e.g., '1' for Ethereum, '137' for Polygon)",
                    "default": "1"
                },
                "api_key": {
                    "type": "string",
                    "description": "ChainBase API key (required)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results",
                    "default": 50
                }
            },
            "required": ["action", "address", "api_key"]
        }

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        address = arguments.get("address")
        chain_id = arguments.get("chain_id", "1")
        api_key = arguments.get("api_key")
        limit = arguments.get("limit", 50)
        
        if not api_key:
            return [{"type": "text", "text": "❌ Error: ChainBase API key is required"}]
        
        try:
            if action == "get_balance":
                return await self._get_balance(address, chain_id, api_key)
            elif action == "get_token_holdings":
                return await self._get_token_holdings(address, chain_id, api_key, limit)
            elif action == "get_nft_holdings":
                return await self._get_nft_holdings(address, chain_id, api_key, limit)
            elif action == "get_transaction_history":
                return await self._get_transaction_history(address, chain_id, api_key, limit)
            elif action == "get_portfolio_summary":
                return await self._get_portfolio_summary(address, chain_id, api_key)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"ChainBase balance tool error: {str(e)}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _get_balance(self, address: str, chain_id: str, api_key: str) -> List[Dict[str, Any]]:
        """Get native token balance for a wallet address"""
        try:
            # ChainBase API endpoint for balance
            url = f"https://api.chainbase.com/v1/account/balance"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json"
            }
            params = {
                "chain_id": chain_id,
                "address": address
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        balance = data.get("data", {}).get("balance", "0")
                        symbol = data.get("data", {}).get("symbol", "ETH")
                        
                        return [{
                            "type": "text", 
                            "text": f"💰 ChainBase Balance for {address[:10]}...\n\n"
                                   f"**Chain ID**: {chain_id}\n"
                                   f"**Native Balance**: {balance} {symbol}\n"
                                   f"**Address**: {address}\n\n"
                                   f"*Data provided by ChainBase API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching balance: {str(e)}"}]

    async def _get_token_holdings(self, address: str, chain_id: str, api_key: str, limit: int) -> List[Dict[str, Any]]:
        """Get ERC-20 token holdings for a wallet address"""
        try:
            # ChainBase API endpoint for token holdings
            url = f"https://api.chainbase.com/v1/account/tokens"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json"
            }
            params = {
                "chain_id": chain_id,
                "address": address,
                "limit": limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        tokens = data.get("data", [])
                        
                        if tokens:
                            token_list = "\n".join([
                                f"• {token.get('symbol', 'Unknown')}: {token.get('balance', '0')} (${token.get('value_usd', '0')})"
                                for token in tokens[:limit]
                            ])
                            
                            return [{
                                "type": "text", 
                                "text": f"🪙 ChainBase Token Holdings for {address[:10]}...\n\n"
                                       f"**Chain ID**: {chain_id}\n"
                                       f"**Total Tokens**: {len(tokens)}\n"
                                       f"**Showing**: {min(limit, len(tokens))} tokens\n\n"
                                       f"**Token Holdings**:\n{token_list}\n\n"
                                       f"*Data provided by ChainBase API*"
                            }]
                        else:
                            return [{"type": "text", "text": f"📭 No token holdings found for {address[:10]}... on chain {chain_id}"}]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching token holdings: {str(e)}"}]

    async def _get_nft_holdings(self, address: str, chain_id: str, api_key: str, limit: int) -> List[Dict[str, Any]]:
        """Get NFT holdings for a wallet address"""
        try:
            # ChainBase API endpoint for NFT holdings
            url = f"https://api.chainbase.com/v1/account/nfts"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json"
            }
            params = {
                "chain_id": chain_id,
                "address": address,
                "limit": limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        nfts = data.get("data", [])
                        
                        if nfts:
                            nft_list = "\n".join([
                                f"• {nft.get('name', 'Unknown')} (#{nft.get('token_id', 'N/A')}) - {nft.get('contract_address', 'N/A')[:10]}..."
                                for nft in nfts[:limit]
                            ])
                            
                            return [{
                                "type": "text", 
                                "text": f"🖼️ ChainBase NFT Holdings for {address[:10]}...\n\n"
                                       f"**Chain ID**: {chain_id}\n"
                                       f"**Total NFTs**: {len(nfts)}\n"
                                       f"**Showing**: {min(limit, len(nfts))} NFTs\n\n"
                                       f"**NFT Holdings**:\n{nft_list}\n\n"
                                       f"*Data provided by ChainBase API*"
                            }]
                        else:
                            return [{"type": "text", "text": f"📭 No NFT holdings found for {address[:10]}... on chain {chain_id}"}]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching NFT holdings: {str(e)}"}]

    async def _get_transaction_history(self, address: str, chain_id: str, api_key: str, limit: int) -> List[Dict[str, Any]]:
        """Get transaction history for a wallet address"""
        try:
            # ChainBase API endpoint for transaction history
            url = f"https://api.chainbase.com/v1/account/transactions"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json"
            }
            params = {
                "chain_id": chain_id,
                "address": address,
                "limit": limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        transactions = data.get("data", [])
                        
                        if transactions:
                            tx_list = "\n".join([
                                f"• {tx.get('hash', 'N/A')[:10]}... - {tx.get('method', 'Transfer')} - {tx.get('value', '0')} {tx.get('symbol', 'ETH')}"
                                for tx in transactions[:limit]
                            ])
                            
                            return [{
                                "type": "text", 
                                "text": f"📋 ChainBase Transaction History for {address[:10]}...\n\n"
                                       f"**Chain ID**: {chain_id}\n"
                                       f"**Total Transactions**: {len(transactions)}\n"
                                       f"**Showing**: {min(limit, len(transactions))} transactions\n\n"
                                       f"**Recent Transactions**:\n{tx_list}\n\n"
                                       f"*Data provided by ChainBase API*"
                            }]
                        else:
                            return [{"type": "text", "text": f"📭 No transactions found for {address[:10]}... on chain {chain_id}"}]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching transaction history: {str(e)}"}]

    async def _get_portfolio_summary(self, address: str, chain_id: str, api_key: str) -> List[Dict[str, Any]]:
        """Get portfolio summary for a wallet address"""
        try:
            # ChainBase API endpoint for portfolio summary
            url = f"https://api.chainbase.com/v1/account/portfolio"
            headers = {
                "x-api-key": api_key,
                "accept": "application/json"
            }
            params = {
                "chain_id": chain_id,
                "address": address
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        portfolio = data.get("data", {})
                        
                        total_value = portfolio.get("total_value_usd", "0")
                        token_count = portfolio.get("token_count", 0)
                        nft_count = portfolio.get("nft_count", 0)
                        
                        return [{
                            "type": "text", 
                            "text": f"📊 ChainBase Portfolio Summary for {address[:10]}...\n\n"
                                   f"**Chain ID**: {chain_id}\n"
                                   f"**Total Portfolio Value**: ${total_value}\n"
                                   f"**Token Holdings**: {token_count}\n"
                                   f"**NFT Holdings**: {nft_count}\n"
                                   f"**Address**: {address}\n\n"
                                   f"*Data provided by ChainBase API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching portfolio summary: {str(e)}"}]
