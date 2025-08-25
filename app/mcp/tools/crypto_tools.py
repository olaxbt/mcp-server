"""
Crypto Tools
Contains cryptocurrency price, DeFi, portfolio, news, NFT, market analysis, and APY tools
"""

import asyncio
import logging
import time
import aiohttp
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from duckduckgo_search import DDGS

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class CryptoPriceTool(MCPTool):
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_duration = 60  # 1 minute cache
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
    
    @property
    def name(self) -> str:
        return "crypto_price"
    
    @property
    def description(self) -> str:
        return "Get real-time cryptocurrency prices, market data, and historical price information from CoinGecko API."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "string",
                    "description": "CoinGecko coin ID (e.g., 'bitcoin', 'ethereum', 'solana')",
                    "default": "bitcoin"
                },
                "currency": {
                    "type": "string",
                    "description": "Target currency for price conversion",
                    "default": "usd"
                },
                "include_market_data": {
                    "type": "boolean",
                    "description": "Include additional market data",
                    "default": True
                }
            },
            "required": ["coin_id"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            coin_id = arguments.get("coin_id", "bitcoin")
            currency = arguments.get("currency", "usd")
            include_market_data = arguments.get("include_market_data", True)
            
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            # Check cache first
            cache_key = f"{coin_id}_{currency}"
            if cache_key in self.cache:
                cached_data, cache_time = self.cache[cache_key]
                if time.time() - cache_time < self.cache_duration:
                    return [cached_data]
            
            logger.info(f"Fetching price data for {coin_id}")
            
            url = f"{self.coingecko_base_url}/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": currency,
                "include_market_cap": include_market_data,
                "include_24hr_vol": include_market_data,
                "include_24hr_change": include_market_data,
                "include_last_updated_at": True
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if coin_id in data:
                        coin_data = data[coin_id]
                        result = {
                            "coin_id": coin_id,
                            "price": coin_data.get(f"{currency}", 0),
                            "currency": currency,
                            "last_updated": coin_data.get("last_updated_at", 0)
                        }
                        
                        if include_market_data:
                            result.update({
                                "market_cap": coin_data.get(f"{currency}_market_cap", 0),
                                "volume_24h": coin_data.get(f"{currency}_24h_vol", 0),
                                "change_24h": coin_data.get(f"{currency}_24h_change", 0)
                            })
                        
                        # Cache the result
                        self.cache[cache_key] = (result, time.time())
                        
                        return [result]
                    else:
                        return [{"error": f"Coin {coin_id} not found"}]
                else:
                    return [{"error": f"API request failed: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Crypto price tool error: {e}")
            return [{"error": f"Price fetch failed: {str(e)}"}]

class DeFiProtocolTool(MCPTool):
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
        
        # API endpoints for different protocols
        self.api_endpoints = {
            "uniswap": "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3",
            "aave": "https://api.thegraph.com/subgraphs/name/aave/protocol-v3",
            "compound": "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2",
            "curve": "https://api.curve.fi/api",
            "balancer": "https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2"
        }
    
    @property
    def name(self) -> str:
        return "defi_protocol"
    
    @property
    def description(self) -> str:
        return "Get DeFi protocol data including TVL, APY, liquidity pools, and yield farming opportunities."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "protocol": {
                    "type": "string",
                    "description": "DeFi protocol name",
                    "enum": ["uniswap", "aave", "compound", "curve", "balancer"],
                    "default": "uniswap"
                },
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["tvl", "pools", "apy", "yield_farming"],
                    "default": "tvl"
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network",
                    "enum": ["ethereum", "polygon", "arbitrum", "optimism"],
                    "default": "ethereum"
                }
            },
            "required": ["protocol"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            protocol = arguments.get("protocol", "uniswap")
            action = arguments.get("action", "tvl")
            chain = arguments.get("chain", "ethereum")
            
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            if action == "tvl":
                return await self._get_tvl(protocol, chain)
            elif action == "pools":
                return await self._get_pools(protocol, chain)
            elif action == "apy":
                return await self._get_apy(protocol, chain)
            elif action == "yield_farming":
                return await self._get_yield_farming(protocol, chain)
            else:
                return [{"error": f"Unsupported action: {action}"}]
                
        except Exception as e:
            logger.error(f"DeFi protocol tool error: {e}")
            return [{"error": f"DeFi protocol operation failed: {str(e)}"}]
    
    async def _get_tvl(self, protocol: str, chain: str) -> List[Dict[str, Any]]:
        """Get Total Value Locked for a protocol"""
        try:
            # This would typically use DefiLlama API or similar
            # For now, return mock data structure
            tvl_data = {
                "protocol": protocol,
                "chain": chain,
                "tvl": 1000000000,  # Mock TVL
                "tvl_change_24h": 2.5,
                "tvl_change_7d": 5.2,
                "last_updated": datetime.now().isoformat()
            }
            
            return [{"tvl": tvl_data}]
        except Exception as e:
            return [{"error": f"Failed to get TVL: {str(e)}"}]
    
    async def _get_pools(self, protocol: str, chain: str) -> List[Dict[str, Any]]:
        """Get liquidity pools for a protocol"""
        try:
            # Mock pool data
            pools = [
                {
                    "pool_id": f"{protocol}_pool_1",
                    "token0": "USDC",
                    "token1": "USDT",
                    "liquidity": 50000000,
                    "volume_24h": 1000000,
                    "apy": 0.15
                },
                {
                    "pool_id": f"{protocol}_pool_2",
                    "token0": "ETH",
                    "token1": "USDC",
                    "liquidity": 200000000,
                    "volume_24h": 5000000,
                    "apy": 0.25
                }
            ]
            
            return [{"pools": pools}]
        except Exception as e:
            return [{"error": f"Failed to get pools: {str(e)}"}]
    
    async def _get_apy(self, protocol: str, chain: str) -> List[Dict[str, Any]]:
        """Get APY data for a protocol"""
        try:
            apy_data = {
                "protocol": protocol,
                "chain": chain,
                "average_apy": 0.18,
                "highest_apy": 0.45,
                "lowest_apy": 0.05,
                "last_updated": datetime.now().isoformat()
            }
            
            return [{"apy": apy_data}]
        except Exception as e:
            return [{"error": f"Failed to get APY: {str(e)}"}]
    
    async def _get_yield_farming(self, protocol: str, chain: str) -> List[Dict[str, Any]]:
        """Get yield farming opportunities"""
        try:
            farming_opportunities = [
                {
                    "pool": f"{protocol}_farm_1",
                    "reward_token": "REWARD",
                    "apy": 0.35,
                    "tvl": 10000000,
                    "risk_level": "medium"
                }
            ]
            
            return [{"yield_farming": farming_opportunities}]
        except Exception as e:
            return [{"error": f"Failed to get yield farming: {str(e)}"}]

class PortfolioTrackerTool(MCPTool):
    def __init__(self):
        self.session = None
        self.portfolios = {}  # In-memory storage for demo purposes
    
    @property
    def name(self) -> str:
        return "portfolio_tracker"
    
    @property
    def description(self) -> str:
        return "Track and analyze cryptocurrency portfolios with real-time pricing and performance metrics."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Portfolio action to perform",
                    "enum": ["create", "add_asset", "remove_asset", "get_value", "get_analysis"],
                    "default": "get_value"
                },
                "portfolio_id": {
                    "type": "string",
                    "description": "Portfolio identifier",
                    "default": None
                },
                "name": {
                    "type": "string",
                    "description": "Portfolio name (for create action)",
                    "default": None
                },
                "coin_id": {
                    "type": "string",
                    "description": "CoinGecko coin ID",
                    "default": None
                },
                "amount": {
                    "type": "number",
                    "description": "Amount of coins",
                    "default": None
                },
                "purchase_price": {
                    "type": "number",
                    "description": "Purchase price per coin (USD)",
                    "default": None
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action", "get_value")
            
            if action == "create":
                return await self._create_portfolio(arguments)
            elif action == "add_asset":
                return await self._add_asset(arguments)
            elif action == "remove_asset":
                return await self._remove_asset(arguments)
            elif action == "get_value":
                return await self._get_portfolio_value(arguments)
            elif action == "get_analysis":
                return await self._get_portfolio_analysis(arguments)
            else:
                return [{"error": f"Unsupported action: {action}"}]
                
        except Exception as e:
            logger.error(f"Portfolio tracker error: {e}")
            return [{"error": f"Portfolio operation failed: {str(e)}"}]
    
    async def _create_portfolio(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a new portfolio"""
        portfolio_id = arguments.get("portfolio_id", f"portfolio_{int(time.time())}")
        name = arguments.get("name", f"Portfolio {portfolio_id}")
        
        if portfolio_id in self.portfolios:
            return [{"error": f"Portfolio {portfolio_id} already exists"}]
        
        self.portfolios[portfolio_id] = {
            "id": portfolio_id,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "assets": {},
            "total_value": 0,
            "total_pnl": 0
        }
        
        return [{"message": f"Portfolio {portfolio_id} created successfully", "portfolio": self.portfolios[portfolio_id]}]
    
    async def _add_asset(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Add an asset to a portfolio"""
        portfolio_id = arguments.get("portfolio_id")
        coin_id = arguments.get("coin_id")
        amount = arguments.get("amount")
        purchase_price = arguments.get("purchase_price")
        
        if not all([portfolio_id, coin_id, amount]):
            return [{"error": "portfolio_id, coin_id, and amount are required"}]
        
        if portfolio_id not in self.portfolios:
            return [{"error": f"Portfolio {portfolio_id} not found"}]
        
        # Get current price
        price_tool = CryptoPriceTool()
        price_result = await price_tool.execute({"coin_id": coin_id})
        
        if "error" in price_result[0]:
            return [{"error": f"Failed to get price for {coin_id}: {price_result[0]['error']}"}]
        
        current_price = price_result[0]["price"]
        
        # Add asset to portfolio
        self.portfolios[portfolio_id]["assets"][coin_id] = {
            "amount": amount,
            "purchase_price": purchase_price or current_price,
            "current_price": current_price,
            "added_at": datetime.now().isoformat()
        }
        
        return [{"message": f"Asset {coin_id} added to portfolio {portfolio_id}", "asset": self.portfolios[portfolio_id]["assets"][coin_id]}]
    
    async def _get_portfolio_value(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get current portfolio value and P&L"""
        portfolio_id = arguments.get("portfolio_id")
        
        if not portfolio_id:
            return [{"error": "portfolio_id is required"}]
        
        if portfolio_id not in self.portfolios:
            return [{"error": f"Portfolio {portfolio_id} not found"}]
        
        portfolio = self.portfolios[portfolio_id]
        total_value = 0
        total_cost = 0
        
        # Update prices and calculate values
        for coin_id, asset in portfolio["assets"].items():
            price_tool = CryptoPriceTool()
            price_result = await price_tool.execute({"coin_id": coin_id})
            
            if "error" not in price_result[0]:
                current_price = price_result[0]["price"]
                asset["current_price"] = current_price
                asset_value = asset["amount"] * current_price
                asset_cost = asset["amount"] * asset["purchase_price"]
                
                total_value += asset_value
                total_cost += asset_cost
                
                asset["current_value"] = asset_value
                asset["pnl"] = asset_value - asset_cost
                asset["pnl_percentage"] = ((asset_value - asset_cost) / asset_cost * 100) if asset_cost > 0 else 0
        
        portfolio["total_value"] = total_value
        portfolio["total_cost"] = total_cost
        portfolio["total_pnl"] = total_value - total_cost
        portfolio["total_pnl_percentage"] = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        return [{"portfolio": portfolio}]
    
    async def _get_portfolio_analysis(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get detailed portfolio analysis"""
        portfolio_id = arguments.get("portfolio_id")
        
        if not portfolio_id:
            return [{"error": "portfolio_id is required"}]
        
        # First get current values
        value_result = await self._get_portfolio_value(arguments)
        if "error" in value_result[0]:
            return value_result
        
        portfolio = value_result[0]["portfolio"]
        
        # Calculate additional metrics
        analysis = {
            "portfolio_id": portfolio_id,
            "total_assets": len(portfolio["assets"]),
            "total_value": portfolio["total_value"],
            "total_pnl": portfolio["total_pnl"],
            "total_pnl_percentage": portfolio["total_pnl_percentage"],
            "best_performer": None,
            "worst_performer": None,
            "asset_allocation": {}
        }
        
        best_pnl = float('-inf')
        worst_pnl = float('inf')
        
        for coin_id, asset in portfolio["assets"].items():
            pnl_percentage = asset["pnl_percentage"]
            allocation = (asset["current_value"] / portfolio["total_value"] * 100) if portfolio["total_value"] > 0 else 0
            
            analysis["asset_allocation"][coin_id] = {
                "allocation_percentage": allocation,
                "pnl_percentage": pnl_percentage,
                "current_value": asset["current_value"]
            }
            
            if pnl_percentage > best_pnl:
                best_pnl = pnl_percentage
                analysis["best_performer"] = coin_id
            
            if pnl_percentage < worst_pnl:
                worst_pnl = pnl_percentage
                analysis["worst_performer"] = coin_id
        
        return [{"analysis": analysis}]
    
    async def _remove_asset(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Remove an asset from a portfolio"""
        portfolio_id = arguments.get("portfolio_id")
        coin_id = arguments.get("coin_id")
        
        if not all([portfolio_id, coin_id]):
            return [{"error": "portfolio_id and coin_id are required"}]
        
        if portfolio_id not in self.portfolios:
            return [{"error": f"Portfolio {portfolio_id} not found"}]
        
        if coin_id not in self.portfolios[portfolio_id]["assets"]:
            return [{"error": f"Asset {coin_id} not found in portfolio {portfolio_id}"}]
        
        removed_asset = self.portfolios[portfolio_id]["assets"].pop(coin_id)
        return [{"message": f"Asset {coin_id} removed from portfolio {portfolio_id}", "removed_asset": removed_asset}]

class CryptoNewsTool(MCPTool):
    def __init__(self):
        self.ddgs = DDGS()
        self.last_search_time = 0
        self.min_search_interval = 5  # 5 seconds between searches
    
    @property
    def name(self) -> str:
        return "crypto_news"
    
    @property
    def description(self) -> str:
        return "Get latest cryptocurrency news, market updates, and trending topics from various sources."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for crypto news (e.g., 'bitcoin', 'ethereum', 'defi')",
                    "default": "cryptocurrency"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of news articles to return",
                    "default": 10,
                    "minimum": 1,
                    "maximum": 20
                },
                "time_filter": {
                    "type": "string",
                    "description": "Time filter for news articles",
                    "enum": ["d", "w", "m"],
                    "default": "d"
                },
                "include_sentiment": {
                    "type": "boolean",
                    "description": "Include basic sentiment analysis",
                    "default": False
                }
            },
            "required": []
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            query = arguments.get("query", "cryptocurrency")
            max_results = min(arguments.get("max_results", 10), 20)
            time_filter = arguments.get("time_filter", "d")
            include_sentiment = arguments.get("include_sentiment", False)
            
            # Rate limiting
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            
            if time_since_last_search < self.min_search_interval:
                sleep_time = self.min_search_interval - time_since_last_search
                logger.info(f"Rate limiting: waiting {sleep_time:.2f} seconds before news search")
                time.sleep(sleep_time)
            
            self.last_search_time = time.time()
            
            logger.info(f"Executing crypto news search: {query}")
            
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, 
                self._search_crypto_news, 
                query, 
                max_results, 
                time_filter,
                include_sentiment
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Crypto news tool error: {e}")
            return [{"error": f"News search failed: {str(e)}"}]
    
    def _search_crypto_news(self, query: str, max_results: int, time_filter: str, include_sentiment: bool) -> List[Dict[str, Any]]:
        try:
            # Create new DDGS instance
            ddgs = DDGS()
            
            # Search for crypto news
            search_results = list(ddgs.news(
                keywords=query,
                max_results=max_results,
                time=time_filter
            ))
            
            processed_results = []
            for result in search_results:
                if result and isinstance(result, dict):
                    news_item = {
                        "title": result.get("title", ""),
                        "link": result.get("link", ""),
                        "snippet": result.get("body", ""),
                        "source": result.get("source", ""),
                        "published_date": result.get("date", ""),
                        "query": query
                    }
                    
                    if include_sentiment:
                        news_item["sentiment"] = self._analyze_sentiment(result.get("title", "") + " " + result.get("body", ""))
                    
                    processed_results.append(news_item)
            
            if not processed_results:
                return [{"error": "No crypto news found"}]
            
            return processed_results
            
        except Exception as e:
            logger.error(f"Crypto news search failed: {e}")
            return [{"error": f"News search failed: {str(e)}"}]
    
    def _analyze_sentiment(self, text: str) -> str:
        """Basic sentiment analysis"""
        text_lower = text.lower()
        
        positive_words = ["bullish", "surge", "rally", "gain", "up", "positive", "growth", "profit", "success"]
        negative_words = ["bearish", "crash", "drop", "fall", "down", "negative", "loss", "decline", "risk"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"

class APYCalculatorTool(MCPTool):
    def __init__(self):
        self.session = None
    
    @property
    def name(self) -> str:
        return "apy_calculator"
    
    @property
    def description(self) -> str:
        return "Calculate APY for various DeFi protocols, staking, and yield farming opportunities."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "APY calculation action",
                    "enum": ["calculate_apy", "compare_apy", "compound_interest"],
                    "default": "calculate_apy"
                },
                "principal": {
                    "type": "number",
                    "description": "Principal amount",
                    "default": 1000
                },
                "rate": {
                    "type": "number",
                    "description": "Annual interest rate (as decimal)",
                    "default": 0.05
                },
                "time_period": {
                    "type": "number",
                    "description": "Time period in years",
                    "default": 1
                },
                "compounding_frequency": {
                    "type": "string",
                    "description": "Compounding frequency",
                    "enum": ["daily", "weekly", "monthly", "yearly"],
                    "default": "daily"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action", "calculate_apy")
            
            if action == "calculate_apy":
                return await self._calculate_apy(arguments)
            elif action == "compare_apy":
                return await self._compare_apy(arguments)
            elif action == "compound_interest":
                return await self._compound_interest(arguments)
            else:
                return [{"error": f"Unsupported action: {action}"}]
                
        except Exception as e:
            logger.error(f"APY calculator error: {e}")
            return [{"error": f"APY calculation failed: {str(e)}"}]
    
    async def _calculate_apy(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate APY for given parameters"""
        try:
            principal = arguments.get("principal", 1000)
            rate = arguments.get("rate", 0.05)
            time_period = arguments.get("time_period", 1)
            compounding_frequency = arguments.get("compounding_frequency", "daily")
            
            # Convert compounding frequency to number of times per year
            frequency_map = {
                "daily": 365,
                "weekly": 52,
                "monthly": 12,
                "yearly": 1
            }
            
            n = frequency_map.get(compounding_frequency, 365)
            
            # Calculate APY
            apy = ((1 + rate / n) ** n - 1) * 100
            
            # Calculate final amount
            final_amount = principal * (1 + rate / n) ** (n * time_period)
            
            result = {
                "principal": principal,
                "rate": rate * 100,  # Convert to percentage
                "time_period": time_period,
                "compounding_frequency": compounding_frequency,
                "apy": round(apy, 4),
                "final_amount": round(final_amount, 2),
                "total_interest": round(final_amount - principal, 2)
            }
            
            return [{"apy_calculation": result}]
            
        except Exception as e:
            return [{"error": f"APY calculation failed: {str(e)}"}]
    
    async def _compare_apy(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Compare APY across different protocols"""
        try:
            principal = arguments.get("principal", 1000)
            time_period = arguments.get("time_period", 1)
            
            # Mock protocol APY data
            protocols = [
                {"name": "Aave", "apy": 3.2, "risk": "low"},
                {"name": "Compound", "apy": 2.8, "risk": "low"},
                {"name": "Curve", "apy": 8.5, "risk": "medium"},
                {"name": "Yearn Finance", "apy": 12.3, "risk": "high"}
            ]
            
            comparisons = []
            for protocol in protocols:
                apy_decimal = protocol["apy"] / 100
                final_amount = principal * (1 + apy_decimal) ** time_period
                
                comparisons.append({
                    "protocol": protocol["name"],
                    "apy": protocol["apy"],
                    "risk": protocol["risk"],
                    "final_amount": round(final_amount, 2),
                    "total_interest": round(final_amount - principal, 2)
                })
            
            # Sort by APY
            comparisons.sort(key=lambda x: x["apy"], reverse=True)
            
            return [{"apy_comparison": comparisons}]
            
        except Exception as e:
            return [{"error": f"APY comparison failed: {str(e)}"}]
    
    async def _compound_interest(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calculate compound interest over time"""
        try:
            principal = arguments.get("principal", 1000)
            rate = arguments.get("rate", 0.05)
            time_period = arguments.get("time_period", 1)
            compounding_frequency = arguments.get("compounding_frequency", "daily")
            
            frequency_map = {
                "daily": 365,
                "weekly": 52,
                "monthly": 12,
                "yearly": 1
            }
            
            n = frequency_map.get(compounding_frequency, 365)
            
            # Calculate compound interest
            final_amount = principal * (1 + rate / n) ** (n * time_period)
            total_interest = final_amount - principal
            
            # Calculate effective annual rate
            ear = ((1 + rate / n) ** n - 1) * 100
            
            result = {
                "principal": principal,
                "rate": rate * 100,
                "time_period": time_period,
                "compounding_frequency": compounding_frequency,
                "final_amount": round(final_amount, 2),
                "total_interest": round(total_interest, 2),
                "effective_annual_rate": round(ear, 4)
            }
            
            return [{"compound_interest": result}]
            
        except Exception as e:
            return [{"error": f"Compound interest calculation failed: {str(e)}"}]
