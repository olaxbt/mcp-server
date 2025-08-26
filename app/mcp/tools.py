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
from .tools.communication_tools import GmailTool, GoogleCalendarTool, SlackTool
from .tools.utility_tools import OpenWeatherTool, GoogleMapsTool, JiraTool, NotificationTool

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
    
    # Communication
    "GmailTool",
    "GoogleCalendarTool",
    "SlackTool",
    
    # Utility
    "OpenWeatherTool",
    "GoogleMapsTool",
    "JiraTool",
    "NotificationTool"
]

