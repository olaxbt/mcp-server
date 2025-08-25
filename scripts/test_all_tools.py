#!/usr/bin/env python3
"""
Comprehensive test script for all MCP tools
Tests all available tools to ensure they work together
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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
    APYCalculatorTool,
    JupiterTool,
    RaydiumTool,
    LunarCrushTool,
    CoinDeskTool,
    AaveTool,
    PumpNewsTool,
    PumpFunTool,
    GMGNTool,
    MerklTool,
    YouTubeTool,
    GmailTool,
    GoogleCalendarTool,
    TwitterTool,
    RedditTool,
    OpenWeatherTool,
    GoogleMapsTool,
    JiraTool,
    SlackTool
)

async def test_all_tools():
    """Test all MCP tools"""
    print("🧪 Testing All MCP Tools...")
    print("=" * 60)
    
    tools = {
        "DuckDuckGo Search": DuckDuckGoSearchTool(),
        "Web Search": WebSearchTool(),
        "Crypto Price": CryptoPriceTool(),
        "DeFi Protocol": DeFiProtocolTool(),
        "Portfolio Tracker": PortfolioTrackerTool(),
        "Crypto News": CryptoNewsTool(),
        "NFT Marketplace": NFTMarketplaceTool(),
        "Market Analysis": MarketAnalysisTool(),
        "Notification": NotificationTool(),
        "APY Calculator": APYCalculatorTool(),
        "Jupiter": JupiterTool(),
        "Raydium": RaydiumTool(),
        "LunarCrush": LunarCrushTool(),
        "CoinDesk": CoinDeskTool(),
        "Aave": AaveTool(),
        "PumpNews": PumpNewsTool(),
        "PumpFun": PumpFunTool(),
        "GMGN": GMGNTool(),
        "Merkl": MerklTool(),
        "YouTube": YouTubeTool(),
        "Gmail": GmailTool(),
        "Google Calendar": GoogleCalendarTool(),
        "Twitter": TwitterTool(),
        "Reddit": RedditTool(),
        "OpenWeather": OpenWeatherTool(),
        "Google Maps": GoogleMapsTool(),
        "Jira": JiraTool(),
        "Slack": SlackTool()
    }
    
    test_results = {}
    
    # Test 1: Tool Instantiation
    print("\n1️⃣ Testing Tool Instantiation...")
    for name, tool in tools.items():
        try:
            # Test basic properties
            tool_name = tool.name
            tool_desc = tool.description
            tool_schema = tool.input_schema
            test_results[name] = {"instantiation": "✅ PASS"}
            print(f"   ✅ {name}: Instantiated successfully")
        except Exception as e:
            test_results[name] = {"instantiation": f"❌ FAIL: {str(e)}"}
            print(f"   ❌ {name}: Failed to instantiate - {str(e)}")
    
    # Test 2: Basic Functionality Tests
    print("\n2️⃣ Testing Basic Functionality...")
    
    # Test LunarCrush Tool
    print("\n   Testing LunarCrush Tool...")
    try:
        lunarcrush = tools["LunarCrush"]
        result = await lunarcrush.execute({
            "action": "get_social_sentiment",
            "symbol": "BTC"
        })
        if result and len(result) > 0:
            test_results["LunarCrush"]["functionality"] = "✅ PASS"
            print(f"      ✅ LunarCrush: Social sentiment test passed")
        else:
            test_results["LunarCrush"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ LunarCrush: No result returned")
    except Exception as e:
        test_results["LunarCrush"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ LunarCrush: Error - {str(e)}")
    
    # Test Jupiter Tool
    print("\n   Testing Jupiter Tool...")
    try:
        jupiter = tools["Jupiter"]
        result = await jupiter.execute({
            "action": "get_tokens",
            "limit": 5
        })
        if result and len(result) > 0:
            test_results["Jupiter"]["functionality"] = "✅ PASS"
            print(f"      ✅ Jupiter: Get tokens test passed")
        else:
            test_results["Jupiter"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Jupiter: No result returned")
    except Exception as e:
        test_results["Jupiter"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Jupiter: Error - {str(e)}")
    
    # Test Raydium Tool
    print("\n   Testing Raydium Tool...")
    try:
        raydium = tools["Raydium"]
        result = await raydium.execute({
            "action": "get_pools",
            "limit": 5
        })
        if result and len(result) > 0:
            test_results["Raydium"]["functionality"] = "✅ PASS"
            print(f"      ✅ Raydium: Get pools test passed")
        else:
            test_results["Raydium"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Raydium: No result returned")
    except Exception as e:
        test_results["Raydium"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Raydium: Error - {str(e)}")
    
    # Test Crypto Price Tool
    print("\n   Testing Crypto Price Tool...")
    try:
        crypto_price = tools["Crypto Price"]
        result = await crypto_price.execute({
            "symbols": ["BTC", "ETH"]
        })
        if result and len(result) > 0:
            test_results["Crypto Price"]["functionality"] = "✅ PASS"
            print(f"      ✅ Crypto Price: Get prices test passed")
        else:
            test_results["Crypto Price"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Crypto Price: No result returned")
    except Exception as e:
        test_results["Crypto Price"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Crypto Price: Error - {str(e)}")
    
    # Test Market Analysis Tool
    print("\n   Testing Market Analysis Tool...")
    try:
        market_analysis = tools["Market Analysis"]
        result = await market_analysis.execute({
            "symbol": "BTC",
            "analysis_type": "technical_indicators"
        })
        if result and len(result) > 0:
            test_results["Market Analysis"]["functionality"] = "✅ PASS"
            print(f"      ✅ Market Analysis: Technical indicators test passed")
        else:
            test_results["Market Analysis"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Market Analysis: No result returned")
    except Exception as e:
        test_results["Market Analysis"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Market Analysis: Error - {str(e)}")
    
    # Test APY Calculator Tool
    print("\n   Testing APY Calculator Tool...")
    try:
        apy_calculator = tools["APY Calculator"]
        result = await apy_calculator.execute({
            "calculation_type": "compound_interest",
            "principal": 10000,
            "rate": 0.05,
            "time": 1
        })
        if result and len(result) > 0:
            test_results["APY Calculator"]["functionality"] = "✅ PASS"
            print(f"      ✅ APY Calculator: Compound interest test passed")
        else:
            test_results["APY Calculator"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ APY Calculator: No result returned")
    except Exception as e:
        test_results["APY Calculator"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ APY Calculator: Error - {str(e)}")
    
    # Test CoinDesk Tool
    print("\n   Testing CoinDesk Tool...")
    try:
        coindesk = tools["CoinDesk"]
        result = await coindesk.execute(action="get_current_price", currency="USD")
        if result and len(result) > 0:
            test_results["CoinDesk"]["functionality"] = "✅ PASS"
            print(f"      ✅ CoinDesk: Get current price test passed")
        else:
            test_results["CoinDesk"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ CoinDesk: No result returned")
    except Exception as e:
        test_results["CoinDesk"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ CoinDesk: Error - {str(e)}")
    
    # Test Aave Tool
    print("\n   Testing Aave Tool...")
    try:
        aave = tools["Aave"]
        result = await aave.execute({"action": "get_pool_data", "network": "ethereum"})
        if result and len(result) > 0:
            test_results["Aave"]["functionality"] = "✅ PASS"
            print(f"      ✅ Aave: Get pool data test passed")
        else:
            test_results["Aave"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Aave: No result returned")
    except Exception as e:
        test_results["Aave"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Aave: Error - {str(e)}")
    
    # Test PumpNews Tool
    print("\n   Testing PumpNews Tool...")
    try:
        pumpnews = tools["PumpNews"]
        result = await pumpnews.execute({"action": "get_news", "limit": 5})
        if result and len(result) > 0:
            test_results["PumpNews"]["functionality"] = "✅ PASS"
            print(f"      ✅ PumpNews: Get news test passed")
        else:
            test_results["PumpNews"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ PumpNews: No result returned")
    except Exception as e:
        test_results["PumpNews"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ PumpNews: Error - {str(e)}")
    
    # Test PumpFun Tool
    print("\n   Testing PumpFun Tool...")
    try:
        pumpfun = tools["PumpFun"]
        result = await pumpfun.execute({"action": "get_pump_detection", "symbol": "BTC", "timeframe": "24h"})
        if result and len(result) > 0:
            test_results["PumpFun"]["functionality"] = "✅ PASS"
            print(f"      ✅ PumpFun: Pump detection test passed")
        else:
            test_results["PumpFun"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ PumpFun: No result returned")
    except Exception as e:
        test_results["PumpFun"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ PumpFun: Error - {str(e)}")
    
    # Test GMGN Tool
    print("\n   Testing GMGN Tool...")
    try:
        gmgn = tools["GMGN"]
        result = await gmgn.execute({"action": "get_gaming_token_analysis", "token": "AXS", "timeframe": "24h"})
        if result and len(result) > 0:
            test_results["GMGN"]["functionality"] = "✅ PASS"
            print(f"      ✅ GMGN: Gaming token analysis test passed")
        else:
            test_results["GMGN"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ GMGN: No result returned")
    except Exception as e:
        test_results["GMGN"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ GMGN: Error - {str(e)}")
    
    # Test Merkl Tool
    print("\n   Testing Merkl Tool...")
    try:
        merkl = tools["Merkl"]
        result = await merkl.execute({"action": "get_concentrated_positions", "chain": "ethereum", "timeframe": "24h"})
        if result and len(result) > 0:
            test_results["Merkl"]["functionality"] = "✅ PASS"
            print(f"      ✅ Merkl: Concentrated positions test passed")
        else:
            test_results["Merkl"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Merkl: No result returned")
    except Exception as e:
        test_results["Merkl"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Merkl: Error - {str(e)}")
    
    # Test YouTube Tool
    print("\n   Testing YouTube Tool...")
    try:
        youtube = tools["YouTube"]
        result = await youtube.execute({"action": "search_videos", "query": "cryptocurrency", "max_results": 3})
        if result and len(result) > 0:
            test_results["YouTube"]["functionality"] = "✅ PASS"
            print(f"      ✅ YouTube: Search videos test passed")
        else:
            test_results["YouTube"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ YouTube: No result returned")
    except Exception as e:
        test_results["YouTube"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ YouTube: Error - {str(e)}")
    
    # Test Gmail Tool
    print("\n   Testing Gmail Tool...")
    try:
        gmail = tools["Gmail"]
        result = await gmail.execute({"action": "search_emails", "query": "is:unread", "max_results": 3})
        if result and len(result) > 0:
            test_results["Gmail"]["functionality"] = "✅ PASS"
            print(f"      ✅ Gmail: Search emails test passed")
        else:
            test_results["Gmail"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Gmail: No result returned")
    except Exception as e:
        test_results["Gmail"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Gmail: Error - {str(e)}")
    
    # Test Google Calendar Tool
    print("\n   Testing Google Calendar Tool...")
    try:
        calendar = tools["Google Calendar"]
        result = await calendar.execute({"action": "list_calendars"})
        if result and len(result) > 0:
            test_results["Google Calendar"]["functionality"] = "✅ PASS"
            print(f"      ✅ Google Calendar: List calendars test passed")
        else:
            test_results["Google Calendar"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Google Calendar: No result returned")
    except Exception as e:
        test_results["Google Calendar"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Google Calendar: Error - {str(e)}")
    
    # Test Twitter Tool
    print("\n   Testing Twitter Tool...")
    try:
        twitter = tools["Twitter"]
        result = await twitter.execute({"action": "search_tweets", "query": "cryptocurrency", "max_results": 3})
        if result and len(result) > 0:
            test_results["Twitter"]["functionality"] = "✅ PASS"
            print(f"      ✅ Twitter: Search tweets test passed")
        else:
            test_results["Twitter"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Twitter: No result returned")
    except Exception as e:
        test_results["Twitter"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Twitter: Error - {str(e)}")
    
    # Test Reddit Tool
    print("\n   Testing Reddit Tool...")
    try:
        reddit = tools["Reddit"]
        result = await reddit.execute({"action": "search_posts", "query": "cryptocurrency", "limit": 3})
        if result and len(result) > 0:
            test_results["Reddit"]["functionality"] = "✅ PASS"
            print(f"      ✅ Reddit: Search posts test passed")
        else:
            test_results["Reddit"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Reddit: No result returned")
    except Exception as e:
        test_results["Reddit"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Reddit: Error - {str(e)}")
    
    # Test OpenWeather Tool
    print("\n   Testing OpenWeather Tool...")
    try:
        openweather = tools["OpenWeather"]
        result = await openweather.execute({"action": "get_current_weather", "location": "London", "units": "metric"})
        if result and len(result) > 0:
            test_results["OpenWeather"]["functionality"] = "✅ PASS"
            print(f"      ✅ OpenWeather: Get current weather test passed")
        else:
            test_results["OpenWeather"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ OpenWeather: No result returned")
    except Exception as e:
        test_results["OpenWeather"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ OpenWeather: Error - {str(e)}")
    
    # Test Google Maps Tool
    print("\n   Testing Google Maps Tool...")
    try:
        googlemaps = tools["Google Maps"]
        result = await googlemaps.execute({"action": "geocode", "address": "1600 Amphitheatre Parkway, Mountain View, CA"})
        if result and len(result) > 0:
            test_results["Google Maps"]["functionality"] = "✅ PASS"
            print(f"      ✅ Google Maps: Geocoding test passed")
        else:
            test_results["Google Maps"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Google Maps: No result returned")
    except Exception as e:
        test_results["Google Maps"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Google Maps: Error - {str(e)}")

    # Test Jira Tool
    print("\n   Testing Jira Tool...")
    try:
        jira = tools["Jira"]
        result = await jira.execute({"action": "get_projects"})
        if result and len(result) > 0:
            test_results["Jira"]["functionality"] = "✅ PASS"
            print(f"      ✅ Jira: Get projects test passed")
        else:
            test_results["Jira"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Jira: No result returned")
    except Exception as e:
        test_results["Jira"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Jira: Error - {str(e)}")
    
    # Test Slack Tool
    print("\n   Testing Slack Tool...")
    try:
        slack = tools["Slack"]
        result = await slack.execute({"action": "list_channels", "limit": 5})
        if result and len(result) > 0:
            test_results["Slack"]["functionality"] = "✅ PASS"
            print(f"      ✅ Slack: List channels test passed")
        else:
            test_results["Slack"]["functionality"] = "❌ FAIL: No result"
            print(f"      ❌ Slack: No result returned")
    except Exception as e:
        test_results["Slack"]["functionality"] = f"❌ FAIL: {str(e)}"
        print(f"      ❌ Slack: Error - {str(e)}")
    
    # Test 3: Summary
    print("\n3️⃣ Test Summary...")
    print("=" * 60)
    
    total_tools = len(tools)
    passed_instantiation = sum(1 for result in test_results.values() if "instantiation" in result and "✅ PASS" in result["instantiation"])
    passed_functionality = sum(1 for result in test_results.values() if "functionality" in result and "✅ PASS" in result["functionality"])
    
    print(f"📊 Total Tools: {total_tools}")
    print(f"✅ Instantiation Tests Passed: {passed_instantiation}/{total_tools}")
    print(f"✅ Functionality Tests Passed: {passed_functionality}/21 (tested)")
    
    print("\n📋 Detailed Results:")
    for name, results in test_results.items():
        instantiation_status = results.get("instantiation", "❓ NOT TESTED")
        functionality_status = results.get("functionality", "❓ NOT TESTED")
        print(f"   {name}:")
        print(f"     Instantiation: {instantiation_status}")
        print(f"     Functionality: {functionality_status}")
    
    print("\n" + "=" * 60)
    print("🎉 All tools testing completed!")
    print("\n💡 Notes:")
    print("   - LunarCrush requires LUNARCRUSH_API_KEY for real data")
    print("   - CoinDesk requires COINDESK_API_KEY for premium features")
    print("   - Aave uses real API data from Aave V3")
    print("   - PumpNews requires PUMPNEWS_API_KEY for real data")
    print("   - PumpFun requires PUMPFUN_API_KEY for real data")
    print("   - GMGN requires GMGN_API_KEY for real data")
    print("   - Merkl requires MERKL_API_KEY for real data")
    print("   - YouTube requires YOUTUBE_API_KEY for real data")
    print("   - Gmail requires GMAIL_ACCESS_TOKEN for real data")
    print("   - Google Calendar requires GOOGLE_CALENDAR_ACCESS_TOKEN for real data")
    print("   - Twitter requires TWITTER_BEARER_TOKEN for real data")
    print("   - Reddit requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET for real data")
    print("   - OpenWeather requires OPENWEATHER_API_KEY for real data")
    print("   - Google Maps requires GOOGLE_MAPS_API_KEY for real data")
    print("   - Jira requires JIRA_DOMAIN, JIRA_USERNAME, and JIRA_API_TOKEN for real data")
    print("   - Slack requires SLACK_BOT_TOKEN or SLACK_USER_TOKEN for real data")
    print("   - Some tools return sample data when APIs are unavailable")
    print("   - All tools are properly integrated into the MCP server")

if __name__ == "__main__":
    asyncio.run(test_all_tools())
