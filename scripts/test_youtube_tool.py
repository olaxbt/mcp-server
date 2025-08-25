#!/usr/bin/env python3
"""
Test script for YouTubeTool
Tests all available actions of the YouTubeTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import YouTubeTool

async def test_youtube_tool():
    """Test all YouTubeTool actions"""
    print("🧪 Testing YouTubeTool...")
    print("=" * 50)

    youtube = YouTubeTool()

    # Test 1: Search videos
    print("\n1. Testing search_videos...")
    result = await youtube.execute({"action": "search_videos", "query": "cryptocurrency", "max_results": 5, "region_code": "US"})
    print(f"Result: {result}")

    # Test 2: Get video details
    print("\n2. Testing get_video_details...")
    result = await youtube.execute({"action": "get_video_details", "video_id": "dQw4w9WgXcQ"})
    print(f"Result: {result}")

    # Test 3: Get channel info
    print("\n3. Testing get_channel_info...")
    result = await youtube.execute({"action": "get_channel_info", "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"})
    print(f"Result: {result}")

    # Test 4: Get trending videos
    print("\n4. Testing get_trending_videos...")
    result = await youtube.execute({"action": "get_trending_videos", "region_code": "US", "max_results": 5})
    print(f"Result: {result}")

    # Test 5: Get video comments
    print("\n5. Testing get_video_comments...")
    result = await youtube.execute({"action": "get_video_comments", "video_id": "dQw4w9WgXcQ", "max_results": 5})
    print(f"Result: {result}")

    # Test 6: Get video statistics
    print("\n6. Testing get_video_statistics...")
    result = await youtube.execute({"action": "get_video_statistics", "video_id": "dQw4w9WgXcQ"})
    print(f"Result: {result}")

    # Test 7: Get playlist videos
    print("\n7. Testing get_playlist_videos...")
    result = await youtube.execute({"action": "get_playlist_videos", "playlist_id": "PLrAXtmRdnEQy6nuLMHjMZOz59Oq8WGfwR", "max_results": 5})
    print(f"Result: {result}")

    # Test 8: Get channel videos
    print("\n8. Testing get_channel_videos...")
    result = await youtube.execute({"action": "get_channel_videos", "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw", "max_results": 5})
    print(f"Result: {result}")

    # Test 9: Get video categories
    print("\n9. Testing get_video_categories...")
    result = await youtube.execute({"action": "get_video_categories", "region_code": "US"})
    print(f"Result: {result}")

    # Test 10: Search channels
    print("\n10. Testing search_channels...")
    result = await youtube.execute({"action": "search_channels", "query": "cryptocurrency", "max_results": 5})
    print(f"Result: {result}")

    # Test 11: Search videos with filters
    print("\n11. Testing search_videos with filters...")
    result = await youtube.execute({
        "action": "search_videos", 
        "query": "bitcoin", 
        "max_results": 3, 
        "order": "viewCount",
        "video_duration": "medium",
        "video_definition": "high"
    })
    print(f"Result: {result}")

    # Test 12: Get trending videos with category
    print("\n12. Testing get_trending_videos with category...")
    result = await youtube.execute({"action": "get_trending_videos", "region_code": "US", "video_category_id": "25"})
    print(f"Result: {result}")

    # Test 13: Error handling - missing query
    print("\n13. Testing error handling (missing query)...")
    result = await youtube.execute({"action": "search_videos"})
    print(f"Result: {result}")

    # Test 14: Error handling - missing video_id
    print("\n14. Testing error handling (missing video_id)...")
    result = await youtube.execute({"action": "get_video_details"})
    print(f"Result: {result}")

    # Test 15: Error handling - missing channel_id
    print("\n15. Testing error handling (missing channel_id)...")
    result = await youtube.execute({"action": "get_channel_info"})
    print(f"Result: {result}")

    # Test 16: Error handling - missing playlist_id
    print("\n16. Testing error handling (missing playlist_id)...")
    result = await youtube.execute({"action": "get_playlist_videos"})
    print(f"Result: {result}")

    # Test 17: Error handling - invalid action
    print("\n17. Testing error handling (invalid action)...")
    result = await youtube.execute({"action": "invalid_action"})
    print(f"Result: {result}")

    # Test 18: Test different regions
    print("\n18. Testing different regions (GB)...")
    result = await youtube.execute({"action": "get_trending_videos", "region_code": "GB", "max_results": 3})
    print(f"Result: {result}")

    # Test 19: Test different order options
    print("\n19. Testing different order options (date)...")
    result = await youtube.execute({"action": "search_videos", "query": "ethereum", "order": "date", "max_results": 3})
    print(f"Result: {result}")

    # Test 20: Test with published date filters
    print("\n20. Testing with published date filters...")
    result = await youtube.execute({
        "action": "search_videos", 
        "query": "defi", 
        "published_after": "2024-01-01T00:00:00Z",
        "published_before": "2024-12-31T23:59:59Z",
        "max_results": 3
    })
    print(f"Result: {result}")

    print("\n" + "=" * 50)
    print("✅ YouTubeTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_youtube_tool())
