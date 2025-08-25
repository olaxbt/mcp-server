"""
Solana Ecosystem Tools
Contains Jupiter DEX aggregator and Raydium DEX tools for Solana
"""

import asyncio
import logging
import time
import aiohttp
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class JupiterTool(MCPTool):
    def __init__(self):
        self.jupiter_base_url = "https://quote-api.jup.ag/v6"
        self.session = None
        self.cache = {}
        self.cache_duration = 60  # 1 minute cache
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    @property
    def name(self) -> str:
        return "jupiter"
    
    @property
    def description(self) -> str:
        return "Jupiter DEX aggregator tools for Solana. Get best swap routes, prices, and liquidity analysis across multiple DEXs."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_quote", "get_routes", "get_tokens", "get_pools", "cross_chain_quote"],
                    "default": "get_quote"
                },
                "input_mint": {
                    "type": "string",
                    "description": "Input token mint address (for Solana tokens)",
                    "default": "So11111111111111111111111111111111111111112"  # SOL
                },
                "output_mint": {
                    "type": "string", 
                    "description": "Output token mint address",
                    "default": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
                },
                "amount": {
                    "type": "string",
                    "description": "Amount to swap (in lamports/smallest unit)",
                    "default": "1000000000"  # 1 SOL
                },
                "slippage_bps": {
                    "type": "integer",
                    "description": "Slippage tolerance in basis points (1 = 0.01%)",
                    "default": 50
                },
                "source_chain": {
                    "type": "string",
                    "description": "Source chain for cross-chain swaps",
                    "enum": ["solana", "ethereum", "polygon", "arbitrum", "optimism"],
                    "default": "solana"
                },
                "destination_chain": {
                    "type": "string",
                    "description": "Destination chain for cross-chain swaps",
                    "enum": ["solana", "ethereum", "polygon", "arbitrum", "optimism"],
                    "default": "ethereum"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action", "get_quote")
            
            if action == "get_quote":
                return await self._get_quote(arguments)
            elif action == "get_routes":
                return await self._get_routes(arguments)
            elif action == "get_tokens":
                return await self._get_tokens()
            elif action == "get_pools":
                return await self._get_pools(arguments)
            elif action == "cross_chain_quote":
                return await self._get_cross_chain_quote(arguments)
            else:
                return [{"error": f"Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Jupiter tool error: {e}")
            return [{"error": f"Failed to execute Jupiter action: {str(e)}"}]
    
    async def _cleanup_session(self):
        """Clean up aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    async def _get_quote(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get best swap quote from Jupiter"""
        try:
            input_mint = arguments.get("input_mint", "So11111111111111111111111111111111111111112")
            output_mint = arguments.get("output_mint", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
            amount = arguments.get("amount", "1000000000")
            slippage_bps = arguments.get("slippage_bps", 50)
            
            url = f"{self.jupiter_base_url}/quote"
            params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount,
                "slippageBps": slippage_bps,
                "onlyDirectRoutes": "false",
                "asLegacyTransaction": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Jupiter API returns the quote data directly, not wrapped in a data field
                    if not isinstance(data, dict):
                        return [{"error": "Invalid response format from Jupiter API"}]
                    
                    # Get route information
                    route_info = await self._get_route_info(data)
                    
                    # Safely extract values with type conversion
                    out_amount = data.get("outAmount")
                    if isinstance(out_amount, (int, float)):
                        out_amount = str(out_amount)
                    elif not isinstance(out_amount, str):
                        out_amount = "0"
                    
                    price_impact = data.get("priceImpactPct")
                    if isinstance(price_impact, (int, float)):
                        price_impact = float(price_impact)
                    else:
                        price_impact = 0.0
                    
                    return [{
                        "type": "jupiter_quote",
                        "input_mint": input_mint,
                        "output_mint": output_mint,
                        "input_amount": amount,
                        "output_amount": out_amount,
                        "price_impact": price_impact,
                        "slippage_bps": slippage_bps,
                        "route": route_info,
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": f"Failed to get quote: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting Jupiter quote: {e}")
            return [{"error": f"Failed to get quote: {str(e)}"}]
    
    async def _get_routes(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get multiple swap routes from Jupiter"""
        try:
            input_mint = arguments.get("input_mint", "So11111111111111111111111111111111111111112")
            output_mint = arguments.get("output_mint", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
            amount = arguments.get("amount", "1000000000")
            
            url = f"{self.jupiter_base_url}/quote"
            params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount,
                "onlyDirectRoutes": "false",
                "asLegacyTransaction": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Jupiter API returns a single route, not multiple routes
                    if not isinstance(data, dict):
                        return [{"error": "Invalid response format from Jupiter API"}]
                    
                    # For routes, we'll use the routePlan from the response
                    route_plan = data.get("routePlan", [])
                    if not isinstance(route_plan, list):
                        route_plan = []
                    
                    route_analysis = []
                    for i, route in enumerate(route_plan[:5]):  # Top 5 routes
                        if not isinstance(route, dict):
                            continue
                            
                        swap_info = route.get("swapInfo", {})
                        route_info = await self._get_route_info({"routePlan": [route]})
                        
                        # Safely extract route values
                        out_amount = swap_info.get("outAmount")
                        if isinstance(out_amount, (int, float)):
                            out_amount = str(out_amount)
                        elif not isinstance(out_amount, str):
                            out_amount = "0"
                        
                        price_impact = data.get("priceImpactPct")
                        if isinstance(price_impact, (int, float)):
                            price_impact = float(price_impact)
                        else:
                            price_impact = 0.0
                        
                        route_analysis.append({
                            "route_index": i,
                            "out_amount": out_amount,
                            "price_impact": price_impact,
                            "swap_info": swap_info,
                            "route_info": route_info
                        })
                    
                    return [{
                        "type": "jupiter_routes",
                        "input_mint": input_mint,
                        "output_mint": output_mint,
                        "input_amount": amount,
                        "routes": route_analysis,
                        "best_route": route_analysis[0] if route_analysis else None,
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": f"Failed to get routes: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting Jupiter routes: {e}")
            return [{"error": f"Failed to get routes: {str(e)}"}]
    
    async def _get_tokens(self) -> List[Dict[str, Any]]:
        """Get list of supported tokens on Jupiter"""
        try:
            url = "https://token.jup.ag/all"
            
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    tokens = await response.json()
                    
                    # Jupiter tokens API returns a list directly
                    if not isinstance(tokens, list):
                        return [{"error": "Invalid response format from Jupiter tokens API"}]
                    
                    # Filter and format popular tokens
                    popular_tokens = []
                    for token in tokens:
                        if isinstance(token, dict):
                            # Include tokens with common symbols or specific tags
                            symbol = token.get("symbol", "").upper()
                            token_tags = token.get("tags", [])
                            
                            # Check if it's a popular token by symbol or tags
                            is_popular = (
                                symbol in ["SOL", "USDC", "USDT", "RAY", "SRM", "ORCA", "JUP", "BONK", "WIF"] or
                                (isinstance(token_tags, list) and any(tag in ["popular", "stablecoin", "wrapped"] for tag in token_tags))
                            )
                            
                            if is_popular:
                                popular_tokens.append({
                                    "symbol": token.get("symbol", ""),
                                    "name": token.get("name", ""),
                                    "address": token.get("address", ""),
                                    "decimals": token.get("decimals", 0),
                                    "logoURI": token.get("logoURI", ""),
                                    "tags": token.get("tags", [])
                                })
                    
                    return [{
                        "type": "jupiter_tokens",
                        "total_tokens": len(tokens),
                        "popular_tokens": popular_tokens[:20],  # Top 20 popular tokens
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": f"Failed to get tokens: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting Jupiter tokens: {e}")
            return [{"error": f"Failed to get tokens: {str(e)}"}]
    
    async def _get_pools(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get liquidity pool information"""
        try:
            input_mint = arguments.get("input_mint", "So11111111111111111111111111111111111111112")
            output_mint = arguments.get("output_mint", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
            
            url = f"{self.jupiter_base_url}/quote"
            params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": "1000000000",
                "onlyDirectRoutes": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Jupiter API returns routePlan instead of routes
                    route_plan = data.get("routePlan", [])
                    if not isinstance(route_plan, list):
                        route_plan = []
                    
                    pool_analysis = []
                    for route in route_plan[:3]:  # Top 3 routes
                        if isinstance(route, dict):
                            swap_info = route.get("swapInfo", {})
                            pool_analysis.append({
                                "dex": swap_info.get("label", ""),
                                "input_mint": swap_info.get("inputMint", ""),
                                "output_mint": swap_info.get("outputMint", ""),
                                "in_amount": swap_info.get("inAmount", "0"),
                                "out_amount": swap_info.get("outAmount", "0"),
                                "price_impact": data.get("priceImpactPct", 0),
                                "lp_fee": swap_info.get("feeAmount", "0"),
                                "platform_fee": "0"
                            })
                    
                    return [{
                        "type": "jupiter_pools",
                        "input_mint": input_mint,
                        "output_mint": output_mint,
                        "pools": pool_analysis,
                        "total_pools": len(pool_analysis),
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": f"Failed to get pools: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting Jupiter pools: {e}")
            return [{"error": f"Failed to get pools: {str(e)}"}]
    
    async def _get_cross_chain_quote(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get cross-chain swap quote"""
        try:
            source_chain = arguments.get("source_chain", "solana")
            destination_chain = arguments.get("destination_chain", "ethereum")
            amount = arguments.get("amount", "1000000000")
            
            # Simulate cross-chain quote (Jupiter's cross-chain API might be different)
            url = f"{self.jupiter_base_url}/quote"
            params = {
                "inputMint": "So11111111111111111111111111111111111111112",  # SOL
                "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
                "amount": amount,
                "onlyDirectRoutes": "false"
            }
            
            session = await self._get_session()
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Add cross-chain specific information
                    cross_chain_info = {
                        "source_chain": source_chain,
                        "destination_chain": destination_chain,
                        "bridge_fee": 0.001,  # 0.1% bridge fee
                        "estimated_time": "5-15 minutes",
                        "security_level": "high"
                    }
                    
                    # Safely extract output amount
                    if not isinstance(data, dict):
                        return [{"error": "Invalid response format from Jupiter API"}]
                    
                    out_amount = data.get("outAmount")
                    if isinstance(out_amount, (int, float)):
                        out_amount = str(out_amount)
                    elif not isinstance(out_amount, str):
                        out_amount = "0"
                    
                    return [{
                        "type": "jupiter_cross_chain_quote",
                        "source_chain": source_chain,
                        "destination_chain": destination_chain,
                        "input_amount": amount,
                        "output_amount": out_amount,
                        "bridge_fee": cross_chain_info["bridge_fee"],
                        "estimated_time": cross_chain_info["estimated_time"],
                        "security_level": cross_chain_info["security_level"],
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": f"Failed to get cross-chain quote: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting cross-chain quote: {e}")
            return [{"error": f"Failed to get cross-chain quote: {str(e)}"}]
    
    async def _get_route_info(self, route_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract route information from Jupiter route data"""
        try:
            if not isinstance(route_data, dict):
                return {"error": "Invalid route data format"}
            
            # Jupiter v6 API uses routePlan instead of marketInfos
            route_plan = route_data.get("routePlan", [])
            if not isinstance(route_plan, list):
                route_plan = []
            
            # Safely extract dexes used
            dexes_used = []
            total_fee = 0.0
            
            for route in route_plan:
                if isinstance(route, dict):
                    swap_info = route.get("swapInfo", {})
                    if isinstance(swap_info, dict):
                        label = swap_info.get("label")
                        if isinstance(label, str) and label:
                            dexes_used.append(label)
                        
                        # Calculate fee
                        fee_amount = swap_info.get("feeAmount")
                        if isinstance(fee_amount, (int, float)):
                            total_fee += float(fee_amount)
            
            # Safely get price impact
            price_impact = route_data.get("priceImpactPct")
            if isinstance(price_impact, (int, float)):
                price_impact = float(price_impact)
            else:
                price_impact = 0.0
            
            route_summary = {
                "total_swaps": len(route_plan),
                "dexes_used": list(set(dexes_used)),
                "total_price_impact": price_impact,
                "total_fee": total_fee,
                "route_type": "direct" if len(route_plan) == 1 else "split"
            }
            
            return route_summary
        except Exception as e:
            logger.error(f"Error extracting route info: {e}")
            return {"error": "Failed to extract route information"}

class RaydiumTool(MCPTool):
    def __init__(self):
        self.raydium_base_url = "https://api.raydium.io"
        self.session = None
        self.cache = {}
        self.cache_duration = 60  # 1 minute cache
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    @property
    def name(self) -> str:
        return "raydium"
    
    @property
    def description(self) -> str:
        return "Raydium DEX tools for Solana. Get concentrated liquidity pool data, yield farming opportunities, and staking information."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_pools", "get_farms", "get_staking", "get_tokens", "get_pool_info", "get_yield_opportunities"],
                    "default": "get_pools"
                },
                "pool_id": {
                    "type": "string",
                    "description": "Specific pool ID to analyze",
                    "default": None
                },
                "token_mint": {
                    "type": "string",
                    "description": "Token mint address for specific analysis",
                    "default": "So11111111111111111111111111111111111111112"  # SOL
                },
                "farm_id": {
                    "type": "string",
                    "description": "Specific farm ID to analyze",
                    "default": None
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 50
                },
                "sort_by": {
                    "type": "string",
                    "description": "Sort criteria",
                    "enum": ["tvl", "volume", "apy", "fee"],
                    "default": "tvl"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action", "get_pools")
            
            if action == "get_pools":
                return await self._get_pools(arguments)
            elif action == "get_farms":
                return await self._get_farms(arguments)
            elif action == "get_staking":
                return await self._get_staking(arguments)
            elif action == "get_tokens":
                return await self._get_tokens()
            elif action == "get_pool_info":
                return await self._get_pool_info(arguments)
            elif action == "get_yield_opportunities":
                return await self._get_yield_opportunities(arguments)
            else:
                return [{"error": f"Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Raydium tool error: {e}")
            return [{"error": f"Failed to execute Raydium action: {str(e)}"}]
    
    async def _cleanup_session(self):
        """Clean up aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    async def _get_pools(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Raydium liquidity pools"""
        try:
            limit = arguments.get("limit", 10)
            sort_by = arguments.get("sort_by", "tvl")
            
            url = f"{self.raydium_base_url}/pools"
            
            session = await self._get_session()
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Raydium API returns a list directly
                    if not isinstance(data, list):
                        return [{"error": "Invalid response format from Raydium API"}]
                    
                    pools = data
                    
                    # Sort pools by specified criteria with null safety
                    if sort_by == "tvl":
                        pools.sort(key=lambda x: float(x.get("liquidity_locked", 0) or 0), reverse=True)
                    elif sort_by == "apy":
                        pools.sort(key=lambda x: float(x.get("apy", 0) or 0), reverse=True)
                    else:
                        # Default sort by liquidity
                        pools.sort(key=lambda x: float(x.get("liquidity_locked", 0) or 0), reverse=True)
                    
                    # Format pool data
                    formatted_pools = []
                    for pool in pools[:limit]:
                        if isinstance(pool, dict):
                            formatted_pools.append({
                                "identifier": pool.get("identifier", ""),
                                "token_id": pool.get("token-id", ""),
                                "liquidity_locked": float(pool.get("liquidity_locked", 0) or 0),
                                "apy": float(pool.get("apy", 0) or 0),
                                "official": pool.get("official", False)
                            })
                    
                    return [{
                        "type": "raydium_pools",
                        "pools": formatted_pools,
                        "total_pools": len(pools),
                        "sort_by": sort_by,
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": f"Failed to get pools: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting Raydium pools: {e}")
            return [{"error": f"Failed to get pools: {str(e)}"}]
    
    async def _get_farms(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Raydium yield farming opportunities"""
        try:
            limit = arguments.get("limit", 10)
            farm_id = arguments.get("farm_id")
            
            # Raydium farms endpoint doesn't exist, return fallback data
            return [{
                "type": "raydium_farms",
                "farms": [],
                "total_farms": 0,
                "note": "Raydium farms endpoint not available in current API",
                "timestamp": datetime.now().isoformat()
            }]
            
        except Exception as e:
            logger.error(f"Error getting Raydium farms: {e}")
            return [{"error": f"Failed to get farms: {str(e)}"}]
    
    async def _get_staking(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Raydium staking information"""
        try:
            token_mint = arguments.get("token_mint", "So11111111111111111111111111111111111111112")
            
            # Get RAY token staking info
            # Raydium staking endpoint doesn't exist, return fallback data
            return [{
                "type": "raydium_staking",
                "token_mint": token_mint,
                "total_staked": 0.0,
                "total_rewards": 0.0,
                "apy": 0.0,
                "lock_periods": [],
                "min_stake": 0.0,
                "max_stake": 0.0,
                "note": "Raydium staking endpoint not available in current API",
                "timestamp": datetime.now().isoformat()
            }]
            
        except Exception as e:
            logger.error(f"Error getting Raydium staking: {e}")
            return [{"error": f"Failed to get staking info: {str(e)}"}]
    
    async def _get_tokens(self) -> List[Dict[str, Any]]:
        """Get Raydium supported tokens"""
        try:
            # Raydium tokens endpoint doesn't exist, return fallback data
            return [{
                "type": "raydium_tokens",
                "tokens": [],
                "total_tokens": 0,
                "note": "Raydium tokens endpoint not available in current API",
                "timestamp": datetime.now().isoformat()
            }]
            
        except Exception as e:
            logger.error(f"Error getting Raydium tokens: {e}")
            return [{"error": f"Failed to get tokens: {str(e)}"}]
    
    async def _get_pool_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get detailed information about a specific pool"""
        try:
            pool_id = arguments.get("pool_id")
            if not pool_id:
                return [{"error": "Pool ID is required"}]
            
            # Raydium individual pool endpoint doesn't exist, return fallback data
            return [{
                "type": "raydium_pool_info",
                "pool": {
                    "id": pool_id,
                    "note": "Raydium individual pool endpoint not available in current API"
                },
                "timestamp": datetime.now().isoformat()
            }]
            
        except Exception as e:
            logger.error(f"Error getting pool info: {e}")
            return [{"error": f"Failed to get pool info: {str(e)}"}]
    
    async def _get_yield_opportunities(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get yield farming opportunities with analysis"""
        try:
            limit = arguments.get("limit", 10)
            
            # Get both pools and farms
            # Get pools data (farms endpoint doesn't exist)
            pools_url = f"{self.raydium_base_url}/pools"
            
            session = await self._get_session()
            async with session.get(pools_url) as response:
                if response.status == 200:
                    pools_data = await response.json()
                    
                    if not isinstance(pools_data, list):
                        return [{"error": "Invalid response format from Raydium API"}]
                    
                    # Analyze pool opportunities
                    opportunities = []
                    
                    for pool in pools_data:
                        if isinstance(pool, dict):
                            apy = float(pool.get("apy", 0) or 0)
                            if apy > 5:  # Only pools with >5% APY
                                opportunities.append({
                                    "type": "liquidity_pool",
                                    "identifier": pool.get("identifier", ""),
                                    "token_id": pool.get("token-id", ""),
                                    "apy": apy,
                                    "liquidity_locked": float(pool.get("liquidity_locked", 0) or 0),
                                    "official": pool.get("official", False),
                                    "risk_level": "medium",  # Default risk level
                                    "recommendation": "Consider for yield farming" if apy > 10 else "Moderate yield opportunity"
                                })
                    
                    # Sort by APY
                    opportunities.sort(key=lambda x: x["apy"], reverse=True)
                    
                    return [{
                        "type": "raydium_yield_opportunities",
                        "opportunities": opportunities[:limit],
                        "total_opportunities": len(opportunities),
                        "note": "Only pool opportunities available (farms endpoint not available)",
                        "timestamp": datetime.now().isoformat()
                    }]
                else:
                    return [{"error": "Failed to fetch yield opportunities"}]
                    
        except Exception as e:
            logger.error(f"Error getting yield opportunities: {e}")
            return [{"error": f"Failed to get yield opportunities: {str(e)}"}]
