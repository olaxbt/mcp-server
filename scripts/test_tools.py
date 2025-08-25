#!/usr/bin/env python3
"""
Test script for OLAXBT MCP Server Tools
Demonstrates usage of all implemented tools
"""

import asyncio
import json
from typing import Dict, Any

# Import all tools
from app.mcp.tools import (
    DuckDuckGoSearchTool,
    WebSearchTool,
    CryptoPriceTool,
    DeFiProtocolTool,
    PortfolioTrackerTool,
    CryptoNewsTool,
    NFTMarketplaceTool,
    MarketAnalysisTool,
    NotificationTool,
    APYCalculatorTool
)

async def test_crypto_price_tool():
    """Test cryptocurrency price tool"""
    print("\n=== Testing Crypto Price Tool ===")
    tool = CryptoPriceTool()
    
    # Test Bitcoin price
    result = await tool.execute({
        "coin_id": "bitcoin",
        "vs_currency": "usd",
        "include_market_data": True,
        "include_24hr_change": True
    })
    print(f"Bitcoin Price: {json.dumps(result, indent=2)}")
    
    # Test Ethereum price
    result = await tool.execute({
        "coin_id": "ethereum",
        "vs_currency": "usd"
    })
    print(f"Ethereum Price: {json.dumps(result, indent=2)}")

async def test_defi_protocol_tool():
    """Test DeFi protocol tool"""
    print("\n=== Testing DeFi Protocol Tool ===")
    tool = DeFiProtocolTool()
    
    # Test Meteora pools
    result = await tool.execute({
        "protocol": "meteora",
        "action": "pools"
    })
    print(f"Meteora Pools: {json.dumps(result, indent=2)}")
    
    # Test Jupiter swap quote (mock)
    result = await tool.execute({
        "protocol": "jupiter",
        "action": "swap_quote",
        "input_mint": "So11111111111111111111111111111111111111112",  # SOL
        "output_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
        "amount": "1000000000"  # 1 SOL in lamports
    })
    print(f"Jupiter Swap Quote: {json.dumps(result, indent=2)}")

async def test_portfolio_tracker_tool():
    """Test portfolio tracker tool"""
    print("\n=== Testing Portfolio Tracker Tool ===")
    tool = PortfolioTrackerTool()
    
    # Create a portfolio
    result = await tool.execute({
        "action": "create",
        "portfolio_id": "test_portfolio",
        "name": "Test Portfolio"
    })
    print(f"Create Portfolio: {json.dumps(result, indent=2)}")
    
    # Add Bitcoin to portfolio
    result = await tool.execute({
        "action": "add_asset",
        "portfolio_id": "test_portfolio",
        "coin_id": "bitcoin",
        "amount": 0.5,
        "purchase_price": 45000
    })
    print(f"Add Bitcoin: {json.dumps(result, indent=2)}")
    
    # Add Ethereum to portfolio
    result = await tool.execute({
        "action": "add_asset",
        "portfolio_id": "test_portfolio",
        "coin_id": "ethereum",
        "amount": 5.0,
        "purchase_price": 3000
    })
    print(f"Add Ethereum: {json.dumps(result, indent=2)}")
    
    # Get portfolio value
    result = await tool.execute({
        "action": "get_value",
        "portfolio_id": "test_portfolio"
    })
    print(f"Portfolio Value: {json.dumps(result, indent=2)}")
    
    # Get portfolio analysis
    result = await tool.execute({
        "action": "get_analysis",
        "portfolio_id": "test_portfolio"
    })
    print(f"Portfolio Analysis: {json.dumps(result, indent=2)}")

async def test_crypto_news_tool():
    """Test crypto news tool"""
    print("\n=== Testing Crypto News Tool ===")
    tool = CryptoNewsTool()
    
    # Get Bitcoin news
    result = await tool.execute({
        "query": "bitcoin",
        "max_results": 5,
        "time_filter": "d",
        "include_sentiment": True
    })
    print(f"Bitcoin News: {json.dumps(result, indent=2)}")
    
    # Get DeFi news
    result = await tool.execute({
        "query": "defi",
        "max_results": 3,
        "time_filter": "w"
    })
    print(f"DeFi News: {json.dumps(result, indent=2)}")

async def test_nft_marketplace_tool():
    """Test NFT marketplace tool"""
    print("\n=== Testing NFT Marketplace Tool ===")
    tool = NFTMarketplaceTool()
    
    # Test Ethereum collection (Bored Ape Yacht Club)
    print("\n--- Testing Ethereum Collection ---")
    result = await tool.execute({
        "action": "collection_info",
        "collection_slug": "bored-ape-yacht-club",
        "chain": "ethereum"
    })
    print(f"Collection Info: {json.dumps(result, indent=2)}")
    
    # Get floor price
    result = await tool.execute({
        "action": "floor_price",
        "collection_slug": "bored-ape-yacht-club",
        "chain": "ethereum"
    })
    print(f"Floor Price: {json.dumps(result, indent=2)}")
    
    # Get trading volume
    result = await tool.execute({
        "action": "trading_volume",
        "collection_slug": "bored-ape-yacht-club",
        "chain": "ethereum",
        "time_period": "7d"
    })
    print(f"Trading Volume: {json.dumps(result, indent=2)}")
    
    # Get recent sales
    result = await tool.execute({
        "action": "recent_sales",
        "collection_slug": "bored-ape-yacht-club",
        "chain": "ethereum",
        "limit": 5
    })
    print(f"Recent Sales: {json.dumps(result, indent=2)}")
    
    # Test Solana collection (Degen Ape Academy)
    print("\n--- Testing Solana Collection ---")
    result = await tool.execute({
        "action": "collection_info",
        "collection_slug": "degen-ape-academy",
        "chain": "solana"
    })
    print(f"Collection Info: {json.dumps(result, indent=2)}")
    
    # Get comprehensive stats
    result = await tool.execute({
        "action": "collection_stats",
        "collection_slug": "bored-ape-yacht-club",
        "chain": "ethereum"
    })
    print(f"Collection Stats: {json.dumps(result, indent=2)}")

