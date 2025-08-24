import os
from typing import Dict, Any, List

# Default service configurations
DEFAULT_SERVICES = {
    "meteora": {
        "name": "Meteora DeFi",
        "description": "DeFi protocol for liquidity pools and swaps",
        "url": "http://localhost:3001",
        "tools": ["meteora_pools", "meteora_swap_quote", "meteora_pool_info"],
        "metadata": {"category": "defi", "chain": "solana"},
        "enabled": True
    },
    "gmgn": {
        "name": "GMGN Gaming",
        "description": "Gaming and NFT platform",
        "url": "http://localhost:3002",
        "tools": ["gmgn_games", "gmgn_nft_collection", "gmgn_user_profile", "gmgn_game_leaderboard"],
        "metadata": {"category": "gaming", "type": "nft_platform"},
        "enabled": True
    },
    "example_service": {
        "name": "Example Service",
        "description": "Template for new services",
        "url": "http://localhost:3003",
        "tools": ["example_tool"],
        "metadata": {"category": "template", "type": "example"},
        "enabled": False
    }
}

# Service categories for organization
SERVICE_CATEGORIES = {
    "defi": ["meteora", "raydium", "orca", "serum"],
    "gaming": ["gmgn", "star_atlas", "aurory", "illuvium"],
    "nft": ["opensea", "magiceden", "solanart", "tensor"],
    "analytics": ["birdeye", "dexscreener", "coingecko", "coinmarketcap"],
    "social": ["twitter", "discord", "telegram", "reddit"],
    "tools": ["duckduckgo_search", "web_search", "calculator", "converter"]
}

def get_service_config(service_id: str) -> Dict[str, Any]:
    """Get configuration for a specific service"""
    return DEFAULT_SERVICES.get(service_id, {})

def get_enabled_services() -> List[str]:
    """Get list of enabled service IDs"""
    return [sid for sid, config in DEFAULT_SERVICES.items() if config.get("enabled", False)]

def get_services_by_category(category: str) -> List[str]:
    """Get services in a specific category"""
    return SERVICE_CATEGORIES.get(category, [])

def get_all_categories() -> List[str]:
    """Get all available service categories"""
    return list(SERVICE_CATEGORIES.keys())

def add_service(service_id: str, config: Dict[str, Any]) -> bool:
    """Add a new service configuration"""
    try:
        DEFAULT_SERVICES[service_id] = config
        return True
    except Exception:
        return False

def remove_service(service_id: str) -> bool:
    """Remove a service configuration"""
    try:
        if service_id in DEFAULT_SERVICES:
            del DEFAULT_SERVICES[service_id]
            return True
        return False
    except Exception:
        return False

def update_service(service_id: str, config: Dict[str, Any]) -> bool:
    """Update an existing service configuration"""
    try:
        if service_id in DEFAULT_SERVICES:
            DEFAULT_SERVICES[service_id].update(config)
            return True
        return False
    except Exception:
        return False
