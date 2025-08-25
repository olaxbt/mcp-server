# Currency Converter Tool

The `CurrencyConverterTool` provides comprehensive currency conversion capabilities, supporting both fiat currencies and cryptocurrencies with real-time exchange rates.

## Features

### 🔄 Currency Conversion
- **Fiat to Fiat**: Convert between traditional currencies (USD, EUR, GBP, etc.)
- **Fiat to Crypto**: Convert fiat currencies to cryptocurrencies
- **Crypto to Fiat**: Convert cryptocurrencies to fiat currencies
- **Crypto to Crypto**: Convert between different cryptocurrencies

### 📊 Exchange Rate Data
- Real-time exchange rates from multiple sources
- Historical exchange rate data
- Current cryptocurrency prices and market data
- Support for 40+ fiat currencies and 20+ cryptocurrencies

### 🌐 Multi-Source Integration
- **Exchange Rate API**: For fiat currency conversions
- **CoinGecko API**: For cryptocurrency data and conversions

## Supported Actions

### 1. `convert`
Convert between different currencies.

**Parameters:**
- `from_currency` (string): Source currency code (e.g., "USD", "EUR", "BTC")
- `to_currency` (string): Target currency code (e.g., "EUR", "JPY", "ETH")
- `amount` (number): Amount to convert (default: 1.0)

**Example:**
```json
{
  "action": "convert",
  "from_currency": "USD",
  "to_currency": "EUR",
  "amount": 100
}
```

### 2. `get_exchange_rates`
Get current exchange rates for a base currency.

**Parameters:**
- `base_currency` (string): Base currency for rates (default: "USD")

**Example:**
```json
{
  "action": "get_exchange_rates",
  "base_currency": "USD"
}
```

### 3. `get_supported_currencies`
Get list of supported currencies.

**Example:**
```json
{
  "action": "get_supported_currencies"
}
```

### 4. `get_historical_rates`
Get historical exchange rates.

**Parameters:**
- `base_currency` (string): Base currency (default: "USD")
- `to_currency` (string): Target currency (default: "EUR")
- `date` (string): Date in YYYY-MM-DD format

**Example:**
```json
{
  "action": "get_historical_rates",
  "base_currency": "USD",
  "to_currency": "EUR",
  "date": "2024-01-01"
}
```

### 5. `get_crypto_rates`
Get current cryptocurrency rates and market data.

**Example:**
```json
{
  "action": "get_crypto_rates"
}
```

## Supported Currencies

### Fiat Currencies (40+)
- USD, EUR, GBP, JPY, AUD, CAD, CHF, CNY, SEK, NZD
- MXN, SGD, HKD, NOK, KRW, TRY, RUB, INR, BRL, ZAR
- PLN, THB, IDR, MYR, PHP, CZK, HUF, ILS, CLP, COP
- EGP, PKR, BDT, VND, NGN, ARS, PEN, UAH, RON, BGN

### Cryptocurrencies (20+)
- BTC, ETH, USDT, USDC, BNB, XRP, ADA, SOL, DOT, DOGE
- AVAX, MATIC, LINK, UNI, LTC, BCH, XLM, ATOM, ETC, FIL

## Usage Examples

### Basic Fiat Conversion
```python
# Convert 100 USD to EUR
result = await tool.execute({
    "action": "convert",
    "from_currency": "USD",
    "to_currency": "EUR",
    "amount": 100
})
```

### Fiat to Crypto Conversion
```python
# Convert 1000 USD to Bitcoin
result = await tool.execute({
    "action": "convert",
    "from_currency": "USD",
    "to_currency": "BTC",
    "amount": 1000
})
```

### Crypto to Crypto Conversion
```python
# Convert 0.01 BTC to ETH
result = await tool.execute({
    "action": "convert",
    "from_currency": "BTC",
    "to_currency": "ETH",
    "amount": 0.01
})
```

### Get Current Exchange Rates
```python
# Get all exchange rates for USD
result = await tool.execute({
    "action": "get_exchange_rates",
    "base_currency": "USD"
})
```

### Get Cryptocurrency Market Data
```python
# Get top 20 cryptocurrencies by market cap
result = await tool.execute({
    "action": "get_crypto_rates"
})
```

## Response Format

### Successful Conversion Response
```json
{
  "success": true,
  "data": {
    "from_currency": "USD",
    "to_currency": "EUR",
    "amount": 100,
    "converted_amount": 92.45,
    "exchange_rate": 0.9245,
    "last_updated": "2024-01-15",
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

### Crypto Conversion Response
```json
{
  "success": true,
  "data": {
    "from_currency": "USD",
    "to_currency": "BTC",
    "amount": 1000,
    "converted_amount": 0.02345678,
    "usd_amount": 1000,
    "crypto_rate": 42650.50,
    "final_rate": 0.00002345,
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

## Error Handling

The tool provides comprehensive error handling for:
- Invalid currency codes
- API service unavailability
- Network connectivity issues
- Invalid parameters

### Error Response Format
```json
{
  "success": false,
  "error": "Currency EUR not found in exchange rates"
}
```

## Rate Limits and Caching

- **API Rate Limits**: Respects rate limits of external APIs
- **Caching**: Implements caching to reduce API calls
- **Fallback**: Graceful handling of API failures

## Dependencies

- `aiohttp`: For asynchronous HTTP requests
- `asyncio`: For asynchronous operations
- External APIs:
  - Exchange Rate API (for fiat currencies)
  - CoinGecko API (for cryptocurrencies)

## Testing

Run the test script to verify functionality:
```bash
python scripts/test_currency_converter_tool.py
```

## Notes

- Exchange rates are updated in real-time
- Cryptocurrency prices may have slight delays
- Historical rates may vary by API provider
- All conversions are calculated using current market rates
- The tool supports both uppercase and lowercase currency codes
