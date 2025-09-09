"""
Main MCP Tools Module
Imports and makes available all tools from the tools directory
"""

# Import all tools from the tools directory
from .tools.search_tools import DuckDuckGoSearchTool, WebSearchTool
from .tools.crypto_tools import CryptoPriceTool, DeFiProtocolTool, PortfolioTrackerTool, CryptoNewsTool, APYCalculatorTool
from .tools.nft_tools import NFTMarketplaceTool
from .tools.market_analysis_tools import MarketAnalysisTool
from .tools.solana_tools import JupiterTool, RaydiumTool
from .tools.defi_tools import AaveTool
from .tools.currency_tools import CurrencyConverterTool
from .tools.analytics_tools import LunarCrushTool, CoinDeskTool, PumpNewsTool, PumpFunTool, GMGNTool, MerklTool
from .tools.social_tools import YouTubeTool, TwitterTool, RedditTool
from .tools.utility_tools import OpenWeatherTool, GoogleMapsTool, JiraTool
from .tools.metasleuth_wallet_tool import MetaSleuthWalletTool
from .tools.chainbase_balance_tool import ChainBaseBalanceTool
from .tools.dune_tools import DuneQueryTool

# Export all tools for easy importing
__all__ = [
    # Search and Web
    "DuckDuckGoSearchTool",
    "WebSearchTool",
    
    # Crypto and DeFi
    "CryptoPriceTool",
    "DeFiProtocolTool",
    "PortfolioTrackerTool",
    "CryptoNewsTool",
    "NFTMarketplaceTool",
    "MarketAnalysisTool",
    "APYCalculatorTool",
    
    # Solana Ecosystem
    "JupiterTool",
    "RaydiumTool",
    
    # DeFi
    "AaveTool",
    
    # Currency
    "CurrencyConverterTool",
    
    # Data Analytics
    "LunarCrushTool",
    "CoinDeskTool",
    "PumpNewsTool",
    "PumpFunTool",
    "GMGNTool",
    "MerklTool",
    
    # Social Media
    "YouTubeTool",
    "TwitterTool",
    "RedditTool",
    
    
    # Utility
    "OpenWeatherTool",
    "GoogleMapsTool",
    "JiraTool",
    
    # Wallet Analytics
    "MetaSleuthWalletTool",
    "ChainBaseBalanceTool",
    
    # Blockchain Data
    "DuneQueryTool"
]

