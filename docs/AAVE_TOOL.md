# Aave Tool Documentation

## Overview

The `AaveTool` provides comprehensive access to Aave Protocol data, including lending pools, user positions, asset information, and DeFi analytics. Aave is one of the most prominent DeFi lending and borrowing protocols, available on multiple blockchain networks.

## Features

### Available Actions

1. **`get_pool_data`** - Get lending pool information and APYs
2. **`get_user_positions`** - Get user lending and borrowing positions
3. **`get_asset_data`** - Get detailed information about a specific asset
4. **`get_flash_loan_info`** - Get flash loan information and fees
5. **`get_interest_rates`** - Get current interest rates for all assets
6. **`get_historical_data`** - Get historical APY and utilization data
7. **`get_risk_analysis`** - Get risk analysis for user positions or assets
8. **`get_cross_chain_data`** - Get Aave data across multiple networks

### Supported Networks

- **Ethereum** (mainnet)
- **Polygon**
- **Avalanche**
- **Arbitrum One**
- **Optimism**
- **Fantom**

## Usage Examples

### Get Pool Data
```python
result = await aave.execute(
    action="get_pool_data",
    network="ethereum"
)
```

### Get User Positions
```python
result = await aave.execute(
    action="get_user_positions",
    user_address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
    network="ethereum"
)
```

### Get Asset Data
```python
result = await aave.execute(
    action="get_asset_data",
    asset="USDC",
    network="ethereum"
)
```

### Get Flash Loan Information
```python
result = await aave.execute(
    action="get_flash_loan_info",
    asset="USDC",
    amount="1000000"
)
```

### Get Interest Rates
```python
result = await aave.execute(
    action="get_interest_rates",
    network="ethereum"
)
```

### Get Historical Data
```python
result = await aave.execute(
    action="get_historical_data",
    asset="USDC",
    days=30,
    network="ethereum"
)
```

### Get Risk Analysis
```python
# For user positions
result = await aave.execute(
    action="get_risk_analysis",
    user_address="0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
    network="ethereum"
)

# For asset analysis
result = await aave.execute(
    action="get_risk_analysis",
    asset="USDC",
    network="ethereum"
)
```

### Get Cross-Chain Data
```python
result = await aave.execute(
    action="get_cross_chain_data",
    networks=["ethereum", "polygon", "avalanche"]
)
```

## Response Format

### Success Response
```json
{
    "success": true,
    "network": "ethereum",
    "data": {
        "total_tvl": "$1,234,567,890.12",
        "total_reserves": 25,
        "reserves": [...],
        "timestamp": "2024-01-15T10:30:00"
    }
}
```

### Error Response
```json
{
    "success": false,
    "error": "Failed to get pool data: Connection timeout"
}
```

## Key Data Points

### Pool Data
- **Total TVL** - Total Value Locked across all reserves
- **Reserve Count** - Number of active lending pools
- **Individual Reserve Data**:
  - Symbol and name
  - Total and available liquidity
  - Variable and stable debt
  - Interest rates (liquidity, variable borrow, stable borrow)
  - Utilization rate
  - Collateral settings
  - Liquidation parameters

### User Positions
- **Health Factor** - Risk metric for user positions
- **Total Collateral** - USD value of deposited assets
- **Total Debt** - USD value of borrowed assets
- **Available Borrows** - Maximum additional borrowing capacity
- **Deposits** - List of deposited assets with balances and rates
- **Borrows** - List of borrowed assets with debt amounts and rates

### Asset Data
- **Token Information** - Symbol, name, decimals, addresses
- **Liquidity Metrics** - Total and available liquidity
- **Debt Metrics** - Variable and stable debt amounts
- **Interest Rates** - Current rates for lending and borrowing
- **Risk Parameters** - Liquidation threshold, bonus, reserve factor
- **Utilization Rate** - Current pool utilization percentage

### Flash Loan Information
- **Fee Rate** - Standard 0.09% fee for most assets
- **Fee Amount** - Calculated fee for specified amount
- **Total Repayment** - Amount including fee
- **Requirements** - Flash loan execution requirements
- **Supported Assets** - List of assets available for flash loans

### Risk Analysis
- **Health Factor Assessment** - Risk level based on health factor
- **Liquidation Risk** - Probability of liquidation
- **Recommendations** - Actionable risk management advice
- **Utilization Risk** - Asset-specific utilization analysis

## Integration

### Router Registration
The `AaveTool` is automatically registered in the MCP router as `"aave"`:

```python
self.local_tools = {
    # ... other tools ...
    "aave": AaveTool()
}
```

### API Endpoints
- **Aave V3 API**: `https://api.aave.com/v3`
- **The Graph Subgraph**: `https://api.thegraph.com/subgraphs/name/aave/protocol-v3`

## Testing

### Individual Tool Testing
```bash
python scripts/test_aave_tool.py
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
4. **Graceful Degradation** - Continues operation even if some data is unavailable

## Notes

- **Real Data**: The tool uses real Aave V3 API data, not mock data
- **Cross-Chain**: Supports multiple blockchain networks
- **Historical Data**: Sample historical data is provided (real historical data would require additional API endpoints)
- **Session Management**: Implements proper aiohttp session management for efficient API calls
- **Risk Assessment**: Provides comprehensive risk analysis for both users and assets
