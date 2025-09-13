"""
Alpha Vantage Stocks MCP Tool
Access stock market data, ETFs, and traditional finance data from Alpha Vantage API
"""

import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class AlphaVantageStocksTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._name = "alpha_vantage_stocks"
        self._description = "Access stock market data, ETFs, and traditional finance data from Alpha Vantage API"
        self.base_url = "https://www.alphavantage.co/query"
        self._session = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_stock_quote",
                        "get_stock_daily",
                        "get_stock_weekly",
                        "get_stock_monthly",
                        "get_stock_intraday",
                        "get_stock_technical_indicators",
                        "get_etf_quote",
                        "get_etf_daily",
                        "get_forex_quote",
                        "get_forex_daily",
                        "get_economic_indicators",
                        "get_earnings",
                        "get_income_statement",
                        "get_balance_sheet",
                        "get_cash_flow",
                        "get_company_overview",
                        "get_news_sentiment",
                        "get_treasury_yield",
                        "get_federal_funds_rate"
                    ],
                    "description": "The action to perform"
                },
                "symbol": {
                    "type": "string",
                    "description": "Stock symbol (e.g., AAPL, MSFT, GOOGL)"
                },
                "function": {
                    "type": "string",
                    "enum": ["TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY", "TIME_SERIES_INTRADAY"],
                    "description": "Time series function"
                },
                "interval": {
                    "type": "string",
                    "enum": ["1min", "5min", "15min", "30min", "60min"],
                    "description": "Time interval for intraday data"
                },
                "from_symbol": {
                    "type": "string",
                    "description": "From currency symbol (e.g., USD, EUR)"
                },
                "to_symbol": {
                    "type": "string",
                    "description": "To currency symbol (e.g., EUR, JPY)"
                },
                "indicator": {
                    "type": "string",
                    "enum": ["SMA", "EMA", "RSI", "MACD", "BBANDS", "STOCH", "ADX", "CCI", "AROON", "MOM"],
                    "description": "Technical indicator"
                },
                "time_period": {
                    "type": "integer",
                    "description": "Time period for technical indicators",
                    "default": 20
                },
                "series_type": {
                    "type": "string",
                    "enum": ["close", "open", "high", "low"],
                    "description": "Series type for technical indicators",
                    "default": "close"
                },
                "api_key": {
                    "type": "string",
                    "description": "Alpha Vantage API key (required for all endpoints)",
                    "default": ""
                }
            },
            "required": ["action"]
        }

    async def _get_session(self):
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_stock_quote":
                return await self._get_stock_quote(arguments)
            elif action == "get_stock_daily":
                return await self._get_stock_daily(arguments)
            elif action == "get_stock_weekly":
                return await self._get_stock_weekly(arguments)
            elif action == "get_stock_monthly":
                return await self._get_stock_monthly(arguments)
            elif action == "get_stock_intraday":
                return await self._get_stock_intraday(arguments)
            elif action == "get_stock_technical_indicators":
                return await self._get_stock_technical_indicators(arguments)
            elif action == "get_etf_quote":
                return await self._get_etf_quote(arguments)
            elif action == "get_etf_daily":
                return await self._get_etf_daily(arguments)
            elif action == "get_forex_quote":
                return await self._get_forex_quote(arguments)
            elif action == "get_forex_daily":
                return await self._get_forex_daily(arguments)
            elif action == "get_economic_indicators":
                return await self._get_economic_indicators(arguments)
            elif action == "get_earnings":
                return await self._get_earnings(arguments)
            elif action == "get_income_statement":
                return await self._get_income_statement(arguments)
            elif action == "get_balance_sheet":
                return await self._get_balance_sheet(arguments)
            elif action == "get_cash_flow":
                return await self._get_cash_flow(arguments)
            elif action == "get_company_overview":
                return await self._get_company_overview(arguments)
            elif action == "get_news_sentiment":
                return await self._get_news_sentiment(arguments)
            elif action == "get_treasury_yield":
                return await self._get_treasury_yield(arguments)
            elif action == "get_federal_funds_rate":
                return await self._get_federal_funds_rate(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request to Alpha Vantage"""
        session = await self._get_session()
        
        # Remove None values from params
        clean_params = {k: v for k, v in params.items() if v is not None}
        
        try:
            async with session.get(self.base_url, params=clean_params) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Alpha Vantage API request failed: {e}")
            return {"error": f"Alpha Vantage API request failed: {e}"}

    async def _get_stock_quote(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get stock quote"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Stock Quote for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching stock quote: {e}")
            return [{"type": "text", "text": f"❌ Error fetching stock quote: {str(e)}"}]

    async def _get_stock_daily(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get daily stock data"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Daily Data for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching daily data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching daily data: {str(e)}"}]

    async def _get_stock_weekly(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get weekly stock data"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "TIME_SERIES_WEEKLY",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Weekly Data for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching weekly data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching weekly data: {str(e)}"}]

    async def _get_stock_monthly(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get monthly stock data"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "TIME_SERIES_MONTHLY",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Monthly Data for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching monthly data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching monthly data: {str(e)}"}]

    async def _get_stock_intraday(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get intraday stock data"""
        symbol = arguments.get("symbol", "AAPL")
        interval = arguments.get("interval", "1min")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": symbol,
                "interval": interval,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Intraday Data for {symbol} ({interval}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching intraday data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching intraday data: {str(e)}"}]

    async def _get_stock_technical_indicators(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get technical indicators"""
        symbol = arguments.get("symbol", "AAPL")
        indicator = arguments.get("indicator", "SMA")
        time_period = arguments.get("time_period", 20)
        series_type = arguments.get("series_type", "close")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": indicator,
                "symbol": symbol,
                "interval": "daily",
                "time_period": time_period,
                "series_type": series_type,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage {indicator} for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching technical indicators: {e}")
            return [{"type": "text", "text": f"❌ Error fetching technical indicators: {str(e)}"}]

    async def _get_etf_quote(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get ETF quote"""
        symbol = arguments.get("symbol", "SPY")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage ETF Quote for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching ETF quote: {e}")
            return [{"type": "text", "text": f"❌ Error fetching ETF quote: {str(e)}"}]

    async def _get_etf_daily(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get ETF daily data"""
        symbol = arguments.get("symbol", "SPY")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage ETF Daily Data for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching ETF daily data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching ETF daily data: {str(e)}"}]

    async def _get_forex_quote(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get forex quote"""
        from_symbol = arguments.get("from_symbol", "USD")
        to_symbol = arguments.get("to_symbol", "EUR")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": from_symbol,
                "to_currency": to_symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Forex Quote {from_symbol}/{to_symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching forex quote: {e}")
            return [{"type": "text", "text": f"❌ Error fetching forex quote: {str(e)}"}]

    async def _get_forex_daily(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get forex daily data"""
        from_symbol = arguments.get("from_symbol", "USD")
        to_symbol = arguments.get("to_symbol", "EUR")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "FX_DAILY",
                "from_symbol": from_symbol,
                "to_symbol": to_symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Forex Daily {from_symbol}/{to_symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching forex daily data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching forex daily data: {str(e)}"}]

    async def _get_economic_indicators(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get economic indicators"""
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "REAL_GDP",
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Economic Indicators:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching economic indicators: {e}")
            return [{"type": "text", "text": f"❌ Error fetching economic indicators: {str(e)}"}]

    async def _get_earnings(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get earnings data"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "EARNINGS",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Earnings for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching earnings: {e}")
            return [{"type": "text", "text": f"❌ Error fetching earnings: {str(e)}"}]

    async def _get_income_statement(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get income statement"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "INCOME_STATEMENT",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Income Statement for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching income statement: {e}")
            return [{"type": "text", "text": f"❌ Error fetching income statement: {str(e)}"}]

    async def _get_balance_sheet(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get balance sheet"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "BALANCE_SHEET",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Balance Sheet for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching balance sheet: {e}")
            return [{"type": "text", "text": f"❌ Error fetching balance sheet: {str(e)}"}]

    async def _get_cash_flow(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get cash flow"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "CASH_FLOW",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Cash Flow for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching cash flow: {e}")
            return [{"type": "text", "text": f"❌ Error fetching cash flow: {str(e)}"}]

    async def _get_company_overview(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get company overview"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "OVERVIEW",
                "symbol": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Company Overview for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching company overview: {e}")
            return [{"type": "text", "text": f"❌ Error fetching company overview: {str(e)}"}]

    async def _get_news_sentiment(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get news sentiment"""
        symbol = arguments.get("symbol", "AAPL")
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "NEWS_SENTIMENT",
                "tickers": symbol,
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage News Sentiment for {symbol}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching news sentiment: {e}")
            return [{"type": "text", "text": f"❌ Error fetching news sentiment: {str(e)}"}]

    async def _get_treasury_yield(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get treasury yield"""
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "TREASURY_YIELD",
                "interval": "monthly",
                "maturity": "10year",
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Treasury Yield:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching treasury yield: {e}")
            return [{"type": "text", "text": f"❌ Error fetching treasury yield: {str(e)}"}]

    async def _get_federal_funds_rate(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get federal funds rate"""
        api_key = arguments.get("api_key")
        
        try:
            params = {
                "function": "FEDERAL_FUNDS_RATE",
                "interval": "monthly",
                "apikey": api_key
            }
            
            data = await self._make_request(params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Alpha Vantage Federal Funds Rate:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching federal funds rate: {e}")
            return [{"type": "text", "text": f"❌ Error fetching federal funds rate: {str(e)}"}]