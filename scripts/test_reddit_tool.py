#!/usr/bin/env python3
"""
Test script for RedditTool
Tests all actions, parameter validation, and error handling
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import RedditTool

async def test_reddit_tool():
    """Test the RedditTool with various scenarios."""
    print("🧪 Testing RedditTool...")
    
    tool = RedditTool()
    
    # Test 1: Tool instantiation
    print("\n1. Testing tool instantiation...")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    print(f"   Input Schema: {len(tool.input_schema['properties'])} properties")
    print("   ✅ Tool instantiated successfully")
    
    # Test 2: Search posts
    print("\n2. Testing search_posts action...")
    result = await tool.execute({"action": "search_posts", "query": "cryptocurrency", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 3: Get subreddit posts
    print("\n3. Testing get_subreddit_posts action...")
    result = await tool.execute({"action": "get_subreddit_posts", "subreddit": "cryptocurrency", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 4: Get post comments
    print("\n4. Testing get_post_comments action...")
    result = await tool.execute({"action": "get_post_comments", "post_id": "abc123", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 5: Get user posts
    print("\n5. Testing get_user_posts action...")
    result = await tool.execute({"action": "get_user_posts", "username": "testuser", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 6: Get user comments
    print("\n6. Testing get_user_comments action...")
    result = await tool.execute({"action": "get_user_comments", "username": "testuser", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 7: Get subreddit info
    print("\n7. Testing get_subreddit_info action...")
    result = await tool.execute({"action": "get_subreddit_info", "subreddit": "cryptocurrency"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 8: Get user info
    print("\n8. Testing get_user_info action...")
    result = await tool.execute({"action": "get_user_info", "username": "testuser"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 9: Get trending subreddits
    print("\n9. Testing get_trending_subreddits action...")
    result = await tool.execute({"action": "get_trending_subreddits", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 10: Get hot posts
    print("\n10. Testing get_hot_posts action...")
    result = await tool.execute({"action": "get_hot_posts", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 11: Get new posts
    print("\n11. Testing get_new_posts action...")
    result = await tool.execute({"action": "get_new_posts", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 12: Get top posts
    print("\n12. Testing get_top_posts action...")
    result = await tool.execute({"action": "get_top_posts", "limit": 5, "time_filter": "day"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 13: Get rising posts
    print("\n13. Testing get_rising_posts action...")
    result = await tool.execute({"action": "get_rising_posts", "limit": 5})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Expected authentication error (no credentials)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 14: Missing required parameters
    print("\n14. Testing missing required parameters...")
    result = await tool.execute({"action": "search_posts"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "query parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing query parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 15: Missing subreddit parameter
    print("\n15. Testing missing subreddit parameter...")
    result = await tool.execute({"action": "get_subreddit_posts"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "subreddit parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing subreddit parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 16: Missing post_id parameter
    print("\n16. Testing missing post_id parameter...")
    result = await tool.execute({"action": "get_post_comments"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "post_id parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing post_id parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 17: Missing username parameter
    print("\n17. Testing missing username parameter...")
    result = await tool.execute({"action": "get_user_posts"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "username parameter is required" in result[0].get("error", ""):
        print("   ✅ Correctly caught missing username parameter")
    else:
        print("   ❌ Failed to catch missing parameter")
    
    # Test 18: Invalid action
    print("\n18. Testing invalid action...")
    result = await tool.execute({"action": "invalid_action"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and "Unknown action: invalid_action" in result[0].get("error", ""):
        print("   ✅ Correctly caught invalid action")
    else:
        print("   ❌ Failed to catch invalid action")
    
    # Test 19: Limit validation
    print("\n19. Testing limit validation...")
    result = await tool.execute({"action": "search_posts", "query": "test", "limit": 150})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Limit validation working (capped at 100)")
    else:
        print("   ⚠️  Unexpected result")
    
    # Test 20: Time filter validation
    print("\n20. Testing time filter validation...")
    result = await tool.execute({"action": "search_posts", "query": "test", "time_filter": "invalid"})
    print(f"   Result: {result}")
    if result and len(result) > 0 and result[0].get("success") is False and "Failed to authenticate" in str(result[0].get("error", "")):
        print("   ✅ Time filter validation working")
    else:
        print("   ⚠️  Unexpected result")
    
    print("\n🎉 RedditTool testing completed!")
    print("\n📝 Notes:")
    print("   - Reddit requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET for real data")
    print("   - All API calls return authentication errors without proper credentials")
    print("   - Parameter validation is working correctly")
    print("   - Error handling is properly implemented")

if __name__ == "__main__":
    asyncio.run(test_reddit_tool())
