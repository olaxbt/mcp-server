#!/usr/bin/env python3
"""
Test script for PumpNewsTool
Tests all available actions of the PumpNewsTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import PumpNewsTool

async def test_pumpnews_tool():
    """Test all PumpNewsTool actions"""
    print("🧪 Testing PumpNewsTool...")
    print("=" * 50)
    
    pumpnews = PumpNewsTool()
    
    # Test 1: Get news
    print("\n1. Testing get_news...")
    result = await pumpnews.execute({"action": "get_news", "limit": 5})
    print(f"Result: {result}")
    
    # Test 2: Get pump detection
    print("\n2. Testing get_pump_detection...")
    result = await pumpnews.execute({"action": "get_pump_detection", "symbol": "BTC", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 3: Get social sentiment
    print("\n3. Testing get_social_sentiment...")
    result = await pumpnews.execute({"action": "get_social_sentiment", "symbol": "ETH", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 4: Get market alerts
    print("\n4. Testing get_market_alerts...")
    result = await pumpnews.execute({"action": "get_market_alerts", "limit": 5, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 5: Get trending coins
    print("\n5. Testing get_trending_coins...")
    result = await pumpnews.execute({"action": "get_trending_coins", "limit": 5, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 6: Get volume analysis
    print("\n6. Testing get_volume_analysis...")
    result = await pumpnews.execute({"action": "get_volume_analysis", "symbol": "DOGE", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 7: Get community insights
    print("\n7. Testing get_community_insights...")
    result = await pumpnews.execute({"action": "get_community_insights", "symbol": "BTC", "limit": 5})
    print(f"Result: {result}")
    
    # Test 8: Get portfolio alerts
    print("\n8. Testing get_portfolio_alerts...")
    result = await pumpnews.execute({"action": "get_portfolio_alerts", "symbols": ["BTC", "ETH", "DOGE"], "limit": 5})
    print(f"Result: {result}")
    
    # Test 9: Get news with category filter
    print("\n9. Testing get_news with category...")
    result = await pumpnews.execute({"action": "get_news", "category": "breaking", "limit": 3})
    print(f"Result: {result}")
    
    # Test 10: Error handling - missing symbol
    print("\n10. Testing error handling (missing symbol)...")
    result = await pumpnews.execute({"action": "get_pump_detection"})
    print(f"Result: {result}")
    
    # Test 11: Error handling - invalid action
    print("\n11. Testing error handling (invalid action)...")
    result = await pumpnews.execute({"action": "invalid_action"})
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ PumpNewsTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_pumpnews_tool())
