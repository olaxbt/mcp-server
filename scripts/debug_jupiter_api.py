import asyncio
import aiohttp
import json
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def debug_jupiter_api():
    """Debug Jupiter API responses to understand the data structure"""
    print("🔍 Debugging Jupiter API Responses")
    print("=" * 50)
    
    jupiter_base_url = "https://quote-api.jup.ag/v6"
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Get quote
        print("\n1. Testing quote endpoint...")
        url = f"{jupiter_base_url}/quote"
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",  # SOL
            "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
            "amount": "1000000000",  # 1 SOL
            "slippageBps": 50,
            "onlyDirectRoutes": "false",
            "asLegacyTransaction": "false"
        }
        
        async with session.get(url, params=params) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print("Raw response structure:")
                print(json.dumps(data, indent=2)[:1000] + "..." if len(json.dumps(data, indent=2)) > 1000 else json.dumps(data, indent=2))
                
                # Analyze data types
                if "data" in data:
                    quote_data = data["data"]
                    print(f"\nQuote data type: {type(quote_data)}")
                    if isinstance(quote_data, dict):
                        for key, value in quote_data.items():
                            print(f"  {key}: {type(value)} = {value}")
        
        # Test 2: Get tokens
        print("\n2. Testing tokens endpoint...")
        tokens_url = "https://token.jup.ag/all"
        
        async with session.get(tokens_url) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print("Tokens response structure:")
                print(f"Type: {type(data)}")
                if isinstance(data, dict):
                    for key, value in data.items():
                        print(f"  {key}: {type(value)}")
                        if key == "tokens" and isinstance(value, list) and len(value) > 0:
                            print(f"    First token: {type(value[0])} = {value[0]}")
                elif isinstance(data, list):
                    print(f"  List length: {len(data)}")
                    if len(data) > 0:
                        print(f"  First item: {type(data[0])} = {data[0]}")

if __name__ == "__main__":
    asyncio.run(debug_jupiter_api())
