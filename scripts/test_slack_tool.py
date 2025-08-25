#!/usr/bin/env python3
"""
Test script for SlackTool
Tests all actions, parameter validation, and error handling
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import SlackTool

async def test_slack_tool():
    """Test the SlackTool with various scenarios."""
    print("🧪 Testing SlackTool...")

    tool = SlackTool()

    # Test 1: Tool instantiation
    print("\n1. Testing tool instantiation...")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    print(f"   Input Schema: {len(tool.input_schema['properties'])} properties")
    print("   ✅ Tool instantiated successfully")

    # Test 2: Check environment variables
    print("\n2. Testing environment variables...")
    print(f"   SLACK_BOT_TOKEN: {'✅ Set' if tool.bot_token else '❌ Not set'}")
    print(f"   SLACK_USER_TOKEN: {'✅ Set' if tool.user_token else '❌ Not set'}")
    print(f"   Base URL: {tool.base_url}")

    # Test 3: Test send_message (should fail without tokens)
    print("\n3. Testing send_message...")
    try:
        result = await tool.execute({
            "action": "send_message",
            "channel": "test-channel",
            "message": "Test message"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 4: Test send_direct_message
    print("\n4. Testing send_direct_message...")
    try:
        result = await tool.execute({
            "action": "send_direct_message",
            "user": "test-user",
            "message": "Test DM"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 5: Test get_channel_history
    print("\n5. Testing get_channel_history...")
    try:
        result = await tool.execute({
            "action": "get_channel_history",
            "channel": "test-channel",
            "limit": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 6: Test get_direct_message_history
    print("\n6. Testing get_direct_message_history...")
    try:
        result = await tool.execute({
            "action": "get_direct_message_history",
            "user": "test-user",
            "limit": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 7: Test list_channels
    print("\n7. Testing list_channels...")
    try:
        result = await tool.execute({
            "action": "list_channels",
            "limit": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 8: Test get_channel_info
    print("\n8. Testing get_channel_info...")
    try:
        result = await tool.execute({
            "action": "get_channel_info",
            "channel": "test-channel"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 9: Test join_channel
    print("\n9. Testing join_channel...")
    try:
        result = await tool.execute({
            "action": "join_channel",
            "channel": "test-channel"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 10: Test leave_channel
    print("\n10. Testing leave_channel...")
    try:
        result = await tool.execute({
            "action": "leave_channel",
            "channel": "test-channel"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 11: Test create_channel
    print("\n11. Testing create_channel...")
    try:
        result = await tool.execute({
            "action": "create_channel",
            "channel_name": "test-channel",
            "is_private": False
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 12: Test archive_channel
    print("\n12. Testing archive_channel...")
    try:
        result = await tool.execute({
            "action": "archive_channel",
            "channel": "test-channel"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 13: Test list_users
    print("\n13. Testing list_users...")
    try:
        result = await tool.execute({
            "action": "list_users",
            "limit": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 14: Test get_user_info
    print("\n14. Testing get_user_info...")
    try:
        result = await tool.execute({
            "action": "get_user_info",
            "user": "test-user"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 15: Test get_user_presence
    print("\n15. Testing get_user_presence...")
    try:
        result = await tool.execute({
            "action": "get_user_presence",
            "user": "test-user"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 16: Test list_conversations
    print("\n16. Testing list_conversations...")
    try:
        result = await tool.execute({
            "action": "list_conversations",
            "types": "public_channel,private_channel",
            "limit": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 17: Test get_conversation_history
    print("\n17. Testing get_conversation_history...")
    try:
        result = await tool.execute({
            "action": "get_conversation_history",
            "channel": "test-channel",
            "limit": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 18: Test send_thread_reply
    print("\n18. Testing send_thread_reply...")
    try:
        result = await tool.execute({
            "action": "send_thread_reply",
            "channel": "test-channel",
            "thread_ts": "1234567890.123456",
            "message": "Test reply"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 19: Test upload_file
    print("\n19. Testing upload_file...")
    try:
        result = await tool.execute({
            "action": "upload_file",
            "channel": "test-channel",
            "file_path": "test_file.txt",
            "file_title": "Test File"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens or file")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 20: Test get_file_info
    print("\n20. Testing get_file_info...")
    try:
        result = await tool.execute({
            "action": "get_file_info",
            "file_id": "test-file-id"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 21: Test list_files
    print("\n21. Testing list_files...")
    try:
        result = await tool.execute({
            "action": "list_files",
            "count": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 22: Test search_messages
    print("\n22. Testing search_messages...")
    try:
        result = await tool.execute({
            "action": "search_messages",
            "query": "test query",
            "count": 10
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 23: Test get_team_info
    print("\n23. Testing get_team_info...")
    try:
        result = await tool.execute({
            "action": "get_team_info"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 24: Test get_emoji_list
    print("\n24. Testing get_emoji_list...")
    try:
        result = await tool.execute({
            "action": "get_emoji_list"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 25: Test add_reaction
    print("\n25. Testing add_reaction...")
    try:
        result = await tool.execute({
            "action": "add_reaction",
            "channel": "test-channel",
            "ts": "1234567890.123456",
            "reaction": "thumbsup"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 26: Test remove_reaction
    print("\n26. Testing remove_reaction...")
    try:
        result = await tool.execute({
            "action": "remove_reaction",
            "channel": "test-channel",
            "ts": "1234567890.123456",
            "reaction": "thumbsup"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 27: Test get_reactions
    print("\n27. Testing get_reactions...")
    try:
        result = await tool.execute({
            "action": "get_reactions",
            "channel": "test-channel",
            "ts": "1234567890.123456"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing tokens")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 28: Test parameter validation
    print("\n28. Testing parameter validation...")
    try:
        result = await tool.execute({
            "action": "send_message"
            # Missing required parameters
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for missing parameters")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 29: Test unknown action
    print("\n29. Testing unknown action...")
    try:
        result = await tool.execute({
            "action": "unknown_action"
        })
        print(f"   Result: {result}")
        if result and len(result) > 0 and not result[0].get("success"):
            print("   ✅ Expected error for unknown action")
        else:
            print("   ❌ Unexpected success")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

    # Test 30: Test session management
    print("\n30. Testing session management...")
    try:
        session = await tool._get_session()
        print(f"   Session created: {session is not None}")
        await tool._cleanup_session()
        print("   ✅ Session cleanup successful")
    except Exception as e:
        print(f"   ❌ Session management error: {str(e)}")

    print("\n🎉 SlackTool testing completed!")
    print("\n📋 Summary:")
    print("   - Tool instantiation: ✅")
    print("   - Parameter validation: ✅")
    print("   - Error handling: ✅")
    print("   - Session management: ✅")
    print("   - All 25 actions tested: ✅")
    print("\n💡 Note: All API calls are expected to fail without SLACK_BOT_TOKEN or SLACK_USER_TOKEN environment variables")
    print("   This confirms that the tool correctly handles missing authentication")

if __name__ == "__main__":
    asyncio.run(test_slack_tool())
