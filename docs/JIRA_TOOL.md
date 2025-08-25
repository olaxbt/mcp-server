# JiraTool Documentation

## Overview

The `JiraTool` provides comprehensive integration with the Jira API for project management, issue tracking, and workflow management. This tool enables AI assistants to interact with Jira instances to manage projects, create and update issues, track workflows, and perform various project management tasks.

## Features

### Core Functionality
- **Issue Management**: Create, read, update, and delete issues
- **Project Management**: Access project information, components, and versions
- **Workflow Management**: View boards, sprints, and workflows
- **User Management**: Search and retrieve user information
- **Search Capabilities**: Advanced JQL (Jira Query Language) search
- **Comment Management**: Add and retrieve issue comments
- **Attachment Handling**: Access issue attachments
- **Issue Relationships**: View issue links and watchers

### Key Capabilities
- **REST API Integration**: Full integration with Jira REST API v3
- **Authentication**: Secure authentication using API tokens
- **Pagination Support**: Handle large result sets efficiently
- **Error Handling**: Comprehensive error handling and validation
- **Flexible Querying**: Support for complex JQL queries
- **Rich Content**: Support for Jira's rich text format

## Actions

### Issue Management

#### `get_issues`
Retrieve issues from a specific project.

**Parameters:**
- `project_key` (string, required): Jira project key
- `max_results` (integer, optional): Maximum number of results (default: 50, max: 100)
- `start_at` (integer, optional): Starting index for pagination (default: 0)
- `expand` (string, optional): Fields to expand in response (default: "names,schema")

**Example:**
```json
{
  "action": "get_issues",
  "project_key": "PROJ",
  "max_results": 10
}
```

#### `get_issue`
Retrieve a specific issue by its key.

**Parameters:**
- `issue_key` (string, required): Jira issue key (e.g., "PROJ-123")
- `expand` (string, optional): Fields to expand in response (default: "names,schema")

**Example:**
```json
{
  "action": "get_issue",
  "issue_key": "PROJ-123"
}
```

#### `create_issue`
Create a new issue.

**Parameters:**
- `project_key` (string, required): Jira project key
- `summary` (string, required): Issue summary/title
- `description` (string, optional): Issue description
- `issue_type` (string, optional): Issue type (default: "Task")
- `priority` (string, optional): Issue priority
- `assignee` (string, optional): Assignee username or account ID
- `reporter` (string, optional): Reporter username or account ID
- `labels` (array, optional): List of labels
- `components` (array, optional): List of component names
- `fix_versions` (array, optional): List of fix version names
- `fields` (object, optional): Additional fields to set

**Example:**
```json
{
  "action": "create_issue",
  "project_key": "PROJ",
  "summary": "Implement new feature",
  "description": "Add user authentication system",
  "issue_type": "Story",
  "priority": "High",
  "assignee": "john.doe",
  "labels": ["feature", "authentication"]
}
```

#### `update_issue`
Update an existing issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key
- `fields` (object, required): Fields to update

**Example:**
```json
{
  "action": "update_issue",
  "issue_key": "PROJ-123",
  "fields": {
    "summary": "Updated summary",
    "priority": {"name": "Medium"}
  }
}
```

#### `delete_issue`
Delete an issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key

**Example:**
```json
{
  "action": "delete_issue",
  "issue_key": "PROJ-123"
}
```

### Project Management

#### `get_projects`
Retrieve all projects.

**Parameters:**
- `expand` (string, optional): Fields to expand (default: "lead,issueTypes")

**Example:**
```json
{
  "action": "get_projects"
}
```

#### `get_project`
Retrieve a specific project.

**Parameters:**
- `project_key` (string, required): Jira project key
- `expand` (string, optional): Fields to expand (default: "lead,issueTypes")

**Example:**
```json
{
  "action": "get_project",
  "project_key": "PROJ"
}
```

#### `get_project_components`
Retrieve components for a project.

**Parameters:**
- `project_key` (string, required): Jira project key

**Example:**
```json
{
  "action": "get_project_components",
  "project_key": "PROJ"
}
```

#### `get_project_versions`
Retrieve versions for a project.

**Parameters:**
- `project_key` (string, required): Jira project key

**Example:**
```json
{
  "action": "get_project_versions",
  "project_key": "PROJ"
}
```

### Workflow Management

