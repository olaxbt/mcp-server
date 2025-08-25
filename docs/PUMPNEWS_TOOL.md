# PumpNews Tool Documentation

## Overview

The `PumpNewsTool` provides comprehensive access to PumpNews data, including crypto news, pump detection, social sentiment analysis, and market alerts. PumpNews is a specialized platform for detecting potential pump and dump schemes and providing real-time crypto market intelligence.

## Features

### Available Actions

1. **`get_news`** - Get latest crypto news and market updates
2. **`get_pump_detection`** - Get pump detection analysis for cryptocurrencies
3. **`get_social_sentiment`** - Get social media sentiment for cryptocurrencies
4. **`get_market_alerts`** - Get market alerts and unusual trading activity
5. **`get_trending_coins`** - Get currently trending cryptocurrencies
6. **`get_volume_analysis`** - Get volume analysis and unusual trading activity
7. **`get_community_insights`** - Get community insights and predictions
8. **`get_portfolio_alerts`** - Get portfolio alerts and watchlist monitoring

### Supported Timeframes

- **1h** - 1 hour analysis
- **24h** - 24 hour analysis (default)
- **7d** - 7 day analysis
- **30d** - 30 day analysis

## Usage Examples

### Get News
```python
result = await pumpnews.execute({
    "action": "get_news",
    "limit": 10,
    "category": "breaking"
})
```

### Get Pump Detection
```python
result = await pumpnews.execute({
    "action": "get_pump_detection",
    "symbol": "BTC",
    "timeframe": "24h"
})
```

### Get Social Sentiment
```python
result = await pumpnews.execute({
    "action": "get_social_sentiment",
    "symbol": "ETH",
    "timeframe": "24h"
})
```

### Get Market Alerts
```python
result = await pumpnews.execute({
    "action": "get_market_alerts",
    "limit": 10,
    "timeframe": "24h"
})
```

### Get Trending Coins
```python
result = await pumpnews.execute({
    "action": "get_trending_coins",
    "limit": 10,
    "timeframe": "24h"
})
```

### Get Volume Analysis
```python
result = await pumpnews.execute({
    "action": "get_volume_analysis",
    "symbol": "DOGE",
    "timeframe": "24h"
})
```

### Get Community Insights
```python
result = await pumpnews.execute({
    "action": "get_community_insights",
    "symbol": "BTC",
    "limit": 10
})
```

### Get Portfolio Alerts
```python
result = await pumpnews.execute({
    "action": "get_portfolio_alerts",
    "symbols": ["BTC", "ETH", "DOGE"],
    "limit": 10
})
```

## Response Format

### Success Response
```json
{
    "success": true,
    "symbol": "BTC",
    "timeframe": "24h",
    "data": {
        "pump_score": 75.5,
        "risk_level": "medium",
        "volume_spike": true,
        "price_change": "+5.2%",
        "social_activity": "high",
        "indicators": [...],
        "timestamp": "2024-01-15T10:30:00"
    }
}
```

### Error Response
```json
{
    "success": false,
    "error": "Failed to get pump detection: Connection timeout"
}
```

## Key Data Points

### News Data
- **News Articles** - Latest crypto news and market updates
- **Categories** - Breaking news, analysis, market updates
- **Symbol Filtering** - News specific to certain cryptocurrencies
- **Timestamps** - Publication times and relevance

### Pump Detection
- **Pump Score** - Algorithmic rating of pump potential (0-100)
- **Risk Level** - Low, medium, high risk assessment
- **Volume Spike** - Detection of unusual volume increases
- **Price Change** - Recent price movements and patterns
- **Social Activity** - Social media activity levels
- **Indicators** - Technical and social indicators

### Social Sentiment
- **Overall Sentiment** - Combined sentiment across platforms
- **Sentiment Score** - Numerical sentiment rating
- **Platform Sentiment** - Twitter, Reddit, Telegram sentiment
- **Mentions Count** - Number of social media mentions
- **Trending Topics** - Popular discussion topics

### Market Alerts
- **Alert Types** - Price alerts, volume alerts, news alerts
- **Unusual Activity** - Detection of unusual trading patterns
- **Alert Severity** - Low, medium, high priority alerts
- **Timeframes** - Alert timeframes and relevance

### Trending Coins
- **Trending List** - Currently trending cryptocurrencies
- **Trending Reasons** - Why coins are trending
- **Social Metrics** - Social media activity and mentions
- **Price Movements** - Recent price changes

### Volume Analysis
- **Current Volume** - Current trading volume
- **Average Volume** - Historical average volume
- **Volume Change** - Percentage change in volume
- **Volume Spike** - Detection of volume spikes
- **Unusual Activity** - Unusual trading patterns
- **Volume Patterns** - Historical volume patterns

### Community Insights
- **Community Ratings** - User ratings and predictions
- **Discussion Topics** - Popular community discussions
- **Predictions** - Community price predictions
- **Insights** - Community analysis and insights

### Portfolio Alerts
- **Price Alerts** - Price movement alerts
- **News Alerts** - News-related alerts
- **Volume Alerts** - Volume spike alerts
- **Custom Alerts** - User-defined alert types

## Integration

### Router Registration
The `PumpNewsTool` is automatically registered in the MCP router as `"pumpnews"`:

```python
self.local_tools = {
    # ... other tools ...
    "pumpnews": PumpNewsTool()
}
```

### API Endpoints
- **PumpNews API**: `https://api.pumpnews.com/v1`
- **Authentication**: Bearer token via `PUMPNEWS_API_KEY` environment variable

## Testing

### Individual Tool Testing
```bash
python scripts/test_pumpnews_tool.py
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
- **`PUMPNEWS_API_KEY`** - API key for PumpNews service

### Optional
- **`PUMPNEWS_API_URL`** - Custom API endpoint (defaults to production)

## Notes

- **Real Data**: The tool uses real PumpNews API data when available
- **API Key Required**: Most features require a valid API key
- **Rate Limiting**: Respects API rate limits and implements proper throttling
- **Session Management**: Implements proper aiohttp session management
- **Pump Detection**: Specialized algorithms for detecting pump and dump schemes
- **Social Sentiment**: Multi-platform sentiment analysis (Twitter, Reddit, Telegram)
- **Market Intelligence**: Real-time market alerts and unusual activity detection