async def test_market_analysis_tool():
    """Test market analysis tool with real data"""
    print("\n=== Testing Market Analysis Tool with Real Data ===")
    tool = MarketAnalysisTool()
    
    # Get technical indicators
    result = await tool.execute({
        "coin_id": "bitcoin",
        "analysis_type": "technical_indicators",
        "timeframe": "7d",
        "include_charts": True
    })
    print(f"Technical Indicators (Bitcoin): {json.dumps(result, indent=2)}")
    
    # Get market sentiment
    result = await tool.execute({
        "coin_id": "bitcoin",
        "analysis_type": "market_sentiment"
    })
    print(f"Market Sentiment (Bitcoin): {json.dumps(result, indent=2)}")
    
    # Get trend analysis
    result = await tool.execute({
        "coin_id": "ethereum",
        "analysis_type": "trend_analysis",
        "timeframe": "30d"
    })
    print(f"Trend Analysis (Ethereum): {json.dumps(result, indent=2)}")
    
    # Get volatility analysis
    result = await tool.execute({
        "coin_id": "ethereum",
        "analysis_type": "volatility",
        "timeframe": "30d"
    })
    print(f"Volatility Analysis (Ethereum): {json.dumps(result, indent=2)}")

async def test_notification_tool():
    """Test notification tool with real market data"""
    print("\n=== Testing Notification Tool with Real Market Data ===")
    tool = NotificationTool()
    
    # Create a price alert
    result = await tool.execute({
        "action": "create_alert",
        "alert_type": "price_alert",
        "alert_id": "btc_alert",
        "coin_id": "bitcoin",
        "price_threshold": 50000,
        "condition": "above"
    })
    print(f"Create Price Alert: {json.dumps(result, indent=2)}")
    
    # Create a news alert
    result = await tool.execute({
        "action": "create_alert",
        "alert_type": "news_alert",
        "alert_id": "defi_news",
        "keywords": "defi ethereum"
    })
    print(f"Create News Alert: {json.dumps(result, indent=2)}")
    
    # List all alerts
    result = await tool.execute({
        "action": "list_alerts"
    })
    print(f"List Alerts: {json.dumps(result, indent=2)}")
    
    # Test an alert
    result = await tool.execute({
        "action": "test_alert",
        "alert_id": "btc_alert"
    })
    print(f"Test Alert: {json.dumps(result, indent=2)}")

async def test_apy_calculator_tool():
    """Test APY calculator tool with real data"""
    print("\n=== Testing APY Calculator Tool with Real Data ===")
    tool = APYCalculatorTool()
    
    # Calculate LP APY
    result = await tool.execute({
        "calculation_type": "liquidity_pool",
        "protocol": "meteora",
        "principal": 10000,
        "time_period": 365,
        "include_impermanent_loss": True
    })
    print(f"LP APY Calculation: {json.dumps(result, indent=2)}")
    
    # Calculate yield farming APY
    result = await tool.execute({
        "calculation_type": "yield_farming",
        "protocol": "compound",
        "principal": 5000,
        "apy_rate": 0.25,
        "compounding_frequency": "daily",
        "time_period": 365
    })
    print(f"Yield Farming APY: {json.dumps(result, indent=2)}")
    
    # Calculate staking APY
    result = await tool.execute({
        "calculation_type": "staking",
        "principal": 2000,
        "apy_rate": 0.08,
        "compounding_frequency": "monthly",
        "time_period": 365
    })
    print(f"Staking APY: {json.dumps(result, indent=2)}")

async def test_web_search_tools():
    """Test web search tools"""
    print("\n=== Testing Web Search Tools ===")
    
    # Test DuckDuckGo search
    tool = DuckDuckGoSearchTool()
    result = await tool.execute({
        "query": "cryptocurrency news",
        "max_results": 3,
        "region": "us-en"
    })
    print(f"DuckDuckGo Search: {json.dumps(result, indent=2)}")
    
    # Test enhanced web search
    tool = WebSearchTool()
    result = await tool.execute({
        "query": "bitcoin price",
        "search_type": "news",
        "max_results": 3
    })
    print(f"Enhanced Web Search: {json.dumps(result, indent=2)}")

async def main():
    """Run all tool tests"""
    print("🚀 Starting OLAXBT MCP Server Tools Test")
    print("=" * 50)
    
    try:
        # Test all tools
        await test_crypto_price_tool()
        await test_defi_protocol_tool()
        await test_portfolio_tracker_tool()
        await test_crypto_news_tool()
        await test_nft_marketplace_tool()
        await test_market_analysis_tool()
        await test_notification_tool()
        await test_apy_calculator_tool()
        await test_web_search_tools()
        
        print("\n✅ All tests completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
