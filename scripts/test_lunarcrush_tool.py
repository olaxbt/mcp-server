#!/usr/bin/env python3
"""
Test script for LunarCrushTool
Tests all available actions with sample data
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import LunarCrushTool

async def test_lunarcrush_tool():
    """Test all LunarCrushTool actions"""
    print("🧪 Testing LunarCrushTool...")
    print("=" * 50)
    
    tool = LunarCrushTool()
    
    # Test 1: Social Sentiment
    print("\n1️⃣ Testing Social Sentiment Analysis...")
    result = await tool.execute({
        "action": "get_social_sentiment",
        "symbol": "BTC",
        "timeframe": "24h"
    })
    print(f"✅ Social Sentiment Result: {result[0].get('type', 'unknown')}")
    if 'note' in result[0]:
        print(f"   📝 Note: {result[0]['note']}")
    elif 'social_score' in result[0]:
        print(f"   📊 Social Score: {result[0]['social_score']}")
    
    # Test 2: Market Intelligence
    print("\n2️⃣ Testing Market Intelligence...")
    result = await tool.execute({
        "action": "get_market_intelligence",
        "symbol": "ETH",
        "timeframe": "24h"
    })
    print(f"✅ Market Intelligence Result: {result[0].get('type', 'unknown')}")
    if 'note' in result[0]:
        print(f"   📝 Note: {result[0]['note']}")
    elif 'price' in result[0]:
        print(f"   💰 Price: ${result[0]['price']:,.2f}")
    
    # Test 3: Influence Analysis
    print("\n3️⃣ Testing Influence Analysis...")
    result = await tool.execute({
        "action": "get_influence_analysis",
        "symbol": "SOL",
        "limit": 5
    })
    print(f"✅ Influence Analysis Result: {result[0].get('type', 'unknown')}")
    if 'note' in result[0]:
        print(f"   📝 Note: {result[0]['note']}")
    elif 'total_influencers' in result[0]:
        print(f"   👥 Total Influencers: {result[0]['total_influencers']}")
    
    # Test 4: Trending Assets
    print("\n4️⃣ Testing Trending Assets...")
    result = await tool.execute({
        "action": "get_trending_assets",
        "limit": 5,
        "timeframe": "24h"
    })
    print(f"✅ Trending Assets Result: {result[0].get('type', 'unknown')}")
    if 'note' in result[0]:
        print(f"   📝 Note: {result[0]['note']}")
    elif 'trending_assets' in result[0]:
        print(f"   📈 Found {len(result[0]['trending_assets'])} trending assets")
    
    # Test 5: Historical Data
    print("\n5️⃣ Testing Historical Data...")
    result = await tool.execute({
        "action": "get_historical_data",
        "symbol": "BTC",
        "timeframe": "7d"
    })
    print(f"✅ Historical Data Result: {result[0].get('type', 'unknown')}")
    if 'note' in result[0]:
        print(f"   📝 Note: {result[0]['note']}")
    elif 'historical_points' in result[0]:
        print(f"   📅 Historical Points: {len(result[0]['historical_points'])}")
    
    # Test 6: Comparative Analysis
    print("\n6️⃣ Testing Comparative Analysis...")
    result = await tool.execute({
        "action": "get_comparative_analysis",
        "symbols": ["BTC", "ETH", "SOL"],
        "timeframe": "24h"
    })
    print(f"✅ Comparative Analysis Result: {result[0].get('type', 'unknown')}")
    if 'note' in result[0]:
        print(f"   📝 Note: {result[0]['note']}")
    elif 'comparison' in result[0]:
        print(f"   🔄 Compared {len(result[0]['comparison'])} assets")
    
    # Test 7: Error handling
    print("\n7️⃣ Testing Error Handling...")
    result = await tool.execute({
        "action": "unknown_action"
    })
    print(f"✅ Error Handling Result: {result[0].get('error', 'no error')}")
    
    print("\n" + "=" * 50)
    print("🎉 LunarCrushTool testing completed!")
    print("\n💡 To use real LunarCrush data, set the LUNARCRUSH_API_KEY environment variable:")
    print("   export LUNARCRUSH_API_KEY=your_api_key_here")

if __name__ == "__main__":
    asyncio.run(test_lunarcrush_tool())