#### `get_boards`
Retrieve all boards.

**Example:**
```json
{
  "action": "get_boards"
}
```

#### `get_sprints`
Retrieve sprints for a board.

**Parameters:**
- `board_id` (integer, required): Board ID
- `state` (string, optional): Sprint state (default: "active")

**Example:**
```json
{
  "action": "get_sprints",
  "board_id": 1
}
```

#### `get_workflows`
Retrieve workflows.

**Example:**
```json
{
  "action": "get_workflows"
}
```

### User Management

#### `get_users`
Retrieve users.

**Parameters:**
- `max_results` (integer, optional): Maximum number of results (default: 50, max: 100)
- `start_at` (integer, optional): Starting index for pagination (default: 0)

**Example:**
```json
{
  "action": "get_users",
  "max_results": 10
}
```

#### `get_user`
Retrieve a specific user.

**Parameters:**
- `username` (string, required): Username or account ID

**Example:**
```json
{
  "action": "get_user",
  "username": "john.doe"
}
```

### Search and Query

#### `search_issues`
Search issues using JQL.

**Parameters:**
- `jql` (string, required): JQL search string
- `max_results` (integer, optional): Maximum number of results (default: 50, max: 100)
- `start_at` (integer, optional): Starting index for pagination (default: 0)
- `expand` (string, optional): Fields to expand (default: "names,schema")

**Example:**
```json
{
  "action": "search_issues",
  "jql": "project = PROJ AND priority = High ORDER BY created DESC",
  "max_results": 20
}
```

### Comments and Attachments

#### `get_issue_comments`
Retrieve comments for an issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key
- `max_results` (integer, optional): Maximum number of results (default: 50, max: 100)
- `start_at` (integer, optional): Starting index for pagination (default: 0)

**Example:**
```json
{
  "action": "get_issue_comments",
  "issue_key": "PROJ-123",
  "max_results": 10
}
```

#### `add_comment`
Add a comment to an issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key
- `comment_body` (string, required): Comment text content

**Example:**
```json
{
  "action": "add_comment",
  "issue_key": "PROJ-123",
  "comment_body": "This issue has been resolved."
}
```

#### `get_attachments`
Retrieve attachments for an issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key

**Example:**
```json
{
  "action": "get_attachments",
  "issue_key": "PROJ-123"
}
```

### Issue Relationships

#### `get_issue_links`
Retrieve issue links for an issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key

**Example:**
```json
{
  "action": "get_issue_links",
  "issue_key": "PROJ-123"
}
```

#### `get_issue_watchers`
Retrieve watchers for an issue.

**Parameters:**
- `issue_key` (string, required): Jira issue key

**Example:**
```json
{
  "action": "get_issue_watchers",
  "issue_key": "PROJ-123"
}
```

## Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // Jira API response data
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error description"
}
```

## Key Data Points

### Issue Fields
- **Basic Info**: Key, summary, description, status, priority
- **Assignment**: Assignee, reporter, watchers
- **Classification**: Labels, components, fix versions
- **Timing**: Created, updated, due date
- **Relationships**: Links, subtasks, parent issues
- **Content**: Comments, attachments, work logs

### Project Information
- **Details**: Name, key, description, lead
- **Settings**: Issue types, components, versions
- **Access**: Permissions, roles, users

### Workflow Data
- **Boards**: Kanban and Scrum boards
- **Sprints**: Active, future, and closed sprints
- **Workflows**: Process definitions and transitions

## Integration

### Environment Variables
Set the following environment variables for authentication:

```bash
# Jira Cloud instance domain (e.g., "mycompany" for mycompany.atlassian.net)
export JIRA_DOMAIN="your-domain"

# Jira username (email address)
export JIRA_USERNAME="your-email@company.com"

# Jira API token (not password)
export JIRA_API_TOKEN="your-api-token"
```

### API Setup
1. **Create API Token**:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a label and copy the token

2. **Verify Permissions**:
   - Ensure your user has appropriate permissions in Jira
   - API token inherits user permissions

3. **Test Connection**:
   - Use the `get_projects` action to verify connectivity
   - Check error messages for authentication issues

### Rate Limits
- **Jira Cloud**: 1000 requests per hour per user
- **Jira Server**: Varies by configuration
- **Best Practices**:
  - Use pagination for large result sets
  - Cache frequently accessed data
  - Implement exponential backoff for retries

## Testing

### Individual Tool Testing
```bash
python scripts/test_jira_tool.py
```

### Comprehensive Testing
```bash
python scripts/test_all_tools.py
```

### Manual Testing
```python
from app.mcp.tools import JiraTool

