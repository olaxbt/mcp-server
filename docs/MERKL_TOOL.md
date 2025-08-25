# Merkl Tool Documentation

## Overview

The `MerklTool` provides comprehensive access to Merkl protocol data, including concentrated liquidity positions, yield farming opportunities, rewards distribution, and protocol analytics. Merkl is a DeFi protocol that specializes in concentrated liquidity and yield farming, particularly focused on Uniswap V3-style concentrated liquidity positions.

## Features

### Available Actions

1. **`get_concentrated_positions`** - Get concentrated liquidity positions data
2. **`get_yield_farming_opportunities`** - Get yield farming opportunities and APY data
3. **`get_rewards_distribution`** - Get rewards distribution and token incentives data
4. **`get_protocol_analytics`** - Get Merkl protocol analytics and metrics
5. **`get_position_performance`** - Get performance metrics for specific positions
6. **`get_liquidity_pools`** - Get available liquidity pools and their data
7. **`get_user_positions`** - Get user's liquidity positions and performance
8. **`get_rewards_calculation`** - Calculate potential rewards for a position

### Supported Parameters

- **`chain`** - Blockchain network (ethereum, polygon, arbitrum, optimism) - default: "ethereum"
- **`token`** - Token address or symbol (e.g., USDC, WETH, 0x...)
- **`user_address`** - User wallet address for position queries
- **`pool_address`** - Liquidity pool address
- **`limit`** - Number of results to return - default: 10
- **`timeframe`** - Timeframe for analysis (1h, 24h, 7d, 30d) - default: "24h"
- **`min_apy`** - Minimum APY filter for yield opportunities - default: 0
- **`amount`** - Amount for rewards calculation

## Usage Examples

### 1. Get Concentrated Positions

```python
# Get all concentrated positions on Ethereum
result = await merkl.execute({
    "action": "get_concentrated_positions",
    "chain": "ethereum",
    "timeframe": "24h"
})

# Get concentrated positions for a specific token
result = await merkl.execute({
    "action": "get_concentrated_positions",
    "chain": "ethereum",
    "token": "WETH",
    "timeframe": "24h"
})
```

### 2. Get Yield Farming Opportunities

```python
# Get yield opportunities with minimum 5% APY
result = await merkl.execute({
    "action": "get_yield_farming_opportunities",
    "chain": "ethereum",
    "min_apy": 5.0,
    "timeframe": "24h"
})

# Get yield opportunities on Polygon
result = await merkl.execute({
    "action": "get_yield_farming_opportunities",
    "chain": "polygon",
    "timeframe": "7d"
})
```

### 3. Get Rewards Distribution

```python
# Get rewards distribution for all tokens
result = await merkl.execute({
    "action": "get_rewards_distribution",
    "chain": "ethereum",
    "timeframe": "24h"
})

# Get rewards distribution for specific token
result = await merkl.execute({
    "action": "get_rewards_distribution",
    "chain": "ethereum",
    "token": "USDC",
    "timeframe": "24h"
})
```

### 4. Get Protocol Analytics

```python
# Get protocol analytics
result = await merkl.execute({
    "action": "get_protocol_analytics",
    "chain": "ethereum",
    "timeframe": "24h"
})
```

### 5. Get Position Performance

```python
# Get performance for a specific pool
result = await merkl.execute({
    "action": "get_position_performance",
    "chain": "ethereum",
    "pool_address": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8",
    "timeframe": "24h"
})

# Get performance for a specific user
result = await merkl.execute({
    "action": "get_position_performance",
    "chain": "ethereum",
    "user_address": "0x742d35cc6634c0532925a3b8d4c9db96c4b4d8b6",
    "timeframe": "24h"
})
```

### 6. Get Liquidity Pools

