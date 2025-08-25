# LunarCrushTool Documentation

## Overview

The **LunarCrushTool** provides access to LunarCrush cryptocurrency analytics and social sentiment data. It offers comprehensive insights into crypto market intelligence, social sentiment analysis, influence tracking, and trending assets.

## Features

### 🔍 Social Sentiment Analysis
- **Social Volume**: Track social media mentions and engagement
- **Social Score**: LunarCrush's proprietary social scoring system
- **Sentiment Analysis**: Bullish/bearish sentiment ratios
- **Social Contributors**: Number of unique social media contributors
- **Engagement Metrics**: Social engagement rates and patterns

### 📊 Market Intelligence
- **Price Data**: Current prices and price changes
- **Volume Analysis**: 24h trading volume and market activity
- **Market Cap**: Market capitalization and dominance metrics
- **Supply Metrics**: Circulating and max supply information
- **Volatility**: Price volatility and correlation data

### 👥 Influence Analysis
- **Top Influencers**: Identify key social media influencers
- **Influence Scores**: Measure influencer impact on crypto markets
- **Platform Analysis**: Track influence across Twitter, Reddit, Telegram
- **Engagement Rates**: Monitor influencer engagement metrics

### 📈 Trending Assets
- **Trending Cryptocurrencies**: Currently trending assets
- **Social Momentum**: Assets gaining social traction
- **Galaxy Score**: LunarCrush's comprehensive scoring system
- **AltRank**: Alternative ranking system for crypto assets

### 📅 Historical Data
- **Time Series Data**: Historical social and market metrics
- **Trend Analysis**: Social and price trends over time
- **Comparative History**: Historical performance comparisons

### 🔄 Comparative Analysis
- **Multi-Asset Comparison**: Compare multiple cryptocurrencies
- **Performance Metrics**: Side-by-side performance analysis
- **Social vs Market**: Social sentiment vs market performance

## API Actions

### 1. `get_social_sentiment`
Get social sentiment data for a specific cryptocurrency.

**Parameters:**
- `symbol` (string): Cryptocurrency symbol (e.g., "BTC", "ETH", "SOL")
- `timeframe` (string): Timeframe for data ("1h", "24h", "7d", "30d")

**Example:**
```json
{
  "action": "get_social_sentiment",
  "symbol": "BTC",
  "timeframe": "24h"
}
```

### 2. `get_market_intelligence`
Get market intelligence data for a cryptocurrency.

**Parameters:**
- `symbol` (string): Cryptocurrency symbol
- `timeframe` (string): Timeframe for data

**Example:**
```json
{
  "action": "get_market_intelligence",
  "symbol": "ETH",
  "timeframe": "24h"
}
```

### 3. `get_influence_analysis`
Get influence analysis and top influencers.

**Parameters:**
- `symbol` (string): Cryptocurrency symbol
- `limit` (integer): Number of influencers to return (max: 50)

**Example:**
```json
{
  "action": "get_influence_analysis",
  "symbol": "SOL",
  "limit": 10
}
```

### 4. `get_trending_assets`
Get currently trending cryptocurrencies.

**Parameters:**
- `limit` (integer): Number of assets to return (max: 100)
- `timeframe` (string): Timeframe for data

**Example:**
```json
{
  "action": "get_trending_assets",
  "limit": 20,
  "timeframe": "24h"
}
```

### 5. `get_historical_data`
Get historical social and market data.

**Parameters:**
- `symbol` (string): Cryptocurrency symbol
- `timeframe` (string): Timeframe for data

**Example:**
```json
{
  "action": "get_historical_data",
  "symbol": "BTC",
  "timeframe": "7d"
}
```

### 6. `get_comparative_analysis`
Compare multiple cryptocurrencies.

**Parameters:**
- `symbols` (array): Array of cryptocurrency symbols
- `timeframe` (string): Timeframe for data

**Example:**
```json
{
  "action": "get_comparative_analysis",
  "symbols": ["BTC", "ETH", "SOL"],
  "timeframe": "24h"
}
```

## Setup

### API Key Configuration

To use real LunarCrush data, you need to set up an API key:

1. **Get API Key**: Sign up at [LunarCrush](https://lunarcrush.com/) and obtain your API key
2. **Set Environment Variable**: 
   ```bash
   export LUNARCRUSH_API_KEY=your_api_key_here
   ```
   Or on Windows:
   ```cmd
   set LUNARCRUSH_API_KEY=your_api_key_here
   ```

### Without API Key

If no API key is provided, the tool will return sample data with informative notes about the required API key.

## Sample Responses

### Social Sentiment Response
```json
{
  "type": "lunarcrush_social_sentiment",
  "symbol": "BTC",
  "timeframe": "24h",
  "social_volume": 125000,
  "social_score": 85.2,
  "social_contributors": 4500,
  "social_engagement": 0.78,
  "sentiment_score": 0.65,
  "bullish_sentiment": 0.68,
  "bearish_sentiment": 0.32,
  "alt_rank": 1,
  "galaxy_score": 82.1,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Market Intelligence Response
```json
{
  "type": "lunarcrush_market_intelligence",
  "symbol": "ETH",
  "timeframe": "24h",
  "price": 2500.0,
  "price_change_24h": 2.5,
  "volume_24h": 15000000000,
  "market_cap": 300000000000,
  "market_cap_change_24h": 1.8,
  "circulating_supply": 120000000,
  "max_supply": null,
  "volatility": 0.045,
  "correlation_rank": 0.92,
  "market_dominance": 18.5,
  "timestamp": "2024-01-15T10:30:00"
}
```

## Use Cases

### 1. Trading Decisions
- Analyze social sentiment before making trades
- Identify trending assets for momentum trading
- Monitor influencer opinions and market sentiment

### 2. Market Research
- Compare social vs market performance
- Track community engagement and growth
- Identify emerging trends in crypto

### 3. Risk Assessment
- Monitor social sentiment for risk signals
- Track volatility and correlation data
- Assess market dominance and competition

### 4. Content Creation
- Identify trending topics and assets
- Track social engagement patterns
- Monitor influencer activity and impact

## Integration

The LunarCrushTool is fully integrated into the MCP server and can be used by AI assistants to:

- Provide real-time crypto market intelligence
- Analyze social sentiment trends
- Identify trending cryptocurrencies
- Compare multiple assets
- Track historical performance

## Notes

- **Rate Limits**: LunarCrush API has rate limits that vary by plan
- **Data Freshness**: Data is updated in real-time from LunarCrush
- **Coverage**: Supports 2000+ cryptocurrencies
- **Historical Data**: Available for various timeframes
- **Sample Data**: Returns realistic sample data when API key is not available

## Support

For issues or questions about the LunarCrushTool:
1. Check the API key configuration
2. Verify the cryptocurrency symbol is supported
3. Review the LunarCrush API documentation
4. Check rate limits and usage quotas
