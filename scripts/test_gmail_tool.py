#!/usr/bin/env python3
"""
Test script for GmailTool
Tests all available actions of the GmailTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import GmailTool

async def test_gmail_tool():
    """Test all GmailTool actions"""
    print("🧪 Testing GmailTool...")
    print("=" * 50)

    gmail = GmailTool()

    # Test 1: Search emails
    print("\n1. Testing search_emails...")
    result = await gmail.execute({"action": "search_emails", "query": "is:unread", "max_results": 5})
    print(f"Result: {result}")

    # Test 2: Get email details
    print("\n2. Testing get_email...")
    result = await gmail.execute({"action": "get_email", "email_id": "test_email_id"})
    print(f"Result: {result}")

    # Test 3: Send email
    print("\n3. Testing send_email...")
    result = await gmail.execute({
        "action": "send_email",
        "to": "test@example.com",
        "subject": "Test Email",
        "body": "This is a test email"
    })
    print(f"Result: {result}")

    # Test 4: Get labels
    print("\n4. Testing get_labels...")
    result = await gmail.execute({"action": "get_labels"})
    print(f"Result: {result}")

    # Test 5: Create label
    print("\n5. Testing create_label...")
    result = await gmail.execute({"action": "create_label", "label_name": "Test Label"})
    print(f"Result: {result}")

    # Test 6: Delete label
    print("\n6. Testing delete_label...")
    result = await gmail.execute({"action": "delete_label", "label_id": "test_label_id"})
    print(f"Result: {result}")

    # Test 7: Get threads
    print("\n7. Testing get_threads...")
    result = await gmail.execute({"action": "get_threads", "query": "important", "max_results": 5})
    print(f"Result: {result}")

    # Test 8: Get attachments
    print("\n8. Testing get_attachments...")
    result = await gmail.execute({"action": "get_attachments", "email_id": "test_email_id", "attachment_id": "test_attachment_id"})
    print(f"Result: {result}")

    # Test 9: Mark as read
    print("\n9. Testing mark_as_read...")
    result = await gmail.execute({"action": "mark_as_read", "email_id": "test_email_id"})
    print(f"Result: {result}")

    # Test 10: Mark as unread
    print("\n10. Testing mark_as_unread...")
    result = await gmail.execute({"action": "mark_as_unread", "email_id": "test_email_id"})
    print(f"Result: {result}")

    # Test 11: Move to trash
    print("\n11. Testing move_to_trash...")
    result = await gmail.execute({"action": "move_to_trash", "email_id": "test_email_id"})
    print(f"Result: {result}")

    # Test 12: Get profile
    print("\n12. Testing get_profile...")
    result = await gmail.execute({"action": "get_profile"})
    print(f"Result: {result}")

    # Test 13: Search emails with spam/trash
    print("\n13. Testing search_emails with spam/trash...")
    result = await gmail.execute({"action": "search_emails", "query": "test", "include_spam_trash": True, "max_results": 3})
    print(f"Result: {result}")

    # Test 14: Error handling - missing email_id
    print("\n14. Testing error handling (missing email_id)...")
    result = await gmail.execute({"action": "get_email"})
    print(f"Result: {result}")

    # Test 15: Error handling - missing required parameters for send_email
    print("\n15. Testing error handling (missing parameters for send_email)...")
    result = await gmail.execute({"action": "send_email", "to": "test@example.com"})
    print(f"Result: {result}")

    # Test 16: Error handling - missing label_name
    print("\n16. Testing error handling (missing label_name)...")
    result = await gmail.execute({"action": "create_label"})
    print(f"Result: {result}")

    # Test 17: Error handling - missing label_id
    print("\n17. Testing error handling (missing label_id)...")
    result = await gmail.execute({"action": "delete_label"})
    print(f"Result: {result}")

    # Test 18: Error handling - missing email_id and attachment_id
    print("\n18. Testing error handling (missing email_id and attachment_id)...")
    result = await gmail.execute({"action": "get_attachments"})
    print(f"Result: {result}")

    # Test 19: Error handling - invalid action
    print("\n19. Testing error handling (invalid action)...")
    result = await gmail.execute({"action": "invalid_action"})
    print(f"Result: {result}")

    # Test 20: Search emails with different queries
    print("\n20. Testing search_emails with different queries...")
    result = await gmail.execute({"action": "search_emails", "query": "from:important@example.com", "max_results": 3})
    print(f"Result: {result}")

    print("\n" + "=" * 50)
    print("✅ GmailTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_gmail_tool())
