"""
Market Analysis Tools
Contains advanced market analysis and technical indicators tools
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

class MarketAnalysisTool(MCPTool):
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_duration = 300  # 5 minutes cache
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.fear_greed_url = "https://api.alternative.me/fng/"
    
    @property
    def name(self) -> str:
        return "market_analysis"
    
    @property
    def description(self) -> str:
        return "Advanced market analysis including technical indicators, trend analysis, and market sentiment."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "string",
                    "description": "CoinGecko coin ID for analysis",
                    "default": "bitcoin"
                },
                "analysis_type": {
                    "type": "string",
                    "description": "Type of analysis to perform",
                    "enum": ["technical_indicators", "trend_analysis", "market_sentiment", "volatility"],
                    "default": "technical_indicators"
                },
                "timeframe": {
                    "type": "string",
                    "description": "Timeframe for analysis",
                    "enum": ["1d", "7d", "30d", "1y"],
                    "default": "7d"
                },
                "include_charts": {
                    "type": "boolean",
                    "description": "Include chart data points",
                    "default": False
                }
            },
            "required": ["coin_id"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            coin_id = arguments.get("coin_id", "bitcoin")
            analysis_type = arguments.get("analysis_type", "technical_indicators")
            timeframe = arguments.get("timeframe", "7d")
            include_charts = arguments.get("include_charts", False)
            
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            if analysis_type == "technical_indicators":
                return await self._get_technical_indicators(coin_id, timeframe, include_charts)
            elif analysis_type == "trend_analysis":
                return await self._get_trend_analysis(coin_id, timeframe)
            elif analysis_type == "market_sentiment":
                return await self._get_market_sentiment(coin_id)
            elif analysis_type == "volatility":
                return await self._get_volatility_analysis(coin_id, timeframe)
            else:
                return [{"error": f"Unsupported analysis type: {analysis_type}"}]
                
        except Exception as e:
            logger.error(f"Market analysis tool error: {e}")
            return [{"error": f"Market analysis failed: {str(e)}"}]
    
    async def _get_technical_indicators(self, coin_id: str, timeframe: str, include_charts: bool) -> List[Dict[str, Any]]:
        """Calculate technical indicators using real market data"""
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            # Get historical price data
            days = self._timeframe_to_days(timeframe)
            url = f"{self.coingecko_base_url}/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    return [{"error": f"Failed to fetch price data: {response.status}"}]
                
                data = await response.json()
                prices = data.get("prices", [])
                volumes = data.get("total_volumes", [])
                
                if not prices:
                    return [{"error": "No price data available"}]
                
                # Calculate technical indicators
                price_values = [price[1] for price in prices]
                volume_values = [volume[1] for volume in volumes]
                
                # Calculate RSI
                rsi = self._calculate_rsi(price_values, 14)
                
                # Calculate Moving Averages
                sma_20 = self._calculate_sma(price_values, 20)
                sma_50 = self._calculate_sma(price_values, 50)
                ema_12 = self._calculate_ema(price_values, 12)
                ema_26 = self._calculate_ema(price_values, 26)
                
                # Calculate MACD
                macd_line = ema_12 - ema_26
                signal_line = self._calculate_ema([macd_line], 9)
                histogram = macd_line - signal_line
                
                # Calculate Bollinger Bands
                bb_period = 20
                bb_std = 2
                sma_bb = self._calculate_sma(price_values, bb_period)
                std_dev = self._calculate_std_deviation(price_values, bb_period)
                bb_upper = sma_bb + (bb_std * std_dev)
                bb_lower = sma_bb - (bb_std * std_dev)
                
                # Calculate Support and Resistance
                support, resistance = self._calculate_support_resistance(price_values)
                
                indicators = {
                    "coin_id": coin_id,
                    "timeframe": timeframe,
                    "current_price": price_values[-1] if price_values else 0,
                    "rsi": round(rsi, 2),
                    "macd": {
                        "macd_line": round(macd_line, 2),
                        "signal_line": round(signal_line, 2),
                        "histogram": round(histogram, 2)
                    },
                    "bollinger_bands": {
                        "upper": round(bb_upper, 2),
                        "middle": round(sma_bb, 2),
                        "lower": round(bb_lower, 2)
                    },
                    "moving_averages": {
                        "sma_20": round(sma_20, 2),
                        "sma_50": round(sma_50, 2),
                        "ema_12": round(ema_12, 2),
                        "ema_26": round(ema_26, 2)
                    },
                    "support_resistance": {
                        "support": round(support, 2),
                        "resistance": round(resistance, 2)
                    },
                    "volume_analysis": {
                        "current_volume": volume_values[-1] if volume_values else 0,
                        "avg_volume": sum(volume_values) / len(volume_values) if volume_values else 0
                    }
                }
                
                if include_charts:
                    indicators["price_data"] = self._format_price_data(prices, volumes)
                
                return [{"technical_indicators": indicators}]
                
        except Exception as e:
            logger.error(f"Technical indicators calculation error: {e}")
            return [{"error": f"Technical indicators calculation failed: {str(e)}"}]
    
    async def _get_trend_analysis(self, coin_id: str, timeframe: str) -> List[Dict[str, Any]]:
        """Analyze market trends using real price data"""
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            # Get historical price data
            days = self._timeframe_to_days(timeframe)
            url = f"{self.coingecko_base_url}/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    return [{"error": f"Failed to fetch price data: {response.status}"}]
                
                data = await response.json()
                prices = data.get("prices", [])
                volumes = data.get("total_volumes", [])
                
                if not prices:
                    return [{"error": "No price data available"}]
                
                price_values = [price[1] for price in prices]
                volume_values = [volume[1] for volume in volumes]
                
                # Calculate trend direction and strength
                trend_direction, trend_strength = self._analyze_trend_direction(price_values)
                
                # Calculate momentum
                price_momentum, volume_momentum, momentum_score = self._calculate_momentum(price_values, volume_values)
                
                # Calculate key levels
                breakout_level, breakdown_level = self._calculate_key_levels(price_values)
                
                # Calculate trend duration
                trend_duration = self._calculate_trend_duration(price_values, trend_direction)
                
                trend_data = {
                    "coin_id": coin_id,
                    "timeframe": timeframe,
                    "current_price": price_values[-1] if price_values else 0,
                    "price_change_24h": self._calculate_price_change(price_values, 1),
                    "price_change_7d": self._calculate_price_change(price_values, 7),
                    "trend_direction": trend_direction,
                    "trend_strength": trend_strength,
                    "trend_duration": trend_duration,
                    "key_levels": {
                        "breakout_level": round(breakout_level, 2),
                        "breakdown_level": round(breakdown_level, 2)
                    },
                    "momentum": {
                        "price_momentum": price_momentum,
                        "volume_momentum": volume_momentum,
                        "momentum_score": round(momentum_score, 2)
                    },
                    "trend_indicators": {
                        "higher_highs": self._count_higher_highs(price_values),
                        "higher_lows": self._count_higher_lows(price_values),
                        "trend_consistency": self._calculate_trend_consistency(price_values)
                    }
                }
                
                return [{"trend_analysis": trend_data}]
                
        except Exception as e:
            logger.error(f"Trend analysis error: {e}")
            return [{"error": f"Trend analysis failed: {str(e)}"}]
    
    async def _get_market_sentiment(self, coin_id: str) -> List[Dict[str, Any]]:
        """Analyze market sentiment using real data"""
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            # Get Fear & Greed Index
            fear_greed_data = await self._get_fear_greed_index()
            
            # Get coin-specific sentiment data
            coin_data = await self._get_coin_sentiment_data(coin_id)
            
            # Calculate overall sentiment score
            sentiment_score = self._calculate_sentiment_score(fear_greed_data, coin_data)
            
            sentiment_data = {
                "coin_id": coin_id,
                "fear_greed_index": fear_greed_data.get("value", 50),
                "fear_greed_classification": fear_greed_data.get("classification", "Neutral"),
                "sentiment_score": round(sentiment_score, 2),
                "market_sentiment": self._classify_sentiment(sentiment_score),
                "social_metrics": {
                    "reddit_score": coin_data.get("reddit_score", 0),
                    "reddit_comments_24h": coin_data.get("reddit_comments_24h", 0),
                    "reddit_posts_24h": coin_data.get("reddit_posts_24h", 0),
                    "twitter_followers": coin_data.get("twitter_followers", 0),
                    "telegram_channel_user_count": coin_data.get("telegram_channel_user_count", 0)
                },
                "community_data": {
                    "community_score": coin_data.get("community_score", 0),
                    "developer_score": coin_data.get("developer_score", 0),
                    "liquidity_score": coin_data.get("liquidity_score", 0),
                    "public_interest_score": coin_data.get("public_interest_score", 0)
                },
                "market_indicators": {
                    "market_cap_rank": coin_data.get("market_cap_rank", 0),
                    "coingecko_score": coin_data.get("coingecko_score", 0),
                    "developer_score": coin_data.get("developer_score", 0),
                    "community_score": coin_data.get("community_score", 0),
                    "liquidity_score": coin_data.get("liquidity_score", 0),
                    "public_interest_score": coin_data.get("public_interest_score", 0)
                }
            }
            
            return [{"market_sentiment": sentiment_data}]
            
        except Exception as e:
            logger.error(f"Market sentiment analysis error: {e}")
            return [{"error": f"Market sentiment analysis failed: {str(e)}"}]
    
    async def _get_volatility_analysis(self, coin_id: str, timeframe: str) -> List[Dict[str, Any]]:
        """Analyze price volatility using real market data"""
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            
            # Get historical price data
            days = self._timeframe_to_days(timeframe)
            url = f"{self.coingecko_base_url}/coins/{coin_id}/market_chart"
            params = {
                "vs_currency": "usd",
                "days": days,
                "interval": "daily"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    return [{"error": f"Failed to fetch price data: {response.status}"}]
                
                data = await response.json()
                prices = data.get("prices", [])
                
                if not prices:
                    return [{"error": "No price data available"}]
                
                price_values = [price[1] for price in prices]
                
                # Calculate volatility metrics
                current_volatility = self._calculate_volatility(price_values, 30)  # 30-day volatility
                historical_volatility = self._calculate_volatility(price_values, len(price_values))
                
                # Calculate volatility trend
                volatility_trend = self._calculate_volatility_trend(price_values)
                
                # Calculate risk metrics
                var_95 = self._calculate_value_at_risk(price_values, 0.95)
                max_drawdown = self._calculate_max_drawdown(price_values)
                
                # Determine volatility rank and risk level
                volatility_rank = self._classify_volatility(current_volatility)
                risk_level = self._classify_risk_level(current_volatility, max_drawdown)
                
                volatility_data = {
                    "coin_id": coin_id,
                    "timeframe": timeframe,
                    "current_price": price_values[-1] if price_values else 0,
                    "current_volatility": round(current_volatility * 100, 2),  # Convert to percentage
                    "historical_volatility": round(historical_volatility * 100, 2),
                    "volatility_rank": volatility_rank,
                    "volatility_trend": volatility_trend,
                    "risk_level": risk_level,
                    "risk_metrics": {
                        "value_at_risk_95": round(var_95, 2),
                        "max_drawdown": round(max_drawdown * 100, 2),
                        "sharpe_ratio": round(self._calculate_sharpe_ratio(price_values), 2),
                        "sortino_ratio": round(self._calculate_sortino_ratio(price_values), 2)
                    },
                    "volatility_breakdown": {
                        "daily_volatility": round(self._calculate_volatility(price_values[-7:], 7) * 100, 2),
                        "weekly_volatility": round(self._calculate_volatility(price_values[-30:], 30) * 100, 2),
                        "monthly_volatility": round(self._calculate_volatility(price_values[-90:], 90) * 100, 2)
                    }
                }
                
                return [{"volatility_analysis": volatility_data}]
                
        except Exception as e:
            logger.error(f"Volatility analysis error: {e}")
            return [{"error": f"Volatility analysis failed: {str(e)}"}]

    # Helper methods for market analysis
    def _timeframe_to_days(self, timeframe: str) -> int:
        """Convert timeframe string to number of days"""
        timeframe_map = {
            "1d": 1,
            "7d": 7,
            "30d": 30,
            "1y": 365
        }
        return timeframe_map.get(timeframe, 7)

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return 50.0  # Neutral RSI if insufficient data
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        return sum(prices[-period:]) / period

    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = prices[0]
        
        for price in prices[1:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema

    def _calculate_std_deviation(self, prices: List[float], period: int) -> float:
        """Calculate Standard Deviation"""
        if len(prices) < period:
            return 0
        
        sma = self._calculate_sma(prices, period)
        squared_diff_sum = sum((price - sma) ** 2 for price in prices[-period:])
        variance = squared_diff_sum / period
        return (variance ** 0.5)

    def _calculate_support_resistance(self, prices: List[float]) -> tuple:
        """Calculate support and resistance levels"""
        if len(prices) < 20:
            return prices[-1] * 0.95, prices[-1] * 1.05
        
        # Simple support/resistance calculation
        recent_prices = prices[-20:]
        support = min(recent_prices) * 0.98
        resistance = max(recent_prices) * 1.02
        
        return support, resistance

    def _format_price_data(self, prices: List[List], volumes: List[List]) -> List[Dict[str, Any]]:
        """Format price and volume data for charts"""
        formatted_data = []
        for i, (price_point, volume_point) in enumerate(zip(prices, volumes)):
            formatted_data.append({
                "timestamp": datetime.fromtimestamp(price_point[0] / 1000).isoformat(),
                "price": price_point[1],
                "volume": volume_point[1]
            })
        return formatted_data

    async def _get_fear_greed_index(self) -> Dict[str, Any]:
        """Get Fear & Greed Index data"""
        try:
            async with self.session.get(self.fear_greed_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("data"):
                        return {
                            "value": int(data["data"][0]["value"]),
                            "classification": data["data"][0]["value_classification"]
                        }
        except Exception as e:
            logger.error(f"Failed to fetch Fear & Greed Index: {e}")
        
        return {"value": 50, "classification": "Neutral"}

    async def _get_coin_sentiment_data(self, coin_id: str) -> Dict[str, Any]:
        """Get coin-specific sentiment data from CoinGecko"""
        try:
            url = f"{self.coingecko_base_url}/coins/{coin_id}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "reddit_score": data.get("community_score", 0),
                        "reddit_comments_24h": data.get("community_data", {}).get("reddit_comments_24h", 0),
                        "reddit_posts_24h": data.get("community_data", {}).get("reddit_posts_24h", 0),
                        "twitter_followers": data.get("community_data", {}).get("twitter_followers", 0),
                        "telegram_channel_user_count": data.get("community_data", {}).get("telegram_channel_user_count", 0),
                        "community_score": data.get("community_score", 0),
                        "developer_score": data.get("developer_score", 0),
                        "liquidity_score": data.get("liquidity_score", 0),
                        "public_interest_score": data.get("public_interest_score", 0),
                        "market_cap_rank": data.get("market_cap_rank", 0),
                        "coingecko_score": data.get("coingecko_score", 0)
                    }
        except Exception as e:
            logger.error(f"Failed to fetch coin sentiment data: {e}")
        
        return {}

    def _calculate_sentiment_score(self, fear_greed_data: Dict[str, Any], coin_data: Dict[str, Any]) -> float:
        """Calculate overall sentiment score"""
        # Fear & Greed Index contribution (0-100 scale, normalize to -1 to 1)
        fear_greed_score = (fear_greed_data.get("value", 50) - 50) / 50
        
        # Community score contribution (0-100 scale, normalize to -1 to 1)
        community_score = (coin_data.get("community_score", 50) - 50) / 50
        
        # Developer score contribution
        developer_score = (coin_data.get("developer_score", 50) - 50) / 50
        
        # Weighted average
        sentiment_score = (fear_greed_score * 0.4 + community_score * 0.3 + developer_score * 0.3)
        return max(-1, min(1, sentiment_score))  # Clamp between -1 and 1

    def _classify_sentiment(self, sentiment_score: float) -> str:
        """Classify sentiment based on score"""
        if sentiment_score >= 0.5:
            return "Very Bullish"
        elif sentiment_score >= 0.1:
            return "Bullish"
        elif sentiment_score >= -0.1:
            return "Neutral"
        elif sentiment_score >= -0.5:
            return "Bearish"
        else:
            return "Very Bearish"

    def _analyze_trend_direction(self, prices: List[float]) -> tuple:
        """Analyze trend direction and strength"""
        if len(prices) < 10:
            return "neutral", "weak"
        
        # Calculate short-term and long-term trends
        short_trend = (prices[-1] - prices[-5]) / prices[-5] if prices[-5] > 0 else 0
        long_trend = (prices[-1] - prices[-10]) / prices[-10] if prices[-10] > 0 else 0
        
        # Determine direction
        if short_trend > 0.02 and long_trend > 0.05:
            direction = "bullish"
            strength = "strong"
        elif short_trend > 0.01:
            direction = "bullish"
            strength = "moderate"
        elif short_trend < -0.02 and long_trend < -0.05:
            direction = "bearish"
            strength = "strong"
        elif short_trend < -0.01:
            direction = "bearish"
            strength = "moderate"
        else:
            direction = "neutral"
            strength = "weak"
        
        return direction, strength

    def _calculate_momentum(self, prices: List[float], volumes: List[float]) -> tuple:
        """Calculate price and volume momentum"""
        if len(prices) < 5 or len(volumes) < 5:
            return "stable", "stable", 0.5
        
        # Price momentum
        price_change = (prices[-1] - prices[-5]) / prices[-5] if prices[-5] > 0 else 0
        if price_change > 0.05:
            price_momentum = "increasing"
        elif price_change < -0.05:
            price_momentum = "decreasing"
        else:
            price_momentum = "stable"
        
        # Volume momentum
        volume_change = (volumes[-1] - volumes[-5]) / volumes[-5] if volumes[-5] > 0 else 0
        if volume_change > 0.2:
            volume_momentum = "increasing"
        elif volume_change < -0.2:
            volume_momentum = "decreasing"
        else:
            volume_momentum = "stable"
        
        # Momentum score (0-1 scale)
        momentum_score = 0.5 + (price_change * 2) + (volume_change * 0.5)
        momentum_score = max(0, min(1, momentum_score))
        
        return price_momentum, volume_momentum, momentum_score

    def _calculate_key_levels(self, prices: List[float]) -> tuple:
        """Calculate key breakout and breakdown levels"""
        if len(prices) < 20:
            current_price = prices[-1] if prices else 0
            return current_price * 1.05, current_price * 0.95
        
        recent_high = max(prices[-20:])
        recent_low = min(prices[-20:])
        current_price = prices[-1]
        
        breakout_level = recent_high * 1.02
        breakdown_level = recent_low * 0.98
        
        return breakout_level, breakdown_level

    def _calculate_trend_duration(self, prices: List[float], trend_direction: str) -> str:
        """Calculate how long the current trend has been active"""
        if len(prices) < 5:
            return "insufficient data"
        
        # Simple trend duration calculation
        if trend_direction == "bullish":
            # Count consecutive higher highs
            duration = 0
            for i in range(len(prices) - 1, 0, -1):
                if prices[i] > prices[i-1]:
                    duration += 1
                else:
                    break
        elif trend_direction == "bearish":
            # Count consecutive lower lows
            duration = 0
            for i in range(len(prices) - 1, 0, -1):
                if prices[i] < prices[i-1]:
                    duration += 1
                else:
                    break
        else:
            return "no clear trend"
        
        if duration == 0:
            return "just started"
        elif duration <= 3:
            return f"{duration} days"
        elif duration <= 7:
            return f"{duration} days"
        else:
            return f"{duration} days"

    def _calculate_price_change(self, prices: List[float], days: int) -> float:
        """Calculate price change over specified days"""
        if len(prices) < days + 1:
            return 0
        
        start_price = prices[-days-1]
        end_price = prices[-1]
        
        if start_price == 0:
            return 0
        
        return ((end_price - start_price) / start_price) * 100

    def _count_higher_highs(self, prices: List[float]) -> int:
        """Count higher highs in recent price action"""
        if len(prices) < 10:
            return 0
        
        higher_highs = 0
        for i in range(len(prices) - 10, len(prices) - 1):
            if prices[i+1] > prices[i]:
                higher_highs += 1
        
        return higher_highs

    def _count_higher_lows(self, prices: List[float]) -> int:
        """Count higher lows in recent price action"""
        if len(prices) < 10:
            return 0
        
        higher_lows = 0
        for i in range(len(prices) - 10, len(prices) - 1):
            if prices[i+1] > prices[i]:
                higher_lows += 1
        
        return higher_lows

    def _calculate_trend_consistency(self, prices: List[float]) -> float:
        """Calculate trend consistency score"""
        if len(prices) < 10:
            return 0.5
        
        # Calculate how consistent the trend is
        trend_changes = 0
        for i in range(len(prices) - 10, len(prices) - 1):
            if (prices[i+1] - prices[i]) * (prices[i] - prices[i-1]) < 0:
                trend_changes += 1
        
        consistency = 1 - (trend_changes / 9)  # 9 is the number of comparisons
        return max(0, min(1, consistency))

    def _calculate_volatility(self, prices: List[float], period: int) -> float:
        """Calculate price volatility"""
        if len(prices) < period + 1:
            return 0
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
        
        if not returns:
            return 0
        
        # Use recent returns for volatility calculation
        recent_returns = returns[-period:] if len(returns) >= period else returns
        mean_return = sum(recent_returns) / len(recent_returns)
        variance = sum((r - mean_return) ** 2 for r in recent_returns) / len(recent_returns)
        
        return (variance ** 0.5)

    def _calculate_volatility_trend(self, prices: List[float]) -> str:
        """Calculate volatility trend"""
        if len(prices) < 60:
            return "insufficient data"
        
        recent_vol = self._calculate_volatility(prices, 30)
        older_vol = self._calculate_volatility(prices[:-30], 30)
        
        if recent_vol > older_vol * 1.1:
            return "increasing"
        elif recent_vol < older_vol * 0.9:
            return "decreasing"
        else:
            return "stable"

    def _calculate_value_at_risk(self, prices: List[float], confidence: float) -> float:
        """Calculate Value at Risk"""
        if len(prices) < 30:
            return 0
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
        
        if not returns:
            return 0
        
        # Sort returns and find VaR
        returns.sort()
        var_index = int(len(returns) * (1 - confidence))
        return abs(returns[var_index]) * 100  # Return as percentage

    def _calculate_max_drawdown(self, prices: List[float]) -> float:
        """Calculate maximum drawdown"""
        if len(prices) < 2:
            return 0
        
        peak = prices[0]
        max_dd = 0
        
        for price in prices:
            if price > peak:
                peak = price
            dd = (peak - price) / peak
            max_dd = max(max_dd, dd)
        
        return max_dd

    def _calculate_sharpe_ratio(self, prices: List[float]) -> float:
        """Calculate Sharpe ratio"""
        if len(prices) < 30:
            return 0
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
        
        if not returns:
            return 0
        
        mean_return = sum(returns) / len(returns)
        std_return = (sum((r - mean_return) ** 2 for r in returns) / len(returns)) ** 0.5
        
        if std_return == 0:
            return 0
        
        # Assuming risk-free rate of 0.02 (2%)
        sharpe = (mean_return - 0.02/365) / std_return
        return sharpe * (365 ** 0.5)  # Annualized

    def _calculate_sortino_ratio(self, prices: List[float]) -> float:
        """Calculate Sortino ratio"""
        if len(prices) < 30:
            return 0
        
        returns = []
        for i in range(1, len(prices)):
            if prices[i-1] > 0:
                returns.append((prices[i] - prices[i-1]) / prices[i-1])
        
        if not returns:
            return 0
        
        mean_return = sum(returns) / len(returns)
        
        # Calculate downside deviation
        downside_returns = [r for r in returns if r < mean_return]
        if not downside_returns:
            return 0
        
        downside_deviation = (sum((r - mean_return) ** 2 for r in downside_returns) / len(downside_returns)) ** 0.5
        
        if downside_deviation == 0:
            return 0
        
        # Assuming risk-free rate of 0.02 (2%)
        sortino = (mean_return - 0.02/365) / downside_deviation
        return sortino * (365 ** 0.5)  # Annualized

    def _classify_volatility(self, volatility: float) -> str:
        """Classify volatility level"""
        if volatility < 0.1:
            return "low"
        elif volatility < 0.25:
            return "medium"
        elif volatility < 0.5:
            return "high"
        else:
            return "very high"

    def _classify_risk_level(self, volatility: float, max_drawdown: float) -> str:
        """Classify risk level"""
        risk_score = volatility * 0.7 + max_drawdown * 0.3
        
        if risk_score < 0.1:
            return "low"
        elif risk_score < 0.25:
            return "moderate"
        elif risk_score < 0.5:
            return "high"
        else:
            return "very high"
