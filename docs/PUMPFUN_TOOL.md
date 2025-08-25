# PumpFun Tool Documentation

## Overview

The `PumpFunTool` provides comprehensive access to PumpFun data, including pump detection, social sentiment analysis, market intelligence, and community insights. PumpFun is a specialized platform for detecting potential pump and dump schemes and providing real-time crypto market intelligence with advanced algorithms.

## Features

### Available Actions

1. **`get_pump_detection`** - Get pump detection analysis using PumpFun's proprietary algorithm
2. **`get_social_sentiment`** - Get comprehensive social media sentiment analysis
3. **`get_market_trends`** - Get market trends and intelligence data
4. **`get_volume_analysis`** - Get detailed volume analysis and unusual activity detection
5. **`get_community_insights`** - Get community-driven insights and predictions
6. **`get_alert_system`** - Get real-time market alerts and notifications
7. **`get_portfolio_monitoring`** - Get portfolio monitoring and watchlist data
8. **`get_risk_assessment`** - Get comprehensive risk assessment and analysis

### Supported Timeframes

- **1h** - 1 hour analysis
- **24h** - 24 hour analysis (default)
- **7d** - 7 day analysis
- **30d** - 30 day analysis

### Supported Platforms

- **twitter** - Twitter sentiment analysis
- **reddit** - Reddit sentiment analysis
- **telegram** - Telegram sentiment analysis
- **discord** - Discord sentiment analysis
- **all** - All platforms combined (default)

## Usage Examples

### Get Pump Detection
```python
result = await pumpfun.execute({
    "action": "get_pump_detection",
    "symbol": "BTC",
    "timeframe": "24h"
})
```

### Get Social Sentiment
```python
result = await pumpfun.execute({
    "action": "get_social_sentiment",
    "symbol": "ETH",
    "timeframe": "24h",
    "platform": "all"
})
```

### Get Market Trends
```python
result = await pumpfun.execute({
    "action": "get_market_trends",
    "limit": 10,
    "timeframe": "24h"
})
```

### Get Volume Analysis
```python
result = await pumpfun.execute({
    "action": "get_volume_analysis",
    "symbol": "DOGE",
    "timeframe": "24h"
})
```

### Get Community Insights
```python
result = await pumpfun.execute({
    "action": "get_community_insights",
    "symbol": "BTC",
    "limit": 10
})
```

### Get Alert System
```python
result = await pumpfun.execute({
    "action": "get_alert_system",
    "limit": 10,
    "timeframe": "24h"
})
```

### Get Portfolio Monitoring
```python
result = await pumpfun.execute({
    "action": "get_portfolio_monitoring",
    "symbols": ["BTC", "ETH", "DOGE"],
    "limit": 10
})
```

### Get Risk Assessment
```python
result = await pumpfun.execute({
    "action": "get_risk_assessment",
    "symbol": "SOL",
    "timeframe": "24h"
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
        "confidence": 0.85,
        "volume_spike": true,
        "price_momentum": "positive",
        "social_hype": "high",
        "technical_indicators": [...],
        "pump_probability": 0.72,
        "dump_risk": "low",
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

### Pump Detection
- **Pump Score** - Algorithmic rating of pump potential (0-100)
- **Risk Level** - Low, medium, high risk assessment
- **Confidence** - Confidence level of the analysis (0-1)
- **Volume Spike** - Detection of unusual volume increases
- **Price Momentum** - Price movement direction and strength
- **Social Hype** - Social media hype levels
- **Technical Indicators** - Technical analysis indicators
- **Pump Probability** - Probability of pump occurrence
- **Dump Risk** - Risk of subsequent dump

### Social Sentiment
- **Overall Sentiment** - Combined sentiment across platforms
- **Sentiment Score** - Numerical sentiment rating
- **Sentiment Change** - Change in sentiment over time
- **Platform Sentiment** - Twitter, Reddit, Telegram, Discord sentiment
- **Mentions Count** - Number of social media mentions
- **Trending Topics** - Popular discussion topics
- **Influencer Mentions** - Mentions by influential accounts
- **Sentiment Trend** - Sentiment trend direction

### Market Trends
- **Trending Coins** - Currently trending cryptocurrencies
- **Market Sentiment** - Overall market sentiment
- **Trending Reasons** - Why coins are trending
- **Market Momentum** - Market momentum indicators
- **Sector Performance** - Performance by crypto sectors
- **Emerging Trends** - New and emerging market trends
- **Market Volatility** - Market volatility metrics

### Volume Analysis
- **Current Volume** - Current trading volume
- **Average Volume** - Historical average volume
- **Volume Change** - Percentage change in volume
- **Volume Spike** - Detection of volume spikes
- **Unusual Activity** - Unusual trading patterns
- **Volume Patterns** - Historical volume patterns
- **Whale Activity** - Large transaction activity
- **Volume Distribution** - Volume distribution analysis

### Community Insights
- **Community Ratings** - User ratings and predictions
- **User Predictions** - Community price predictions
- **Discussion Topics** - Popular community discussions
- **Community Sentiment** - Overall community sentiment
- **Expert Opinions** - Expert analysis and opinions
- **Crowd Wisdom** - Collective community wisdom

### Alert System
- **Active Alerts** - Currently active market alerts
- **Alert Types** - Types of alerts available
- **Priority Alerts** - High-priority alerts
- **Alert Statistics** - Alert statistics and metrics
- **Custom Alerts** - User-defined custom alerts

### Portfolio Monitoring
- **Portfolio Alerts** - Portfolio-specific alerts
- **Price Alerts** - Price movement alerts
- **Volume Alerts** - Volume spike alerts
- **News Alerts** - News-related alerts
- **Risk Alerts** - Risk assessment alerts
- **Portfolio Summary** - Portfolio summary and metrics

### Risk Assessment
- **Overall Risk** - Overall risk assessment
- **Risk Score** - Numerical risk score
- **Volatility Risk** - Volatility-based risk
- **Liquidity Risk** - Liquidity-based risk
- **Market Risk** - Market-based risk factors
- **Social Risk** - Social media risk factors
- **Technical Risk** - Technical analysis risk
- **Risk Factors** - Specific risk factors
- **Risk Recommendations** - Risk mitigation recommendations

## Integration

### Router Registration
The `PumpFunTool` is automatically registered in the MCP router as `"pumpfun"`:

```python
self.local_tools = {
    # ... other tools ...
    "pumpfun": PumpFunTool()
}
```

### API Endpoints
- **PumpFun API**: `https://api.pumpfun.com/v1`
- **Authentication**: Bearer token via `PUMPFUN_API_KEY` environment variable

## Testing

### Individual Tool Testing
```bash
python scripts/test_pumpfun_tool.py
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
- **`PUMPFUN_API_KEY`** - API key for PumpFun service

### Optional
- **`PUMPFUN_API_URL`** - Custom API endpoint (defaults to production)

## Notes

- **Real Data**: The tool uses real PumpFun API data when available
- **API Key Required**: Most features require a valid API key
- **Rate Limiting**: Respects API rate limits and implements proper throttling
- **Session Management**: Implements proper aiohttp session management
- **Pump Detection**: Advanced proprietary algorithms for detecting pump and dump schemes
- **Social Sentiment**: Multi-platform sentiment analysis (Twitter, Reddit, Telegram, Discord)
- **Market Intelligence**: Real-time market trends and intelligence data
- **Risk Assessment**: Comprehensive risk analysis and recommendations
- **Community Features**: Community-driven insights and predictions
- **Alert System**: Real-time market alerts and notifications
- **Portfolio Monitoring**: Advanced portfolio tracking and monitoring
