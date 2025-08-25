# CoinDesk Tool Documentation

## Overview

The `CoinDeskTool` provides access to CoinDesk's cryptocurrency data, including real-time prices, historical data, Bitcoin Price Index (BPI), and market information. CoinDesk is a leading cryptocurrency news and data provider.

## Features

### Available Actions

1. **`get_current_price`** - Get current Bitcoin price in specified currency
2. **`get_historical_price`** - Get historical Bitcoin price data
3. **`get_bitcoin_price_index`** - Get Bitcoin Price Index (BPI) data
4. **`get_supported_currencies`** - Get list of supported currencies
5. **`get_market_data`** - Get additional market data (sample implementation)
6. **`get_news`** - Get CoinDesk news (sample implementation)

### API Requirements

- **Free Tier**: Basic price data and BPI information
- **Premium Tier**: Market data and news (requires `COINDESK_API_KEY`)
- **API Base URL**: `https://api.coindesk.com/v1`

## Usage Examples

### Get Current Bitcoin Price

```python
result = await coindesk_tool.execute(
    action="get_current_price",
    currency="USD"
)
```

**Response:**
```json
{
    "success": true,
    "data": {
        "currency": "USD",
        "price": 45000.0,
        "description": "United States Dollar",
        "updated": "Jan 15, 2024 10:30:00 UTC",
        "updated_iso": "2024-01-15T10:30:00+00:00"
    }
}
```

### Get Historical Price Data

```python
result = await coindesk_tool.execute(
    action="get_historical_price",
    currency="USD",
    start_date="2024-01-01",
    end_date="2024-01-15"
)
```

**Response:**
```json
{
    "success": true,
    "data": {
        "currency": "USD",
        "start_date": "2024-01-01",
        "end_date": "2024-01-15",
        "prices": {
            "2024-01-01": 42000.00,
            "2024-01-02": 42500.00,
            "2024-01-03": 43000.00,
            // ... more dates
        },
        "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index...",
        "updated": "Jan 15, 2024 10:30:00 UTC"
    }
}
```

### Get Bitcoin Price Index

```python
result = await coindesk_tool.execute(
    action="get_bitcoin_price_index"
)
```

**Response:**
```json
{
    "success": true,
    "data": {
        "bpi": {
            "USD": {
                "code": "USD",
                "symbol": "&#36;",
                "rate": "45,000.0000",
                "description": "United States Dollar",
                "rate_float": 45000.0
            },
            "EUR": {
                "code": "EUR",
                "symbol": "&euro;",
                "rate": "42,000.0000",
                "description": "Euro",
                "rate_float": 42000.0
            }
            // ... more currencies
        },
        "disclaimer": "This data was produced from the CoinDesk Bitcoin Price Index...",
        "chart_name": "Bitcoin Price Index",
        "updated": "Jan 15, 2024 10:30:00 UTC",
        "updated_iso": "2024-01-15T10:30:00+00:00"
    }
}
```

### Get Supported Currencies

```python
result = await coindesk_tool.execute(
    action="get_supported_currencies"
)
```

**Response:**
```json
{
    "success": true,
    "data": {
        "currencies": [
            {"currency": "USD", "country": "United States"},
            {"currency": "EUR", "country": "European Union"},
            {"currency": "GBP", "country": "United Kingdom"},
            // ... more currencies
        ],
        "count": 25
    }
}
```

## Error Handling

The tool provides clear error messages when the API is unavailable:

```json
{
    "success": false,
    "error": "Failed to get current price: Cannot connect to host api.coindesk.com:443 ssl:default [getaddrinfo failed]"
}
```

## Environment Variables

Set the following environment variable for premium features:

```bash
export COINDESK_API_KEY="your_api_key_here"
```

## Sample Data

For premium features (`get_market_data` and `get_news`), the tool returns sample data with a note indicating that real data requires premium API access.

### Market Data Sample

```json
{
    "success": true,
    "data": {
        "market_cap": "$1,234,567,890,123",
        "24h_volume": "$45,678,901,234",
        "24h_change": "+2.34%",
        "7d_change": "+5.67%",
        "dominance": "48.2%",
        "note": "This is sample data. For real market data, consider CoinDesk's premium API."
    }
}
```

### News Sample

```json
{
    "success": true,
    "data": {
        "news": [
            {
                "title": "Bitcoin Reaches New All-Time High",
                "summary": "Bitcoin has reached a new all-time high, surpassing previous records.",
                "published": "2024-01-15T10:30:00Z",
                "url": "https://www.coindesk.com/sample-article-1"
            }
            // ... more articles
        ],
        "count": 3,
        "note": "This is sample news data. For real news, consider CoinDesk's premium API."
    }
}
```

## Integration

The CoinDesk tool is automatically registered in the MCP router and available for use by AI assistants. It follows the same pattern as other tools in the system:

1. **Tool Registration**: Automatically registered in `app/mcp/router.py`
2. **Error Handling**: Robust error handling with clear error messages
3. **Session Management**: Proper aiohttp session management with cleanup
4. **Testing**: Included in comprehensive test suite

## Testing

Test the CoinDesk tool individually:

```bash
python scripts/test_coindesk_tool.py
```

Or test all tools including CoinDesk:

```bash
python scripts/test_all_tools.py
```

## Notes

- The tool does not return sample data when the API is unavailable (as per user requirements)
- Clear error messages are provided for connectivity issues
- Premium features return sample data with appropriate notes
- All API calls are properly handled with try-catch blocks
- Session cleanup is ensured in all cases
