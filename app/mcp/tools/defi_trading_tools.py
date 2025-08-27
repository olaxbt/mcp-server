import os
import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class CoinGeckoTool(MCPTool):
    """Tool for accessing CoinGecko cryptocurrency data"""
    
    @property
    def name(self) -> str:
        return "coingecko"
    
    @property
    def description(self) -> str:
        return "Access comprehensive cryptocurrency data from CoinGecko including prices, market data, and trends."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_coin_price", "get_market_data", "get_trending", "get_exchange_rates", "get_coin_info"]
                },
                "coin_id": {"type": "string", "description": "Coin ID (e.g., 'bitcoin', 'ethereum')"},
                "vs_currency": {"type": "string", "description": "Target currency", "default": "usd"},
                "days": {"type": "string", "description": "Number of days for historical data", "default": "1"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the CoinGecko tool"""
        try:
            action = arguments.get("action")
            
            if action == "get_coin_price":
                return await self._get_coin_price(arguments)
            elif action == "get_market_data":
                return await self._get_market_data(arguments)
            elif action == "get_trending":
                return await self._get_trending(arguments)
            elif action == "get_exchange_rates":
                return await self._get_exchange_rates(arguments)
            elif action == "get_coin_info":
                return await self._get_coin_info(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in CoinGecko tool: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_coin_price(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get coin price data"""
        coin_id = arguments.get("coin_id", "bitcoin")
        vs_currency = arguments.get("vs_currency", "usd")
        days = arguments.get("days", "1")
        
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        params = {"vs_currency": vs_currency, "days": days}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ CoinGecko price data for {coin_id}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get price data: {response.status}"}]
    
    async def _get_market_data(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get market data"""
        limit = arguments.get("limit", 10)
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ CoinGecko market data: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get market data: {response.status}"}]
    
    async def _get_trending(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get trending coins"""
        url = "https://api.coingecko.com/api/v3/search/trending"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ CoinGecko trending coins: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get trending data: {response.status}"}]
    
    async def _get_exchange_rates(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange rates"""
        url = "https://api.coingecko.com/api/v3/exchange_rates"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ CoinGecko exchange rates: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get exchange rates: {response.status}"}]
    
    async def _get_coin_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get detailed coin information"""
        coin_id = arguments.get("coin_id", "bitcoin")
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ CoinGecko coin info for {coin_id}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get coin info: {response.status}"}]


class EtherscanTool(MCPTool):
    """Tool for accessing Ethereum blockchain data via Etherscan"""
    
    @property
    def name(self) -> str:
        return "etherscan"
    
    @property
    def description(self) -> str:
        return "Access Ethereum blockchain data including transactions, balances, and contract information."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_balance", "get_transactions", "get_contract_info", "get_gas_price", "get_block_info"]
                },
                "address": {"type": "string", "description": "Ethereum address"},
                "start_block": {"type": "string", "description": "Starting block number"},
                "end_block": {"type": "string", "description": "Ending block number"},
                "block_number": {"type": "string", "description": "Block number"}
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Etherscan tool"""
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Etherscan API key is required. Please provide your API key."}]
            
            if action == "get_balance":
                return await self._get_balance(arguments, api_key)
            elif action == "get_transactions":
                return await self._get_transactions(arguments, api_key)
            elif action == "get_contract_info":
                return await self._get_contract_info(arguments, api_key)
            elif action == "get_gas_price":
                return await self._get_gas_price(api_key)
            elif action == "get_block_info":
                return await self._get_block_info(arguments, api_key)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in Etherscan tool: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_balance(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Get account balance"""
        address = arguments.get("address")
        if not address:
            return [{"type": "text", "text": "❌ Address is required for balance check"}]
        
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "balance",
            "address": address,
            "tag": "latest",
            "apikey": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Etherscan balance for {address}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get balance: {response.status}"}]
    
    async def _get_transactions(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Get account transactions"""
        address = arguments.get("address")
        if not address:
            return [{"type": "text", "text": "❌ Address is required for transaction history"}]
        
        url = "https://api.etherscan.io/api"
        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "startblock": arguments.get("start_block", "0"),
            "endblock": arguments.get("end_block", "99999999"),
            "sort": "desc",
            "apikey": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Etherscan transactions for {address}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get transactions: {response.status}"}]
    
    async def _get_contract_info(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Get contract information"""
        address = arguments.get("address")
        if not address:
            return [{"type": "text", "text": "❌ Contract address is required"}]
        
        url = "https://api.etherscan.io/api"
        params = {
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Etherscan contract info for {address}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get contract info: {response.status}"}]
    
    async def _get_gas_price(self, api_key: str) -> List[Dict[str, Any]]:
        """Get current gas price"""
        url = "https://api.etherscan.io/api"
        params = {
            "module": "gastracker",
            "action": "gasoracle",
            "apikey": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Etherscan gas price: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get gas price: {response.status}"}]
    
    async def _get_block_info(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Get block information"""
        block_number = arguments.get("block_number", "latest")
        
        url = "https://api.etherscan.io/api"
        params = {
            "module": "proxy",
            "action": "eth_getBlockByNumber",
            "tag": block_number,
            "boolean": "false",
            "apikey": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Etherscan block info for {block_number}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get block info: {response.status}"}]


class BinanceTool(MCPTool):
    """Tool for accessing Binance exchange data"""
    
    @property
    def name(self) -> str:
        return "binance"
    
    @property
    def description(self) -> str:
        return "Access Binance exchange data including prices, order books, and trading information."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_price", "get_orderbook", "get_24hr_stats", "get_recent_trades", "get_exchange_info"]
                },
                "symbol": {"type": "string", "description": "Trading pair symbol (e.g., 'BTCUSDT')"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Binance tool"""
        try:
            action = arguments.get("action")
            
            if action == "get_price":
                return await self._get_price(arguments)
            elif action == "get_orderbook":
                return await self._get_orderbook(arguments)
            elif action == "get_24hr_stats":
                return await self._get_24hr_stats(arguments)
            elif action == "get_recent_trades":
                return await self._get_recent_trades(arguments)
            elif action == "get_exchange_info":
                return await self._get_exchange_info()
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in Binance tool: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_price(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get current price for a symbol"""
        symbol = arguments.get("symbol", "BTCUSDT")
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Binance price for {symbol}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get price: {response.status}"}]
    
    async def _get_orderbook(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get order book for a symbol"""
        symbol = arguments.get("symbol", "BTCUSDT")
        limit = arguments.get("limit", 10)
        url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit={limit}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Binance orderbook for {symbol}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get orderbook: {response.status}"}]
    
    async def _get_24hr_stats(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get 24hr statistics for a symbol"""
        symbol = arguments.get("symbol", "BTCUSDT")
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Binance 24hr stats for {symbol}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get 24hr stats: {response.status}"}]
    
    async def _get_recent_trades(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recent trades for a symbol"""
        symbol = arguments.get("symbol", "BTCUSDT")
        limit = arguments.get("limit", 10)
        url = f"https://api.binance.com/api/v3/trades?symbol={symbol}&limit={limit}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Binance recent trades for {symbol}: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get recent trades: {response.status}"}]
    
    async def _get_exchange_info(self) -> List[Dict[str, Any]]:
        """Get exchange information"""
        url = "https://api.binance.com/api/v3/exchangeInfo"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Binance exchange info: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get exchange info: {response.status}"}]


class UniswapTool(MCPTool):
    """Tool for accessing Uniswap DEX data"""
    
    @property
    def name(self) -> str:
        return "uniswap"
    
    @property
    def description(self) -> str:
        return "Access Uniswap DEX data including pools, swaps, and liquidity information."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_pools", "get_pool_info", "get_token_info", "get_swaps", "get_liquidity"]
                },
                "pool_address": {"type": "string", "description": "Pool contract address"},
                "token_address": {"type": "string", "description": "Token contract address"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Uniswap tool"""
        try:
            action = arguments.get("action")
            
            if action == "get_pools":
                return await self._get_pools(arguments)
            elif action == "get_pool_info":
                return await self._get_pool_info(arguments)
            elif action == "get_token_info":
                return await self._get_token_info(arguments)
            elif action == "get_swaps":
                return await self._get_swaps(arguments)
            elif action == "get_liquidity":
                return await self._get_liquidity(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in Uniswap tool: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_pools(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get Uniswap pools"""
        limit = arguments.get("limit", 10)
        # Using The Graph API for Uniswap data
        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        query = """
        {
          pools(first: %d, orderBy: totalValueLockedUSD, orderDirection: desc) {
            id
            token0Price
            token1Price
            totalValueLockedUSD
            volumeUSD
          }
        }
        """ % limit
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"query": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Uniswap pools: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get pools: {response.status}"}]
    
    async def _get_pool_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get specific pool information"""
        pool_address = arguments.get("pool_address")
        if not pool_address:
            return [{"type": "text", "text": "❌ Pool address is required"}]
        
        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        query = """
        {
          pool(id: "%s") {
            id
            token0Price
            token1Price
            totalValueLockedUSD
            volumeUSD
            feeTier
          }
        }
        """ % pool_address
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"query": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Uniswap pool info: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get pool info: {response.status}"}]
    
    async def _get_token_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get token information"""
        token_address = arguments.get("token_address")
        if not token_address:
            return [{"type": "text", "text": "❌ Token address is required"}]
        
        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        query = """
        {
          token(id: "%s") {
            id
            symbol
            name
            totalValueLockedUSD
            volumeUSD
          }
        }
        """ % token_address
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"query": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Uniswap token info: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get token info: {response.status}"}]
    
    async def _get_swaps(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recent swaps"""
        limit = arguments.get("limit", 10)
        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        query = """
        {
          swaps(first: %d, orderBy: timestamp, orderDirection: desc) {
            id
            timestamp
            pool {
              id
            }
            amountUSD
          }
        }
        """ % limit
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"query": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Uniswap swaps: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get swaps: {response.status}"}]
    
    async def _get_liquidity(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get liquidity information"""
        limit = arguments.get("limit", 10)
        url = "https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v3"
        query = """
        {
          pools(first: %d, orderBy: totalValueLockedUSD, orderDirection: desc) {
            id
            totalValueLockedUSD
            totalValueLockedToken0
            totalValueLockedToken1
          }
        }
        """ % limit
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json={"query": query}) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Uniswap liquidity: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get liquidity: {response.status}"}]


class ChainlinkTool(MCPTool):
    """Tool for accessing Chainlink oracle data"""
    
    @property
    def name(self) -> str:
        return "chainlink"
    
    @property
    def description(self) -> str:
        return "Access Chainlink oracle data including price feeds and network information."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_price_feed", "get_network_info", "get_node_info", "get_job_info"]
                },
                "feed_address": {"type": "string", "description": "Price feed contract address"},
                "network": {"type": "string", "description": "Network name", "default": "ethereum"}
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Chainlink tool"""
        try:
            action = arguments.get("action")
            
            if action == "get_price_feed":
                return await self._get_price_feed(arguments)
            elif action == "get_network_info":
                return await self._get_network_info(arguments)
            elif action == "get_node_info":
                return await self._get_node_info(arguments)
            elif action == "get_job_info":
                return await self._get_job_info(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in Chainlink tool: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_price_feed(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get price feed data"""
        feed_address = arguments.get("feed_address")
        if not feed_address:
            return [{"type": "text", "text": "❌ Feed address is required"}]
        
        # Using Chainlink's public API
        url = f"https://api.chain.link/v1/price-feeds/{feed_address}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Chainlink price feed: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get price feed: {response.status}"}]
    
    async def _get_network_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get network information"""
        network = arguments.get("network", "ethereum")
        url = f"https://api.chain.link/v1/networks/{network}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Chainlink network info: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get network info: {response.status}"}]
    
    async def _get_node_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get node information"""
        url = "https://api.chain.link/v1/nodes"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Chainlink nodes: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get node info: {response.status}"}]
    
    async def _get_job_info(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get job information"""
        url = "https://api.chain.link/v1/jobs"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"type": "text", "text": f"✅ Chainlink jobs: {data}"}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get job info: {response.status}"}]
