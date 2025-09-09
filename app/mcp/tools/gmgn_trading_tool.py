"""
GMGN Trading API Tool - Real GMGN.AI Trading API Integration
Based on: https://docs.gmgn.ai/index/cooperation-api-integrate-gmgn-eth-base-bsc-trading-api
"""

import aiohttp
import asyncio
from datetime import datetime
from typing import Dict, Any, List
from .mcp_tool import MCPTool


class GMGNTradingTool(MCPTool):
    """Tool for accessing GMGN.AI Trading API and Data API"""
    
    def __init__(self):
        super().__init__()
        # GMGN Solana Trading API (public, no key required)
        self.solana_trading_url = "https://gmgn.ai/defi/router/v1/sol"
        self.session = None
    
    @property
    def name(self) -> str:
        return "gmgn_trading"
    
    @property
    def description(self) -> str:
        return "Get optimal swap routes and pricing data from GMGN.AI Solana API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_swap_route"
                    ],
                    "default": "get_swap_route"
                },
                "token_in_address": {
                    "type": "string",
                    "description": "Input token address (for Solana trading)"
                },
                "token_out_address": {
                    "type": "string",
                    "description": "Output token address (for Solana trading)"
                },
                "in_amount": {
                    "type": "string",
                    "description": "Input amount in lamports (for Solana trading)"
                },
                "from_address": {
                    "type": "string",
                    "description": "Wallet address (for Solana trading)"
                },
                "slippage": {
                    "type": "number",
                    "description": "Slippage percentage (for Solana trading)",
                    "default": 10
                },
                "fee": {
                    "type": "number",
                    "description": "Network priority fees and RPC node tip fees in SOL (for Solana trading)",
                    "default": 0.006
                },

            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            # Only get_swap_route is supported
            result = await self._get_swap_route(arguments)
            return [result]
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: Tool execution failed: {str(e)}"}]
    
    async def _get_swap_route(self, arguments: Dict[str, Any]) -> dict:
        """Get optimal swap route from GMGN Solana Trading API"""
        try:
            token_in_address = arguments.get("token_in_address")
            token_out_address = arguments.get("token_out_address")
            in_amount = arguments.get("in_amount")
            from_address = arguments.get("from_address")
            slippage = arguments.get("slippage", 10)
            
            if not all([token_in_address, token_out_address, in_amount, from_address]):
                return {
                    "success": False,
                    "error": "Missing required parameters: token_in_address, token_out_address, in_amount, from_address"
                }
            
            session = await self._get_session()
            
            url = f"{self.solana_trading_url}/tx/get_swap_route"
            fee = arguments.get("fee", 0.006)
            params = {
                "token_in_address": token_in_address,
                "token_out_address": token_out_address,
                "in_amount": in_amount,
                "from_address": from_address,
                "slippage": slippage,
                "fee": fee
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "swap_route": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    error_text = await response.text()
                    return {
                        "success": False,
                        "error": f"API request failed: {response.status} - {error_text}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get swap route: {str(e)}"
            }
    


