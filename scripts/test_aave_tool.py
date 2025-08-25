#!/usr/bin/env python3
"""
Test script for AaveTool
Tests all available actions of the AaveTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import AaveTool

async def test_aave_tool():
    """Test all AaveTool actions"""
    print("🧪 Testing AaveTool...")
    print("=" * 50)
    
    aave = AaveTool()
    
    # Test 1: Get pool data
    print("\n1. Testing get_pool_data...")
    result = await aave.execute({"action": "get_pool_data", "network": "ethereum"})
    print(f"Result: {result}")
    
    # Test 2: Get interest rates
    print("\n2. Testing get_interest_rates...")
    result = await aave.execute({"action": "get_interest_rates", "network": "ethereum"})
    print(f"Result: {result}")
    
    # Test 3: Get asset data
    print("\n3. Testing get_asset_data...")
    result = await aave.execute({"action": "get_asset_data", "asset": "USDC", "network": "ethereum"})
    print(f"Result: {result}")
    
    # Test 4: Get flash loan info
    print("\n4. Testing get_flash_loan_info...")
    result = await aave.execute({"action": "get_flash_loan_info", "asset": "USDC", "amount": "1000000"})
    print(f"Result: {result}")
    
    # Test 5: Get historical data
    print("\n5. Testing get_historical_data...")
    result = await aave.execute({"action": "get_historical_data", "asset": "USDC", "days": 7})
    print(f"Result: {result}")
    
    # Test 6: Get risk analysis for asset
    print("\n6. Testing get_risk_analysis (asset)...")
    result = await aave.execute({"action": "get_risk_analysis", "asset": "USDC", "network": "ethereum"})
    print(f"Result: {result}")
    
    # Test 7: Get cross-chain data
    print("\n7. Testing get_cross_chain_data...")
    result = await aave.execute({"action": "get_cross_chain_data", "networks": ["ethereum", "polygon"]})
    print(f"Result: {result}")
    
    # Test 8: Get user positions (with sample address)
    print("\n8. Testing get_user_positions...")
    sample_address = "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6"  # Sample address
    result = await aave.execute({"action": "get_user_positions", "user_address": sample_address, "network": "ethereum"})
    print(f"Result: {result}")
    
    # Test 9: Get risk analysis for user
    print("\n9. Testing get_risk_analysis (user)...")
    result = await aave.execute({"action": "get_risk_analysis", "user_address": sample_address, "network": "ethereum"})
    print(f"Result: {result}")
    
    # Test 10: Error handling - invalid action
    print("\n10. Testing error handling (invalid action)...")
    result = await aave.execute({"action": "invalid_action"})
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ AaveTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_aave_tool())
