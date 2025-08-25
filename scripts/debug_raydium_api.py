import asyncio
import aiohttp
import json
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def debug_raydium_api():
    """Debug Raydium API endpoints to find the correct ones"""
    print("🔍 Debugging Raydium API Endpoints")
    print("=" * 50)
    
    base_url = "https://api.raydium.io"
    
    # Test various endpoints
    endpoints = [
        "/pools",
        "/tokens",
        "/farms", 
        "/staking",
        "/yield",
        "/liquidity",
        "/stats",
        "/info",
        "/api/pools",
        "/api/farms",
        "/api/tokens"
    ]
    
    async with aiohttp.ClientSession() as session:
        print(f"\n🔍 Testing base URL: {base_url}")
        print("-" * 40)
        
        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                async with session.get(url) as response:
                    print(f"  {endpoint}: {response.status}")
                    if response.status == 200:
                        data = await response.json()
                        if isinstance(data, dict):
                            print(f"    Keys: {list(data.keys())[:5]}...")
                        elif isinstance(data, list):
                            print(f"    List length: {len(data)}")
                            if len(data) > 0 and isinstance(data[0], dict):
                                print(f"    First item keys: {list(data[0].keys())[:5]}...")
                        else:
                            print(f"    Type: {type(data)}")
                    elif response.status == 404:
                        print(f"    ❌ 404 Not Found")
                    else:
                        print(f"    ❌ {response.status}")
            except Exception as e:
                print(f"  {endpoint}: ❌ Error - {str(e)[:50]}...")
        
        # Test the working pools endpoint in detail
        print(f"\n🔍 Detailed analysis of /pools endpoint:")
        print("-" * 40)
        try:
            async with session.get(f"{base_url}/pools") as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 0:
                        first_pool = data[0]
                        print(f"First pool structure:")
                        print(json.dumps(first_pool, indent=2)[:500] + "..." if len(json.dumps(first_pool, indent=2)) > 500 else json.dumps(first_pool, indent=2))
        except Exception as e:
            print(f"Error analyzing pools: {e}")

if __name__ == "__main__":
    asyncio.run(debug_raydium_api())
