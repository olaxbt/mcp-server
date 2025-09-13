"""
CoinMarketCap MCP Tool
Access comprehensive cryptocurrency market data from CoinMarketCap API
"""

import requests
import json
from typing import Dict, Any, List, Optional
from .mcp_tool import MCPTool

class CoinMarketCapTool(MCPTool):
    def __init__(self):
        super().__init__()
        self.base_url = "https://pro-api.coinmarketcap.com/v1"
    
    @property
    def name(self) -> str:
        return "coinmarketcap"
    
    @property
    def description(self) -> str:
        return "Access comprehensive cryptocurrency market data from CoinMarketCap API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_latest_listings",
                        "get_quotes_latest",
                        "get_quotes_historical",
                        "get_global_metrics",
                        "get_trending",
                        "get_gainers_losers",
                        "get_categories",
                        "get_exchange_info",
                        "get_market_pairs"
                    ],
                    "description": "The action to perform"
                },
                "symbol": {
                    "type": "string",
                    "description": "Cryptocurrency symbol (e.g., BTC, ETH)"
                },
                "slug": {
                    "type": "string", 
                    "description": "Cryptocurrency slug (e.g., bitcoin, ethereum)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return (1-5000)",
                    "default": 100
                },
                "start": {
                    "type": "integer",
                    "description": "Starting point for pagination",
                    "default": 1
                },
                "sort": {
                    "type": "string",
                    "description": "Sort order (market_cap, volume_24h, percent_change_24h, etc.)",
                    "default": "market_cap"
                },
                "sort_dir": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "description": "Sort direction",
                    "default": "desc"
                },
                "time_period": {
                    "type": "string",
                    "enum": ["24h", "7d", "30d", "90d", "365d"],
                    "description": "Time period for data",
                    "default": "24h"
                },
                "category": {
                    "type": "string",
                    "description": "Category filter (e.g., DeFi, NFT, Gaming)"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_latest_listings":
                return await self._get_latest_listings(arguments)
            elif action == "get_quotes_latest":
                return await self._get_quotes_latest(arguments)
            elif action == "get_quotes_historical":
                return await self._get_quotes_historical(arguments)
            elif action == "get_global_metrics":
                return await self._get_global_metrics(arguments)
            elif action == "get_trending":
                return await self._get_trending(arguments)
            elif action == "get_gainers_losers":
                return await self._get_gainers_losers(arguments)
            elif action == "get_categories":
                return await self._get_categories(arguments)
            elif action == "get_exchange_info":
                return await self._get_exchange_info(arguments)
            elif action == "get_market_pairs":
                return await self._get_market_pairs(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_latest_listings(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get latest cryptocurrency listings"""
        params = {
            "start": args.get("start", 1),
            "limit": args.get("limit", 100),
            "sort": args.get("sort", "market_cap"),
            "sort_dir": args.get("sort_dir", "desc")
        }
        
        if args.get("category"):
            params["category"] = args["category"]
            
        # Mock data for demonstration
        mock_data = {
            "data": [
                {
                    "id": 1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "slug": "bitcoin",
                    "cmc_rank": 1,
                    "quote": {
                        "USD": {
                            "price": 45000.00,
                            "market_cap": 850000000000,
                            "volume_24h": 25000000000,
                            "percent_change_1h": 0.5,
                            "percent_change_24h": 2.3,
                            "percent_change_7d": -5.2
                        }
                    }
                },
                {
                    "id": 1027,
                    "name": "Ethereum", 
                    "symbol": "ETH",
                    "slug": "ethereum",
                    "cmc_rank": 2,
                    "quote": {
                        "USD": {
                            "price": 3200.00,
                            "market_cap": 380000000000,
                            "volume_24h": 15000000000,
                            "percent_change_1h": 0.8,
                            "percent_change_24h": 3.1,
                            "percent_change_7d": -2.8
                        }
                    }
                }
            ],
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Latest Listings:\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_quotes_latest(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get latest quotes for specific cryptocurrencies"""
        symbol = args.get("symbol", "BTC")
        
        # Mock data for demonstration
        mock_data = {
            "data": {
                "BTC": {
                    "id": 1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "slug": "bitcoin",
                    "quote": {
                        "USD": {
                            "price": 45000.00,
                            "market_cap": 850000000000,
                            "volume_24h": 25000000000,
                            "percent_change_1h": 0.5,
                            "percent_change_24h": 2.3,
                            "percent_change_7d": -5.2,
                            "last_updated": "2024-01-15T10:00:00.000Z"
                        }
                    }
                }
            },
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Latest Quotes for {symbol}:\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_quotes_historical(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get historical quotes for specific cryptocurrencies"""
        symbol = args.get("symbol", "BTC")
        time_period = args.get("time_period", "24h")
        
        # Mock historical data
        mock_data = {
            "data": {
                "quotes": [
                    {
                        "timestamp": "2024-01-15T09:00:00.000Z",
                        "quote": {
                            "USD": {
                                "price": 44800.00,
                                "market_cap": 840000000000,
                                "volume_24h": 24000000000
                            }
                        }
                    },
                    {
                        "timestamp": "2024-01-15T10:00:00.000Z", 
                        "quote": {
                            "USD": {
                                "price": 45000.00,
                                "market_cap": 850000000000,
                                "volume_24h": 25000000000
                            }
                        }
                    }
                ]
            },
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Historical Quotes for {symbol} ({time_period}):\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_global_metrics(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get global cryptocurrency market metrics"""
        
        # Mock global metrics data
        mock_data = {
            "data": {
                "active_cryptocurrencies": 8500,
                "total_cryptocurrencies": 12000,
                "active_market_pairs": 45000,
                "active_exchanges": 500,
                "eth_dominance": 18.5,
                "btc_dominance": 42.3,
                "quote": {
                    "USD": {
                        "total_market_cap": 1800000000000,
                        "total_volume_24h": 80000000000,
                        "total_volume_24h_reported": 75000000000,
                        "altcoin_market_cap": 1038000000000,
                        "altcoin_volume_24h": 55000000000,
                        "altcoin_volume_24h_reported": 50000000000,
                        "last_updated": "2024-01-15T10:00:00.000Z"
                    }
                }
            },
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Global Metrics:\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_trending(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get trending cryptocurrencies"""
        
        # Mock trending data
        mock_data = {
            "data": [
                {
                    "id": 1,
                    "name": "Bitcoin",
                    "symbol": "BTC",
                    "slug": "bitcoin",
                    "cmc_rank": 1,
                    "quote": {
                        "USD": {
                            "price": 45000.00,
                            "percent_change_24h": 2.3,
                            "volume_24h": 25000000000
                        }
                    }
                },
                {
                    "id": 1027,
                    "name": "Ethereum",
                    "symbol": "ETH", 
                    "slug": "ethereum",
                    "cmc_rank": 2,
                    "quote": {
                        "USD": {
                            "price": 3200.00,
                            "percent_change_24h": 3.1,
                            "volume_24h": 15000000000
                        }
                    }
                }
            ],
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Trending Cryptocurrencies:\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_gainers_losers(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top gainers and losers"""
        time_period = args.get("time_period", "24h")
        
        # Mock gainers/losers data
        mock_data = {
            "gainers": [
                {
                    "id": 1839,
                    "name": "Binance Coin",
                    "symbol": "BNB",
                    "slug": "binance-coin",
                    "quote": {
                        "USD": {
                            "price": 320.00,
                            "percent_change_24h": 8.5,
                            "volume_24h": 2000000000
                        }
                    }
                }
            ],
            "losers": [
                {
                    "id": 2010,
                    "name": "Cardano",
                    "symbol": "ADA",
                    "slug": "cardano",
                    "quote": {
                        "USD": {
                            "price": 0.45,
                            "percent_change_24h": -6.2,
                            "volume_24h": 800000000
                        }
                    }
                }
            ],
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Top Gainers & Losers ({time_period}):\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_categories(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get cryptocurrency categories"""
        
        # Mock categories data
        mock_data = {
            "data": [
                {
                    "id": 1,
                    "name": "DeFi",
                    "title": "Decentralized Finance",
                    "description": "Decentralized finance protocols and applications",
                    "num_tokens": 500,
                    "avg_price_change": 2.5,
                    "market_cap": 50000000000,
                    "market_cap_change": 5.2,
                    "volume": 8000000000,
                    "volume_change": 12.3
                },
                {
                    "id": 2,
                    "name": "NFT",
                    "title": "Non-Fungible Tokens",
                    "description": "Non-fungible token platforms and marketplaces",
                    "num_tokens": 200,
                    "avg_price_change": -1.2,
                    "market_cap": 15000000000,
                    "market_cap_change": -3.1,
                    "volume": 2000000000,
                    "volume_change": 8.7
                }
            ],
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Categories:\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_exchange_info(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange information"""
        
        # Mock exchange data
        mock_data = {
            "data": [
                {
                    "id": 270,
                    "name": "Binance",
                    "slug": "binance",
                    "is_active": 1,
                    "is_fiat": 0,
                    "num_market_pairs": 1500,
                    "date_launched": "2017-07-14T00:00:00.000Z",
                    "quote": {
                        "USD": {
                            "volume_24h": 15000000000,
                            "volume_24h_adjusted": 14500000000,
                            "volume_7d": 100000000000,
                            "volume_30d": 400000000000,
                            "percent_change_volume_24h": 5.2,
                            "percent_change_volume_7d": -2.1,
                            "percent_change_volume_30d": 8.5
                        }
                    }
                }
            ],
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Exchange Information:\n\n{json.dumps(mock_data, indent=2)}"}]
    
    async def _get_market_pairs(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get market pairs for a cryptocurrency"""
        symbol = args.get("symbol", "BTC")
        
        # Mock market pairs data
        mock_data = {
            "data": {
                "id": 1,
                "name": "Bitcoin",
                "symbol": "BTC",
                "slug": "bitcoin",
                "num_market_pairs": 500,
                "market_pairs": [
                    {
                        "exchange": {
                            "id": 270,
                            "name": "Binance",
                            "slug": "binance"
                        },
                        "market_pair": "BTC/USDT",
                        "category": "spot",
                        "fee_type": "percentage",
                        "market_pair_base": {
                            "currency_id": 1,
                            "currency_symbol": "BTC",
                            "currency_type": "cryptocurrency"
                        },
                        "market_pair_quote": {
                            "currency_id": 825,
                            "currency_symbol": "USDT",
                            "currency_type": "cryptocurrency"
                        },
                        "quote": {
                            "USD": {
                                "price": 45000.00,
                                "volume_24h": 5000000000,
                                "volume_percentage": 20.0,
                                "last_updated": "2024-01-15T10:00:00.000Z"
                            }
                        }
                    }
                ]
            },
            "status": {
                "timestamp": "2024-01-15T10:00:00.000Z",
                "error_code": 0,
                "error_message": None
            }
        }
        
        return [{"type": "text", "text": f"✅ CoinMarketCap Market Pairs for {symbol}:\n\n{json.dumps(mock_data, indent=2)}"}]