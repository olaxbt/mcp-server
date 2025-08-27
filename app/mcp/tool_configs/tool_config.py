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
        "required_params": ["action", "opensea_api_key", "reservoir_api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["collection_info", "floor_price", "trading_volume", "recent_sales"]},
                "opensea_api_key": {"type": "string", "description": "OpenSea API key (required for Ethereum/Polygon)"},
                "reservoir_api_key": {"type": "string", "description": "Reservoir API key (required for Ethereum/Polygon)"},
                "collection_slug": {"type": "string", "description": "Collection identifier"},
                "chain": {"type": "string", "description": "Blockchain network", "default": "ethereum"},
                "limit": {"type": "integer", "description": "Number of results", "default": 10}
            }
        }
    },
    
    # Analytics Tools
    "lunarcrush": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_coin_metrics", "get_influence_score", "get_social_metrics"]},
                "api_key": {"type": "string", "description": "LunarCrush API key (required)"},
                "symbol": {"type": "string", "description": "Cryptocurrency symbol"},
                "timeframe": {"type": "string", "description": "Timeframe for data", "default": "24h"}
            }
        }
    },
    
    "coindesk": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_market_data", "get_news", "get_price_index"]},
                "api_key": {"type": "string", "description": "CoinDesk API key (required)"},
                "asset": {"type": "string", "description": "Asset identifier"},
                "currency": {"type": "string", "description": "Currency", "default": "USD"}
            }
        }
    },
    
    "pumpnews": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_latest_news", "search_news", "get_trending"]},
                "api_key": {"type": "string", "description": "PumpNews API key (required)"},
                "limit": {"type": "integer", "description": "Number of news items", "default": 10},
                "category": {"type": "string", "description": "News category", "default": "all"}
            }
        }
    },
    
    "pumpfun": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_token_info", "get_market_data", "get_social_metrics"]},
                "api_key": {"type": "string", "description": "PumpFun API key (required)"},
                "token_address": {"type": "string", "description": "Token contract address"},
                "network": {"type": "string", "description": "Blockchain network", "default": "ethereum"}
            }
        }
    },
    
    "gmgn": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_gaming_data", "get_nft_collections", "get_market_stats"]},
                "api_key": {"type": "string", "description": "GMGN API key (required)"},
                "game": {"type": "string", "description": "Game identifier"},
                "category": {"type": "string", "description": "Data category", "default": "all"}
            }
        }
    },
    
    "merkl": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_campaigns", "get_rewards", "get_user_data"]},
                "api_key": {"type": "string", "description": "Merkl API key (required)"},
                "network": {"type": "string", "description": "Blockchain network", "default": "ethereum"},
                "user_address": {"type": "string", "description": "User wallet address (optional)"}
            }
        }
    },
    
    "pendle": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_markets", "get_market_info", "get_yields", "get_liquidity", "get_tokens", "get_protocol_stats"]},
                "api_key": {"type": "string", "description": "Pendle API key (required)"},
                "chain": {"type": "string", "description": "Blockchain network", "default": "ethereum"},
                "market_address": {"type": "string", "description": "Market address for specific queries"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 20}
            }
        }
    },
    
    "meteora": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_pools", "get_pool_info", "get_tokens", "get_trading_pairs", "get_volume_data", "get_liquidity_data"]},
                "api_key": {"type": "string", "description": "Meteora API key (required)"},
                "chain": {"type": "string", "description": "Blockchain network", "default": "solana"},
                "pool_address": {"type": "string", "description": "Pool address for specific queries"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 20}
            }
        }
    },
    
    "deribit": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_instruments", "get_ticker", "get_orderbook", "get_trades", "get_index_price"]},
                "api_key": {"type": "string", "description": "Deribit API key (required)"},
                "instrument_name": {"type": "string", "description": "Instrument name (e.g., 'BTC-PERPETUAL')"},
                "currency": {"type": "string", "description": "Currency for the instrument", "default": "BTC"}
            }
        }
    },
    
    "twitter": {
        "required_params": ["action", "bearer_token"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_tweets", "get_user_tweets", "get_user_profile", "get_tweet_details", "get_trending_topics", "get_user_followers", "get_user_following", "get_tweet_likes", "get_tweet_retweets", "get_user_mentions", "get_hashtag_tweets", "get_user_timeline"]},
                "bearer_token": {"type": "string", "description": "Twitter Bearer Token (required)"},
                "query": {"type": "string", "description": "Search query for tweets"},
                "username": {"type": "string", "description": "Twitter username (without @)"},
                "max_results": {"type": "integer", "description": "Maximum number of results", "default": 10}
            }
        }
    },
    
    "reddit": {
        "required_params": ["action", "client_id", "client_secret"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_posts", "get_subreddit_posts", "get_post_comments", "get_user_posts", "get_user_comments", "get_subreddit_info", "get_user_info", "get_trending_subreddits", "get_hot_posts", "get_new_posts", "get_top_posts", "get_rising_posts"]},
                "client_id": {"type": "string", "description": "Reddit Client ID (required)"},
                "client_secret": {"type": "string", "description": "Reddit Client Secret (required)"},
                "user_agent": {"type": "string", "description": "Reddit User Agent", "default": "MCP-Reddit-Tool/1.0"},
                "query": {"type": "string", "description": "Search query for posts"},
                "subreddit": {"type": "string", "description": "Subreddit name (without r/)"},
                "limit": {"type": "integer", "description": "Number of results", "default": 25}
            }
        }
    },
    
    "jira": {
        "required_params": ["action", "jira_domain", "jira_username", "jira_api_token"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_issues", "get_issue", "create_issue", "update_issue", "delete_issue", "get_projects", "get_project", "get_boards", "get_sprints", "get_workflows", "get_users", "get_user", "search_issues", "get_issue_comments", "add_comment", "get_attachments", "get_issue_links", "get_issue_watchers", "get_project_components", "get_project_versions"]},
                "jira_domain": {"type": "string", "description": "JIRA domain (e.g., 'company' for company.atlassian.net)"},
                "jira_username": {"type": "string", "description": "JIRA username or email (required)"},
                "jira_api_token": {"type": "string", "description": "JIRA API token (required)"},
                "issue_key": {"type": "string", "description": "JIRA issue key (e.g., PROJ-123)"},
                "project_key": {"type": "string", "description": "JIRA project key"},
                "jql": {"type": "string", "description": "JQL search string"}
            }
        }
    },
    
    # Social Media Tools
    "youtube": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_videos", "get_channel_info", "get_video_stats"]},
                "api_key": {"type": "string", "description": "YouTube API key (required)"},
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
        "required_params": ["action", "api_key", "access_token"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["list_messages", "send_message", "get_message"]},
                "api_key": {"type": "string", "description": "Gmail API key (required)"},
                "access_token": {"type": "string", "description": "Gmail access token (required)"},
                "max_results": {"type": "integer", "description": "Maximum results", "default": 10},
                "query": {"type": "string", "description": "Search query (optional)"},
                "label": {"type": "string", "description": "Gmail label (optional)"}
            }
        }
    },
    
    "google_calendar": {
        "required_params": ["action", "api_key", "access_token"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["list_events", "create_event", "get_event"]},
                "api_key": {"type": "string", "description": "Google Calendar API key (required)"},
                "access_token": {"type": "string", "description": "Google Calendar access token (required)"},
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
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_current_weather", "get_weather_forecast", "get_weather_alerts", "get_air_pollution", "get_geocoding", "get_reverse_geocoding", "get_weather_history"]},
                "api_key": {"type": "string", "description": "OpenWeatherMap API key (required)"},
                "location": {"type": "string", "description": "City name, coordinates (lat,lon), or location query"},
                "latitude": {"type": "number", "description": "Latitude coordinate"},
                "longitude": {"type": "number", "description": "Longitude coordinate"},
                "units": {"type": "string", "description": "Temperature units", "enum": ["metric", "imperial", "standard"], "default": "metric"},
                "lang": {"type": "string", "description": "Language for weather descriptions", "default": "en"},
                "days": {"type": "integer", "description": "Number of days for forecast (max 16)", "default": 5},
                "exclude": {"type": "string", "description": "Exclude parts from response (current,minutely,hourly,daily,alerts)"}
            }
        }
    },
    
    "googlemaps": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["geocode", "reverse_geocode", "get_directions"]},
                "api_key": {"type": "string", "description": "Google Maps API key (required)"},
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
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["convert", "get_exchange_rates", "get_supported_currencies", "get_historical_rates", "get_crypto_rates"]},
                "from_currency": {"type": "string", "description": "Source currency code (required for convert action)"},
                "to_currency": {"type": "string", "description": "Target currency code (required for convert action)"},
                "amount": {"type": "number", "description": "Amount to convert (default: 1)"},
                "base_currency": {"type": "string", "description": "Base currency for exchange rates (default: USD)"},
                "date": {"type": "string", "description": "Date for historical rates (YYYY-MM-DD format)"}
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
    },
    
    # New MCP Tools
    "dune_query": {
        "required_params": ["action", "address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_balances", "get_activity", "get_collectibles", "get_transactions", "get_token_info", "get_token_holders"]},
                "address": {"type": "string", "description": "Wallet address to query"},
                "chain": {"type": "string", "description": "Blockchain network", "enum": ["ethereum", "polygon", "bsc", "arbitrum", "optimism", "avalanche"], "default": "ethereum"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10},
                "offset": {"type": "string", "description": "Pagination offset token"},
                "api_key": {"type": "string", "description": "Dune API key (required)"}
            }
        }
    },
    
    "meteora": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_pools", "get_pool_info", "get_tokens", "get_trading_pairs", "get_volume_data", "get_liquidity_data"]},
                "chain": {"type": "string", "description": "Blockchain network", "enum": ["solana", "ethereum", "polygon"], "default": "solana"},
                "pool_address": {"type": "string", "description": "Pool address for specific pool queries"},
                "token_address": {"type": "string", "description": "Token address for token-specific queries"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 20}
            }
        }
    },
    
    "pendle": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_markets", "get_market_info", "get_yields", "get_liquidity", "get_tokens", "get_protocol_stats"]},
                "chain": {"type": "string", "description": "Blockchain network", "enum": ["ethereum", "arbitrum", "bsc"], "default": "ethereum"},
                "market_address": {"type": "string", "description": "Market address for specific market queries"},
                "token_address": {"type": "string", "description": "Token address for token-specific queries"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 20}
            }
        }
    },
    
    "defillama": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_protocols", "get_protocol_tvl", "get_token_prices", "get_chains", "get_historical_tvl"]},
                "protocol": {"type": "string", "description": "Protocol name (e.g., 'aave', 'uniswap')"},
                "chain": {"type": "string", "description": "Blockchain network"},
                "token_address": {"type": "string", "description": "Token contract address"}
            }
        }
    },
    
    "deribit": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_instruments", "get_ticker", "get_orderbook", "get_trades", "get_index_price"]},
                "instrument_name": {"type": "string", "description": "Instrument name (e.g., 'BTC-PERPETUAL')"},
                "currency": {"type": "string", "description": "Currency for the instrument", "enum": ["BTC", "ETH", "SOL"], "default": "BTC"}
            }
        }
    },
    
    "chainbase_token_metadata": {
        "required_params": ["chain_id", "contract_address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "contract_address": {"type": "string", "description": "Token contract address"},
                "api_key": {"type": "string", "description": "Chainbase API key (required)"}
            }
        }
    },
    
    "chainbase_token_top_holders": {
        "required_params": ["chain_id", "contract_address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "contract_address": {"type": "string", "description": "Token contract address"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10},
                "api_key": {"type": "string", "description": "Chainbase API key (required)"}
            }
        }
    },
    
    "chainbase_token_holders": {
        "required_params": ["chain_id", "contract_address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "contract_address": {"type": "string", "description": "Token contract address"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10},
                "api_key": {"type": "string", "description": "Chainbase API key (required)"}
            }
        }
    },
    
    "chainbase_token_price": {
        "required_params": ["chain_id", "contract_address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "contract_address": {"type": "string", "description": "Token contract address"},
                "api_key": {"type": "string", "description": "Chainbase API key (required)"}
            }
        }
    },
    
    "chainbase_token_price_history": {
        "required_params": ["chain_id", "contract_address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "contract_address": {"type": "string", "description": "Token contract address"},
                "api_key": {"type": "string", "description": "Chainbase API key (required)"}
            }
        }
    },
    
    "chainbase_nft": {
        "required_params": ["action", "api_key", "chain_id", "contract_address"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_nft_metadata", "get_nft_owners_by_collection", "get_nft_owner_by_token", "get_nft_rarity", "get_nft_owner_history", "get_nft_transfers", "get_collection_items", "get_collection_metadata"]},
                "api_key": {"type": "string", "description": "Chainbase API key (required)"},
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "contract_address": {"type": "string", "description": "NFT contract address"},
                "token_id": {"type": "string", "description": "NFT token ID"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            }
        }
    },
    
    "pumpfun_data": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_pump_detection", "get_social_sentiment", "get_token_launches", "get_market_alerts", "get_trending_coins"]},
                "symbol": {"type": "string", "description": "Token symbol"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            }
        }
    },
    
    "coindesk_assets": {
        "required_params": ["action", "asset"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_asset_info", "get_asset_prices", "get_market_data", "get_asset_news", "get_asset_metrics"]},
                "asset": {"type": "string", "description": "Asset symbol (e.g., 'BTC', 'ETH')"},
                "currency": {"type": "string", "description": "Target currency", "default": "USD"}
            }
        }
    },
    
    "bnbchain": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_block_info", "get_transaction", "get_account_balance", "get_token_info", "get_contract_info"]},
                "network": {"type": "string", "description": "BNB Chain network", "enum": ["bsc", "opbnb"], "default": "bsc"},
                "block_number": {"type": "string", "description": "Block number or hash"},
                "address": {"type": "string", "description": "Account or contract address"}
            }
        }
    },
    
    "chainbase_basic": {
        "required_params": ["action", "chain_id"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_latest_block", "get_block_by_number", "get_block_by_hash", "get_transaction", "get_network_info"]},
                "chain_id": {"type": "string", "description": "Chain network ID"},
                "block_number": {"type": "string", "description": "Block number"},
                "block_hash": {"type": "string", "description": "Block hash"},
                "tx_hash": {"type": "string", "description": "Transaction hash"}
            }
        }
    },
    
    # DeFi and Trading Tools
    "coingecko": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_coin_price", "get_market_data", "get_trending", "get_exchange_rates", "get_coin_info"]},
                "coin_id": {"type": "string", "description": "Coin ID (e.g., 'bitcoin', 'ethereum')"},
                "vs_currency": {"type": "string", "description": "Target currency", "default": "usd"},
                "days": {"type": "string", "description": "Number of days for historical data", "default": "1"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            }
        }
    },
    
    "etherscan": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_balance", "get_transactions", "get_contract_info", "get_gas_price", "get_block_info"]},
                "address": {"type": "string", "description": "Ethereum address"},
                "start_block": {"type": "string", "description": "Starting block number"},
                "end_block": {"type": "string", "description": "Ending block number"},
                "block_number": {"type": "string", "description": "Block number"}
            }
        }
    },
    
    "binance": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_price", "get_orderbook", "get_24hr_stats", "get_recent_trades", "get_exchange_info"]},
                "symbol": {"type": "string", "description": "Trading pair symbol (e.g., 'BTCUSDT')"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            }
        }
    },
    
    "uniswap": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_pools", "get_pool_info", "get_token_info", "get_swaps", "get_liquidity"]},
                "pool_address": {"type": "string", "description": "Pool contract address"},
                "token_address": {"type": "string", "description": "Token contract address"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
            }
        }
    },
    
    "chainlink": {
        "required_params": ["action"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_price_feed", "get_network_info", "get_node_info", "get_job_info"]},
                "feed_address": {"type": "string", "description": "Price feed contract address"},
                "network": {"type": "string", "description": "Network name", "default": "ethereum"}
            }
        }
    },
    

    
    # Wallet Tools

    
    # Real Wallet Data Tools
    "chainbase_balance": {
        "required_params": ["action", "address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_balance", "get_token_holdings", "get_nft_holdings", "get_transaction_history", "get_portfolio_summary"]},
                "address": {"type": "string", "description": "Wallet address to query"},
                "chain_id": {"type": "string", "description": "Chain ID to query (e.g., '1' for Ethereum, '137' for Polygon)"},
                "api_key": {"type": "string", "description": "ChainBase API key (required)"},
                "limit": {"type": "integer", "description": "Maximum number of results"}
            }
        }
    },
    
    "metasleuth_wallet": {
        "required_params": ["action", "address", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["get_wallet_intel", "get_risk_score", "get_transaction_analysis", "get_behavior_patterns", "get_entity_connections", "get_compliance_check"]},
                "address": {"type": "string", "description": "Wallet address to analyze"},
                "api_key": {"type": "string", "description": "MetaSleuth API key (required)"},
                "timeframe": {"type": "string", "description": "Time period for analysis", "enum": ["7d", "30d", "90d", "1y", "all"]},
                "include_metadata": {"type": "boolean", "description": "Include additional metadata in response"}
            }
        }
    },
    
    "apollo": {
        "required_params": ["action", "api_key"],
        "schema": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform", "enum": ["search_people", "search_organizations", "get_job_postings", "get_organization_info", "search_news_articles"]},
                "api_key": {"type": "string", "description": "Apollo API key (required)"},
                "query": {"type": "string", "description": "Search query or keywords"},
                "company_name": {"type": "string", "description": "Company name for search or organization ID"},
                "job_title": {"type": "string", "description": "Job title for people search"},
                "industry": {"type": "string", "description": "Industry filter"},
                "location": {"type": "string", "description": "Location filter (city, state, country)"},
                "company_size": {"type": "string", "description": "Company size filter (1-10, 11-50, 51-200, etc.)"},
                "seniority": {"type": "string", "description": "Seniority level (VP, Director, Manager, etc.)"},
                "limit": {"type": "integer", "description": "Maximum number of results", "default": 10}
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