```python
# Get all liquidity pools
result = await merkl.execute({
    "action": "get_liquidity_pools",
    "chain": "ethereum",
    "limit": 10,
    "timeframe": "24h"
})

# Get pools for specific token
result = await merkl.execute({
    "action": "get_liquidity_pools",
    "chain": "ethereum",
    "token": "USDC",
    "timeframe": "24h"
})
```

### 7. Get User Positions

```python
# Get user's positions
result = await merkl.execute({
    "action": "get_user_positions",
    "chain": "ethereum",
    "user_address": "0x742d35cc6634c0532925a3b8d4c9db96c4b4d8b6",
    "timeframe": "24h"
})
```

### 8. Calculate Rewards

```python
# Calculate rewards for a specific pool
result = await merkl.execute({
    "action": "get_rewards_calculation",
    "chain": "ethereum",
    "pool_address": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8",
    "amount": 1000,
    "timeframe": "24h"
})

# Calculate rewards for a specific token
result = await merkl.execute({
    "action": "get_rewards_calculation",
    "chain": "ethereum",
    "token": "USDC",
    "amount": 1000,
    "timeframe": "24h"
})
```

## Response Format

### Success Response

```json
{
    "success": true,
    "chain": "ethereum",
    "timeframe": "24h",
    "data": {
        "positions": [...],
        "total_tvl": "1000000",
        "active_positions": 150,
        "average_apy": 12.5,
        "position_distribution": {...},
        "top_tokens": [...],
        "timestamp": "2024-01-01T12:00:00"
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": "Failed to fetch concentrated positions: 404"
}
```

## Key Data Points

### Concentrated Positions
- Position details and ranges
- Total TVL and active positions
- Average APY across positions
- Position distribution by token
- Top performing tokens

### Yield Farming Opportunities
- Available opportunities with APY
- Risk levels and token distribution
- Protocol distribution
- Highest and average APY

### Rewards Distribution
- Active reward programs
- Reward tokens and distribution
- User rewards and incentives
- Distribution by token and pool

### Protocol Analytics
- Total TVL and volume
- Active users and positions
- Protocol fees and growth metrics
- Market share and risk metrics

### Position Performance
- Performance metrics and APY history
- Rewards earned and fees collected
- Impermanent loss calculations
- Risk assessment

### Liquidity Pools
- Available pools and their data
- Pool distribution and top pools
- New pools and trends
- Total pools and average APY

### User Positions
- User's active positions
- Total value and rewards
- Position history and performance
- Performance summary

### Rewards Calculation
- Estimated rewards and APY
- Reward tokens and distribution
- Time to break even
- Risk assessment and optimization suggestions

## Integration

### Environment Variables

Set the following environment variable for API access:

```bash
export MERKL_API_KEY="your_merkl_api_key_here"
```

### MCP Server Integration

The tool is automatically registered in the MCP server router:

```python
"merkl": MerklTool()
```

### API Endpoints

The tool uses the following base URL:
- **Base URL**: `https://api.merkl.xyz/v1`
- **Authentication**: Bearer token via `Authorization` header
- **Rate Limiting**: Subject to Merkl API limits

## Testing

### Individual Tool Testing

Run the dedicated test script:

```bash
python scripts/test_merkl_tool.py
```

### Comprehensive Testing

Include in the comprehensive test suite:

```bash
python scripts/test_all_tools.py
```

## Error Handling

The tool handles various error scenarios:

1. **API Unavailable**: Returns error message instead of sample data
2. **Missing Parameters**: Validates required parameters
3. **Invalid Actions**: Returns error for unknown actions
4. **Network Errors**: Graceful handling of connection issues

## Notes

- **Real Data**: Uses actual Merkl API data when available
- **API Key Required**: Requires `MERKL_API_KEY` for real data access
- **Multi-Chain Support**: Supports Ethereum, Polygon, Arbitrum, and Optimism
- **Concentrated Liquidity**: Specialized in Uniswap V3-style positions
- **Yield Farming**: Focus on yield optimization and rewards
- **Performance Tracking**: Comprehensive position performance analysis
