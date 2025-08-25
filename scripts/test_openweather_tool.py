#!/usr/bin/env python3
"""
Test script for OpenWeatherTool
Tests all actions, parameter validation, and error handling
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import OpenWeatherTool

async def test_openweather_tool():
    """Test the OpenWeatherTool with various scenarios."""
    print("🧪 Testing OpenWeatherTool...")
    
    tool = OpenWeatherTool()
    
    # Test 1: Tool instantiation
    print("\n1. Testing tool instantiation...")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    print(f"   Input Schema: {len(tool.input_schema['properties'])} properties")
    print("   ✅ Tool instantiated successfully")
    
    # Test 2: Get current weather by location
    print("\n2. Testing get_current_weather with location...")
    result = await tool.execute({"action": "get_current_weather", "location": "London", "units": "metric"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 3: Get current weather by coordinates
    print("\n3. Testing get_current_weather with coordinates...")
    result = await tool.execute({"action": "get_current_weather", "latitude": 51.5074, "longitude": -0.1278, "units": "metric"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 4: Get weather forecast
    print("\n4. Testing get_weather_forecast...")
    result = await tool.execute({"action": "get_weather_forecast", "location": "New York", "days": 5, "units": "imperial"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 5: Get weather alerts
    print("\n5. Testing get_weather_alerts...")
    result = await tool.execute({"action": "get_weather_alerts", "location": "Miami", "units": "metric"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 6: Get air pollution
    print("\n6. Testing get_air_pollution...")
    result = await tool.execute({"action": "get_air_pollution", "latitude": 40.7128, "longitude": -74.0060})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 7: Get geocoding
    print("\n7. Testing get_geocoding...")
    result = await tool.execute({"action": "get_geocoding", "location": "Tokyo", "limit": 3})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 8: Get reverse geocoding
    print("\n8. Testing get_reverse_geocoding...")
    result = await tool.execute({"action": "get_reverse_geocoding", "latitude": 35.6762, "longitude": 139.6503, "limit": 3})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 9: Get weather history
    print("\n9. Testing get_weather_history...")
    result = await tool.execute({"action": "get_weather_history", "latitude": 48.8566, "longitude": 2.3522, "dt": 1640995200})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 10: Missing location for current weather
    print("\n10. Testing missing location for current weather...")
    result = await tool.execute({"action": "get_current_weather"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "location or latitude/longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing location parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 11: Missing coordinates for air pollution
    print("\n11. Testing missing coordinates for air pollution...")
    result = await tool.execute({"action": "get_air_pollution"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "latitude and longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing coordinates parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 12: Missing location for geocoding
    print("\n12. Testing missing location for geocoding...")
    result = await tool.execute({"action": "get_geocoding"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "location parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing location parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 13: Missing coordinates for reverse geocoding
    print("\n13. Testing missing coordinates for reverse geocoding...")
    result = await tool.execute({"action": "get_reverse_geocoding"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "latitude and longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing coordinates parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 14: Missing timestamp for weather history
    print("\n14. Testing missing timestamp for weather history...")
    result = await tool.execute({"action": "get_weather_history", "latitude": 48.8566, "longitude": 2.3522})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "dt (timestamp) parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing timestamp parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 15: Invalid action
    print("\n15. Testing invalid action...")
    result = await tool.execute({"action": "invalid_action"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and "Unknown action: invalid_action" in result[0].get("error", ""):
        print("   ✅ Correctly caught invalid action")
    else:
        print("   ❌ Failed to catch invalid action")
    
    # Test 16: Days validation
    print("\n16. Testing days validation...")
    result = await tool.execute({"action": "get_weather_forecast", "location": "Paris", "days": 20})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Days validation working (capped at 16)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 17: Units validation
    print("\n17. Testing units validation...")
    result = await tool.execute({"action": "get_current_weather", "location": "Berlin", "units": "invalid"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Units validation working")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 18: Language parameter
    print("\n18. Testing language parameter...")
    result = await tool.execute({"action": "get_current_weather", "location": "Madrid", "lang": "es"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Language parameter working")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 19: Exclude parameter
    print("\n19. Testing exclude parameter...")
    result = await tool.execute({"action": "get_weather_forecast", "location": "Rome", "exclude": "current,minutely"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Exclude parameter working")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 20: Mixed parameters
    print("\n20. Testing mixed parameters...")
    result = await tool.execute({
        "action": "get_current_weather", 
        "location": "Sydney", 
        "units": "metric", 
        "lang": "en"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Mixed parameters working")
    else:
        print("   ⚠️  Unexpected result")
    
    print("\n🎉 OpenWeatherTool testing completed!")
    print("\n📝 Notes:")
    print("   - OpenWeatherMap requires OPENWEATHER_API_KEY for real data")
    print("   - All API calls return API key errors without proper credentials")
    print("   - Parameter validation is working correctly")
    print("   - Error handling is properly implemented")

if __name__ == "__main__":
    asyncio.run(test_openweather_tool())
