"""
Tool Configuration
Defines all 29 MCP tools with their parameters, validation rules, and schemas
"""

from typing import Dict, Any, List

# Tool configurations with required parameters and schemas
TOOL_CONFIGS = {
    # Search and Web Tools
    "duckduckgo_search": {
        "required_params": ["query"],
        "schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "description": "Maximum results to return", "default": 5},
                "region": {"type": "string", "description": "Search region", "default": "us-en"},
                "time": {"type": "string", "description": "Time filter", "default": ""},
                "search_type": {"type": "string", "description": "Type of search", "default": "text"}
            }
        }
    },
    
    "web_search": {
        "required_params": ["query"],
        "schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "search_type": {"type": "string", "description": "Type of search", "default": "text"},
                "max_results": {"type": "integer", "description": "Maximum results to return", "default": 5},
                "region": {"type": "string", "description": "Search region", "default": "us-en"}
            }
        }
    },
    
    # Crypto Tools
    "crypto_price": {
        "required_params": ["coin_id"],
        "schema": {
            "type": "object",
            "properties": {
                "coin_id": {"type": "string", "description": "CoinGecko coin ID (e.g., 'bitcoin', 'ethereum')"},
                "currency": {"type": "string", "description": "Target currency", "default": "usd"},
                "include_market_data": {"type": "boolean", "description": "Include market data", "default": True}
            }
        }
    },
    
    "crypto_news": {
        "required_params": ["query"],
        "schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query for news"},
                "max_results": {"type": "integer", "description": "Maximum news articles", "default": 5},
                "time_filter": {"type": "string", "description": "Time filter (d=day, w=week, m=month)", "default": "d"},
                "include_sentiment": {"type": "boolean", "description": "Include sentiment analysis", "default": True}
            }
        }
    },
    
    "market_analysis": {
        "required_params": ["coin_id", "analysis_type"],
        "schema": {
            "type": "object",
            "properties": {
                "coin_id": {"type": "string", "description": "Coin ID for analysis"},
                "analysis_type": {"type": "string", "description": "Type of analysis", "enum": ["technical_indicators", "market_sentiment", "trend_analysis", "volatility"]},
                "timeframe": {"type": "string", "description": "Analysis timeframe", "default": "7d"},
                "include_charts": {"type": "boolean", "description": "Include chart data", "default": False}
            }
        }
    },
    
    "portfolio_tracker": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["create", "add_asset", "get_value", "get_analysis"]},
                "portfolio_id": {"type": "string", "description": "Portfolio identifier"},
                "name": {"type": "string", "description": "Portfolio name (for create action)"},
                "coin_id": {"type": "string", "description": "Coin ID to add (for add_asset action)"},
                "amount": {"type": "number", "description": "Amount of coin (for add_asset action)"},
                "purchase_price": {"type": "number", "description": "Purchase price per coin (for add_asset action)"}
            }
        }
    },
    
    # DeFi Tools
    "defi_protocol": {
        "required_params": ["protocol"],
        "schema": {
            "type": "object",
            "properties": {
                "protocol": {"type": "string", "description": "DeFi protocol name", "enum": ["uniswap", "aave", "compound", "curve", "balancer"]},
                "action": {"type": "string", "description": "Action to perform", "enum": ["tvl", "pools", "apy", "yield_farming"], "default": "tvl"},
                "chain": {"type": "string", "description": "Blockchain network", "default": "ethereum"}
            }
        }
    },
    
    "aave": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_pool_data", "get_user_data", "get_reserves"]},
                "network": {"type": "string", "description": "Network", "default": "ethereum"},
                "pool_address": {"type": "string", "description": "Pool address (optional)"}
            }
        }
    },
    
    "apy_calculator": {
        "required_params": ["calculation_type"],
        "schema": {
            "type": "object",
            "properties": {
                "calculation_type": {"type": "string", "description": "Type of calculation", "enum": ["liquidity_pool", "yield_farming", "staking"]},
                "principal": {"type": "number", "description": "Principal amount", "default": 1000},
                "rate": {"type": "number", "description": "Annual interest rate", "default": 0.05},
                "time_period": {"type": "number", "description": "Time period in years", "default": 1},
                "compounding_frequency": {"type": "string", "description": "Compounding frequency", "default": "daily"}
            }
        }
    },
    
    # Solana Tools
    "jupiter": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_quote", "get_tokens", "get_routes"]},
                "input_mint": {"type": "string", "description": "Input token mint address"},
                "output_mint": {"type": "string", "description": "Output token mint address"},
                "amount": {"type": "string", "description": "Amount in lamports"}
            }
        }
    },
    
    "raydium": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_pools", "get_tokens", "get_quote"]},
                "token": {"type": "string", "description": "Token address or symbol"}
            }
        }
    },
    
    # NFT Tools
    "nft_marketplace": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["collection_info", "floor_price", "trading_volume", "recent_sales"]},
                "collection_slug": {"type": "string", "description": "Collection identifier"},
                "chain": {"type": "string", "description": "Blockchain network", "default": "ethereum"},
                "limit": {"type": "integer", "description": "Number of results", "default": 10}
            }
        }
    },
    
    # Analytics Tools
    "lunarcrush": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_coin_metrics", "get_influence_score", "get_social_metrics"]},
                "symbol": {"type": "string", "description": "Cryptocurrency symbol"},
                "timeframe": {"type": "string", "description": "Timeframe for data", "default": "24h"}
            }
        }
    },
    
    "coindesk": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_market_data", "get_news", "get_price_index"]},
                "asset": {"type": "string", "description": "Asset identifier"},
                "currency": {"type": "string", "description": "Currency", "default": "USD"}
            }
        }
    },
    
    "pumpnews": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_latest_news", "search_news", "get_trending"]},
                "limit": {"type": "integer", "description": "Number of news items", "default": 10},
                "category": {"type": "string", "description": "News category", "default": "all"}
            }
        }
    },
    
    "pumpfun": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_token_info", "get_market_data", "get_social_metrics"]},
                "token_address": {"type": "string", "description": "Token contract address"},
                "network": {"type": "string", "description": "Blockchain network", "default": "ethereum"}
            }
        }
    },
    
    "gmgn": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_gaming_data", "get_nft_collections", "get_market_stats"]},
                "game": {"type": "string", "description": "Game identifier"},
                "category": {"type": "string", "description": "Data category", "default": "all"}
            }
        }
    },
    
    "merkl": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_campaigns", "get_rewards", "get_user_data"]},
                "network": {"type": "string", "description": "Blockchain network", "default": "ethereum"},
                "user_address": {"type": "string", "description": "User wallet address (optional)"}
            }
        }
    },
    
    # Social Media Tools
    "youtube": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_videos", "get_channel_info", "get_video_stats"]},
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 10},
                "channel_id": {"type": "string", "description": "YouTube channel ID (optional)"}
            }
        }
    },
    
    "twitter": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_tweets", "get_user_info", "get_trending"]},
                "query": {"type": "string", "description": "Search query"},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 10},
                "username": {"type": "string", "description": "Twitter username (optional)"}
            }
        }
    },
    
    "reddit": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_posts", "get_subreddit_info", "get_hot_posts"]},
                "subreddit": {"type": "string", "description": "Subreddit name"},
                "query": {"type": "string", "description": "Search query"},
                "limit": {"type": "integer", "description": "Number of posts", "default": 10}
            }
        }
    },
    
    # Communication Tools
    "gmail": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["list_messages", "send_message", "get_message"]},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 10},
                "query": {"type": "string", "description": "Search query (optional)"},
                "label": {"type": "string", "description": "Gmail label (optional)"}
            }
        }
    },
    
    "google_calendar": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["list_events", "create_event", "get_event"]},
                "time_min": {"type": "string", "description": "Start time (ISO format)", "default": "now"},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 10},
                "calendar_id": {"type": "string", "description": "Calendar ID (optional)"}
            }
        }
    },
    
    "slack": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["list_channels", "send_message", "get_messages"]},
                "workspace": {"type": "string", "description": "Slack workspace"},
                "channel": {"type": "string", "description": "Channel name (optional)"},
                "message": {"type": "string", "description": "Message text (for send_message)"}
            }
        }
    },
    
    # Utility Tools
    "openweather": {
        "required_params": ["city"],
        "schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
                "country_code": {"type": "string", "description": "Country code", "default": "US"},
                "units": {"type": "string", "description": "Temperature units", "enum": ["metric", "imperial"], "default": "metric"}
            }
        }
    },
    
    "googlemaps": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["geocode", "reverse_geocode", "get_directions"]},
                "address": {"type": "string", "description": "Address or coordinates"},
                "destination": {"type": "string", "description": "Destination (for directions)"}
            }
        }
    },
    
    "jira": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_issues", "create_issue", "update_issue"]},
                "project": {"type": "string", "description": "Jira project key"},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 10},
                "issue_key": {"type": "string", "description": "Issue key (for update_issue)"}
            }
        }
    },
    
    "currency_converter": {
        "required_params": ["from_currency", "to_currency"],
        "schema": {
            "type": "object",
            "properties": {
                "from_currency": {"type": "string", "description": "Source currency code"},
                "to_currency": {"type": "string", "description": "Target currency code"},
                "amount": {"type": "number", "description": "Amount to convert", "default": 1}
            }
        }
    },
    
    "notification": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["create_alert", "list_alerts", "test_alert"]},
                "alert_type": {"type": "string", "description": "Type of alert", "enum": ["price_alert", "news_alert"]},
                "alert_id": {"type": "string", "description": "Alert identifier"},
                "message": {"type": "string", "description": "Alert message"}
            }
        }
    }
}

def get_tool_config(tool_name: str) -> Dict[str, Any]:
    """Get configuration for a specific tool"""
    return TOOL_CONFIGS.get(tool_name, {})

def get_all_tool_names() -> List[str]:
    """Get list of all available tool names"""
    return list(TOOL_CONFIGS.keys())

def get_tool_required_params(tool_name: str) -> List[str]:
    """Get required parameters for a specific tool"""
    config = get_tool_config(tool_name)
    return config.get("required_params", [])

def get_tool_schema(tool_name: str) -> Dict[str, Any]:
    """Get schema for a specific tool"""
    config = get_tool_config(tool_name)
    return config.get("schema", {})
