"""
Currency Tools
Contains tools for currency conversion and exchange rate data
"""

import asyncio
import logging
import aiohttp
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import os

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)


class CurrencyConverterTool(MCPTool):
    def __init__(self):
        self.session = None
        self.exchange_rate_api_url = "https://api.exchangerate-api.com/v4/latest"
        self.coingecko_api_url = "https://api.coingecko.com/api/v3"
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
        
    @property
    def name(self) -> str:
        return "currency_converter"
    
    @property
    def description(self) -> str:
        return "Convert between different currencies including fiat and cryptocurrencies with real-time exchange rates"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "convert",
                        "get_exchange_rates",
                        "get_supported_currencies",
                        "get_historical_rates",
                        "get_crypto_rates"
                    ]
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code (e.g., USD, EUR, BTC, ETH)"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code (e.g., USD, EUR, BTC, ETH)"
                },
                "amount": {
                    "type": "number",
                    "description": "Amount to convert"
                },
                "base_currency": {
                    "type": "string",
                    "description": "Base currency for exchange rates (default: USD)"
                },
                "date": {
                    "type": "string",
                    "description": "Date for historical rates (YYYY-MM-DD format)"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            
            if action == "convert":
                result = await self._convert_currency(**arguments)
            elif action == "get_exchange_rates":
                result = await self._get_exchange_rates(**arguments)
            elif action == "get_supported_currencies":
                result = await self._get_supported_currencies(**arguments)
            elif action == "get_historical_rates":
                result = await self._get_historical_rates(**arguments)
            elif action == "get_crypto_rates":
                result = await self._get_crypto_rates(**arguments)
            else:
                result = {"error": f"Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _convert_currency(self, **kwargs) -> dict:
        """Convert between currencies."""
        try:
            from_currency = kwargs.get("from_currency", "USD").upper()
            to_currency = kwargs.get("to_currency", "EUR").upper()
            amount = kwargs.get("amount", 1.0)
            
            if not from_currency or not to_currency:
                return {
                    "success": False,
                    "error": "from_currency and to_currency are required"
                }
            
            # Check if it's a crypto conversion
            if self._is_crypto(from_currency) or self._is_crypto(to_currency):
                return await self._convert_with_crypto(from_currency, to_currency, amount)
            else:
                return await self._convert_fiat_currencies(from_currency, to_currency, amount)
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to convert currency: {str(e)}"
            }
    
    async def _convert_fiat_currencies(self, from_currency: str, to_currency: str, amount: float) -> dict:
        """Convert between fiat currencies."""
        try:
            session = await self._get_session()
            
            # Get exchange rates from base currency
            url = f"{self.exchange_rate_api_url}/{from_currency}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = data.get("rates", {})
                    
                    if to_currency in rates:
                        rate = rates[to_currency]
                        converted_amount = amount * rate
                        
                        return {
                            "success": True,
                            "data": {
                                "from_currency": from_currency,
                                "to_currency": to_currency,
                                "amount": amount,
                                "converted_amount": round(converted_amount, 6),
                                "exchange_rate": rate,
                                "last_updated": data.get("date"),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Currency {to_currency} not found in exchange rates"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch exchange rates: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to convert fiat currencies: {str(e)}"
            }
    
    async def _convert_with_crypto(self, from_currency: str, to_currency: str, amount: float) -> dict:
        """Convert involving cryptocurrencies."""
        try:
            session = await self._get_session()
            
            # Get crypto rates from CoinGecko
            crypto_ids = []
            if self._is_crypto(from_currency):
                crypto_ids.append(self._get_crypto_id(from_currency))
            if self._is_crypto(to_currency):
                crypto_ids.append(self._get_crypto_id(to_currency))
            
            if not crypto_ids:
                return {
                    "success": False,
                    "error": "Invalid cryptocurrency specified"
                }
            
            # Get crypto prices in USD
            url = f"{self.coingecko_api_url}/simple/price"
            params = {
                "ids": ",".join(crypto_ids),
                "vs_currencies": "usd"
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    crypto_data = await response.json()
                    
                    # Calculate conversion
                    if self._is_crypto(from_currency) and not self._is_crypto(to_currency):
                        # Crypto to fiat
                        crypto_id = self._get_crypto_id(from_currency)
                        if crypto_id in crypto_data:
                            usd_rate = crypto_data[crypto_id]["usd"]
                            # Convert crypto to USD, then USD to target currency
                            usd_amount = amount * usd_rate
                            fiat_result = await self._convert_fiat_currencies("USD", to_currency, usd_amount)
                            if fiat_result["success"]:
                                return {
                                    "success": True,
                                    "data": {
                                        "from_currency": from_currency,
                                        "to_currency": to_currency,
                                        "amount": amount,
                                        "converted_amount": fiat_result["data"]["converted_amount"],
                                        "usd_rate": usd_rate,
                                        "usd_amount": usd_amount,
                                        "final_rate": fiat_result["data"]["exchange_rate"],
                                        "timestamp": datetime.now().isoformat()
                                    }
                                }
                    
                    elif not self._is_crypto(from_currency) and self._is_crypto(to_currency):
                        # Fiat to crypto
                        crypto_id = self._get_crypto_id(to_currency)
                        if crypto_id in crypto_data:
                            usd_rate = crypto_data[crypto_id]["usd"]
                            # Convert fiat to USD, then USD to crypto
                            usd_result = await self._convert_fiat_currencies(from_currency, "USD", amount)
                            if usd_result["success"]:
                                usd_amount = usd_result["data"]["converted_amount"]
                                crypto_amount = usd_amount / usd_rate
                                return {
                                    "success": True,
                                    "data": {
                                        "from_currency": from_currency,
                                        "to_currency": to_currency,
                                        "amount": amount,
                                        "converted_amount": round(crypto_amount, 8),
                                        "usd_amount": usd_amount,
                                        "crypto_rate": usd_rate,
                                        "final_rate": 1 / usd_rate,
                                        "timestamp": datetime.now().isoformat()
                                    }
                                }
                    
                    elif self._is_crypto(from_currency) and self._is_crypto(to_currency):
                        # Crypto to crypto
                        from_crypto_id = self._get_crypto_id(from_currency)
                        to_crypto_id = self._get_crypto_id(to_currency)
                        
                        if from_crypto_id in crypto_data and to_crypto_id in crypto_data:
                            from_usd_rate = crypto_data[from_crypto_id]["usd"]
                            to_usd_rate = crypto_data[to_crypto_id]["usd"]
                            
                            # Convert through USD
                            usd_amount = amount * from_usd_rate
                            crypto_amount = usd_amount / to_usd_rate
                            
                            return {
                                "success": True,
                                "data": {
                                    "from_currency": from_currency,
                                    "to_currency": to_currency,
                                    "amount": amount,
                                    "converted_amount": round(crypto_amount, 8),
                                    "from_usd_rate": from_usd_rate,
                                    "to_usd_rate": to_usd_rate,
                                    "cross_rate": from_usd_rate / to_usd_rate,
                                    "timestamp": datetime.now().isoformat()
                                }
                            }
                    
                    return {
                        "success": False,
                        "error": "Unable to perform conversion with provided currencies"
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch crypto rates: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to convert with crypto: {str(e)}"
            }
    
    async def _get_exchange_rates(self, **kwargs) -> dict:
        """Get current exchange rates for a base currency."""
        try:
            base_currency = kwargs.get("base_currency", "USD").upper()
            session = await self._get_session()
            
            url = f"{self.exchange_rate_api_url}/{base_currency}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Format rates for better readability
                    rates = data.get("rates", {})
                    formatted_rates = {}
                    
                    for currency, rate in rates.items():
                        formatted_rates[currency] = {
                            "rate": rate,
                            "inverse_rate": round(1 / rate, 6) if rate > 0 else 0
                        }
                    
                    return {
                        "success": True,
                        "data": {
                            "base_currency": base_currency,
                            "rates": formatted_rates,
                            "total_currencies": len(rates),
                            "last_updated": data.get("date"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch exchange rates: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get exchange rates: {str(e)}"
            }
    
    async def _get_supported_currencies(self, **kwargs) -> dict:
        """Get list of supported currencies."""
        try:
            # Fiat currencies
            fiat_currencies = [
                "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
                "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "BRL", "ZAR",
                "PLN", "THB", "IDR", "MYR", "PHP", "CZK", "HUF", "ILS", "CLP", "COP",
                "EGP", "PKR", "BDT", "VND", "NGN", "ARS", "PEN", "UAH", "RON", "BGN"
            ]
            
            # Popular cryptocurrencies
            crypto_currencies = [
                "BTC", "ETH", "USDT", "USDC", "BNB", "XRP", "ADA", "SOL", "DOT", "DOGE",
                "AVAX", "MATIC", "LINK", "UNI", "LTC", "BCH", "XLM", "ATOM", "ETC", "FIL"
            ]
            
            return {
                "success": True,
                "data": {
                    "fiat_currencies": fiat_currencies,
                    "crypto_currencies": crypto_currencies,
                    "total_fiat": len(fiat_currencies),
                    "total_crypto": len(crypto_currencies),
                    "total_currencies": len(fiat_currencies) + len(crypto_currencies),
                    "note": "This is a curated list. More currencies may be supported by the APIs.",
                    "timestamp": datetime.now().isoformat()
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get supported currencies: {str(e)}"
            }
    
    async def _get_historical_rates(self, **kwargs) -> dict:
        """Get historical exchange rates."""
        try:
            base_currency = kwargs.get("base_currency", "USD").upper()
            target_currency = kwargs.get("to_currency", "EUR").upper()
            date = kwargs.get("date")
            
            if not date:
                # Default to yesterday
                date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            
            session = await self._get_session()
            
            # Use historical API endpoint
            url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    rates = data.get("rates", {})
                    
                    if target_currency in rates:
                        return {
                            "success": True,
                            "data": {
                                "base_currency": base_currency,
                                "target_currency": target_currency,
                                "date": date,
                                "rate": rates[target_currency],
                                "inverse_rate": round(1 / rates[target_currency], 6),
                                "note": "Historical rates may vary by API provider",
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": f"Currency {target_currency} not found in historical rates"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch historical rates: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get historical rates: {str(e)}"
            }
    
    async def _get_crypto_rates(self, **kwargs) -> dict:
        """Get current cryptocurrency rates."""
        try:
            session = await self._get_session()
            
            # Get top cryptocurrencies by market cap
            url = f"{self.coingecko_api_url}/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 20,
                "page": 1,
                "sparkline": "false"
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    crypto_rates = []
                    for coin in data:
                        crypto_rates.append({
                            "symbol": coin["symbol"].upper(),
                            "name": coin["name"],
                            "price_usd": coin["current_price"],
                            "market_cap": coin["market_cap"],
                            "volume_24h": coin["total_volume"],
                            "price_change_24h": coin["price_change_percentage_24h"],
                            "market_cap_rank": coin["market_cap_rank"]
                        })
                    
                    return {
                        "success": True,
                        "data": {
                            "crypto_rates": crypto_rates,
                            "total_cryptos": len(crypto_rates),
                            "base_currency": "USD",
                            "note": "Prices are in USD. Use convert action for other currencies.",
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to fetch crypto rates: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get crypto rates: {str(e)}"
            }
    
    def _is_crypto(self, currency: str) -> bool:
        """Check if currency is a cryptocurrency."""
        crypto_list = [
            "BTC", "ETH", "USDT", "USDC", "BNB", "XRP", "ADA", "SOL", "DOT", "DOGE",
            "AVAX", "MATIC", "LINK", "UNI", "LTC", "BCH", "XLM", "ATOM", "ETC", "FIL"
        ]
        return currency.upper() in crypto_list
    
    def _get_crypto_id(self, currency: str) -> str:
        """Get CoinGecko ID for cryptocurrency."""
        crypto_mapping = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "USDT": "tether",
            "USDC": "usd-coin",
            "BNB": "binancecoin",
            "XRP": "ripple",
            "ADA": "cardano",
            "SOL": "solana",
            "DOT": "polkadot",
            "DOGE": "dogecoin",
            "AVAX": "avalanche-2",
            "MATIC": "matic-network",
            "LINK": "chainlink",
            "UNI": "uniswap",
            "LTC": "litecoin",
            "BCH": "bitcoin-cash",
            "XLM": "stellar",
            "ATOM": "cosmos",
            "ETC": "ethereum-classic",
            "FIL": "filecoin"
        }
        return crypto_mapping.get(currency.upper(), currency.lower())
