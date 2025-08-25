#!/usr/bin/env python3
"""
Test script for MerklTool
Tests all available actions of the MerklTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import MerklTool

async def test_merkl_tool():
    """Test all MerklTool actions"""
    print("🧪 Testing MerklTool...")
    print("=" * 50)
    
    merkl = MerklTool()
    
    # Test 1: Get concentrated positions
    print("\n1. Testing get_concentrated_positions...")
    result = await merkl.execute({"action": "get_concentrated_positions", "chain": "ethereum", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 2: Get yield farming opportunities
    print("\n2. Testing get_yield_farming_opportunities...")
    result = await merkl.execute({"action": "get_yield_farming_opportunities", "chain": "ethereum", "min_apy": 5.0, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 3: Get rewards distribution
    print("\n3. Testing get_rewards_distribution...")
    result = await merkl.execute({"action": "get_rewards_distribution", "chain": "ethereum", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 4: Get protocol analytics
    print("\n4. Testing get_protocol_analytics...")
    result = await merkl.execute({"action": "get_protocol_analytics", "chain": "ethereum", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 5: Get position performance
    print("\n5. Testing get_position_performance...")
    result = await merkl.execute({"action": "get_position_performance", "chain": "ethereum", "pool_address": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 6: Get liquidity pools
    print("\n6. Testing get_liquidity_pools...")
    result = await merkl.execute({"action": "get_liquidity_pools", "chain": "ethereum", "limit": 5, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 7: Get user positions
    print("\n7. Testing get_user_positions...")
    result = await merkl.execute({"action": "get_user_positions", "chain": "ethereum", "user_address": "0x742d35cc6634c0532925a3b8d4c9db96c4b4d8b6", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 8: Get rewards calculation
    print("\n8. Testing get_rewards_calculation...")
    result = await merkl.execute({"action": "get_rewards_calculation", "chain": "ethereum", "token": "USDC", "amount": 1000, "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 9: Get concentrated positions with token filter
    print("\n9. Testing get_concentrated_positions with token...")
    result = await merkl.execute({"action": "get_concentrated_positions", "chain": "ethereum", "token": "WETH", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 10: Get rewards distribution with token filter
    print("\n10. Testing get_rewards_distribution with token...")
    result = await merkl.execute({"action": "get_rewards_distribution", "chain": "ethereum", "token": "USDC", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 11: Error handling - missing user_address
    print("\n11. Testing error handling (missing user_address)...")
    result = await merkl.execute({"action": "get_user_positions", "chain": "ethereum"})
    print(f"Result: {result}")
    
    # Test 12: Error handling - missing pool_address and user_address
    print("\n12. Testing error handling (missing pool_address and user_address)...")
    result = await merkl.execute({"action": "get_position_performance", "chain": "ethereum"})
    print(f"Result: {result}")
    
    # Test 13: Error handling - invalid action
    print("\n13. Testing error handling (invalid action)...")
    result = await merkl.execute({"action": "invalid_action"})
    print(f"Result: {result}")
    
    # Test 14: Test different chains
    print("\n14. Testing different chains (Polygon)...")
    result = await merkl.execute({"action": "get_protocol_analytics", "chain": "polygon", "timeframe": "24h"})
    print(f"Result: {result}")
    
    # Test 15: Test different timeframes
    print("\n15. Testing different timeframes (7d)...")
    result = await merkl.execute({"action": "get_yield_farming_opportunities", "chain": "ethereum", "timeframe": "7d"})
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ MerklTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_merkl_tool())
