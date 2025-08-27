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



class LunarCrushTool(MCPTool):
    """Tool for accessing LunarCrush cryptocurrency analytics and social sentiment data"""
    
    def __init__(self):
        self.session = None
        self.lunarcrush_base_url = "https://api.lunarcrush.com/v2"
        # Note: LunarCrush API requires authentication - user needs to provide API key
    
    @property
    def name(self) -> str:
        return "lunarcrush"
    
    @property
    def description(self) -> str:
        return "Access LunarCrush cryptocurrency analytics, social sentiment, and market intelligence data"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_social_sentiment",
                        "get_market_intelligence", 
                        "get_influence_analysis",
                        "get_trending_assets",
                        "get_historical_data",
                        "get_comparative_analysis"
                    ],
                    "description": "The action to perform"
                },
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol (e.g., 'BTC', 'ETH', 'SOL')"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return (default: 10, max: 100)"
                },
                "timeframe": {
                    "type": "string",
                    "enum": ["1h", "24h", "7d", "30d"],
                    "description": "Timeframe for data (default: 24h)"
                },
                "metrics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific metrics to include"
                },
                "api_key": {
                    "type": "string",
                    "description": "LunarCrush API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute LunarCrush tool based on action"""
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: LunarCrush API key is required. Please provide your API key."}]
            
            if action == "get_social_sentiment":
                return await self._get_social_sentiment(arguments, api_key)
            elif action == "get_market_intelligence":
                return await self._get_market_intelligence(arguments, api_key)
            elif action == "get_influence_analysis":
                return await self._get_influence_analysis(arguments, api_key)
            elif action == "get_trending_assets":
                return await self._get_trending_assets(arguments, api_key)
            elif action == "get_historical_data":
                return await self._get_historical_data(arguments, api_key)
            elif action == "get_comparative_analysis":
                return await self._get_comparative_analysis(arguments, api_key)
            else:
                return [{"type": "text", "text": f"❌ Error: Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in LunarCrush tool: {e}")
            return [{"type": "text", "text": f"❌ Error: LunarCrush tool error: {str(e)}"}]
        finally:
            await self._cleanup_session()
    
    async def _get_social_sentiment(self, arguments: Dict[str, Any], api_key: str = None) -> List[Dict[str, Any]]:
        """Get social sentiment data for a cryptocurrency"""
        try:
            symbol = arguments.get("symbol", "BTC")
            timeframe = arguments.get("timeframe", "24h")
            
            if not api_key:
                return [{
                    "type": "lunarcrush_social_sentiment",
                    "symbol": symbol,
                    "note": "LunarCrush API key required. Set LUNARCRUSH_API_KEY environment variable.",
                    "sample_data": {
                        "social_volume": 125000,
                        "social_score": 85.2,
                        "social_contributors": 4500,
                        "social_engagement": 0.78,
                        "sentiment_score": 0.65,
                        "bullish_sentiment": 0.68,
                        "bearish_sentiment": 0.32,
                        "top_mentions": [
                            {"platform": "Twitter", "count": 45000},
                            {"platform": "Reddit", "count": 32000},
                            {"platform": "Telegram", "count": 28000}
                        ],
                        "trending_topics": ["DeFi", "NFT", "Layer2", "Staking"]
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            
            session = await self._get_session()
            url = f"{self.lunarcrush_base_url}/assets"
            params = {
                "symbol": symbol,
                "interval": timeframe,
                "key": api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    asset_data = data.get("data", [{}])[0] if data.get("data") else {}
                    
                    sentiment_data = {
                        "type": "lunarcrush_social_sentiment",
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "social_volume": asset_data.get("social_volume", 0),
                        "social_score": asset_data.get("social_score", 0),
                        "social_contributors": asset_data.get("social_contributors", 0),
                        "social_engagement": asset_data.get("social_engagement", 0),
                        "sentiment_score": asset_data.get("sentiment_score", 0),
                        "bullish_sentiment": asset_data.get("bullish_sentiment", 0),
                        "bearish_sentiment": asset_data.get("bearish_sentiment", 0),
                        "alt_rank": asset_data.get("alt_rank", 0),
                        "galaxy_score": asset_data.get("galaxy_score", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    return [sentiment_data]
                else:
                    return [{"error": f"Failed to get social sentiment: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting social sentiment: {e}")
            return [{"error": f"Failed to get social sentiment: {str(e)}"}]
    
    async def _get_market_intelligence(self, arguments: Dict[str, Any], api_key: str = None) -> List[Dict[str, Any]]:
        """Get market intelligence data for a cryptocurrency"""
        try:
            symbol = arguments.get("symbol", "BTC")
            timeframe = arguments.get("timeframe", "24h")
            
            if not api_key:
                return [{
                    "type": "lunarcrush_market_intelligence",
                    "symbol": symbol,
                    "note": "LunarCrush API key required. Set LUNARCRUSH_API_KEY environment variable.",
                    "sample_data": {
                        "price": 45000.0,
                        "price_change_24h": 2.5,
                        "volume_24h": 28000000000,
                        "market_cap": 850000000000,
                        "market_cap_change_24h": 1.8,
                        "circulating_supply": 18900000,
                        "max_supply": 21000000,
                        "volatility": 0.045,
                        "correlation_rank": 0.92,
                        "market_dominance": 42.5
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            
            session = await self._get_session()
            url = f"{self.lunarcrush_base_url}/assets"
            params = {
                "symbol": symbol,
                "interval": timeframe,
                "key": api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    asset_data = data.get("data", [{}])[0] if data.get("data") else {}
                    
                    market_data = {
                        "type": "lunarcrush_market_intelligence",
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "price": asset_data.get("price", 0),
                        "price_change_24h": asset_data.get("price_change_24h", 0),
                        "volume_24h": asset_data.get("volume_24h", 0),
                        "market_cap": asset_data.get("market_cap", 0),
                        "market_cap_change_24h": asset_data.get("market_cap_change_24h", 0),
                        "circulating_supply": asset_data.get("circulating_supply", 0),
                        "max_supply": asset_data.get("max_supply", 0),
                        "volatility": asset_data.get("volatility", 0),
                        "correlation_rank": asset_data.get("correlation_rank", 0),
                        "market_dominance": asset_data.get("market_dominance", 0),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    return [market_data]
                else:
                    return [{"error": f"Failed to get market intelligence: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting market intelligence: {e}")
            return [{"error": f"Failed to get market intelligence: {str(e)}"}]
    
    async def _get_influence_analysis(self, arguments: Dict[str, Any], api_key: str = None) -> List[Dict[str, Any]]:
        """Get influence analysis and top influencers"""
        try:
            symbol = arguments.get("symbol", "BTC")
            limit = min(arguments.get("limit", 10), 50)
            
            if not api_key:
                return [{
                    "type": "lunarcrush_influence_analysis",
                    "symbol": symbol,
                    "note": "LunarCrush API key required. Set LUNARCRUSH_API_KEY environment variable.",
                    "sample_data": {
                        "total_influencers": 1250,
                        "top_influencers": [
                            {
                                "username": "@crypto_expert",
                                "platform": "Twitter",
                                "followers": 2500000,
                                "influence_score": 95.2,
                                "sentiment_impact": 0.78
                            },
                            {
                                "username": "crypto_analyst",
                                "platform": "Reddit",
                                "followers": 150000,
                                "influence_score": 88.5,
                                "sentiment_impact": 0.65
                            }
                        ],
                        "influence_distribution": {
                            "high_influence": 45,
                            "medium_influence": 320,
                            "low_influence": 885
                        }
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            
            session = await self._get_session()
            url = f"{self.lunarcrush_base_url}/influencers"
            params = {
                "symbol": symbol,
                "limit": limit,
                "key": api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    influencers = data.get("data", [])
                    
                    influence_data = {
                        "type": "lunarcrush_influence_analysis",
                        "symbol": symbol,
                        "total_influencers": len(influencers),
                        "top_influencers": [
                            {
                                "username": inf.get("username", ""),
                                "platform": inf.get("platform", ""),
                                "followers": inf.get("followers", 0),
                                "influence_score": inf.get("influence_score", 0),
                                "sentiment_impact": inf.get("sentiment_impact", 0),
                                "engagement_rate": inf.get("engagement_rate", 0)
                            }
                            for inf in influencers[:limit]
                        ],
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    return [influence_data]
                else:
                    return [{"error": f"Failed to get influence analysis: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting influence analysis: {e}")
            return [{"error": f"Failed to get influence analysis: {str(e)}"}]
    
    async def _get_trending_assets(self, arguments: Dict[str, Any], api_key: str = None) -> List[Dict[str, Any]]:
        """Get currently trending cryptocurrencies"""
        try:
            limit = min(arguments.get("limit", 10), 100)
            timeframe = arguments.get("timeframe", "24h")
            
            if not api_key:
                return [{
                    "type": "lunarcrush_trending_assets",
                    "note": "LunarCrush API key required. Set LUNARCRUSH_API_KEY environment variable.",
                    "sample_data": {
                        "trending_assets": [
                            {
                                "symbol": "SOL",
                                "name": "Solana",
                                "social_score": 92.5,
                                "galaxy_score": 88.3,
                                "price_change_24h": 15.2,
                                "social_volume": 180000,
                                "trend_reason": "DeFi ecosystem growth"
                            },
                            {
                                "symbol": "ETH",
                                "name": "Ethereum",
                                "social_score": 89.1,
                                "galaxy_score": 85.7,
                                "price_change_24h": 3.8,
                                "social_volume": 150000,
                                "trend_reason": "Layer 2 developments"
                            }
                        ]
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            
            session = await self._get_session()
            url = f"{self.lunarcrush_base_url}/assets"
            params = {
                "interval": timeframe,
                "limit": limit,
                "sort": "social_score",
                "key": api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    assets = data.get("data", [])
                    
                    trending_data = {
                        "type": "lunarcrush_trending_assets",
                        "timeframe": timeframe,
                        "trending_assets": [
                            {
                                "symbol": asset.get("symbol", ""),
                                "name": asset.get("name", ""),
                                "social_score": asset.get("social_score", 0),
                                "galaxy_score": asset.get("galaxy_score", 0),
                                "alt_rank": asset.get("alt_rank", 0),
                                "price": asset.get("price", 0),
                                "price_change_24h": asset.get("price_change_24h", 0),
                                "social_volume": asset.get("social_volume", 0),
                                "market_cap": asset.get("market_cap", 0)
                            }
                            for asset in assets[:limit]
                        ],
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    return [trending_data]
                else:
                    return [{"error": f"Failed to get trending assets: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting trending assets: {e}")
            return [{"error": f"Failed to get trending assets: {str(e)}"}]
    
    async def _get_historical_data(self, arguments: Dict[str, Any], api_key: str = None) -> List[Dict[str, Any]]:
        """Get historical social and market data"""
        try:
            symbol = arguments.get("symbol", "BTC")
            timeframe = arguments.get("timeframe", "7d")
            
            if not api_key:
                return [{
                    "type": "lunarcrush_historical_data",
                    "symbol": symbol,
                    "note": "LunarCrush API key required. Set LUNARCRUSH_API_KEY environment variable.",
                    "sample_data": {
                        "historical_points": [
                            {
                                "timestamp": "2024-01-01T00:00:00Z",
                                "price": 42000.0,
                                "social_volume": 120000,
                                "social_score": 82.5,
                                "sentiment_score": 0.68
                            },
                            {
                                "timestamp": "2024-01-02T00:00:00Z", 
                                "price": 43500.0,
                                "social_volume": 135000,
                                "social_score": 85.2,
                                "sentiment_score": 0.72
                            }
                        ]
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            
            session = await self._get_session()
            url = f"{self.lunarcrush_base_url}/assets/{symbol}/time-series"
            params = {
                "interval": timeframe,
                "key": api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    time_series = data.get("data", [])
                    
                    historical_data = {
                        "type": "lunarcrush_historical_data",
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "historical_points": [
                            {
                                "timestamp": point.get("timestamp", ""),
                                "price": point.get("price", 0),
                                "social_volume": point.get("social_volume", 0),
                                "social_score": point.get("social_score", 0),
                                "sentiment_score": point.get("sentiment_score", 0),
                                "volume_24h": point.get("volume_24h", 0),
                                "market_cap": point.get("market_cap", 0)
                            }
                            for point in time_series
                        ],
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    return [historical_data]
                else:
                    return [{"error": f"Failed to get historical data: {response.status}"}]
                    
        except Exception as e:
            logger.error(f"Error getting historical data: {e}")
            return [{"error": f"Failed to get historical data: {str(e)}"}]
    
    async def _get_comparative_analysis(self, arguments: Dict[str, Any], api_key: str = None) -> List[Dict[str, Any]]:
        """Compare multiple cryptocurrencies"""
        try:
            symbols = arguments.get("symbols", ["BTC", "ETH", "SOL"])
            timeframe = arguments.get("timeframe", "24h")
            
            if not api_key:
                return [{
                    "type": "lunarcrush_comparative_analysis",
                    "symbols": symbols,
                    "note": "LunarCrush API key required. Set LUNARCRUSH_API_KEY environment variable.",
                    "sample_data": {
                        "comparison": [
                            {
                                "symbol": "BTC",
                                "social_score": 85.2,
                                "galaxy_score": 82.1,
                                "price_change_24h": 2.5,
                                "social_volume": 150000,
                                "market_cap": 850000000000
                            },
                            {
                                "symbol": "ETH", 
                                "social_score": 88.7,
                                "galaxy_score": 85.3,
                                "price_change_24h": 3.8,
                                "social_volume": 120000,
                                "market_cap": 320000000000
                            }
                        ]
                    },
                    "timestamp": datetime.now().isoformat()
                }]
            
            session = await self._get_session()
            comparison_data = []
            
            for symbol in symbols:
                url = f"{self.lunarcrush_base_url}/assets"
                params = {
                    "symbol": symbol,
                    "interval": timeframe,
                    "key": api_key
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        asset_data = data.get("data", [{}])[0] if data.get("data") else {}
                        
                        comparison_data.append({
                            "symbol": symbol,
                            "social_score": asset_data.get("social_score", 0),
                            "galaxy_score": asset_data.get("galaxy_score", 0),
                            "alt_rank": asset_data.get("alt_rank", 0),
                            "price": asset_data.get("price", 0),
                            "price_change_24h": asset_data.get("price_change_24h", 0),
                            "social_volume": asset_data.get("social_volume", 0),
                            "market_cap": asset_data.get("market_cap", 0),
                            "sentiment_score": asset_data.get("sentiment_score", 0)
                        })
            
            return [{
                "type": "lunarcrush_comparative_analysis",
                "symbols": symbols,
                "timeframe": timeframe,
                "comparison": comparison_data,
                "timestamp": datetime.now().isoformat()
            }]
                    
        except Exception as e:
            logger.error(f"Error getting comparative analysis: {e}")
            return [{"error": f"Failed to get comparative analysis: {str(e)}"}]


class CoinDeskTool(MCPTool):
    """Tool for accessing CoinDesk cryptocurrency data, prices, indices, and news."""
    
    def __init__(self):
        self.session = None
        self.coindesk_base_url = "https://api.coindesk.com/v1"
        # Note: CoinDesk API key will be provided by user
    
    @property
    def name(self) -> str:
        return "coindesk"
    
    @property
    def description(self) -> str:
        return "Access CoinDesk cryptocurrency data including real-time prices, historical data, Bitcoin Price Index, and market information"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_current_price",
                        "get_historical_price",
                        "get_bitcoin_price_index",
                        "get_supported_currencies",
                        "get_market_data",
                        "get_news"
                    ],
                    "description": "The action to perform"
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code (e.g., 'USD', 'EUR', 'GBP')",
                    "default": "USD"
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date for historical data (YYYY-MM-DD)",
                    "default": None
                },
                "end_date": {
                    "type": "string",
                    "description": "End date for historical data (YYYY-MM-DD)",
                    "default": None
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 10
                },
                "api_key": {
                    "type": "string",
                    "description": "CoinDesk API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the CoinDesk tool action."""
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: CoinDesk API key is required. Please provide your API key."}]
            
            if action == "get_current_price":
                result = await self._get_current_price(arguments, api_key)
                return [result]
            elif action == "get_historical_price":
                result = await self._get_historical_price(arguments, api_key)
                return [result]
            elif action == "get_bitcoin_price_index":
                result = await self._get_bitcoin_price_index(arguments, api_key)
                return [result]
            elif action == "get_supported_currencies":
                result = await self._get_supported_currencies(arguments, api_key)
                return [result]
            elif action == "get_market_data":
                result = await self._get_market_data(arguments, api_key)
                return [result]
            elif action == "get_news":
                result = await self._get_news(arguments, api_key)
                return [result]
            else:
                return [{"error": f"Unknown action: {action}"}]
        finally:
            await self._cleanup_session()
    
    async def _get_current_price(self, arguments: Dict[str, Any], api_key: str = None) -> dict:
        """Get current Bitcoin price in specified currency."""
        currency = arguments.get("currency", "USD")
        
        # If no API key, return sample data
        if not api_key:
            return {
                "success": True,
                "data": {
                    "currency": currency,
                    "price": 45000.0,
                    "description": f"Bitcoin price in {currency}",
                    "updated": datetime.now().isoformat(),
                    "note": "Sample data. Provide CoinDesk API key for real-time data."
                }
            }
        
        try:
            session = await self._get_session()
            url = f"{self.coindesk_base_url}/bpi/currentprice/{currency}.json"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "currency": currency,
                            "price": data.get("bpi", {}).get(currency, {}).get("rate_float"),
                            "description": data.get("bpi", {}).get(currency, {}).get("description"),
                            "updated": data.get("time", {}).get("updated"),
                            "updated_iso": data.get("time", {}).get("updatedISO")
                        }
                    }
                else:
                    return {"error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get current price: {str(e)}"
            }
    
    async def _get_historical_price(self, arguments: Dict[str, Any], api_key: str = None) -> dict:
        """Get historical Bitcoin price data."""
        currency = arguments.get("currency", "USD")
        start_date = arguments.get("start_date")
        end_date = arguments.get("end_date")
        
        if not start_date or not end_date:
            # Default to last 30 days if no dates provided
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # If no API key, return sample data
        if not api_key:
            return {
                "success": True,
                "data": {
                    "currency": currency,
                    "start_date": start_date,
                    "end_date": end_date,
                    "prices": {
                        "2024-01-01": 42000.0,
                        "2024-01-15": 45000.0,
                        "2024-01-30": 48000.0
                    },
                    "note": "Sample data. Provide CoinDesk API key for real-time data."
                }
            }
        
        try:
            session = await self._get_session()
            url = f"{self.coindesk_base_url}/bpi/historical/close.json"
            params = {
                "currency": currency,
                "start": start_date,
                "end": end_date
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "currency": currency,
                            "start_date": start_date,
                            "end_date": end_date,
                            "prices": data.get("bpi", {}),
                            "disclaimer": data.get("disclaimer"),
                            "updated": data.get("time", {}).get("updated")
                        }
                    }
                else:
                    return {"error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get historical price data: {str(e)}"
            }
    
    async def _get_bitcoin_price_index(self, arguments: Dict[str, Any], api_key: str = None) -> dict:
        """Get Bitcoin Price Index (BPI) data."""
        
        # If no API key, return sample data
        if not api_key:
            return {
                "success": True,
                "data": {
                    "bpi": {
                        "USD": {"code": "USD", "rate": "45,000.00", "description": "United States Dollar", "rate_float": 45000.0},
                        "EUR": {"code": "EUR", "rate": "41,500.00", "description": "Euro", "rate_float": 41500.0},
                        "GBP": {"code": "GBP", "rate": "35,800.00", "description": "British Pound Sterling", "rate_float": 35800.0}
                    },
                    "chart_name": "Bitcoin",
                    "updated": datetime.now().isoformat(),
                    "note": "Sample data. Provide CoinDesk API key for real-time data."
                }
            }
        
        try:
            session = await self._get_session()
            url = f"{self.coindesk_base_url}/bpi/currentprice.json"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "bpi": data.get("bpi", {}),
                            "disclaimer": data.get("disclaimer"),
                            "chart_name": data.get("chartName"),
                            "updated": data.get("time", {}).get("updated"),
                            "updated_iso": data.get("time", {}).get("updatedISO")
                        }
                    }
                else:
                    return {"error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get Bitcoin Price Index: {str(e)}"
            }
    
    async def _get_supported_currencies(self, arguments: Dict[str, Any], api_key: str = None) -> dict:
        """Get list of supported currencies."""
        
        # If no API key, return sample data
        if not api_key:
            return {
                "success": True,
                "data": {
                    "currencies": [
                        {"currency": "USD", "country": "United States"},
                        {"currency": "EUR", "country": "European Union"},
                        {"currency": "GBP", "country": "United Kingdom"},
                        {"currency": "JPY", "country": "Japan"},
                        {"currency": "CNY", "country": "China"}
                    ],
                    "count": 5,
                    "note": "Sample data. Provide CoinDesk API key for real-time data."
                }
            }
        
        try:
            session = await self._get_session()
            url = f"{self.coindesk_base_url}/bpi/supported-currencies.json"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "currencies": data,
                            "count": len(data)
                        }
                    }
                else:
                    return {"error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get supported currencies: {str(e)}"
            }
    
    async def _get_market_data(self, arguments: Dict[str, Any], api_key: str = None) -> dict:
        """Get additional market data (sample implementation)."""
        # Note: CoinDesk's free API is limited, so this returns sample data
        # For real market data, you'd need their premium API
        
        # If no API key, return sample data
        if not api_key:
            return {
                "success": True,
                "data": {
                    "market_cap": "$1,234,567,890,123",
                    "24h_volume": "$45,678,901,234",
                    "24h_change": "+2.34%",
                    "7d_change": "+5.67%",
                    "dominance": "48.2%",
                    "note": "Sample data. Provide CoinDesk API key for real-time data."
                }
            }
    
    async def _get_news(self, arguments: Dict[str, Any], api_key: str = None) -> dict:
        """Get CoinDesk news (sample implementation)."""
        # Note: CoinDesk's news API requires premium access
        # This returns sample news data
        limit = arguments.get("limit", 5)
        
        # If no API key, return sample data
        if not api_key:
            sample_news = [
            {
                "title": "Bitcoin Reaches New All-Time High",
                "summary": "Bitcoin has reached a new all-time high, surpassing previous records.",
                "published": "2024-01-15T10:30:00Z",
                "url": "https://www.coindesk.com/sample-article-1"
            },
            {
                "title": "Ethereum 2.0 Update Progress",
                "summary": "Latest developments in Ethereum's transition to proof-of-stake.",
                "published": "2024-01-14T15:45:00Z",
                "url": "https://www.coindesk.com/sample-article-2"
            },
            {
                "title": "Regulatory Updates in Crypto Space",
                "summary": "New regulations affecting cryptocurrency markets worldwide.",
                "published": "2024-01-13T09:15:00Z",
                "url": "https://www.coindesk.com/sample-article-3"
            }
        ]
        
            return {
                "success": True,
                "data": {
                    "news": sample_news[:limit],
                    "count": min(limit, len(sample_news)),
                    "note": "Sample data. Provide CoinDesk API key for real-time data."
                }
            }
        
        # If API key is provided, try to get real data
        try:
            session = await self._get_session()
            # Note: CoinDesk news API requires premium access
            # This would be the real API call implementation
            return {
                "success": False,
                "error": "CoinDesk news API requires premium access. Using sample data instead."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get news: {str(e)}"
            }


class PumpNewsTool(MCPTool):
    def __init__(self):
        self.session = None
        self.pumpnews_api_url = "https://api.pumpnews.com/v1"
        # Note: PumpNews API key will be provided by user
        # Alternative APIs for fallback
        self.coingecko_api_url = "https://api.coingecko.com/api/v3"
        self.cryptocompare_api_url = "https://min-api.cryptocompare.com/data"
    
    @property
    def name(self) -> str:
        return "pumpnews"
    
    @property
    def description(self) -> str:
        return "Access PumpNews data including crypto news, pump detection, social sentiment, and market alerts"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_news",
                        "get_pump_detection",
                        "get_social_sentiment",
                        "get_market_alerts",
                        "get_trending_coins",
                        "get_volume_analysis",
                        "get_community_insights",
                        "get_portfolio_alerts"
                    ]
                },
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol (e.g., BTC, ETH, DOGE)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 10
                },
                "timeframe": {
                    "type": "string",
                    "description": "Timeframe for analysis (1h, 24h, 7d, 30d)",
                    "default": "24h"
                },
                "category": {
                    "type": "string",
                    "description": "News category (breaking, analysis, market, etc.)",
                    "default": "all"
                },
                "api_key": {
                    "type": "string",
                    "description": "PumpNews API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: PumpNews API key is required. Please provide your API key."}]
            
            if action == "get_news":
                result = await self._get_news(**arguments)
            elif action == "get_pump_detection":
                result = await self._get_pump_detection(**arguments)
            elif action == "get_social_sentiment":
                result = await self._get_social_sentiment(**arguments)
            elif action == "get_market_alerts":
                result = await self._get_market_alerts(**arguments)
            elif action == "get_trending_coins":
                result = await self._get_trending_coins(**arguments)
            elif action == "get_volume_analysis":
                result = await self._get_volume_analysis(**arguments)
            elif action == "get_community_insights":
                result = await self._get_community_insights(**arguments)
            elif action == "get_portfolio_alerts":
                result = await self._get_portfolio_alerts(**arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_news(self, **kwargs) -> dict:
        """Get latest crypto news and market updates."""
        try:
            limit = kwargs.get("limit", 10)
            category = kwargs.get("category", "all")
            symbol = kwargs.get("symbol")
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/news"
                params = {"limit": limit, "category": category}
                if symbol:
                    params["symbol"] = symbol
                
                headers = {}
                api_key = kwargs.get("api_key")
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                
                async with session.get(url, params=params, headers=headers, allow_redirects=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "data": {
                                "news": data.get("news", []),
                                "count": len(data.get("news", [])),
                                "category": category,
                                "symbol": symbol,
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    elif response.status in [301, 302, 307, 308]:
                        # API is redirecting (likely to domain parking page)
                        logger.warning(f"PumpNews API redirecting: {response.status} -> {response.headers.get('location', 'unknown')}")
                    else:
                        logger.warning(f"PumpNews API returned status: {response.status}")
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/news",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get news: {str(e)}"
            }
    
    async def _get_pump_detection(self, **kwargs) -> dict:
        """Get pump detection analysis for cryptocurrencies."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for pump detection"
                }
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/pump-detection"
                params = {"symbol": symbol, "timeframe": timeframe}
                
                headers = {}
                api_key = kwargs.get("api_key")
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                
                async with session.get(url, params=params, headers=headers, allow_redirects=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "symbol": symbol,
                            "timeframe": timeframe,
                            "data": {
                                "pump_score": data.get("pump_score"),
                                "risk_level": data.get("risk_level"),
                                "volume_spike": data.get("volume_spike"),
                                "price_change": data.get("price_change"),
                                "social_activity": data.get("social_activity"),
                                "indicators": data.get("indicators", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    elif response.status in [301, 302, 307, 308]:
                        # API is redirecting (likely to domain parking page)
                        logger.warning(f"PumpNews API redirecting: {response.status} -> {response.headers.get('location', 'unknown')}")
                    else:
                        logger.warning(f"PumpNews API returned status: {response.status}")
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/pump-detection",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get pump detection: {str(e)}"
            }
    
    async def _get_social_sentiment(self, **kwargs) -> dict:
        """Get social media sentiment for cryptocurrencies."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for social sentiment"
                }
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/social-sentiment"
                params = {"symbol": symbol, "timeframe": timeframe}
                
                headers = {}
                api_key = kwargs.get("api_key")
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "symbol": symbol,
                            "timeframe": timeframe,
                            "data": {
                                "overall_sentiment": data.get("overall_sentiment"),
                                "sentiment_score": data.get("sentiment_score"),
                                "twitter_sentiment": data.get("twitter_sentiment"),
                                "reddit_sentiment": data.get("reddit_sentiment"),
                                "telegram_sentiment": data.get("telegram_sentiment"),
                                "mentions_count": data.get("mentions_count"),
                                "trending_topics": data.get("trending_topics", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/social-sentiment",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get social sentiment: {str(e)}"
            }
    
    async def _get_market_alerts(self, **kwargs) -> dict:
        """Get market alerts and unusual trading activity."""
        try:
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/market-alerts"
                params = {"limit": limit, "timeframe": timeframe}
                
                headers = {}
                api_key = kwargs.get("api_key")
                if api_key:
                    headers["Authorization"] = f"Bearer {api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "timeframe": timeframe,
                            "data": {
                                "alerts": data.get("alerts", []),
                                "count": len(data.get("alerts", [])),
                                "alert_types": data.get("alert_types", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/market-alerts",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get market alerts: {str(e)}"
            }
    
    async def _get_trending_coins(self, **kwargs) -> dict:
        """Get currently trending cryptocurrencies."""
        try:
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/trending"
                params = {"limit": limit, "timeframe": timeframe}
                
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "timeframe": timeframe,
                            "data": {
                                "trending_coins": data.get("trending_coins", []),
                                "count": len(data.get("trending_coins", [])),
                                "trending_reasons": data.get("trending_reasons", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/trending",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get trending coins: {str(e)}"
            }
    
    async def _get_volume_analysis(self, **kwargs) -> dict:
        """Get volume analysis and unusual trading activity."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for volume analysis"
                }
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/volume-analysis"
                params = {"symbol": symbol, "timeframe": timeframe}
                
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "symbol": symbol,
                            "timeframe": timeframe,
                            "data": {
                                "current_volume": data.get("current_volume"),
                                "average_volume": data.get("average_volume"),
                                "volume_change": data.get("volume_change"),
                                "volume_spike": data.get("volume_spike"),
                                "unusual_activity": data.get("unusual_activity"),
                                "volume_patterns": data.get("volume_patterns", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/volume-analysis",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get volume analysis: {str(e)}"
            }
    
    async def _get_community_insights(self, **kwargs) -> dict:
        """Get community insights and predictions."""
        try:
            symbol = kwargs.get("symbol")
            limit = kwargs.get("limit", 10)
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/community-insights"
                params = {"limit": limit}
                if symbol:
                    params["symbol"] = symbol
                
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "symbol": symbol,
                            "data": {
                                "insights": data.get("insights", []),
                                "predictions": data.get("predictions", []),
                                "community_ratings": data.get("community_ratings", []),
                                "discussion_topics": data.get("discussion_topics", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/community-insights",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get community insights: {str(e)}"
            }
    
    async def _get_portfolio_alerts(self, **kwargs) -> dict:
        """Get portfolio alerts and watchlist monitoring."""
        try:
            symbols = kwargs.get("symbols", [])
            limit = kwargs.get("limit", 10)
            
            if not symbols:
                return {
                    "success": False,
                    "error": "symbols parameter is required for portfolio alerts"
                }
            
            session = await self._get_session()
            
            # Try PumpNews API first
            try:
                url = f"{self.pumpnews_api_url}/portfolio-alerts"
                params = {"symbols": ",".join(symbols), "limit": limit}
                
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                async with session.get(url, params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "symbols": symbols,
                            "data": {
                                "alerts": data.get("alerts", []),
                                "price_alerts": data.get("price_alerts", []),
                                "news_alerts": data.get("news_alerts", []),
                                "volume_alerts": data.get("volume_alerts", []),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
            except Exception as pump_error:
                logger.warning(f"PumpNews API failed: {pump_error}")
            
            # PumpNews API is not available - return clear error
            return {
                "success": False,
                "error": "PumpNews API is currently unavailable. The service appears to be permanently shut down.",
                "details": {
                    "api_endpoint": f"{self.pumpnews_api_url}/portfolio-alerts",
                    "status": "Service redirects to domain parking page",
                    "recommendation": "This MCP tool requires PumpNews API to be operational. Please check if the service has been restored or contact the service provider.",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get portfolio alerts: {str(e)}"
            }




class PumpFunTool(MCPTool):
    def __init__(self):
        self.session = None
        self.pumpfun_api_url = "https://api.pumpfun.com/v1"
        # Note: PumpFun API key will be provided by user
    
    @property
    def name(self) -> str:
        return "pumpfun"
    
    @property
    def description(self) -> str:
        return "Access PumpFun data including pump detection, social sentiment analysis, market intelligence, and community insights"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_pump_detection",
                        "get_social_sentiment",
                        "get_market_trends",
                        "get_volume_analysis",
                        "get_community_insights",
                        "get_alert_system",
                        "get_portfolio_monitoring",
                        "get_risk_assessment"
                    ]
                },
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol (e.g., BTC, ETH, DOGE)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 10
                },
                "timeframe": {
                    "type": "string",
                    "description": "Timeframe for analysis (1h, 24h, 7d, 30d)",
                    "default": "24h"
                },
                "platform": {
                    "type": "string",
                    "description": "Social media platform (twitter, reddit, telegram, discord, all)",
                    "default": "all"
                },
                "api_key": {
                    "type": "string",
                    "description": "PumpFun API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: PumpFun API key is required. Please provide your API key."}]
            
            if action == "get_pump_detection":
                result = await self._get_pump_detection(**arguments)
            elif action == "get_social_sentiment":
                result = await self._get_social_sentiment(**arguments)
            elif action == "get_market_trends":
                result = await self._get_market_trends(**arguments)
            elif action == "get_volume_analysis":
                result = await self._get_volume_analysis(**arguments)
            elif action == "get_community_insights":
                result = await self._get_community_insights(**arguments)
            elif action == "get_alert_system":
                result = await self._get_alert_system(**arguments)
            elif action == "get_portfolio_monitoring":
                result = await self._get_portfolio_monitoring(**arguments)
            elif action == "get_risk_assessment":
                result = await self._get_risk_assessment(**arguments)
            else:
                result = {"error": f"Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_pump_detection(self, **kwargs) -> dict:
        """Get pump detection analysis using PumpFun's proprietary algorithm."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for pump detection"
                }
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/pump-detection"
            params = {"symbol": symbol, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "data": {
                            "pump_score": data.get("pump_score"),
                            "risk_level": data.get("risk_level"),
                            "confidence": data.get("confidence"),
                            "volume_spike": data.get("volume_spike"),
                            "price_momentum": data.get("price_momentum"),
                            "social_hype": data.get("social_hype"),
                            "technical_indicators": data.get("technical_indicators", []),
                            "pump_probability": data.get("pump_probability"),
                            "dump_risk": data.get("dump_risk"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch pump detection: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get pump detection: {str(e)}"
            }
    
    async def _get_social_sentiment(self, **kwargs) -> dict:
        """Get comprehensive social media sentiment analysis."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            platform = kwargs.get("platform", "all")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for social sentiment"
                }
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/social-sentiment"
            params = {"symbol": symbol, "timeframe": timeframe, "platform": platform}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "platform": platform,
                        "data": {
                            "overall_sentiment": data.get("overall_sentiment"),
                            "sentiment_score": data.get("sentiment_score"),
                            "sentiment_change": data.get("sentiment_change"),
                            "twitter_sentiment": data.get("twitter_sentiment"),
                            "reddit_sentiment": data.get("reddit_sentiment"),
                            "telegram_sentiment": data.get("telegram_sentiment"),
                            "discord_sentiment": data.get("discord_sentiment"),
                            "mentions_count": data.get("mentions_count"),
                            "trending_topics": data.get("trending_topics", []),
                            "influencer_mentions": data.get("influencer_mentions", []),
                            "sentiment_trend": data.get("sentiment_trend"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch social sentiment: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get social sentiment: {str(e)}"
            }
    
    async def _get_market_trends(self, **kwargs) -> dict:
        """Get market trends and intelligence data."""
        try:
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/market-trends"
            params = {"limit": limit, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "timeframe": timeframe,
                        "data": {
                            "trending_coins": data.get("trending_coins", []),
                            "market_sentiment": data.get("market_sentiment"),
                            "trending_reasons": data.get("trending_reasons", []),
                            "market_momentum": data.get("market_momentum"),
                            "sector_performance": data.get("sector_performance", []),
                            "emerging_trends": data.get("emerging_trends", []),
                            "market_volatility": data.get("market_volatility"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch market trends: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get market trends: {str(e)}"
            }
    
    async def _get_volume_analysis(self, **kwargs) -> dict:
        """Get detailed volume analysis and unusual activity detection."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for volume analysis"
                }
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/volume-analysis"
            params = {"symbol": symbol, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "data": {
                            "current_volume": data.get("current_volume"),
                            "average_volume": data.get("average_volume"),
                            "volume_change": data.get("volume_change"),
                            "volume_spike": data.get("volume_spike"),
                            "unusual_activity": data.get("unusual_activity"),
                            "volume_patterns": data.get("volume_patterns", []),
                            "whale_activity": data.get("whale_activity"),
                            "volume_distribution": data.get("volume_distribution"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch volume analysis: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get volume analysis: {str(e)}"
            }
    
    async def _get_community_insights(self, **kwargs) -> dict:
        """Get community-driven insights and predictions."""
        try:
            symbol = kwargs.get("symbol")
            limit = kwargs.get("limit", 10)
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/community-insights"
            params = {"limit": limit}
            if symbol:
                params["symbol"] = symbol
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "symbol": symbol,
                        "data": {
                            "community_ratings": data.get("community_ratings", []),
                            "user_predictions": data.get("user_predictions", []),
                            "discussion_topics": data.get("discussion_topics", []),
                            "community_sentiment": data.get("community_sentiment"),
                            "expert_opinions": data.get("expert_opinions", []),
                            "crowd_wisdom": data.get("crowd_wisdom"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch community insights: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get community insights: {str(e)}"
            }
    
    async def _get_alert_system(self, **kwargs) -> dict:
        """Get real-time market alerts and notifications."""
        try:
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/alerts"
            params = {"limit": limit, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "timeframe": timeframe,
                        "data": {
                            "active_alerts": data.get("active_alerts", []),
                            "alert_types": data.get("alert_types", []),
                            "priority_alerts": data.get("priority_alerts", []),
                            "alert_statistics": data.get("alert_statistics"),
                            "custom_alerts": data.get("custom_alerts", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch alerts: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get alerts: {str(e)}"
            }
    
    async def _get_portfolio_monitoring(self, **kwargs) -> dict:
        """Get portfolio monitoring and watchlist data."""
        try:
            symbols = kwargs.get("symbols", [])
            limit = kwargs.get("limit", 10)
            
            if not symbols:
                return {
                    "success": False,
                    "error": "symbols parameter is required for portfolio monitoring"
                }
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/portfolio-monitoring"
            params = {"symbols": ",".join(symbols), "limit": limit}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "symbols": symbols,
                        "data": {
                            "portfolio_alerts": data.get("portfolio_alerts", []),
                            "price_alerts": data.get("price_alerts", []),
                            "volume_alerts": data.get("volume_alerts", []),
                            "news_alerts": data.get("news_alerts", []),
                            "risk_alerts": data.get("risk_alerts", []),
                            "portfolio_summary": data.get("portfolio_summary"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch portfolio monitoring: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get portfolio monitoring: {str(e)}"
            }
    
    async def _get_risk_assessment(self, **kwargs) -> dict:
        """Get comprehensive risk assessment and analysis."""
        try:
            symbol = kwargs.get("symbol")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not symbol:
                return {
                    "success": False,
                    "error": "symbol parameter is required for risk assessment"
                }
            
            session = await self._get_session()
            
            url = f"{self.pumpfun_api_url}/risk-assessment"
            params = {"symbol": symbol, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "data": {
                            "overall_risk": data.get("overall_risk"),
                            "risk_score": data.get("risk_score"),
                            "volatility_risk": data.get("volatility_risk"),
                            "liquidity_risk": data.get("liquidity_risk"),
                            "market_risk": data.get("market_risk"),
                            "social_risk": data.get("social_risk"),
                            "technical_risk": data.get("technical_risk"),
                            "risk_factors": data.get("risk_factors", []),
                            "risk_recommendations": data.get("risk_recommendations", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch risk assessment: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get risk assessment: {str(e)}"
            }

class GMGNTool(MCPTool):
    def __init__(self):
        self.session = None
        self.gmgn_api_url = "https://api.gmgn.com/v1"
        # Note: GMGN API key will be provided by user
    
    @property
    def name(self) -> str:
        return "gmgn"
    
    @property
    def description(self) -> str:
        return "Access GMGN (Global Market Gaming Network) data including gaming token analysis, P2E analytics, gaming NFT markets, and gaming industry insights"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_gaming_token_analysis",
                        "get_p2e_analytics",
                        "get_gaming_nft_markets",
                        "get_gaming_community_insights",
                        "get_gaming_project_ratings",
                        "get_gaming_industry_trends",
                        "get_gaming_token_discovery",
                        "get_gaming_investment_analysis"
                    ]
                },
                "token": {
                    "type": "string",
                    "description": "Gaming token symbol or address (e.g., AXS, SAND, MANA)"
                },
                "game": {
                    "type": "string",
                    "description": "Game name or identifier (e.g., Axie Infinity, The Sandbox)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 10
                },
                "timeframe": {
                    "type": "string",
                    "description": "Timeframe for analysis (1h, 24h, 7d, 30d)",
                    "default": "24h"
                },
                "category": {
                    "type": "string",
                    "description": "Gaming category (p2e, nft, metaverse, strategy, etc.)",
                    "default": "all"
                },
                "api_key": {
                    "type": "string",
                    "description": "GMGN API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: GMGN API key is required. Please provide your API key."}]
            
            if action == "get_gaming_token_analysis":
                result = await self._get_gaming_token_analysis(**arguments)
            elif action == "get_p2e_analytics":
                result = await self._get_p2e_analytics(**arguments)
            elif action == "get_gaming_nft_markets":
                result = await self._get_gaming_nft_markets(**arguments)
            elif action == "get_gaming_community_insights":
                result = await self._get_gaming_community_insights(**arguments)
            elif action == "get_gaming_project_ratings":
                result = await self._get_gaming_project_ratings(**arguments)
            elif action == "get_gaming_industry_trends":
                result = await self._get_gaming_industry_trends(**arguments)
            elif action == "get_gaming_token_discovery":
                result = await self._get_gaming_token_discovery(**arguments)
            elif action == "get_gaming_investment_analysis":
                result = await self._get_gaming_investment_analysis(**arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_gaming_token_analysis(self, **kwargs) -> dict:
        """Get comprehensive analysis of gaming tokens."""
        try:
            token = kwargs.get("token")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not token:
                return {
                    "success": False,
                    "error": "token parameter is required for gaming token analysis"
                }
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-token-analysis"
            params = {"token": token, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "token": token,
                        "timeframe": timeframe,
                        "data": {
                            "token_info": data.get("token_info", {}),
                            "price_analysis": data.get("price_analysis", {}),
                            "volume_analysis": data.get("volume_analysis", {}),
                            "market_cap": data.get("market_cap"),
                            "circulating_supply": data.get("circulating_supply"),
                            "total_supply": data.get("total_supply"),
                            "price_change_24h": data.get("price_change_24h"),
                            "volume_24h": data.get("volume_24h"),
                            "gaming_metrics": data.get("gaming_metrics", {}),
                            "utility_score": data.get("utility_score"),
                            "adoption_score": data.get("adoption_score"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch gaming token analysis: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get gaming token analysis: {str(e)}"
            }
    
    async def _get_p2e_analytics(self, **kwargs) -> dict:
        """Get Play-to-Earn game analytics and performance."""
        try:
            game = kwargs.get("game")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not game:
                return {
                    "success": False,
                    "error": "game parameter is required for P2E analytics"
                }
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/p2e-analytics"
            params = {"game": game, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "game": game,
                        "timeframe": timeframe,
                        "data": {
                            "game_info": data.get("game_info", {}),
                            "player_stats": data.get("player_stats", {}),
                            "tokenomics": data.get("tokenomics", {}),
                            "revenue_metrics": data.get("revenue_metrics", {}),
                            "earning_potential": data.get("earning_potential"),
                            "player_count": data.get("player_count"),
                            "active_users": data.get("active_users"),
                            "daily_revenue": data.get("daily_revenue"),
                            "token_price": data.get("token_price"),
                            "market_cap": data.get("market_cap"),
                            "p2e_score": data.get("p2e_score"),
                            "sustainability_score": data.get("sustainability_score"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch P2E analytics: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get P2E analytics: {str(e)}"
            }
    
    async def _get_gaming_nft_markets(self, **kwargs) -> dict:
        """Get gaming NFT marketplace data and trends."""
        try:
            limit = kwargs.get("limit", 10)
            category = kwargs.get("category", "all")
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-nft-markets"
            params = {"limit": limit, "category": category, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "category": category,
                        "timeframe": timeframe,
                        "data": {
                            "nft_collections": data.get("nft_collections", []),
                            "trading_volume": data.get("trading_volume"),
                            "floor_prices": data.get("floor_prices", {}),
                            "sales_count": data.get("sales_count"),
                            "unique_buyers": data.get("unique_buyers"),
                            "unique_sellers": data.get("unique_sellers"),
                            "trending_nfts": data.get("trending_nfts", []),
                            "market_metrics": data.get("market_metrics", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch gaming NFT markets: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get gaming NFT markets: {str(e)}"
            }
    
    async def _get_gaming_community_insights(self, **kwargs) -> dict:
        """Get gaming community insights and sentiment."""
        try:
            token = kwargs.get("token")
            game = kwargs.get("game")
            limit = kwargs.get("limit", 10)
            
            if not token and not game:
                return {
                    "success": False,
                    "error": "Either token or game parameter is required for community insights"
                }
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-community-insights"
            params = {"limit": limit}
            if token:
                params["token"] = token
            if game:
                params["game"] = game
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "token": token,
                        "game": game,
                        "data": {
                            "community_sentiment": data.get("community_sentiment"),
                            "sentiment_score": data.get("sentiment_score"),
                            "community_size": data.get("community_size"),
                            "active_members": data.get("active_members"),
                            "engagement_rate": data.get("engagement_rate"),
                            "discussion_topics": data.get("discussion_topics", []),
                            "community_ratings": data.get("community_ratings", []),
                            "user_feedback": data.get("user_feedback", []),
                            "social_metrics": data.get("social_metrics", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch community insights: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get community insights: {str(e)}"
            }
    
    async def _get_gaming_project_ratings(self, **kwargs) -> dict:
        """Get expert ratings and reviews of gaming projects."""
        try:
            token = kwargs.get("token")
            game = kwargs.get("game")
            limit = kwargs.get("limit", 10)
            
            if not token and not game:
                return {
                    "success": False,
                    "error": "Either token or game parameter is required for project ratings"
                }
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-project-ratings"
            params = {"limit": limit}
            if token:
                params["token"] = token
            if game:
                params["game"] = game
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "token": token,
                        "game": game,
                        "data": {
                            "overall_rating": data.get("overall_rating"),
                            "expert_reviews": data.get("expert_reviews", []),
                            "rating_breakdown": data.get("rating_breakdown", {}),
                            "pros_cons": data.get("pros_cons", {}),
                            "recommendation": data.get("recommendation"),
                            "risk_assessment": data.get("risk_assessment"),
                            "long_term_potential": data.get("long_term_potential"),
                            "market_position": data.get("market_position"),
                            "competitive_analysis": data.get("competitive_analysis", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch project ratings: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get project ratings: {str(e)}"
            }
    
    async def _get_gaming_industry_trends(self, **kwargs) -> dict:
        """Get gaming industry trends and market movements."""
        try:
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            category = kwargs.get("category", "all")
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-industry-trends"
            params = {"limit": limit, "timeframe": timeframe, "category": category}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "timeframe": timeframe,
                        "category": category,
                        "data": {
                            "trending_games": data.get("trending_games", []),
                            "trending_tokens": data.get("trending_tokens", []),
                            "market_trends": data.get("market_trends", {}),
                            "industry_metrics": data.get("industry_metrics", {}),
                            "sector_performance": data.get("sector_performance", []),
                            "emerging_trends": data.get("emerging_trends", []),
                            "market_sentiment": data.get("market_sentiment"),
                            "investment_flows": data.get("investment_flows", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch industry trends: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get industry trends: {str(e)}"
            }
    
    async def _get_gaming_token_discovery(self, **kwargs) -> dict:
        """Discover new and trending gaming tokens."""
        try:
            limit = kwargs.get("limit", 10)
            category = kwargs.get("category", "all")
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-token-discovery"
            params = {"limit": limit, "category": category, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "category": category,
                        "timeframe": timeframe,
                        "data": {
                            "new_tokens": data.get("new_tokens", []),
                            "trending_tokens": data.get("trending_tokens", []),
                            "upcoming_releases": data.get("upcoming_releases", []),
                            "discovery_metrics": data.get("discovery_metrics", {}),
                            "token_categories": data.get("token_categories", []),
                            "market_opportunities": data.get("market_opportunities", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch token discovery: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get token discovery: {str(e)}"
            }
    
    async def _get_gaming_investment_analysis(self, **kwargs) -> dict:
        """Get gaming investment analysis and recommendations."""
        try:
            token = kwargs.get("token")
            game = kwargs.get("game")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not token and not game:
                return {
                    "success": False,
                    "error": "Either token or game parameter is required for investment analysis"
                }
            
            session = await self._get_session()
            
            url = f"{self.gmgn_api_url}/gaming-investment-analysis"
            params = {"timeframe": timeframe}
            if token:
                params["token"] = token
            if game:
                params["game"] = game
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "token": token,
                        "game": game,
                        "timeframe": timeframe,
                        "data": {
                            "investment_score": data.get("investment_score"),
                            "risk_level": data.get("risk_level"),
                            "potential_return": data.get("potential_return"),
                            "investment_recommendation": data.get("investment_recommendation"),
                            "market_analysis": data.get("market_analysis", {}),
                            "competitive_position": data.get("competitive_position"),
                            "growth_potential": data.get("growth_potential"),
                            "investment_risks": data.get("investment_risks", []),
                            "investment_opportunities": data.get("investment_opportunities", []),
                            "portfolio_fit": data.get("portfolio_fit"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch investment analysis: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get investment analysis: {str(e)}"
            }


class MerklTool(MCPTool):
    def __init__(self):
        self.session = None
        self.merkl_api_url = "https://api.merkl.xyz/v1"
        # Note: Merkl API key will be provided by user
    
    @property
    def name(self) -> str:
        return "merkl"
    
    @property
    def description(self) -> str:
        return "Access Merkl protocol data including concentrated liquidity positions, yield farming opportunities, rewards distribution, and protocol analytics"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "get_concentrated_positions",
                        "get_yield_farming_opportunities",
                        "get_rewards_distribution",
                        "get_protocol_analytics",
                        "get_position_performance",
                        "get_liquidity_pools",
                        "get_user_positions",
                        "get_rewards_calculation"
                    ]
                },
                "chain": {
                    "type": "string",
                    "description": "Blockchain network (e.g., ethereum, polygon, arbitrum, optimism)",
                    "default": "ethereum"
                },
                "token": {
                    "type": "string",
                    "description": "Token address or symbol (e.g., USDC, WETH, 0x...)"
                },
                "user_address": {
                    "type": "string",
                    "description": "User wallet address for position queries"
                },
                "pool_address": {
                    "type": "string",
                    "description": "Liquidity pool address"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 10
                },
                "timeframe": {
                    "type": "string",
                    "description": "Timeframe for analysis (1h, 24h, 7d, 30d)",
                    "default": "24h"
                },
                "min_apy": {
                    "type": "number",
                    "description": "Minimum APY filter for yield opportunities",
                    "default": 0
                },
                "api_key": {
                    "type": "string",
                    "description": "Merkl API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Merkl API key is required. Please provide your API key."}]
            
            if action == "get_concentrated_positions":
                result = await self._get_concentrated_positions(**arguments)
            elif action == "get_yield_farming_opportunities":
                result = await self._get_yield_farming_opportunities(**arguments)
            elif action == "get_rewards_distribution":
                result = await self._get_rewards_distribution(**arguments)
            elif action == "get_protocol_analytics":
                result = await self._get_protocol_analytics(**arguments)
            elif action == "get_position_performance":
                result = await self._get_position_performance(**arguments)
            elif action == "get_liquidity_pools":
                result = await self._get_liquidity_pools(**arguments)
            elif action == "get_user_positions":
                result = await self._get_user_positions(**arguments)
            elif action == "get_rewards_calculation":
                result = await self._get_rewards_calculation(**arguments)
            else:
                result = {"error": f"Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_concentrated_positions(self, **kwargs) -> dict:
        """Get concentrated liquidity positions data."""
        try:
            chain = kwargs.get("chain", "ethereum")
            token = kwargs.get("token")
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/concentrated-positions"
            params = {"chain": chain, "limit": limit, "timeframe": timeframe}
            if token:
                params["token"] = token
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "timeframe": timeframe,
                        "data": {
                            "positions": data.get("positions", []),
                            "total_tvl": data.get("total_tvl"),
                            "active_positions": data.get("active_positions"),
                            "average_apy": data.get("average_apy"),
                            "position_distribution": data.get("position_distribution", {}),
                            "top_tokens": data.get("top_tokens", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch concentrated positions: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get concentrated positions: {str(e)}"
            }
    
    async def _get_yield_farming_opportunities(self, **kwargs) -> dict:
        """Get yield farming opportunities and APY data."""
        try:
            chain = kwargs.get("chain", "ethereum")
            min_apy = kwargs.get("min_apy", 0)
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/yield-opportunities"
            params = {"chain": chain, "min_apy": min_apy, "limit": limit, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "min_apy": min_apy,
                        "timeframe": timeframe,
                        "data": {
                            "opportunities": data.get("opportunities", []),
                            "highest_apy": data.get("highest_apy"),
                            "average_apy": data.get("average_apy"),
                            "total_opportunities": data.get("total_opportunities"),
                            "risk_levels": data.get("risk_levels", {}),
                            "token_distribution": data.get("token_distribution", {}),
                            "protocol_distribution": data.get("protocol_distribution", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch yield opportunities: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get yield opportunities: {str(e)}"
            }
    
    async def _get_rewards_distribution(self, **kwargs) -> dict:
        """Get rewards distribution and token incentives data."""
        try:
            chain = kwargs.get("chain", "ethereum")
            token = kwargs.get("token")
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/rewards-distribution"
            params = {"chain": chain, "limit": limit, "timeframe": timeframe}
            if token:
                params["token"] = token
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "timeframe": timeframe,
                        "data": {
                            "rewards": data.get("rewards", []),
                            "total_rewards_distributed": data.get("total_rewards_distributed"),
                            "active_reward_programs": data.get("active_reward_programs"),
                            "reward_tokens": data.get("reward_tokens", []),
                            "distribution_by_token": data.get("distribution_by_token", {}),
                            "distribution_by_pool": data.get("distribution_by_pool", {}),
                            "user_rewards": data.get("user_rewards", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch rewards distribution: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get rewards distribution: {str(e)}"
            }
    
    async def _get_protocol_analytics(self, **kwargs) -> dict:
        """Get Merkl protocol analytics and metrics."""
        try:
            chain = kwargs.get("chain", "ethereum")
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/protocol-analytics"
            params = {"chain": chain, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "timeframe": timeframe,
                        "data": {
                            "total_tvl": data.get("total_tvl"),
                            "total_volume": data.get("total_volume"),
                            "active_users": data.get("active_users"),
                            "total_positions": data.get("total_positions"),
                            "average_apy": data.get("average_apy"),
                            "rewards_distributed": data.get("rewards_distributed"),
                            "protocol_fees": data.get("protocol_fees"),
                            "growth_metrics": data.get("growth_metrics", {}),
                            "market_share": data.get("market_share"),
                            "risk_metrics": data.get("risk_metrics", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch protocol analytics: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get protocol analytics: {str(e)}"
            }
    
    async def _get_position_performance(self, **kwargs) -> dict:
        """Get performance metrics for specific positions."""
        try:
            chain = kwargs.get("chain", "ethereum")
            pool_address = kwargs.get("pool_address")
            user_address = kwargs.get("user_address")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not pool_address and not user_address:
                return {
                    "success": False,
                    "error": "Either pool_address or user_address parameter is required"
                }
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/position-performance"
            params = {"chain": chain, "timeframe": timeframe}
            if pool_address:
                params["pool_address"] = pool_address
            if user_address:
                params["user_address"] = user_address
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "pool_address": pool_address,
                        "user_address": user_address,
                        "timeframe": timeframe,
                        "data": {
                            "performance_metrics": data.get("performance_metrics", {}),
                            "apy_history": data.get("apy_history", []),
                            "rewards_earned": data.get("rewards_earned"),
                            "impermanent_loss": data.get("impermanent_loss"),
                            "fees_collected": data.get("fees_collected"),
                            "position_value": data.get("position_value"),
                            "risk_metrics": data.get("risk_metrics", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch position performance: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get position performance: {str(e)}"
            }
    
    async def _get_liquidity_pools(self, **kwargs) -> dict:
        """Get available liquidity pools and their data."""
        try:
            chain = kwargs.get("chain", "ethereum")
            token = kwargs.get("token")
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/liquidity-pools"
            params = {"chain": chain, "limit": limit, "timeframe": timeframe}
            if token:
                params["token"] = token
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "timeframe": timeframe,
                        "data": {
                            "pools": data.get("pools", []),
                            "total_pools": data.get("total_pools"),
                            "total_tvl": data.get("total_tvl"),
                            "average_apy": data.get("average_apy"),
                            "pool_distribution": data.get("pool_distribution", {}),
                            "top_pools": data.get("top_pools", []),
                            "new_pools": data.get("new_pools", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch liquidity pools: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get liquidity pools: {str(e)}"
            }
    
    async def _get_user_positions(self, **kwargs) -> dict:
        """Get user's liquidity positions and performance."""
        try:
            chain = kwargs.get("chain", "ethereum")
            user_address = kwargs.get("user_address")
            limit = kwargs.get("limit", 10)
            timeframe = kwargs.get("timeframe", "24h")
            
            if not user_address:
                return {
                    "success": False,
                    "error": "user_address parameter is required"
                }
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/user-positions"
            params = {"chain": chain, "user_address": user_address, "limit": limit, "timeframe": timeframe}
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "user_address": user_address,
                        "timeframe": timeframe,
                        "data": {
                            "positions": data.get("positions", []),
                            "total_value": data.get("total_value"),
                            "total_rewards": data.get("total_rewards"),
                            "average_apy": data.get("average_apy"),
                            "active_positions": data.get("active_positions"),
                            "position_history": data.get("position_history", []),
                            "performance_summary": data.get("performance_summary", {}),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch user positions: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get user positions: {str(e)}"
            }
    
    async def _get_rewards_calculation(self, **kwargs) -> dict:
        """Calculate potential rewards for a position."""
        try:
            chain = kwargs.get("chain", "ethereum")
            pool_address = kwargs.get("pool_address")
            token = kwargs.get("token")
            amount = kwargs.get("amount")
            timeframe = kwargs.get("timeframe", "24h")
            
            if not pool_address and not token:
                return {
                    "success": False,
                    "error": "Either pool_address or token parameter is required"
                }
            
            session = await self._get_session()
            
            url = f"{self.merkl_api_url}/rewards-calculation"
            params = {"chain": chain, "timeframe": timeframe}
            if pool_address:
                params["pool_address"] = pool_address
            if token:
                params["token"] = token
            if amount:
                params["amount"] = amount
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "chain": chain,
                        "pool_address": pool_address,
                        "token": token,
                        "amount": amount,
                        "timeframe": timeframe,
                        "data": {
                            "estimated_rewards": data.get("estimated_rewards"),
                            "apy": data.get("apy"),
                            "reward_tokens": data.get("reward_tokens", []),
                            "reward_distribution": data.get("reward_distribution", {}),
                            "time_to_break_even": data.get("time_to_break_even"),
                            "risk_assessment": data.get("risk_assessment", {}),
                            "optimization_suggestions": data.get("optimization_suggestions", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to calculate rewards: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to calculate rewards: {str(e)}"
            }

