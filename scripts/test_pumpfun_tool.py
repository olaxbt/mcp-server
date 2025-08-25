#!/usr/bin/env python3
"""
Test script for PumpFunTool
Tests all available actions of the PumpFunTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import PumpFunTool

async def test_pumpfun_tool():
    """Test all PumpFunTool actions"""
    print("🧪 Testing PumpFunTool...")
    print("=" * 50)
    
    pumpfun = PumpFunTool()
    
    # Test 1: Get pump detection
    print("\n1. Testing get_pump_detection...")
    result = await pumpfun.execute({"action": "get_pump_detection", "symbol": "BTC", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 2: Get social sentiment
    print("\n2. Testing get_social_sentiment...")
    result = await pumpfun.execute({"action": "get_social_sentiment", "symbol": "ETH", "timeframe": "24h", "platform": "all"})
    print(f"Result: {result}")
    
    # Test 3: Get market trends
    print("\n3. Testing get_market_trends...")
    result = await pumpfun.execute({"action": "get_market_trends", "limit": 5, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 4: Get volume analysis
    print("\n4. Testing get_volume_analysis...")
    result = await pumpfun.execute({"action": "get_volume_analysis", "symbol": "DOGE", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 5: Get community insights
    print("\n5. Testing get_community_insights...")
    result = await pumpfun.execute({"action": "get_community_insights", "symbol": "BTC", "limit": 5})
    print(f"Result: {result}")
    
    # Test 6: Get alert system
    print("\n6. Testing get_alert_system...")
    result = await pumpfun.execute({"action": "get_alert_system", "limit": 5, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 7: Get portfolio monitoring
    print("\n7. Testing get_portfolio_monitoring...")
    result = await pumpfun.execute({"action": "get_portfolio_monitoring", "symbols": ["BTC", "ETH", "DOGE"], "limit": 5})
    print(f"Result: {result}")
    
    # Test 8: Get risk assessment
    print("\n8. Testing get_risk_assessment...")
    result = await pumpfun.execute({"action": "get_risk_assessment", "symbol": "SOL", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 9: Get social sentiment with specific platform
    print("\n9. Testing get_social_sentiment with Twitter...")
    result = await pumpfun.execute({"action": "get_social_sentiment", "symbol": "ADA", "timeframe": "24h", "platform": "twitter"})
    print(f"Result: {result}")
    
    # Test 10: Error handling - missing symbol
    print("\n10. Testing error handling (missing symbol)...")
    result = await pumpfun.execute({"action": "get_pump_detection"})
    print(f"Result: {result}")
    
    # Test 11: Error handling - invalid action
    print("\n11. Testing error handling (invalid action)...")
    result = await pumpfun.execute({"action": "invalid_action"})
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ PumpFunTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_pumpfun_tool())
