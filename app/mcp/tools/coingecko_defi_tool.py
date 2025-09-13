"""
CoinGecko DeFi MCP Tool
Access DeFi protocols, NFT data, and advanced crypto metrics from CoinGecko API
"""

import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class CoinGeckoDeFiTool(MCPTool):
    def __init__(self):
        super().__init__()
        self._name = "coingecko_defi"
        self._description = "Access DeFi protocols, NFT data, and advanced crypto metrics from CoinGecko API"
        self.base_url = "https://api.coingecko.com/api/v3"
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
                        "get_defi_protocols",
                        "get_defi_tvl",
                        "get_defi_protocol_tvl",
                        "get_defi_yield_pools",
                        "get_defi_lending_rates",
                        "get_defi_borrowing_rates",
                        "get_defi_volume",
                        "get_defi_fees",
                        "get_defi_revenue",
                        "get_nft_collections",
                        "get_nft_collection_by_id",
                        "get_nft_floor_price",
                        "get_nft_volume",
                        "get_nft_sales",
                        "get_nft_holders",
                        "get_nft_market_cap",
                        "get_derivatives",
                        "get_derivative_by_id",
                        "get_derivatives_exchanges",
                        "get_derivatives_tickers",
                        "get_global_defi",
                        "get_defi_coins",
                        "get_defi_categories",
                        "get_defi_historical_tvl",
                        "get_defi_trending"
                    ],
                    "description": "The action to perform"
                },
                "protocol_id": {
                    "type": "string",
                    "description": "DeFi protocol ID (e.g., uniswap, compound, aave)"
                },
                "collection_id": {
                    "type": "string",
                    "description": "NFT collection ID (e.g., bored-ape-yacht-club, cryptopunks)"
                },
                "derivative_id": {
                    "type": "string",
                    "description": "Derivative ID (e.g., bitcoin, ethereum)"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days for historical data",
                    "default": 30
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 100
                },
                "page": {
                    "type": "integer",
                    "description": "Page number for pagination",
                    "default": 1
                },
                "api_key": {
                    "type": "string",
                    "description": "CoinGecko API key (optional, for higher rate limits)",
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
            if action == "get_defi_protocols":
                return await self._get_defi_protocols(arguments)
            elif action == "get_defi_tvl":
                return await self._get_defi_tvl(arguments)
            elif action == "get_defi_protocol_tvl":
                return await self._get_defi_protocol_tvl(arguments)
            elif action == "get_defi_yield_pools":
                return await self._get_defi_yield_pools(arguments)
            elif action == "get_defi_lending_rates":
                return await self._get_defi_lending_rates(arguments)
            elif action == "get_defi_borrowing_rates":
                return await self._get_defi_borrowing_rates(arguments)
            elif action == "get_defi_volume":
                return await self._get_defi_volume(arguments)
            elif action == "get_defi_fees":
                return await self._get_defi_fees(arguments)
            elif action == "get_defi_revenue":
                return await self._get_defi_revenue(arguments)
            elif action == "get_nft_collections":
                return await self._get_nft_collections(arguments)
            elif action == "get_nft_collection_by_id":
                return await self._get_nft_collection_by_id(arguments)
            elif action == "get_nft_floor_price":
                return await self._get_nft_floor_price(arguments)
            elif action == "get_nft_volume":
                return await self._get_nft_volume(arguments)
            elif action == "get_nft_sales":
                return await self._get_nft_sales(arguments)
            elif action == "get_nft_holders":
                return await self._get_nft_holders(arguments)
            elif action == "get_nft_market_cap":
                return await self._get_nft_market_cap(arguments)
            elif action == "get_derivatives":
                return await self._get_derivatives(arguments)
            elif action == "get_derivative_by_id":
                return await self._get_derivative_by_id(arguments)
            elif action == "get_derivatives_exchanges":
                return await self._get_derivatives_exchanges(arguments)
            elif action == "get_derivatives_tickers":
                return await self._get_derivatives_tickers(arguments)
            elif action == "get_global_defi":
                return await self._get_global_defi(arguments)
            elif action == "get_defi_coins":
                return await self._get_defi_coins(arguments)
            elif action == "get_defi_categories":
                return await self._get_defi_categories(arguments)
            elif action == "get_defi_historical_tvl":
                return await self._get_defi_historical_tvl(arguments)
            elif action == "get_defi_trending":
                return await self._get_defi_trending(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:
        """Make API request to CoinGecko"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        
        # Only use API key from frontend form input
        headers = {}
        if api_key and api_key.strip():
            headers["x-cg-demo-api-key"] = api_key
        
        try:
            async with session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"CoinGecko API request failed: {e}")
            return {"error": f"CoinGecko API request failed: {e}"}

    async def _get_defi_protocols(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi protocols"""
        api_key = arguments.get("api_key")
        try:
            data = await self._make_request("/global/decentralized_finance_defi", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Protocols:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi protocols: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi protocols: {str(e)}"}]

    async def _get_defi_tvl(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi TVL"""
        try:
            data = await self._make_request("/global/decentralized_finance_defi")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi TVL:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi TVL: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi TVL: {str(e)}"}]

    async def _get_defi_protocol_tvl(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get protocol-specific TVL"""
        protocol_id = arguments.get("protocol_id", "uniswap")
        days = arguments.get("days", 30)
        
        try:
            # Use coins/markets endpoint to get protocol data
            params = {
                "vs_currency": "usd",
                "category": "decentralized-finance-defi",
                "order": "market_cap_desc",
                "per_page": 100,
                "page": 1,
                "sparkline": "true",
                "price_change_percentage": "24h"
            }
            
            data = await self._make_request("/coins/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            # Filter for the specific protocol
            protocol_data = next((item for item in data if item.get("id") == protocol_id), None)
            if not protocol_data:
                return [{"type": "text", "text": f"❌ Protocol {protocol_id} not found"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko {protocol_id} TVL:\n\n{protocol_data}"}]
        except Exception as e:
            logger.error(f"Error fetching protocol TVL: {e}")
            return [{"type": "text", "text": f"❌ Error fetching protocol TVL: {str(e)}"}]

    async def _get_defi_yield_pools(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi yield pools"""
        try:
            # Use coins/markets endpoint with DeFi category
            params = {
                "vs_currency": "usd",
                "category": "decentralized-finance-defi",
                "order": "market_cap_desc",
                "per_page": 50,
                "page": 1
            }
            
            data = await self._make_request("/coins/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Yield Pools:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi yield pools: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi yield pools: {str(e)}"}]

    async def _get_defi_lending_rates(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi lending rates"""
        try:
            # Use coins/markets endpoint with DeFi category
            params = {
                "vs_currency": "usd",
                "category": "decentralized-finance-defi",
                "order": "market_cap_desc",
                "per_page": 50,
                "page": 1
            }
            
            data = await self._make_request("/coins/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Lending Rates:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi lending rates: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi lending rates: {str(e)}"}]

    async def _get_defi_borrowing_rates(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi borrowing rates"""
        try:
            # Use coins/markets endpoint with DeFi category
            params = {
                "vs_currency": "usd",
                "category": "decentralized-finance-defi",
                "order": "market_cap_desc",
                "per_page": 50,
                "page": 1
            }
            
            data = await self._make_request("/coins/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Borrowing Rates:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi borrowing rates: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi borrowing rates: {str(e)}"}]

    async def _get_defi_volume(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi volume"""
        try:
            data = await self._make_request("/global/decentralized_finance_defi")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Volume:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi volume: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi volume: {str(e)}"}]

    async def _get_defi_fees(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi fees"""
        try:
            data = await self._make_request("/global/decentralized_finance_defi")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Fees:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi fees: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi fees: {str(e)}"}]

    async def _get_defi_revenue(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi revenue"""
        try:
            data = await self._make_request("/global/decentralized_finance_defi")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Revenue:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi revenue: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi revenue: {str(e)}"}]

    async def _get_nft_collections(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT collections"""
        api_key = arguments.get("api_key")
        try:
            data = await self._make_request("/nfts/list", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Collections:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT collections: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT collections: {str(e)}"}]

    async def _get_nft_collection_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT collection by ID"""
        collection_id = arguments.get("collection_id", "bored-ape-yacht-club")
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request(f"/nfts/{collection_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Collection {collection_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT collection: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT collection: {str(e)}"}]

    async def _get_nft_floor_price(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT floor price"""
        collection_id = arguments.get("collection_id", "bored-ape-yacht-club")
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request(f"/nfts/{collection_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Floor Price for {collection_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT floor price: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT floor price: {str(e)}"}]

    async def _get_nft_volume(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT volume"""
        collection_id = arguments.get("collection_id", "bored-ape-yacht-club")
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request(f"/nfts/{collection_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Volume for {collection_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT volume: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT volume: {str(e)}"}]

    async def _get_nft_sales(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT sales"""
        collection_id = arguments.get("collection_id", "bored-ape-yacht-club")
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request(f"/nfts/{collection_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Sales for {collection_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT sales: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT sales: {str(e)}"}]

    async def _get_nft_holders(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT holders"""
        collection_id = arguments.get("collection_id", "bored-ape-yacht-club")
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request(f"/nfts/{collection_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Holders for {collection_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT holders: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT holders: {str(e)}"}]

    async def _get_nft_market_cap(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get NFT market cap"""
        collection_id = arguments.get("collection_id", "bored-ape-yacht-club")
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request(f"/nfts/{collection_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko NFT Market Cap for {collection_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching NFT market cap: {e}")
            return [{"type": "text", "text": f"❌ Error fetching NFT market cap: {str(e)}"}]

    async def _get_derivatives(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get derivatives"""
        try:
            data = await self._make_request("/derivatives")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko Derivatives:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching derivatives: {e}")
            return [{"type": "text", "text": f"❌ Error fetching derivatives: {str(e)}"}]

    async def _get_derivative_by_id(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get derivative by ID"""
        derivative_id = arguments.get("derivative_id", "bitcoin")
        
        try:
            data = await self._make_request(f"/derivatives/{derivative_id}")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko Derivative {derivative_id}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching derivative: {e}")
            return [{"type": "text", "text": f"❌ Error fetching derivative: {str(e)}"}]

    async def _get_derivatives_exchanges(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get derivatives exchanges"""
        try:
            data = await self._make_request("/derivatives/exchanges")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko Derivatives Exchanges:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching derivatives exchanges: {e}")
            return [{"type": "text", "text": f"❌ Error fetching derivatives exchanges: {str(e)}"}]

    async def _get_derivatives_tickers(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get derivatives tickers"""
        try:
            data = await self._make_request("/derivatives/tickers")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko Derivatives Tickers:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching derivatives tickers: {e}")
            return [{"type": "text", "text": f"❌ Error fetching derivatives tickers: {str(e)}"}]

    async def _get_global_defi(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get global DeFi data"""
        try:
            data = await self._make_request("/global/decentralized_finance_defi")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko Global DeFi:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching global DeFi: {e}")
            return [{"type": "text", "text": f"❌ Error fetching global DeFi: {str(e)}"}]

    async def _get_defi_coins(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi coins"""
        try:
            params = {
                "vs_currency": "usd",
                "category": "decentralized-finance-defi",
                "order": "market_cap_desc",
                "per_page": 100,
                "page": 1
            }
            
            data = await self._make_request("/coins/markets", params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Coins:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi coins: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi coins: {str(e)}"}]

    async def _get_defi_categories(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi categories"""
        try:
            data = await self._make_request("/coins/categories")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Categories:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi categories: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi categories: {str(e)}"}]

    async def _get_defi_historical_tvl(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi historical TVL"""
        days = arguments.get("days", 30)
        
        try:
            data = await self._make_request("/global/decentralized_finance_defi")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Historical TVL ({days} days):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi historical TVL: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi historical TVL: {str(e)}"}]

    async def _get_defi_trending(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get DeFi trending"""
        try:
            data = await self._make_request("/search/trending")
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ CoinGecko DeFi Trending:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching DeFi trending: {e}")
            return [{"type": "text", "text": f"❌ Error fetching DeFi trending: {str(e)}"}]