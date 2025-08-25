# GMGN Tool Documentation

## Overview

The `GMGNTool` provides comprehensive access to GMGN (Global Market Gaming Network) data, including gaming token analysis, P2E (Play-to-Earn) analytics, gaming NFT markets, and gaming industry insights. GMGN is a specialized platform for analyzing gaming-related cryptocurrencies, blockchain games, and the gaming industry.

## Features

### Available Actions

1. **`get_gaming_token_analysis`** - Get comprehensive analysis of gaming tokens
2. **`get_p2e_analytics`** - Get Play-to-Earn game analytics and performance
3. **`get_gaming_nft_markets`** - Get gaming NFT marketplace data and trends
4. **`get_gaming_community_insights`** - Get gaming community insights and sentiment
5. **`get_gaming_project_ratings`** - Get expert ratings and reviews of gaming projects
6. **`get_gaming_industry_trends`** - Get gaming industry trends and market movements
7. **`get_gaming_token_discovery`** - Discover new and trending gaming tokens
8. **`get_gaming_investment_analysis`** - Get gaming investment analysis and recommendations

### Supported Timeframes

- **1h** - 1 hour analysis
- **24h** - 24 hour analysis (default)
- **7d** - 7 day analysis
- **30d** - 30 day analysis

### Supported Categories

- **p2e** - Play-to-Earn games
- **nft** - NFT gaming projects
- **metaverse** - Metaverse and virtual world projects
- **strategy** - Strategy games
- **rpg** - Role-playing games
- **all** - All categories (default)

## Usage Examples

### Get Gaming Token Analysis
```python
result = await gmgn.execute({
    "action": "get_gaming_token_analysis",
    "token": "AXS",
    "timeframe": "24h"
})
```

### Get P2E Analytics
```python
result = await gmgn.execute({
    "action": "get_p2e_analytics",
    "game": "Axie Infinity",
    "timeframe": "24h"
})
```

### Get Gaming NFT Markets
```python
result = await gmgn.execute({
    "action": "get_gaming_nft_markets",
    "limit": 10,
    "category": "p2e",
    "timeframe": "24h"
})
```

### Get Gaming Community Insights
```python
result = await gmgn.execute({
    "action": "get_gaming_community_insights",
    "token": "SAND",
    "limit": 10
})
```

### Get Gaming Project Ratings
```python
result = await gmgn.execute({
    "action": "get_gaming_project_ratings",
    "game": "The Sandbox",
    "limit": 10
})
```

### Get Gaming Industry Trends
```python
result = await gmgn.execute({
    "action": "get_gaming_industry_trends",
    "limit": 10,
    "timeframe": "24h",
    "category": "metaverse"
})
```

### Get Gaming Token Discovery
```python
result = await gmgn.execute({
    "action": "get_gaming_token_discovery",
    "limit": 10,
    "category": "nft",
    "timeframe": "24h"
})
```

### Get Gaming Investment Analysis
```python
result = await gmgn.execute({
    "action": "get_gaming_investment_analysis",
    "token": "MANA",
    "timeframe": "24h"
})
```

## Response Format

### Success Response
```json
{
    "success": true,
    "token": "AXS",
    "timeframe": "24h",
    "data": {
        "token_info": {
            "name": "Axie Infinity",
            "symbol": "AXS",
            "blockchain": "Ethereum"
        },
        "price_analysis": {
            "current_price": 12.50,
            "price_change_24h": 5.2,
            "price_change_7d": -2.1
        },
        "volume_analysis": {
            "volume_24h": 45000000,
            "volume_change_24h": 15.3
        },
        "market_cap": 1500000000,
        "circulating_supply": 120000000,
        "total_supply": 270000000,
        "gaming_metrics": {
            "player_count": 2500000,
            "daily_active_users": 180000,
            "revenue_24h": 250000
        },
        "utility_score": 85.5,
        "adoption_score": 78.2,
        "timestamp": "2024-01-15T10:30:00"
    }
}
```

### Error Response
```json
{
    "success": false,
    "error": "Failed to get gaming token analysis: Connection timeout"
}
```

## Key Data Points

### Gaming Token Analysis
- **Token Info** - Basic token information and metadata
- **Price Analysis** - Current price and price changes
- **Volume Analysis** - Trading volume and volume changes
- **Market Cap** - Market capitalization
- **Circulating Supply** - Current circulating supply
- **Total Supply** - Maximum total supply
- **Gaming Metrics** - Game-specific metrics (players, revenue, etc.)
- **Utility Score** - Token utility assessment (0-100)
- **Adoption Score** - Adoption and usage assessment (0-100)

