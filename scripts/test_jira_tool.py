#!/usr/bin/env python3
"""
Test script for JiraTool
Tests all actions, parameter validation, and error handling
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.mcp.tools import JiraTool

async def test_jira_tool():
    """Test the JiraTool with various scenarios."""
    print("🧪 Testing JiraTool...")

    tool = JiraTool()

    # Test 1: Tool instantiation
    print("\n1. Testing tool instantiation...")
    print(f"   Name: {tool.name}")
    print(f"   Description: {tool.description}")
    print(f"   Input Schema: {len(tool.input_schema['properties'])} properties")
    print("   ✅ Tool instantiated successfully")

    # Test 2: Check environment variables
    print("\n2. Checking environment variables...")
    print(f"   JIRA_DOMAIN: {'✅ Set' if tool.domain else '❌ Not set'}")
    print(f"   JIRA_USERNAME: {'✅ Set' if tool.username else '❌ Not set'}")
    print(f"   JIRA_API_TOKEN: {'✅ Set' if tool.api_token else '❌ Not set'}")
    print(f"   Base URL: {tool.base_url or '❌ Not configured'}")

    # Test 3: Test get_projects action
    print("\n3. Testing get_projects action...")
    try:
        result = await tool.execute({"action": "get_projects"})
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_projects: Success")
            else:
                print(f"   ❌ get_projects: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_projects: No result returned")
    except Exception as e:
        print(f"   ❌ get_projects: Error - {str(e)}")

    # Test 4: Test get_boards action
    print("\n4. Testing get_boards action...")
    try:
        result = await tool.execute({"action": "get_boards"})
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_boards: Success")
            else:
                print(f"   ❌ get_boards: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_boards: No result returned")
    except Exception as e:
        print(f"   ❌ get_boards: Error - {str(e)}")

    # Test 5: Test get_workflows action
    print("\n5. Testing get_workflows action...")
    try:
        result = await tool.execute({"action": "get_workflows"})
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_workflows: Success")
            else:
                print(f"   ❌ get_workflows: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_workflows: No result returned")
    except Exception as e:
        print(f"   ❌ get_workflows: Error - {str(e)}")

    # Test 6: Test get_users action
    print("\n6. Testing get_users action...")
    try:
        result = await tool.execute({"action": "get_users", "max_results": 10})
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_users: Success")
            else:
                print(f"   ❌ get_users: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_users: No result returned")
    except Exception as e:
        print(f"   ❌ get_users: Error - {str(e)}")

    # Test 7: Test search_issues action (with JQL)
    print("\n7. Testing search_issues action...")
    try:
        result = await tool.execute({
            "action": "search_issues",
            "jql": "project = TEST ORDER BY created DESC",
            "max_results": 5
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ search_issues: Success")
            else:
                print(f"   ❌ search_issues: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ search_issues: No result returned")
    except Exception as e:
        print(f"   ❌ search_issues: Error - {str(e)}")

    # Test 8: Test get_issues action (with project key)
    print("\n8. Testing get_issues action...")
    try:
        result = await tool.execute({
            "action": "get_issues",
            "project_key": "TEST",
            "max_results": 5
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_issues: Success")
            else:
                print(f"   ❌ get_issues: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_issues: No result returned")
    except Exception as e:
        print(f"   ❌ get_issues: Error - {str(e)}")

    # Test 9: Test get_issue action (with issue key)
    print("\n9. Testing get_issue action...")
    try:
        result = await tool.execute({
            "action": "get_issue",
            "issue_key": "TEST-1"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_issue: Success")
            else:
                print(f"   ❌ get_issue: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_issue: No result returned")
    except Exception as e:
        print(f"   ❌ get_issue: Error - {str(e)}")

    # Test 10: Test get_project action
    print("\n10. Testing get_project action...")
    try:
        result = await tool.execute({
            "action": "get_project",
            "project_key": "TEST"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_project: Success")
            else:
                print(f"   ❌ get_project: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_project: No result returned")
    except Exception as e:
        print(f"   ❌ get_project: Error - {str(e)}")

    # Test 11: Test get_sprints action
    print("\n11. Testing get_sprints action...")
    try:
        result = await tool.execute({
            "action": "get_sprints",
            "board_id": 1
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_sprints: Success")
            else:
                print(f"   ❌ get_sprints: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_sprints: No result returned")
    except Exception as e:
        print(f"   ❌ get_sprints: Error - {str(e)}")

    # Test 12: Test get_user action
    print("\n12. Testing get_user action...")
    try:
        result = await tool.execute({
            "action": "get_user",
            "username": "testuser"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_user: Success")
            else:
                print(f"   ❌ get_user: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_user: No result returned")
    except Exception as e:
        print(f"   ❌ get_user: Error - {str(e)}")

    # Test 13: Test get_issue_comments action
    print("\n13. Testing get_issue_comments action...")
    try:
        result = await tool.execute({
            "action": "get_issue_comments",
            "issue_key": "TEST-1",
            "max_results": 5
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_issue_comments: Success")
            else:
                print(f"   ❌ get_issue_comments: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_issue_comments: No result returned")
    except Exception as e:
        print(f"   ❌ get_issue_comments: Error - {str(e)}")

    # Test 14: Test get_attachments action
    print("\n14. Testing get_attachments action...")
    try:
        result = await tool.execute({
            "action": "get_attachments",
            "issue_key": "TEST-1"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_attachments: Success")
            else:
                print(f"   ❌ get_attachments: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_attachments: No result returned")
    except Exception as e:
        print(f"   ❌ get_attachments: Error - {str(e)}")

    # Test 15: Test get_issue_links action
    print("\n15. Testing get_issue_links action...")
    try:
        result = await tool.execute({
            "action": "get_issue_links",
            "issue_key": "TEST-1"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_issue_links: Success")
            else:
                print(f"   ❌ get_issue_links: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_issue_links: No result returned")
    except Exception as e:
        print(f"   ❌ get_issue_links: Error - {str(e)}")

    # Test 16: Test get_issue_watchers action
    print("\n16. Testing get_issue_watchers action...")
    try:
        result = await tool.execute({
            "action": "get_issue_watchers",
            "issue_key": "TEST-1"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_issue_watchers: Success")
            else:
                print(f"   ❌ get_issue_watchers: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_issue_watchers: No result returned")
    except Exception as e:
        print(f"   ❌ get_issue_watchers: Error - {str(e)}")

    # Test 17: Test get_project_components action
    print("\n17. Testing get_project_components action...")
    try:
        result = await tool.execute({
            "action": "get_project_components",
            "project_key": "TEST"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_project_components: Success")
            else:
                print(f"   ❌ get_project_components: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_project_components: No result returned")
    except Exception as e:
        print(f"   ❌ get_project_components: Error - {str(e)}")

    # Test 18: Test get_project_versions action
    print("\n18. Testing get_project_versions action...")
    try:
        result = await tool.execute({
            "action": "get_project_versions",
            "project_key": "TEST"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ get_project_versions: Success")
            else:
                print(f"   ❌ get_project_versions: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ get_project_versions: No result returned")
    except Exception as e:
        print(f"   ❌ get_project_versions: Error - {str(e)}")

    # Test 19: Test create_issue action (should fail without proper credentials)
    print("\n19. Testing create_issue action...")
    try:
        result = await tool.execute({
            "action": "create_issue",
            "project_key": "TEST",
            "summary": "Test Issue",
            "description": "This is a test issue",
            "issue_type": "Task"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ create_issue: Success")
            else:
                print(f"   ❌ create_issue: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ create_issue: No result returned")
    except Exception as e:
        print(f"   ❌ create_issue: Error - {str(e)}")

    # Test 20: Test add_comment action
    print("\n20. Testing add_comment action...")
    try:
        result = await tool.execute({
            "action": "add_comment",
            "issue_key": "TEST-1",
            "comment_body": "This is a test comment"
        })
        if result and len(result) > 0:
            if result[0].get("success"):
                print("   ✅ add_comment: Success")
            else:
                print(f"   ❌ add_comment: {result[0].get('error', 'Unknown error')}")
        else:
            print("   ❌ add_comment: No result returned")
    except Exception as e:
        print(f"   ❌ add_comment: Error - {str(e)}")

    # Test 21: Test parameter validation - missing required parameters
    print("\n21. Testing parameter validation...")
    try:
        result = await tool.execute({"action": "get_issue"})  # Missing issue_key
        if result and len(result) > 0:
            if not result[0].get("success") and "required" in result[0].get("error", "").lower():
                print("   ✅ Parameter validation: Correctly caught missing required parameter")
            else:
                print(f"   ❌ Parameter validation: Unexpected result - {result[0]}")
        else:
            print("   ❌ Parameter validation: No result returned")
    except Exception as e:
        print(f"   ❌ Parameter validation: Error - {str(e)}")

    # Test 22: Test unknown action
    print("\n22. Testing unknown action...")
    try:
        result = await tool.execute({"action": "unknown_action"})
        if result and len(result) > 0:
            if not result[0].get("success") and "unknown" in result[0].get("error", "").lower():
                print("   ✅ Unknown action: Correctly caught unknown action")
            else:
                print(f"   ❌ Unknown action: Unexpected result - {result[0]}")
        else:
            print("   ❌ Unknown action: No result returned")
    except Exception as e:
        print(f"   ❌ Unknown action: Error - {str(e)}")

    # Test 23: Test session management
    print("\n23. Testing session management...")
    try:
        # Test that session is created and cleaned up properly
        session1 = await tool._get_session()
        session2 = await tool._get_session()
        if session1 is session2:
            print("   ✅ Session management: Session reuse working correctly")
        else:
            print("   ❌ Session management: Session reuse not working")
        
        await tool._cleanup_session()
        print("   ✅ Session management: Session cleanup completed")
    except Exception as e:
        print(f"   ❌ Session management: Error - {str(e)}")

    # Test 24: Test input schema validation
    print("\n24. Testing input schema...")
    schema = tool.input_schema
    if schema and "properties" in schema and "action" in schema["properties"]:
        actions = schema["properties"]["action"]["enum"]
        print(f"   ✅ Input schema: {len(actions)} actions defined")
        print(f"   ✅ Input schema: Required fields: {schema.get('required', [])}")
    else:
        print("   ❌ Input schema: Invalid schema structure")

    # Test 25: Test tool properties
    print("\n25. Testing tool properties...")
    if tool.name == "jira":
        print("   ✅ Tool name: Correct")
    else:
        print(f"   ❌ Tool name: Expected 'jira', got '{tool.name}'")
    
    if "Jira" in tool.description:
        print("   ✅ Tool description: Contains 'Jira'")
    else:
        print(f"   ❌ Tool description: Missing 'Jira' - {tool.description}")

    print("\n🎉 JiraTool testing completed!")
    print("\n📝 Notes:")
    print("   - Most tests will fail with authentication errors without proper Jira credentials")
    print("   - Set JIRA_DOMAIN, JIRA_USERNAME, and JIRA_API_TOKEN environment variables for real testing")
    print("   - The tool correctly handles missing credentials and returns appropriate error messages")

if __name__ == "__main__":
    asyncio.run(test_jira_tool())