# Create tool instance
jira = JiraTool()

# Test basic functionality
result = await jira.execute({
    "action": "get_projects"
})
print(result)
```

## Error Handling

### Common Errors
- **401 Unauthorized**: Invalid credentials or expired token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **429 Too Many Requests**: Rate limit exceeded

### Error Recovery
- **Authentication Errors**: Verify credentials and token validity
- **Permission Errors**: Check user permissions in Jira
- **Rate Limit Errors**: Implement retry logic with backoff
- **Network Errors**: Handle connection timeouts and retries

## Use Cases

### Project Management
- **Issue Tracking**: Create and manage development tasks
- **Sprint Planning**: Organize work into sprints
- **Release Management**: Track versions and releases
- **Team Coordination**: Assign work and track progress

### Development Workflow
- **Bug Tracking**: Report and track software defects
- **Feature Development**: Manage new feature implementation
- **Code Reviews**: Link issues to pull requests
- **Testing**: Track test cases and results

### Reporting and Analytics
- **Progress Tracking**: Monitor project and sprint progress
- **Team Performance**: Analyze work patterns and velocity
- **Quality Metrics**: Track bug rates and resolution times
- **Capacity Planning**: Analyze team workload and availability

## Advanced Features

### JQL Queries
JQL (Jira Query Language) provides powerful search capabilities:

```json
{
  "action": "search_issues",
  "jql": "project = PROJ AND priority in (High, Critical) AND status != Done ORDER BY created DESC"
}
```

### Rich Text Content
Support for Jira's rich text format in descriptions and comments:

```json
{
  "action": "create_issue",
  "project_key": "PROJ",
  "summary": "Test Issue",
  "description": "This is a **bold** description with *italic* text and [links](https://example.com)"
}
```

### Bulk Operations
Efficient handling of multiple issues:

```json
{
  "action": "search_issues",
  "jql": "project = PROJ AND status = 'In Progress'",
  "max_results": 100
}
```

## Best Practices

### Performance Optimization
- **Pagination**: Use `start_at` and `max_results` for large datasets
- **Field Selection**: Use `expand` parameter to limit returned fields
- **Caching**: Cache frequently accessed data like projects and users
- **Batch Operations**: Group related operations when possible

### Security Considerations
- **API Tokens**: Use API tokens instead of passwords
- **Permissions**: Follow principle of least privilege
- **Audit Logging**: Monitor API usage for security
- **Token Rotation**: Regularly rotate API tokens

### Error Handling
- **Graceful Degradation**: Handle API failures gracefully
- **Retry Logic**: Implement exponential backoff for retries
- **User Feedback**: Provide clear error messages to users
- **Logging**: Log errors for debugging and monitoring

## Troubleshooting

### Common Issues

#### Authentication Problems
```
Error: Jira credentials not configured
```
**Solution**: Verify environment variables are set correctly

#### Permission Errors
```
Error: API error 403: Forbidden
```
**Solution**: Check user permissions in Jira project settings

#### Rate Limiting
```
Error: API error 429: Too Many Requests
```
**Solution**: Implement rate limiting and retry logic

#### Network Issues
```
Error: Request failed: Connection timeout
```
**Solution**: Check network connectivity and Jira instance availability

### Debug Mode
Enable detailed logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Documentation
- **Jira REST API**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **JQL Reference**: https://confluence.atlassian.com/jiracorecloud/advanced-searching-764478330.html
- **Authentication**: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/

## Future Enhancements

### Planned Features
- **Webhook Support**: Real-time issue updates
- **Bulk Operations**: Batch create/update issues
- **Advanced Search**: Complex JQL builder
- **Workflow Automation**: Trigger workflows via API
- **Reporting**: Built-in analytics and reporting
- **Integration**: Connect with other development tools

### Customization Options
- **Custom Fields**: Support for custom issue fields
- **Workflow Transitions**: Automated status changes
- **Notification Rules**: Custom notification settings
- **Template Management**: Issue templates and forms
- **Dashboard Integration**: Embed Jira data in dashboards
