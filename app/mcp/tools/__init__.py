"""
MCP Tools Package
Contains all tool implementations organized by category
"""

# Search and Web Tools
from .search_tools import (
    DuckDuckGoSearchTool,
    WebSearchTool
)

# Crypto and DeFi Tools
from .crypto_tools import (
    CryptoPriceTool,
    DeFiProtocolTool,
    PortfolioTrackerTool,
    CryptoNewsTool,
    APYCalculatorTool
)

# NFT Tools
from .nft_tools import (
    NFTMarketplaceTool
)

# Market Analysis Tools
from .market_analysis_tools import (
    MarketAnalysisTool
)

# Solana Ecosystem Tools
from .solana_tools import (
    JupiterTool,
    RaydiumTool
)

# DeFi Tools
from .defi_tools import (
    AaveTool
)

# Currency Tools
from .currency_tools import (
    CurrencyConverterTool
)

# Data Analytics Tools
from .analytics_tools import (
    LunarCrushTool,
    CoinDeskTool,
    PumpNewsTool,
    PumpFunTool,
    GMGNTool,
    MerklTool
)

# Social Media Tools
from .social_tools import (
    YouTubeTool,
    TwitterTool,
    RedditTool
)

# Communication Tools
from .communication_tools import (
    GmailTool,
    GoogleCalendarTool,
    SlackTool
)

# Utility Tools
from .utility_tools import (
    OpenWeatherTool,
    GoogleMapsTool,
    JiraTool,
    NotificationTool
)

# New MCP Tools
from .dune_tools import DuneQueryTool
from .meteora_tools import MeteoraTool
from .pendle_tools import PendleTool
from .defi_tools_extended import (
    DefiLlamaTool,
    DeribitTool,
    ChainbaseTokenMetadataTool,
    ChainbaseTokenTopHoldersTool,
    ChainbaseTokenHoldersTool,
    ChainbaseTokenPriceTool,
    ChainbaseTokenPriceHistoryTool
)
from .chainbase_nft_tool import ChainbaseNFTTool
from .additional_tools import (
    PumpFunDataTool,
    CoinDeskAssetsTool,
    BNBChainTool,
    ChainbaseBasicTool
)

# DeFi and Trading Tools
from .defi_trading_tools import (
    CoinGeckoTool,
    EtherscanTool,
    BinanceTool,
    UniswapTool,
    ChainlinkTool
)





# Real Wallet Data Tools
from .chainbase_balance_tool import ChainBaseBalanceTool
from .metasleuth_wallet_tool import MetaSleuthWalletTool

# Business Intelligence Tools
from .apollo_tool import ApolloTool

# Export all tools for easy importing
__all__ = [
    # Search and Web
    "DuckDuckGoSearchTool",
    "WebSearchTool",
    
    # Crypto Tools
    "CryptoPriceTool",
    "CryptoNewsTool",
    
    # DeFi Tools
    "DeFiProtocolTool",
    "PortfolioTrackerTool",
    "AaveTool",
    "APYCalculatorTool",
    "JupiterTool",
    "RaydiumTool",
    
    # NFT Tools
    "NFTMarketplaceTool",
    
    # Analytics Tools
    "MarketAnalysisTool",
    "LunarCrushTool",
    "CoinDeskTool",
    "PumpNewsTool",
    "PumpFunTool",
    "GMGNTool",
    "MerklTool",
    
    # Social Tools
    "YouTubeTool",
    "TwitterTool",
    "RedditTool",
    "GmailTool",
    "GoogleCalendarTool",
    "SlackTool",
    
    # Utility Tools
    "OpenWeatherTool",
    "GoogleMapsTool",
    "JiraTool",
    "NotificationTool",
    
    # New MCP Tools
    "DuneQueryTool",
    "MeteoraTool",
    "PendleTool",
    "DefiLlamaTool",
    "DeribitTool",
    "ChainbaseTokenMetadataTool",
    "ChainbaseTokenTopHoldersTool",
    "ChainbaseTokenHoldersTool",
    "ChainbaseTokenPriceTool",
    "ChainbaseTokenPriceHistoryTool",
    "ChainbaseNFTTool",
    "PumpFunDataTool",
    "CoinDeskAssetsTool",
    "BNBChainTool",
    "ChainbaseBasicTool",
    
    # DeFi and Trading Tools
    "CoinGeckoTool",
    "EtherscanTool",
    "BinanceTool",
    "UniswapTool",
    "ChainlinkTool",
    




# Real Wallet Data Tools
"ChainBaseBalanceTool",
"MetaSleuthWalletTool",

# Business Intelligence Tools
"ApolloTool"
]