### P2E Analytics
- **Game Info** - Basic game information
- **Player Stats** - Player statistics and metrics
- **Tokenomics** - Token economics and distribution
- **Revenue Metrics** - Revenue and financial metrics
- **Earning Potential** - Potential earnings for players
- **Player Count** - Total number of players
- **Active Users** - Daily/monthly active users
- **Daily Revenue** - Daily revenue generated
- **Token Price** - Current token price
- **Market Cap** - Game token market cap
- **P2E Score** - Play-to-Earn viability score
- **Sustainability Score** - Long-term sustainability assessment

### Gaming NFT Markets
- **NFT Collections** - Gaming NFT collections
- **Trading Volume** - Total trading volume
- **Floor Prices** - Floor prices for collections
- **Sales Count** - Number of sales
- **Unique Buyers** - Number of unique buyers
- **Unique Sellers** - Number of unique sellers
- **Trending NFTs** - Currently trending NFTs
- **Market Metrics** - Overall market metrics

### Gaming Community Insights
- **Community Sentiment** - Overall community sentiment
- **Sentiment Score** - Numerical sentiment rating
- **Community Size** - Total community size
- **Active Members** - Number of active members
- **Engagement Rate** - Community engagement rate
- **Discussion Topics** - Popular discussion topics
- **Community Ratings** - Community ratings and reviews
- **User Feedback** - User feedback and comments
- **Social Metrics** - Social media metrics

### Gaming Project Ratings
- **Overall Rating** - Overall project rating
- **Expert Reviews** - Expert reviews and analysis
- **Rating Breakdown** - Detailed rating breakdown
- **Pros Cons** - Project pros and cons
- **Recommendation** - Investment recommendation
- **Risk Assessment** - Risk assessment
- **Long Term Potential** - Long-term growth potential
- **Market Position** - Market position and competition
- **Competitive Analysis** - Competitive landscape analysis

### Gaming Industry Trends
- **Trending Games** - Currently trending games
- **Trending Tokens** - Trending gaming tokens
- **Market Trends** - Overall market trends
- **Industry Metrics** - Industry-wide metrics
- **Sector Performance** - Performance by gaming sectors
- **Emerging Trends** - New and emerging trends
- **Market Sentiment** - Overall market sentiment
- **Investment Flows** - Investment flow analysis

### Gaming Token Discovery
- **New Tokens** - Newly launched gaming tokens
- **Trending Tokens** - Currently trending tokens
- **Upcoming Releases** - Upcoming game releases
- **Discovery Metrics** - Discovery and trending metrics
- **Token Categories** - Token categories and classifications
- **Market Opportunities** - Market opportunity analysis

### Gaming Investment Analysis
- **Investment Score** - Investment attractiveness score
- **Risk Level** - Investment risk assessment
- **Potential Return** - Potential return on investment
- **Investment Recommendation** - Investment recommendation
- **Market Analysis** - Market analysis and outlook
- **Competitive Position** - Competitive position analysis
- **Growth Potential** - Growth potential assessment
- **Investment Risks** - Specific investment risks
- **Investment Opportunities** - Investment opportunities
- **Portfolio Fit** - Portfolio fit assessment

## Integration

### Router Registration
The `GMGNTool` is automatically registered in the MCP router as `"gmgn"`:

```python
self.local_tools = {
    # ... other tools ...
    "gmgn": GMGNTool()
}
```

### API Endpoints
- **GMGN API**: `https://api.gmgn.com/v1`
- **Authentication**: Bearer token via `GMGN_API_KEY` environment variable

## Testing

### Individual Tool Testing
```bash
python scripts/test_gmgn_tool.py
```

### Comprehensive Testing
```bash
python scripts/test_all_tools.py
```

## Error Handling

The tool implements robust error handling:

1. **Network Errors** - Returns clear error messages for connection issues
2. **API Errors** - Handles HTTP status codes and API-specific errors
3. **Data Validation** - Validates required parameters and data formats
4. **Missing Parameters** - Clear error messages for required parameters
5. **Graceful Degradation** - Continues operation even if some data is unavailable

## Environment Variables

### Required
- **`GMGN_API_KEY`** - API key for GMGN service

### Optional
- **`GMGN_API_URL`** - Custom API endpoint (defaults to production)

## Notes

- **Real Data**: The tool uses real GMGN API data when available
- **API Key Required**: Most features require a valid API key
- **Rate Limiting**: Respects API rate limits and implements proper throttling
- **Session Management**: Implements proper aiohttp session management
- **Gaming Focus**: Specialized analysis for gaming and blockchain gaming sector
- **P2E Analytics**: Comprehensive Play-to-Earn game analysis
- **NFT Markets**: Gaming NFT marketplace data and trends
- **Community Insights**: Gaming community sentiment and engagement
- **Project Ratings**: Expert ratings and reviews of gaming projects
- **Industry Trends**: Gaming industry trends and market movements
- **Token Discovery**: Discovery of new and trending gaming tokens
- **Investment Analysis**: Gaming investment analysis and recommendations
