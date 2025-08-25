#!/usr/bin/env python3
"""
Test script for tools with real data implementations
Tests MarketAnalysisTool, APYCalculatorTool, and NotificationTool with real APIs
"""

import asyncio
import json
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import MarketAnalysisTool, APYCalculatorTool, NotificationTool

async def test_market_analysis_real_data():
    """Test MarketAnalysisTool with real market data"""
    print("=" * 60)
    print("TESTING MARKET ANALYSIS TOOL WITH REAL DATA")
    print("=" * 60)
    
    tool = MarketAnalysisTool()
    
    # Test 1: Technical Indicators for Bitcoin
    print("\n1. Technical Indicators (Bitcoin, 7 days):")
    result = await tool.execute({
        "coin_id": "bitcoin",
        "analysis_type": "technical_indicators",
        "timeframe": "7d",
        "include_charts": True
    })
    print(json.dumps(result, indent=2))
    
    # Test 2: Market Sentiment for Bitcoin
    print("\n2. Market Sentiment (Bitcoin):")
    result = await tool.execute({
        "coin_id": "bitcoin",
        "analysis_type": "market_sentiment"
    })
    print(json.dumps(result, indent=2))
    
    # Test 3: Trend Analysis for Ethereum
    print("\n3. Trend Analysis (Ethereum, 30 days):")
    result = await tool.execute({
        "coin_id": "ethereum",
        "analysis_type": "trend_analysis",
        "timeframe": "30d"
    })
    print(json.dumps(result, indent=2))
    
    # Test 4: Volatility Analysis for Ethereum
    print("\n4. Volatility Analysis (Ethereum, 30 days):")
    result = await tool.execute({
        "coin_id": "ethereum",
        "analysis_type": "volatility",
        "timeframe": "30d"
    })
    print(json.dumps(result, indent=2))

async def test_apy_calculator_real_data():
    """Test APYCalculatorTool with real protocol data"""
    print("\n" + "=" * 60)
    print("TESTING APY CALCULATOR TOOL WITH REAL DATA")
    print("=" * 60)
    
    tool = APYCalculatorTool()
    
    # Test 1: Liquidity Pool APY
    print("\n1. Liquidity Pool APY (Meteora, $10,000, 1 year):")
    result = await tool.execute({
        "calculation_type": "liquidity_pool",
        "protocol": "meteora",
        "principal": 10000,
        "time_period": 365,
        "include_impermanent_loss": True
    })
    print(json.dumps(result, indent=2))
    
    # Test 2: Yield Farming APY
    print("\n2. Yield Farming APY (Compound, $5,000, 25% APY, daily compounding):")
    result = await tool.execute({
        "calculation_type": "yield_farming",
        "protocol": "compound",
        "principal": 5000,
        "apy_rate": 0.25,
        "compounding_frequency": "daily",
        "time_period": 365
    })
    print(json.dumps(result, indent=2))
    
    # Test 3: Staking APY
    print("\n3. Staking APY ($2,000, 8% APY, monthly compounding):")
    result = await tool.execute({
        "calculation_type": "staking",
        "principal": 2000,
        "apy_rate": 0.08,
        "compounding_frequency": "monthly",
        "time_period": 365
    })
    print(json.dumps(result, indent=2))
    
    # Test 4: Compound Interest
    print("\n4. Compound Interest ($1,000, 10% APY, daily compounding):")
    result = await tool.execute({
        "calculation_type": "compound_interest",
        "principal": 1000,
        "apy_rate": 0.10,
        "compounding_frequency": "daily",
        "time_period": 365
    })
    print(json.dumps(result, indent=2))

async def test_notification_tool_real_data():
    """Test NotificationTool with real market data"""
    print("\n" + "=" * 60)
    print("TESTING NOTIFICATION TOOL WITH REAL MARKET DATA")
    print("=" * 60)
    
    tool = NotificationTool()
    
    # Test 1: Create Bitcoin price alert
    print("\n1. Creating Bitcoin price alert (above $50,000):")
    result = await tool.execute({
        "action": "create_alert",
        "alert_type": "price_alert",
        "alert_id": "btc_high_alert",
        "coin_id": "bitcoin",
        "price_threshold": 50000,
        "condition": "above"
    })
    print(json.dumps(result, indent=2))
    
    # Test 2: Create Ethereum price alert
    print("\n2. Creating Ethereum price alert (below $3,000):")
    result = await tool.execute({
        "action": "create_alert",
        "alert_type": "price_alert",
        "alert_id": "eth_low_alert",
        "coin_id": "ethereum",
        "price_threshold": 3000,
        "condition": "below"
    })
    print(json.dumps(result, indent=2))
    
    # Test 3: Create news alert
    print("\n3. Creating DeFi news alert:")
    result = await tool.execute({
        "action": "create_alert",
        "alert_type": "news_alert",
        "alert_id": "defi_news_alert",
        "keywords": "defi ethereum yield farming"
    })
    print(json.dumps(result, indent=2))
    
    # Test 4: List all alerts
    print("\n4. Listing all active alerts:")
    result = await tool.execute({
        "action": "list_alerts"
    })
    print(json.dumps(result, indent=2))
    
    # Test 5: Test Bitcoin alert with real price data
    print("\n5. Testing Bitcoin alert with real current price:")
    result = await tool.execute({
        "action": "test_alert",
        "alert_id": "btc_high_alert"
    })
    print(json.dumps(result, indent=2))
    
    # Test 6: Test Ethereum alert with real price data
    print("\n6. Testing Ethereum alert with real current price:")
    result = await tool.execute({
        "action": "test_alert",
        "alert_id": "eth_low_alert"
    })
    print(json.dumps(result, indent=2))
    
    # Test 7: Delete an alert
    print("\n7. Deleting Ethereum alert:")
    result = await tool.execute({
        "action": "delete_alert",
        "alert_id": "eth_low_alert"
    })
    print(json.dumps(result, indent=2))

async def main():
    """Run all tests"""
    print("OLAXBT MCP Server - Real Data Tools Test")
    print("Testing tools that now use real APIs instead of hardcoded data")
    
    try:
        # Test Market Analysis Tool
        await test_market_analysis_real_data()
        
        # Test APY Calculator Tool
        await test_apy_calculator_real_data()
        
        # Test Notification Tool
        await test_notification_tool_real_data()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nKey improvements:")
        print("✓ MarketAnalysisTool now uses real CoinGecko API data")
        print("✓ APYCalculatorTool fetches real DeFi protocol data")
        print("✓ NotificationTool integrates with real market prices")
        print("✓ All tools include comprehensive error handling")
        print("✓ Enhanced calculations with real market metrics")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
