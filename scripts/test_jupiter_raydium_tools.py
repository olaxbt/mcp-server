#!/usr/bin/env python3
"""
Test script for Jupiter and Raydium tools
Tests the new Solana DeFi tools with real API data
"""

import asyncio
import sys
import os
import json

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import JupiterTool, RaydiumTool

async def test_jupiter_tool():
    """Test Jupiter DEX aggregator tool"""
    print("🔍 Testing Jupiter Tool...")
    print("=" * 50)
    
    jupiter = JupiterTool()
    
    # Test 1: Get quote
    print("\n1. Testing get_quote...")
    try:
        result = await jupiter._get_quote({
            "input_mint": "So11111111111111111111111111111111111111112",  # SOL
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
            "amount": "1000000000",  # 1 SOL
            "slippage_bps": 50
        })
        print("✅ Quote result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting quote: {e}")
    
    # Test 2: Get routes
    print("\n2. Testing get_routes...")
    try:
        result = await jupiter._get_routes({
            "input_mint": "So11111111111111111111111111111111111111112",  # SOL
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
            "amount": "1000000000"  # 1 SOL
        })
        print("✅ Routes result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting routes: {e}")
    
    # Test 3: Get tokens
    print("\n3. Testing get_tokens...")
    try:
        result = await jupiter._get_tokens()
        print("✅ Tokens result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting tokens: {e}")
    
    # Test 4: Get pools
    print("\n4. Testing get_pools...")
    try:
        result = await jupiter._get_pools({
            "input_mint": "So11111111111111111111111111111111111111112",  # SOL
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
        })
        print("✅ Pools result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting pools: {e}")
    
    # Test 5: Cross-chain quote
    print("\n5. Testing cross_chain_quote...")
    try:
        result = await jupiter._get_cross_chain_quote({
            "source_chain": "solana",
            "destination_chain": "ethereum",
            "amount": "1000000000"  # 1 SOL
        })
        print("✅ Cross-chain quote result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting cross-chain quote: {e}")

async def test_raydium_tool():
    """Test Raydium DEX tool"""
    print("\n\n🔍 Testing Raydium Tool...")
    print("=" * 50)
    
    raydium = RaydiumTool()
    
    # Test 1: Get pools
    print("\n1. Testing get_pools...")
    try:
        result = await raydium._get_pools({
            "limit": 5,
            "sort_by": "tvl"
        })
        print("✅ Pools result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting pools: {e}")
    
    # Test 2: Get farms
    print("\n2. Testing get_farms...")
    try:
        result = await raydium._get_farms({
            "limit": 5
        })
        print("✅ Farms result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting farms: {e}")
    
    # Test 3: Get staking
    print("\n3. Testing get_staking...")
    try:
        result = await raydium._get_staking({
            "token_mint": "So11111111111111111111111111111111111111112"  # SOL
        })
        print("✅ Staking result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting staking: {e}")
    
    # Test 4: Get tokens
    print("\n4. Testing get_tokens...")
    try:
        result = await raydium._get_tokens()
        print("✅ Tokens result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting tokens: {e}")
    
    # Test 5: Get yield opportunities
    print("\n5. Testing get_yield_opportunities...")
    try:
        result = await raydium._get_yield_opportunities({
            "limit": 5
        })
        print("✅ Yield opportunities result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error getting yield opportunities: {e}")

async def test_tool_execution():
    """Test the main execute method for both tools"""
    print("\n\n🔍 Testing Tool Execution...")
    print("=" * 50)
    
    jupiter = JupiterTool()
    raydium = RaydiumTool()
    
    # Test Jupiter execute
    print("\n1. Testing Jupiter execute...")
    try:
        result = await jupiter.execute({
            "action": "get_quote",
            "input_mint": "So11111111111111111111111111111111111111112",
            "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            "amount": "1000000000"
        })
        print("✅ Jupiter execute result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error in Jupiter execute: {e}")
    
    # Test Raydium execute
    print("\n2. Testing Raydium execute...")
    try:
        result = await raydium.execute({
            "action": "get_pools",
            "limit": 3,
            "sort_by": "apy"
        })
        print("✅ Raydium execute result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error in Raydium execute: {e}")

async def main():
    """Main test function"""
    print("🚀 Starting Jupiter and Raydium Tools Test")
    print("=" * 60)
    
    # Test Jupiter tool
    await test_jupiter_tool()
    
    # Test Raydium tool
    await test_raydium_tool()
    
    # Test tool execution
    await test_tool_execution()
    
    print("\n\n✅ Jupiter and Raydium Tools Test Completed!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
