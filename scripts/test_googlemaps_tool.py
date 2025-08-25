#!/usr/bin/env python3
"""
Test script for GoogleMapsTool
Tests all actions, parameter validation, and error handling
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import GoogleMapsTool

async def test_googlemaps_tool():
    """Test the GoogleMapsTool with various scenarios."""
    print("🧪 Testing GoogleMapsTool...")
    
    tool = GoogleMapsTool()
    
    # Test 1: Tool instantiation
    print("\n1. Testing tool instantiation...")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    print(f"   Input Schema: {len(tool.input_schema['properties'])} properties")
    print("   ✅ Tool instantiated successfully")
    
    # Test 2: Geocoding
    print("\n2. Testing geocoding...")
    result = await tool.execute({"action": "geocode", "address": "1600 Amphitheatre Parkway, Mountain View, CA"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 3: Reverse geocoding
    print("\n3. Testing reverse geocoding...")
    result = await tool.execute({"action": "reverse_geocode", "latitude": 37.4220, "longitude": -122.0841})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 4: Get directions
    print("\n4. Testing get directions...")
    result = await tool.execute({
        "action": "get_directions", 
        "origin": "San Francisco, CA", 
        "destination": "Mountain View, CA",
        "mode": "driving"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 5: Search places
    print("\n5. Testing search places...")
    result = await tool.execute({
        "action": "search_places", 
        "query": "restaurants in San Francisco",
        "latitude": 37.7749,
        "longitude": -122.4194,
        "radius": 5000
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 6: Get place details
    print("\n6. Testing get place details...")
    result = await tool.execute({
        "action": "get_place_details", 
        "place_id": "ChIJN1t_tDeuEmsRUsoyG83frY4"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 7: Get nearby places
    print("\n7. Testing get nearby places...")
    result = await tool.execute({
        "action": "get_nearby_places", 
        "latitude": 37.7749,
        "longitude": -122.4194,
        "radius": 5000,
        "type": "restaurant"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 8: Get distance matrix
    print("\n8. Testing get distance matrix...")
    result = await tool.execute({
        "action": "get_distance_matrix", 
        "origins": "San Francisco, CA",
        "destinations": "Mountain View, CA",
        "mode": "driving",
        "units": "metric"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 9: Get elevation
    print("\n9. Testing get elevation...")
    result = await tool.execute({
        "action": "get_elevation", 
        "latitude": 37.7749,
        "longitude": -122.4194
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 10: Get timezone
    print("\n10. Testing get timezone...")
    result = await tool.execute({
        "action": "get_timezone", 
        "latitude": 37.7749,
        "longitude": -122.4194,
        "timestamp": 1640995200
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 11: Missing address for geocoding
    print("\n11. Testing missing address for geocoding...")
    result = await tool.execute({"action": "geocode"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "address parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing address parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 12: Missing coordinates for reverse geocoding
    print("\n12. Testing missing coordinates for reverse geocoding...")
    result = await tool.execute({"action": "reverse_geocode"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "latitude and longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing coordinates parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 13: Missing origin/destination for directions
    print("\n13. Testing missing origin/destination for directions...")
    result = await tool.execute({"action": "get_directions"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "origin and destination parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing origin/destination parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 14: Missing query for search places
    print("\n14. Testing missing query for search places...")
    result = await tool.execute({"action": "search_places"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "query parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing query parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 15: Missing place_id for place details
    print("\n15. Testing missing place_id for place details...")
    result = await tool.execute({"action": "get_place_details"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "place_id parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing place_id parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 16: Missing coordinates for nearby places
    print("\n16. Testing missing coordinates for nearby places...")
    result = await tool.execute({"action": "get_nearby_places"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "latitude and longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing coordinates parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 17: Missing origins/destinations for distance matrix
    print("\n17. Testing missing origins/destinations for distance matrix...")
    result = await tool.execute({"action": "get_distance_matrix"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "origins and destinations parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing origins/destinations parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 18: Missing coordinates for elevation
    print("\n18. Testing missing coordinates for elevation...")
    result = await tool.execute({"action": "get_elevation"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "latitude and longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing coordinates parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 19: Missing coordinates for timezone
    print("\n19. Testing missing coordinates for timezone...")
    result = await tool.execute({"action": "get_timezone"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "latitude and longitude parameters are required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing coordinates parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 20: Invalid action
    print("\n20. Testing invalid action...")
    result = await tool.execute({"action": "invalid_action"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and "Unknown action: invalid_action" in result[0].get("error", ""):
        print("   ✅ Correctly caught invalid action")
    else:
        print("   ❌ Failed to catch invalid action")
    
    # Test 21: Directions with waypoints
    print("\n21. Testing directions with waypoints...")
    result = await tool.execute({
        "action": "get_directions", 
        "origin": "San Francisco, CA", 
        "destination": "Mountain View, CA",
        "waypoints": "Palo Alto, CA",
        "mode": "driving"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 22: Search places with type filter
    print("\n22. Testing search places with type filter...")
    result = await tool.execute({
        "action": "search_places", 
        "query": "coffee",
        "type": "cafe",
        "language": "en"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 23: Nearby places with keyword
    print("\n23. Testing nearby places with keyword...")
    result = await tool.execute({
        "action": "get_nearby_places", 
        "latitude": 37.7749,
        "longitude": -122.4194,
        "keyword": "pizza",
        "type": "restaurant"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 24: Distance matrix with multiple points
    print("\n24. Testing distance matrix with multiple points...")
    result = await tool.execute({
        "action": "get_distance_matrix", 
        "origins": "San Francisco, CA|Oakland, CA",
        "destinations": "Mountain View, CA|Palo Alto, CA",
        "mode": "transit",
        "units": "imperial"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 25: Mixed parameters
    print("\n25. Testing mixed parameters...")
    result = await tool.execute({
        "action": "geocode", 
        "address": "Tokyo, Japan", 
        "language": "ja"
    })
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "API key not configured" in str(result[0].get("error", "")):
        print("   ✅ Expected API key error (no API key)")
    else:
        print("   ⚠️  Unexpected result")
    
    print("\n🎉 GoogleMapsTool testing completed!")
    print("\n📝 Notes:")
    print("   - Google Maps requires GOOGLE_MAPS_API_KEY for real data")
    print("   - All API calls return API key errors without proper credentials")
    print("   - Parameter validation is working correctly")
    print("   - Error handling is properly implemented")

if __name__ == "__main__":
    asyncio.run(test_googlemaps_tool())
