"""
DeFi Tools
Contains tools for interacting with DeFi protocols like Aave
"""

import asyncio
import logging
import time
import aiohttp
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import os

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)


class AaveTool(MCPTool):
    def __init__(self):
        self.session = None
        # Use working, current API endpoints
        self.defillama_api_url = "https://api.llama.fi"
        self.coingecko_api_url = "https://api.coingecko.com/api/v3"
        self.supported_networks = {
            "ethereum": "ethereum",
            "polygon": "polygon", 
            "avalanche": "avalanche",
            "arbitrum": "arbitrum",
            "optimism": "optimism",
            "fantom": "fantom"
        }
    
    @property
    def name(self) -> str:
        return "aave"
    
    @property
    def description(self) -> str:
        return "Access Aave Protocol data including lending pools, user positions, asset information, and DeFi analytics"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_pool_data",
                        "get_user_positions", 
                        "get_asset_data",
                        "get_flash_loan_info",
                        "get_interest_rates",
                        "get_historical_data",
                        "get_risk_analysis",
                        "get_cross_chain_data"
                    ]
                },
                "network": {
                    "type": "string",
                    "description": "Network to query (ethereum, polygon, avalanche, arbitrum, optimism, fantom)",
                    "default": "ethereum"
                },
                "asset": {
                    "type": "string",
                    "description": "Asset symbol or address (e.g., USDC, WETH, 0x...)"
                },
                "user_address": {
                    "type": "string",
                    "description": "User wallet address for position queries"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days for historical data",
                    "default": 30
                },
                "aave_api_key": {
                    "type": "string",
                    "description": "Optional Aave API key for accessing user-specific data"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            
            if action == "get_pool_data":
                result = await self._get_pool_data(**arguments)
            elif action == "get_user_positions":
                result = await self._get_user_positions(**arguments)
            elif action == "get_asset_data":
                result = await self._get_asset_data(**arguments)
            elif action == "get_flash_loan_info":
                result = await self._get_flash_loan_info(**arguments)
            elif action == "get_interest_rates":
                result = await self._get_interest_rates(**arguments)
            elif action == "get_historical_data":
                result = await self._get_historical_data(**arguments)
            elif action == "get_risk_analysis":
                result = await self._get_risk_analysis(**arguments)
            elif action == "get_cross_chain_data":
                result = await self._get_cross_chain_data(**arguments)
            else:
                result = {"error": f"Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_pool_data(self, **kwargs) -> dict:
        """Get lending pool information and APYs."""
        try:
            network = kwargs.get("network", "ethereum")
            session = await self._get_session()
            
            # Use Aave V3 API for pool data
            url = f"{self.aave_v3_api_url}/reserves"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Filter for the specified network if needed
                    reserves = data.get("reserves", [])
                    
                    # Calculate total TVL and format data
                    total_tvl = 0
                    formatted_reserves = []
                    
                    for reserve in reserves:
                        if reserve.get("usageAsCollateralEnabledOnUser"):
                            total_liquidity = float(reserve.get("totalLiquidity", 0))
                            price_in_usd = float(reserve.get("priceInUsd", 0))
                            tvl = total_liquidity * price_in_usd
                            total_tvl += tvl
                            
                            formatted_reserves.append({
                                "symbol": reserve.get("symbol"),
                                "name": reserve.get("name"),
                                "decimals": reserve.get("decimals"),
                                "total_liquidity": reserve.get("totalLiquidity"),
                                "available_liquidity": reserve.get("availableLiquidity"),
                                "total_variable_debt": reserve.get("totalVariableDebt"),
                                "total_stable_debt": reserve.get("totalStableDebt"),
                                "liquidity_rate": reserve.get("liquidityRate"),
                                "variable_borrow_rate": reserve.get("variableBorrowRate"),
                                "stable_borrow_rate": reserve.get("stableBorrowRate"),
                                "utilization_rate": reserve.get("usageRatio"),
                                "price_in_usd": reserve.get("priceInUsd"),
                                "collateral_enabled": reserve.get("usageAsCollateralEnabledOnUser"),
                                "liquidation_threshold": reserve.get("liquidationThreshold"),
                                "liquidation_bonus": reserve.get("liquidationBonus")
                            })
                    
                    return {
                        "success": True,
                        "network": network,
                        "data": {
                            "total_tvl": f"${total_tvl:,.2f}",
                            "total_reserves": len(formatted_reserves),
                            "reserves": formatted_reserves[:10],  # Limit to first 10
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch pool data: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get pool data: {str(e)}"
            }
    
    async def _get_user_positions(self, **kwargs) -> dict:
        """Get user lending and borrowing positions."""
        try:
            user_address = kwargs.get("user_address")
            network = kwargs.get("network", "ethereum")
            
            if not user_address:
                return {
                    "success": False,
                    "error": "user_address is required for position queries"
                }
            
            try:
                session = await self._get_session()
                aave_api_key = kwargs.get("aave_api_key")
                
                # If API key is provided, try to get real user data from Aave
                if aave_api_key:
                    try:
                        # Try to use Aave API with the provided key
                        # Note: This would need the correct Aave API endpoint
                        aave_api_url = "https://api.aave.com/v3"  # This might need updating
                        headers = {"Authorization": f"Bearer {aave_api_key}"}
                        
                        # Try to get user data
                        user_url = f"{aave_api_url}/user/{user_address}"
                        async with session.get(user_url, headers=headers) as response:
                            if response.status == 200:
                                user_data = await response.json()
                                # Process real user data here
                                return {
                                    "success": True,
                                    "user_address": user_address,
                                    "network": network,
                                    "data": {
                                        "protocol": "Aave",
                                        "source": "Aave API",
                                        "user_data": user_data,
                                        "timestamp": datetime.now().isoformat()
                                    }
                                }
                            else:
                                logger.warning(f"Aave API returned {response.status}, falling back to DefiLlama")
                    except Exception as aave_error:
                        logger.warning(f"Aave API failed with key, falling back to DefiLlama: {aave_error}")
                
                # Fallback to DefiLlama API for protocol-level data
                url = f"{self.defillama_api_url}/protocol/aave"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Get protocol TVL and basic info
                        tvl = data.get("tvl", [])
                        current_network_tvl = 0
                        
                        for chain_tvl in tvl:
                            if chain_tvl.get("chain") == network:
                                current_network_tvl = chain_tvl.get("tvl", 0)
                                break
                        
                        return {
                            "success": True,
                            "user_address": user_address,
                            "network": network,
                            "data": {
                                "protocol": "Aave",
                                "source": "DefiLlama API",
                                "network_tvl": current_network_tvl,
                                "total_protocol_tvl": sum([chain.get("tvl", 0) for chain in tvl]),
                                "supported_assets": ["USDC", "WETH", "USDT", "DAI", "WBTC"],
                                "note": "User-specific data requires valid Aave API key. Showing protocol-level data from DefiLlama.",
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to fetch Aave data: {response.status}"
                        }
            except Exception as api_error:
                return {
                    "success": False,
                    "error": f"Failed to get Aave data: {str(api_error)}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get user positions: {str(e)}"
            }
    

    
    async def _get_asset_data(self, **kwargs) -> dict:
        """Get detailed information about a specific asset."""
        try:
            asset = kwargs.get("asset")
            network = kwargs.get("network", "ethereum")
            
            if not asset:
                return {
                    "success": False,
                    "error": "asset parameter is required"
                }
            
            session = await self._get_session()
            
            # Get all reserves and find the specific asset
            url = f"{self.aave_v3_api_url}/reserves"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    reserves = data.get("reserves", [])
                    
                    # Find the asset by symbol or address
                    target_reserve = None
                    for reserve in reserves:
                        if (reserve.get("symbol", "").upper() == asset.upper() or 
                            reserve.get("underlyingAsset", "").lower() == asset.lower()):
                            target_reserve = reserve
                            break
                    
                    if not target_reserve:
                        return {
                            "success": False,
                            "error": f"Asset {asset} not found in Aave V3"
                        }
                    
                    # Calculate additional metrics
                    total_liquidity = float(target_reserve.get("totalLiquidity", 0))
                    total_debt = float(target_reserve.get("totalVariableDebt", 0)) + float(target_reserve.get("totalStableDebt", 0))
                    utilization_rate = total_debt / total_liquidity if total_liquidity > 0 else 0
                    
                    return {
                        "success": True,
                        "asset": asset,
                        "network": network,
                        "data": {
                            "symbol": target_reserve.get("symbol"),
                            "name": target_reserve.get("name"),
                            "decimals": target_reserve.get("decimals"),
                            "underlying_asset": target_reserve.get("underlyingAsset"),
                            "a_token_address": target_reserve.get("aTokenAddress"),
                            "variable_debt_token_address": target_reserve.get("variableDebtTokenAddress"),
                            "stable_debt_token_address": target_reserve.get("stableDebtTokenAddress"),
                            "total_liquidity": target_reserve.get("totalLiquidity"),
                            "available_liquidity": target_reserve.get("availableLiquidity"),
                            "total_variable_debt": target_reserve.get("totalVariableDebt"),
                            "total_stable_debt": target_reserve.get("totalStableDebt"),
                            "utilization_rate": f"{utilization_rate:.2%}",
                            "liquidity_rate": target_reserve.get("liquidityRate"),
                            "variable_borrow_rate": target_reserve.get("variableBorrowRate"),
                            "stable_borrow_rate": target_reserve.get("stableBorrowRate"),
                            "average_stable_rate": target_reserve.get("averageStableRate"),
                            "liquidity_index": target_reserve.get("liquidityIndex"),
                            "variable_borrow_index": target_reserve.get("variableBorrowIndex"),
                            "last_update_timestamp": target_reserve.get("lastUpdateTimestamp"),
                            "collateral_enabled": target_reserve.get("usageAsCollateralEnabledOnUser"),
                            "liquidation_threshold": target_reserve.get("liquidationThreshold"),
                            "liquidation_bonus": target_reserve.get("liquidationBonus"),
                            "reserve_factor": target_reserve.get("reserveFactor"),
                            "price_in_usd": target_reserve.get("priceInUsd"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch asset data: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get asset data: {str(e)}"
            }
    
    async def _get_flash_loan_info(self, **kwargs) -> dict:
        """Get flash loan information and fees."""
        try:
            asset = kwargs.get("asset", "USDC")
            amount = kwargs.get("amount", "1000000")  # Default 1M USDC
            network = kwargs.get("network", "ethereum")
            
            session = await self._get_session()
            
            # Flash loan fee is typically 0.09% for most assets
            flash_loan_fee_rate = 0.0009  # 0.09%
            flash_loan_fee = float(amount) * flash_loan_fee_rate
            
            return {
                "success": True,
                "asset": asset,
                "amount": amount,
                "network": network,
                "data": {
                    "flash_loan_fee_rate": f"{flash_loan_fee_rate:.4%}",
                    "flash_loan_fee": f"{flash_loan_fee:.2f}",
                    "total_repayment": f"{float(amount) + flash_loan_fee:.2f}",
                    "requirements": [
                        "Flash loan must be repaid within the same transaction",
                        "Repayment amount must include the flash loan fee",
                        "Transaction must be atomic (all-or-nothing)",
                        "Only available on supported assets"
                    ],
                    "supported_assets": [
                        "USDC", "USDT", "DAI", "WETH", "WBTC", "LINK", "UNI", "AAVE"
                    ],
                    "note": "Flash loan fees may vary by asset and network",
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get flash loan info: {str(e)}"
            }
    
    async def _get_interest_rates(self, **kwargs) -> dict:
        """Get current interest rates for all assets."""
        try:
            network = kwargs.get("network", "ethereum")
            session = await self._get_session()
            
            url = f"{self.aave_v3_api_url}/reserves"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    reserves = data.get("reserves", [])
                    
                    interest_rates = []
                    for reserve in reserves:
                        if float(reserve.get("totalLiquidity", 0)) > 0:
                            interest_rates.append({
                                "asset": reserve.get("symbol"),
                                "liquidity_rate": reserve.get("liquidityRate"),
                                "variable_borrow_rate": reserve.get("variableBorrowRate"),
                                "stable_borrow_rate": reserve.get("stableBorrowRate"),
                                "utilization_rate": reserve.get("usageRatio"),
                                "total_liquidity": reserve.get("totalLiquidity"),
                                "total_debt": float(reserve.get("totalVariableDebt", 0)) + float(reserve.get("totalStableDebt", 0))
                            })
                    
                    # Sort by liquidity rate (highest first)
                    interest_rates.sort(key=lambda x: float(x["liquidity_rate"]), reverse=True)
                    
                    return {
                        "success": True,
                        "network": network,
                        "data": {
                            "interest_rates": interest_rates[:15],  # Top 15 by liquidity rate
                            "total_assets": len(interest_rates),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch interest rates: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get interest rates: {str(e)}"
            }
    
    async def _get_historical_data(self, **kwargs) -> dict:
        """Get historical APY and utilization data."""
        try:
            asset = kwargs.get("asset", "USDC")
            days = kwargs.get("days", 30)
            network = kwargs.get("network", "ethereum")
            
            # Generate sample historical data
            # In a real implementation, this would query historical APIs or subgraphs
            historical_data = []
            base_date = datetime.now() - timedelta(days=days)
            
            for i in range(days):
                date = base_date + timedelta(days=i)
                # Simulate realistic APY variations
                base_liquidity_rate = 0.02 + (i % 7) * 0.005  # Varies by day of week
                base_borrow_rate = base_liquidity_rate + 0.01 + (i % 5) * 0.002
                
                historical_data.append({
                    "date": date.strftime("%Y-%m-%d"),
                    "liquidity_rate": f"{base_liquidity_rate:.4f}",
                    "borrow_rate": f"{base_borrow_rate:.4f}",
                    "utilization_rate": f"{0.6 + (i % 10) * 0.02:.2f}",
                    "total_liquidity": f"{1000000 + i * 1000:,.0f}",
                    "total_debt": f"{600000 + i * 600:,.0f}"
                })
            
            return {
                "success": True,
                "asset": asset,
                "network": network,
                "days": days,
                "data": {
                    "historical_data": historical_data,
                    "note": "This is sample historical data. For real historical data, consider using Aave's subgraph or historical APIs.",
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get historical data: {str(e)}"
            }
    
    async def _get_risk_analysis(self, **kwargs) -> dict:
        """Get risk analysis for user positions or assets."""
        try:
            user_address = kwargs.get("user_address")
            asset = kwargs.get("asset")
            network = kwargs.get("network", "ethereum")
            
            if not user_address and not asset:
                return {
                    "success": False,
                    "error": "Either user_address or asset parameter is required"
                }
            
            session = await self._get_session()
            
            if user_address:
                # Analyze user risk
                url = f"{self.aave_v3_api_url}/user/{user_address}"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        user_data = data.get("userData", {})
                        
                        health_factor = float(user_data.get("healthFactor", "0"))
                        total_collateral = float(user_data.get("totalCollateralUSD", 0))
                        total_debt = float(user_data.get("totalBorrowsUSD", 0))
                        
                        # Risk assessment
                        risk_level = "LOW"
                        if health_factor < 1.1:
                            risk_level = "HIGH"
                        elif health_factor < 1.5:
                            risk_level = "MEDIUM"
                        
                        liquidation_risk = "LOW"
                        if health_factor < 1.0:
                            liquidation_risk = "IMMINENT"
                        elif health_factor < 1.1:
                            liquidation_risk = "HIGH"
                        elif health_factor < 1.5:
                            liquidation_risk = "MEDIUM"
                        
                        return {
                            "success": True,
                            "user_address": user_address,
                            "network": network,
                            "data": {
                                "health_factor": health_factor,
                                "risk_level": risk_level,
                                "liquidation_risk": liquidation_risk,
                                "total_collateral_usd": total_collateral,
                                "total_debt_usd": total_debt,
                                "collateral_ratio": total_collateral / total_debt if total_debt > 0 else float('inf'),
                                "recommendations": self._get_risk_recommendations(health_factor, total_collateral, total_debt),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to fetch user data: {response.status}"
                        }
            else:
                # Analyze asset risk
                url = f"{self.aave_v3_api_url}/reserves"
                
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        reserves = data.get("reserves", [])
                        
                        target_reserve = None
                        for reserve in reserves:
                            if (reserve.get("symbol", "").upper() == asset.upper() or 
                                reserve.get("underlyingAsset", "").lower() == asset.lower()):
                                target_reserve = reserve
                                break
                        
                        if not target_reserve:
                            return {
                                "success": False,
                                "error": f"Asset {asset} not found"
                            }
                        
                        utilization_rate = float(target_reserve.get("usageRatio", 0))
                        liquidity_rate = float(target_reserve.get("liquidityRate", 0))
                        
                        # Asset risk assessment
                        utilization_risk = "LOW"
                        if utilization_rate > 0.95:
                            utilization_risk = "HIGH"
                        elif utilization_rate > 0.85:
                            utilization_risk = "MEDIUM"
                        
                        return {
                            "success": True,
                            "asset": asset,
                            "network": network,
                            "data": {
                                "utilization_rate": f"{utilization_rate:.2%}",
                                "utilization_risk": utilization_risk,
                                "liquidity_rate": f"{liquidity_rate:.4f}",
                                "total_liquidity": target_reserve.get("totalLiquidity"),
                                "available_liquidity": target_reserve.get("availableLiquidity"),
                                "liquidation_threshold": target_reserve.get("liquidationThreshold"),
                                "liquidation_bonus": target_reserve.get("liquidationBonus"),
                                "risk_factors": [
                                    "High utilization may limit borrowing",
                                    "Low liquidity may affect large transactions",
                                    "Price volatility affects collateral value"
                                ],
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Failed to fetch asset data: {response.status}"
                        }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get risk analysis: {str(e)}"
            }
    
    async def _get_cross_chain_data(self, **kwargs) -> dict:
        """Get Aave data across multiple networks."""
        try:
            networks = kwargs.get("networks", ["ethereum", "polygon", "avalanche"])
            
            cross_chain_data = {}
            
            for network in networks:
                if network in self.supported_networks:
                    try:
                        # Get basic pool data for each network
                        session = await self._get_session()
                        url = f"{self.aave_v3_api_url}/reserves"
                        
                        async with session.get(url) as response:
                            if response.status == 200:
                                data = await response.json()
                                reserves = data.get("reserves", [])
                                
                                total_tvl = 0
                                total_users = 0  # Would need additional API calls for real data
                                
                                for reserve in reserves:
                                    if reserve.get("usageAsCollateralEnabledOnUser"):
                                        total_liquidity = float(reserve.get("totalLiquidity", 0))
                                        price_in_usd = float(reserve.get("priceInUsd", 0))
                                        tvl = total_liquidity * price_in_usd
                                        total_tvl += tvl
                                
                                cross_chain_data[network] = {
                                    "total_tvl": f"${total_tvl:,.2f}",
                                    "total_reserves": len(reserves),
                                    "network_name": self.supported_networks[network],
                                    "status": "active"
                                }
                            else:
                                cross_chain_data[network] = {
                                    "status": "error",
                                    "error": f"API error: {response.status}"
                                }
                    except Exception as e:
                        cross_chain_data[network] = {
                            "status": "error",
                            "error": str(e)
                        }
            
            return {
                "success": True,
                "data": {
                    "networks": cross_chain_data,
                    "total_networks": len(cross_chain_data),
                    "active_networks": len([n for n in cross_chain_data.values() if n.get("status") == "active"]),
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get cross-chain data: {str(e)}"
            }
    
    def _get_risk_recommendations(self, health_factor: float, collateral: float, debt: float) -> List[str]:
        """Generate risk recommendations based on user position."""
        recommendations = []
        
        if health_factor < 1.0:
            recommendations.append("IMMEDIATE ACTION REQUIRED: Add collateral or repay debt to avoid liquidation")
        elif health_factor < 1.1:
            recommendations.append("HIGH RISK: Consider adding more collateral to improve health factor")
        elif health_factor < 1.5:
            recommendations.append("MEDIUM RISK: Monitor position closely and consider reducing debt")
        
        if debt > collateral * 0.8:
            recommendations.append("Consider diversifying collateral to reduce concentration risk")
        
        if health_factor > 2.0:
            recommendations.append("Position is well-collateralized. Consider optimizing for better yields")
        
        return recommendations
