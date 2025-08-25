#!/usr/bin/env python3
"""
Test script for CurrencyConverterTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools.currency_tools import CurrencyConverterTool


async def test_currency_converter():
    """Test the CurrencyConverterTool functionality."""
    
    print("🧪 Testing CurrencyConverterTool...")
    print("=" * 50)
    
    tool = CurrencyConverterTool()
    
    # Test 1: Get supported currencies
    print("\n1. Testing get_supported_currencies...")
    result = await tool.execute({"action": "get_supported_currencies"})
    print(f"Result: {result[0]}")
    
    # Test 2: Convert USD to EUR
    print("\n2. Testing USD to EUR conversion...")
    result = await tool.execute({
        "action": "convert",
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 100
    })
    print(f"Result: {result[0]}")
    
    # Test 3: Convert EUR to USD
    print("\n3. Testing EUR to USD conversion...")
    result = await tool.execute({
        "action": "convert",
        "from_currency": "EUR",
        "to_currency": "USD",
        "amount": 50
    })
    print(f"Result: {result[0]}")
    
    # Test 4: Convert USD to BTC (fiat to crypto)
    print("\n4. Testing USD to BTC conversion...")
    result = await tool.execute({
        "action": "convert",
        "from_currency": "USD",
        "to_currency": "BTC",
        "amount": 1000
    })
    print(f"Result: {result[0]}")
    
    # Test 5: Convert BTC to USD (crypto to fiat)
    print("\n5. Testing BTC to USD conversion...")
    result = await tool.execute({
        "action": "convert",
        "from_currency": "BTC",
        "to_currency": "USD",
        "amount": 0.1
    })
    print(f"Result: {result[0]}")
    
    # Test 6: Convert BTC to ETH (crypto to crypto)
    print("\n6. Testing BTC to ETH conversion...")
    result = await tool.execute({
        "action": "convert",
        "from_currency": "BTC",
        "to_currency": "ETH",
        "amount": 0.01
    })
    print(f"Result: {result[0]}")
    
    # Test 7: Get exchange rates for USD
    print("\n7. Testing get_exchange_rates for USD...")
    result = await tool.execute({
        "action": "get_exchange_rates",
        "base_currency": "USD"
    })
    print(f"Result: {result[0]}")
    
    # Test 8: Get crypto rates
    print("\n8. Testing get_crypto_rates...")
    result = await tool.execute({"action": "get_crypto_rates"})
    print(f"Result: {result[0]}")
    
    # Test 9: Get historical rates
    print("\n9. Testing get_historical_rates...")
    result = await tool.execute({
        "action": "get_historical_rates",
        "base_currency": "USD",
        "to_currency": "EUR",
        "date": "2024-01-01"
    })
    print(f"Result: {result[0]}")
    
    # Test 10: Convert with different amounts
    print("\n10. Testing various conversion amounts...")
    amounts = [1, 10, 100, 1000, 10000]
    for amount in amounts:
        result = await tool.execute({
            "action": "convert",
            "from_currency": "USD",
            "to_currency": "EUR",
            "amount": amount
        })
        if result[0].get("success"):
            data = result[0]["data"]
            print(f"${amount} USD = {data['converted_amount']} EUR (Rate: {data['exchange_rate']})")
    
    print("\n✅ CurrencyConverterTool tests completed!")


if __name__ == "__main__":
    asyncio.run(test_currency_converter())
