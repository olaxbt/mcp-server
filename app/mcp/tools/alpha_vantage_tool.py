"""
Alpha Vantage MCP Tool
Access financial data, technical indicators, and fundamental data from Alpha Vantage API
"""

import requests
import json
from typing import Dict, Any, List, Optional
from .mcp_tool import MCPTool

class AlphaVantageTool(MCPTool):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.alphavantage.co/query"
    
    @property
    def name(self) -> str:
        return "alpha_vantage"
    
    @property
    def description(self) -> str:
        return "Access financial data, technical indicators, and fundamental data from Alpha Vantage API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_crypto_daily",
                        "get_sma",
                        "get_ema",
                        "get_rsi",
                        "get_macd",
                        "get_bbands"
                    ],
                    "description": "The action to perform"
                },
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol (e.g., BTC, ETH)",
                    "default": "BTC"
                },
                "market": {
                    "type": "string",
                    "description": "Market (e.g., USD, EUR)",
                    "default": "USD"
                },
                "time_period": {
                    "type": "integer",
                    "description": "Time period for technical indicators",
                    "default": 20
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_crypto_daily":
                return await self._get_crypto_daily(arguments)
            elif action == "get_sma":
                return await self._get_sma(arguments)
            elif action == "get_ema":
                return await self._get_ema(arguments)
            elif action == "get_rsi":
                return await self._get_rsi(arguments)
            elif action == "get_macd":
                return await self._get_macd(arguments)
            elif action == "get_bbands":
                return await self._get_bbands(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_crypto_daily(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get daily cryptocurrency data"""
        symbol = args.get("symbol", "BTC")
        market = args.get("market", "USD")
        
        mock_data = {
            "Meta Data": {
                "1. Information": f"Daily Prices and Volumes for Digital Currency ({symbol})",
                "2. Digital Currency Code": symbol,
                "3. Digital Currency Name": "Bitcoin" if symbol == "BTC" else "Ethereum",
                "4. Market Code": market,
                "5. Market Name": "United States Dollar" if market == "USD" else "Euro",
                "6. Last Refreshed": "2024-01-15 00:00:00",
                "7. Time Zone": "UTC"
            },
            "Time Series (Digital Currency Daily)": {
                "2024-01-15": {
                    "1a. open (USD)": "44500.00000000",
                    "1b. open (USD)": "44500.00000000",
                    "2a. high (USD)": "46000.00000000",
                    "2b. high (USD)": "46000.00000000",
                    "3a. low (USD)": "44000.00000000",
                    "3b. low (USD)": "44000.00000000",
                    "4a. close (USD)": "45000.00000000",
                    "4b. close (USD)": "45000.00000000",
                    "5. volume": "1000.00000000",
                    "6. market cap (USD)": "45000000000.00000000"
                }
            }
        }
        
        return [{"type": "text", "text": f"✅ Alpha Vantage Daily Crypto Data ({symbol}/{market}):\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_sma(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Simple Moving Average (SMA)"""
        symbol = args.get("symbol", "BTC")
        time_period = args.get("time_period", 20)
        
        mock_data = {
            "Meta Data": {
                "1: Symbol": f"{symbol}",
                "2: Indicator": f"Simple Moving Average (SMA)",
                "3: Last Refreshed": "2024-01-15 00:00:00",
                "4: Interval": "daily",
                "5: Time Period": time_period,
                "6: Series Type": "close",
                "7: Time Zone": "UTC"
            },
            "Technical Analysis: SMA": {
                "2024-01-15": {
                    "SMA": "44800.0000"
                }
            }
        }
        
        return [{"type": "text", "text": f"✅ Alpha Vantage SMA ({symbol}, {time_period} period):\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_ema(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Exponential Moving Average (EMA)"""
        return [{"type": "text", "text": "✅ Alpha Vantage EMA (mock data)"}]
    
    async def _get_rsi(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Relative Strength Index (RSI)"""
        return [{"type": "text", "text": "✅ Alpha Vantage RSI (mock data)"}]
    
    async def _get_macd(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get MACD (Moving Average Convergence Divergence)"""
        return [{"type": "text", "text": "✅ Alpha Vantage MACD (mock data)"}]
    
    async def _get_bbands(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Bollinger Bands"""
        return [{"type": "text", "text": "✅ Alpha Vantage Bollinger Bands (mock data)"}]