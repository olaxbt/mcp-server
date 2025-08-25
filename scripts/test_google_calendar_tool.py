#!/usr/bin/env python3
"""
Test script for GoogleCalendarTool
Tests all available actions of the GoogleCalendarTool
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import GoogleCalendarTool

async def test_google_calendar_tool():
    """Test all GoogleCalendarTool actions"""
    print("🧪 Testing GoogleCalendarTool...")
    print("=" * 50)

    calendar = GoogleCalendarTool()

    # Test 1: List calendars
    print("\n1. Testing list_calendars...")
    result = await calendar.execute({"action": "list_calendars"})
    print(f"Result: {result}")

    # Test 2: Get calendar
    print("\n2. Testing get_calendar...")
    result = await calendar.execute({"action": "get_calendar", "calendar_id": "primary"})
    print(f"Result: {result}")

    # Test 3: List events
    print("\n3. Testing list_events...")
    result = await calendar.execute({
        "action": "list_events",
        "calendar_id": "primary",
        "time_min": "2024-01-01T00:00:00Z",
        "time_max": "2024-12-31T23:59:59Z",
        "max_results": 5
    })
    print(f"Result: {result}")

    # Test 4: Get event
    print("\n4. Testing get_event...")
    result = await calendar.execute({"action": "get_event", "calendar_id": "primary", "event_id": "test_event_id"})
    print(f"Result: {result}")

    # Test 5: Create event
    print("\n5. Testing create_event...")
    result = await calendar.execute({
        "action": "create_event",
        "calendar_id": "primary",
        "summary": "Test Event",
        "description": "This is a test event",
        "location": "Test Location",
        "start_time": "2024-12-25T10:00:00Z",
        "end_time": "2024-12-25T11:00:00Z",
        "attendees": ["test@example.com"]
    })
    print(f"Result: {result}")

    # Test 6: Update event
    print("\n6. Testing update_event...")
    result = await calendar.execute({
        "action": "update_event",
        "calendar_id": "primary",
        "event_id": "test_event_id",
        "summary": "Updated Test Event",
        "description": "This is an updated test event"
    })
    print(f"Result: {result}")

    # Test 7: Delete event
    print("\n7. Testing delete_event...")
    result = await calendar.execute({"action": "delete_event", "calendar_id": "primary", "event_id": "test_event_id"})
    print(f"Result: {result}")

    # Test 8: Get free/busy
    print("\n8. Testing get_free_busy...")
    result = await calendar.execute({
        "action": "get_free_busy",
        "time_min": "2024-12-25T00:00:00Z",
        "time_max": "2024-12-25T23:59:59Z",
        "calendar_ids": ["primary"]
    })
    print(f"Result: {result}")

    # Test 9: Get calendar list
    print("\n9. Testing get_calendar_list...")
    result = await calendar.execute({"action": "get_calendar_list"})
    print(f"Result: {result}")

    # Test 10: Create calendar
    print("\n10. Testing create_calendar...")
    result = await calendar.execute({
        "action": "create_calendar",
        "summary": "Test Calendar",
        "description": "This is a test calendar",
        "time_zone": "UTC"
    })
    print(f"Result: {result}")

    # Test 11: Delete calendar
    print("\n11. Testing delete_calendar...")
    result = await calendar.execute({"action": "delete_calendar", "calendar_id": "test_calendar_id"})
    print(f"Result: {result}")

    # Test 12: Get event instances
    print("\n12. Testing get_event_instances...")
    result = await calendar.execute({
        "action": "get_event_instances",
        "calendar_id": "primary",
        "event_id": "test_event_id",
        "time_min": "2024-01-01T00:00:00Z",
        "time_max": "2024-12-31T23:59:59Z"
    })
    print(f"Result: {result}")

    # Test 13: List events with different parameters
    print("\n13. Testing list_events with different parameters...")
    result = await calendar.execute({
        "action": "list_events",
        "calendar_id": "primary",
        "max_results": 3,
        "single_events": False,
        "order_by": "updated"
    })
    print(f"Result: {result}")

    # Test 14: Error handling - missing event_id
    print("\n14. Testing error handling (missing event_id)...")
    result = await calendar.execute({"action": "get_event", "calendar_id": "primary"})
    print(f"Result: {result}")

    # Test 15: Error handling - missing required parameters for create_event
    print("\n15. Testing error handling (missing parameters for create_event)...")
    result = await calendar.execute({"action": "create_event", "calendar_id": "primary", "summary": "Test"})
    print(f"Result: {result}")

    # Test 16: Error handling - missing event_id for update_event
    print("\n16. Testing error handling (missing event_id for update_event)...")
    result = await calendar.execute({"action": "update_event", "calendar_id": "primary"})
    print(f"Result: {result}")

    # Test 17: Error handling - missing event_id for delete_event
    print("\n17. Testing error handling (missing event_id for delete_event)...")
    result = await calendar.execute({"action": "delete_event", "calendar_id": "primary"})
    print(f"Result: {result}")

    # Test 18: Error handling - missing time parameters for free/busy
    print("\n18. Testing error handling (missing time parameters for free/busy)...")
    result = await calendar.execute({"action": "get_free_busy"})
    print(f"Result: {result}")

    # Test 19: Error handling - missing summary for create_calendar
    print("\n19. Testing error handling (missing summary for create_calendar)...")
    result = await calendar.execute({"action": "create_calendar"})
    print(f"Result: {result}")

    # Test 20: Error handling - missing calendar_id for delete_calendar
    print("\n20. Testing error handling (missing calendar_id for delete_calendar)...")
    result = await calendar.execute({"action": "delete_calendar"})
    print(f"Result: {result}")

    # Test 21: Error handling - invalid action
    print("\n21. Testing error handling (invalid action)...")
    result = await calendar.execute({"action": "invalid_action"})
    print(f"Result: {result}")

    # Test 22: Create event with minimal parameters
    print("\n22. Testing create_event with minimal parameters...")
    result = await calendar.execute({
        "action": "create_event",
        "summary": "Minimal Test Event",
        "start_time": "2024-12-26T10:00:00Z",
        "end_time": "2024-12-26T11:00:00Z"
    })
    print(f"Result: {result}")

    print("\n" + "=" * 50)
    print("✅ GoogleCalendarTool testing completed!")

if __name__ == "__main__":
    asyncio.run(test_google_calendar_tool())
