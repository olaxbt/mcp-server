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
