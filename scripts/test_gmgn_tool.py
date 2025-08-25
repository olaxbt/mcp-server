#!/usr/bin/env python3
"""
Test script for GMGNTool
Tests all available actions of the GMGNTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import GMGNTool

async def test_gmgn_tool():
    """Test all GMGNTool actions"""
    print("🧪 Testing GMGNTool...")
    print("=" * 50)
    
    gmgn = GMGNTool()
    
    # Test 1: Get gaming token analysis
    print("\n1. Testing get_gaming_token_analysis...")
    result = await gmgn.execute({"action": "get_gaming_token_analysis", "token": "AXS", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 2: Get P2E analytics
    print("\n2. Testing get_p2e_analytics...")
    result = await gmgn.execute({"action": "get_p2e_analytics", "game": "Axie Infinity", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 3: Get gaming NFT markets
    print("\n3. Testing get_gaming_nft_markets...")
    result = await gmgn.execute({"action": "get_gaming_nft_markets", "limit": 5, "category": "p2e", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 4: Get gaming community insights
    print("\n4. Testing get_gaming_community_insights...")
    result = await gmgn.execute({"action": "get_gaming_community_insights", "token": "SAND", "limit": 5})
    print(f"Result: {result}")
    
    # Test 5: Get gaming project ratings
    print("\n5. Testing get_gaming_project_ratings...")
    result = await gmgn.execute({"action": "get_gaming_project_ratings", "game": "The Sandbox", "limit": 5})
    print(f"Result: {result}")
    
    # Test 6: Get gaming industry trends
    print("\n6. Testing get_gaming_industry_trends...")
    result = await gmgn.execute({"action": "get_gaming_industry_trends", "limit": 5, "timeframe": "24h", "category": "metaverse"})
    print(f"Result: {result}")
    
    # Test 7: Get gaming token discovery
    print("\n7. Testing get_gaming_token_discovery...")
    result = await gmgn.execute({"action": "get_gaming_token_discovery", "limit": 5, "category": "nft", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 8: Get gaming investment analysis
    print("\n8. Testing get_gaming_investment_analysis...")
    result = await gmgn.execute({"action": "get_gaming_investment_analysis", "token": "MANA", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 9: Get gaming community insights with game parameter
    print("\n9. Testing get_gaming_community_insights with game...")
    result = await gmgn.execute({"action": "get_gaming_community_insights", "game": "Decentraland", "limit": 5})
    print(f"Result: {result}")
    
    # Test 10: Error handling - missing token/game
    print("\n10. Testing error handling (missing token/game)...")
    result = await gmgn.execute({"action": "get_gaming_token_analysis"})
    print(f"Result: {result}")
    
    # Test 11: Error handling - invalid action
    print("\n11. Testing error handling (invalid action)...")
    result = await gmgn.execute({"action": "invalid_action"})
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ GMGNTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_gmgn_tool())
