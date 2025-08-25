#!/usr/bin/env python3
"""
Test script for NFT Marketplace Tool
Demonstrates real API integrations with OpenSea and Magic Eden
"""

import asyncio
import json
import os
from typing import Dict, Any

# Import the NFT tool
from app.mcp.tools import NFTMarketplaceTool

async def test_ethereum_collections():
    """Test Ethereum NFT collections via OpenSea"""
    print("\n=== Testing Ethereum Collections (OpenSea) ===")
    tool = NFTMarketplaceTool()
    
    # Popular Ethereum collections to test
    collections = [
        "bored-ape-yacht-club",
        "cryptopunks",
        "doodles-official",
        "azuki"
    ]
    
    for collection in collections:
        print(f"\n--- Testing {collection} ---")
        
        try:
            # Get collection info
            result = await tool.execute({
                "action": "collection_info",
                "collection_slug": collection,
                "chain": "ethereum"
            })
            print(f"Collection Info: {json.dumps(result, indent=2)}")
            
            # Get floor price
            result = await tool.execute({
                "action": "floor_price",
                "collection_slug": collection,
                "chain": "ethereum"
            })
            print(f"Floor Price: {json.dumps(result, indent=2)}")
            
            # Small delay to respect rate limits
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error testing {collection}: {e}")

async def test_solana_collections():
    """Test Solana NFT collections via Magic Eden"""
    print("\n=== Testing Solana Collections (Magic Eden) ===")
    tool = NFTMarketplaceTool()
    
    # Popular Solana collections to test
    collections = [
        "degen-ape-academy",
        "okay-bears",
        "y00ts",
        "taiyo-robotics"
    ]
    
    for collection in collections:
        print(f"\n--- Testing {collection} ---")
        
        try:
            # Get collection info
            result = await tool.execute({
                "action": "collection_info",
                "collection_slug": collection,
                "chain": "solana"
            })
            print(f"Collection Info: {json.dumps(result, indent=2)}")
            
            # Get floor price
            result = await tool.execute({
                "action": "floor_price",
                "collection_slug": collection,
                "chain": "solana"
            })
            print(f"Floor Price: {json.dumps(result, indent=2)}")
            
            # Small delay to respect rate limits
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error testing {collection}: {e}")

async def test_comprehensive_stats():
    """Test comprehensive collection statistics"""
    print("\n=== Testing Comprehensive Collection Stats ===")
    tool = NFTMarketplaceTool()
    
    # Test comprehensive stats for a popular collection
    try:
        result = await tool.execute({
            "action": "collection_stats",
            "collection_slug": "bored-ape-yacht-club",
            "chain": "ethereum"
        })
        print(f"Comprehensive Stats: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error getting comprehensive stats: {e}")

async def test_recent_sales():
    """Test recent sales functionality"""
    print("\n=== Testing Recent Sales ===")
    tool = NFTMarketplaceTool()
    
    try:
        # Get recent sales for BAYC
        result = await tool.execute({
            "action": "recent_sales",
            "collection_slug": "bored-ape-yacht-club",
            "chain": "ethereum",
            "limit": 5
        })
        print(f"Recent Sales (BAYC): {json.dumps(result, indent=2)}")
        
        # Get recent sales for Solana collection
        result = await tool.execute({
            "action": "recent_sales",
            "collection_slug": "degen-ape-academy",
            "chain": "solana",
            "limit": 3
        })
        print(f"Recent Sales (DAA): {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"Error getting recent sales: {e}")

async def test_trading_volume():
    """Test trading volume functionality"""
    print("\n=== Testing Trading Volume ===")
    tool = NFTMarketplaceTool()
    
    time_periods = ["1d", "7d", "30d"]
    
    for period in time_periods:
        try:
            result = await tool.execute({
                "action": "trading_volume",
                "collection_slug": "bored-ape-yacht-club",
                "chain": "ethereum",
                "time_period": period
            })
            print(f"Trading Volume ({period}): {json.dumps(result, indent=2)}")
            
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error getting trading volume for {period}: {e}")

async def main():
    """Run all NFT marketplace tests"""
    print("🚀 Starting NFT Marketplace Tool Tests")
    print("=" * 50)
    
    # Check for API keys
    if os.getenv("OPENSEA_API_KEY"):
        print("✅ OpenSea API key found")
    else:
        print("⚠️  No OpenSea API key found - will use rate-limited access")
    
    try:
        # Run all tests
        await test_ethereum_collections()
        await test_solana_collections()
        await test_comprehensive_stats()
        await test_recent_sales()
        await test_trading_volume()
        
        print("\n✅ All NFT marketplace tests completed!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
