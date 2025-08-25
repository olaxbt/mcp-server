#!/usr/bin/env python3
"""
Test script for CoinDeskTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import CoinDeskTool

async def test_coindesk_tool():
    """Test the CoinDeskTool with various actions."""
    print("Testing CoinDeskTool...")
    print("=" * 50)
    
    tool = CoinDeskTool()
    
    # Test 1: Get current Bitcoin price
    print("\n1. Testing get_current_price (USD):")
    result = await tool.execute(action="get_current_price", currency="USD")
    print(f"Result: {result}")
    
    # Test 2: Get current Bitcoin price in EUR
    print("\n2. Testing get_current_price (EUR):")
    result = await tool.execute(action="get_current_price", currency="EUR")
    print(f"Result: {result}")
    
    # Test 3: Get historical price data
    print("\n3. Testing get_historical_price:")
    result = await tool.execute(
        action="get_historical_price", 
        currency="USD",
        start_date="2024-01-01",
        end_date="2024-01-15"
    )
    print(f"Result: {result}")
    
    # Test 4: Get Bitcoin Price Index
    print("\n4. Testing get_bitcoin_price_index:")
    result = await tool.execute(action="get_bitcoin_price_index")
    print(f"Result: {result}")
    
    # Test 5: Get supported currencies
    print("\n5. Testing get_supported_currencies:")
    result = await tool.execute(action="get_supported_currencies")
    print(f"Result: {result}")
    
    # Test 6: Get market data
    print("\n6. Testing get_market_data:")
    result = await tool.execute(action="get_market_data")
    print(f"Result: {result}")
    
    # Test 7: Get news
    print("\n7. Testing get_news:")
    result = await tool.execute(action="get_news", limit=3)
    print(f"Result: {result}")
    
    # Test 8: Error handling - unknown action
    print("\n8. Testing error handling (unknown action):")
    result = await tool.execute(action="unknown_action")
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("CoinDeskTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_coindesk_tool())
