# SlackTool Documentation

## Overview

The `SlackTool` provides comprehensive integration with the Slack API for messaging, channel management, user operations, and team collaboration. This tool enables AI assistants to interact with Slack workspaces to send messages, manage channels, handle files, and perform various team collaboration tasks.

## Features

- **Messaging**: Send messages to channels and direct messages
- **Channel Management**: List, join, leave, create, and archive channels
- **User Operations**: Get user information and presence status
- **File Management**: Upload, list, and get file information
- **Search**: Search for messages across the workspace
- **Reactions**: Add and remove emoji reactions
- **Thread Management**: Send replies in message threads
- **Team Information**: Get workspace and emoji information

## Actions

### 1. send_message
Send a message to a specific channel.

**Parameters:**
- `channel` (string, required): Channel ID or name (with #)
- `message` (string, required): Message text to send
- `thread_ts` (string, optional): Thread timestamp for replies

**Example:**
```json
{
  "action": "send_message",
  "channel": "general",
  "message": "Hello from AI assistant!",
  "thread_ts": "1234567890.123456"
}
```

### 2. send_direct_message
Send a direct message to a specific user.

**Parameters:**
- `user` (string, required): User ID or username
- `message` (string, required): Message text to send

**Example:**
```json
{
  "action": "send_direct_message",
  "user": "U1234567890",
  "message": "Hello! This is a direct message."
}
```

### 3. get_channel_history
Get message history for a specific channel.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `limit` (integer, optional): Maximum number of results (1-1000, default: 100)
- `oldest` (string, optional): Start of time range (timestamp)
- `latest` (string, optional): End of time range (timestamp)
- `inclusive` (boolean, optional): Include messages with oldest or latest timestamps (default: false)

**Example:**
```json
{
  "action": "get_channel_history",
  "channel": "general",
  "limit": 50,
  "oldest": "1234567890.000000",
  "latest": "1234567899.999999"
}
```

### 4. get_direct_message_history
Get message history for a direct message conversation.

**Parameters:**
- `user` (string, required): User ID or username
- `limit` (integer, optional): Maximum number of results (1-1000, default: 100)
- `oldest` (string, optional): Start of time range (timestamp)
- `latest` (string, optional): End of time range (timestamp)

**Example:**
```json
{
  "action": "get_direct_message_history",
  "user": "U1234567890",
  "limit": 20
}
```

### 5. list_channels
List all channels in the workspace.

**Parameters:**
- `limit` (integer, optional): Maximum number of results (1-1000, default: 100)
- `exclude_archived` (boolean, optional): Exclude archived conversations (default: true)

**Example:**
```json
{
  "action": "list_channels",
  "limit": 50,
  "exclude_archived": true
}
```

### 6. get_channel_info
Get information about a specific channel.

**Parameters:**
- `channel` (string, required): Channel ID or name

**Example:**
```json
{
  "action": "get_channel_info",
  "channel": "general"
}
```

### 7. join_channel
Join a specific channel.

**Parameters:**
- `channel` (string, required): Channel name (without #)

**Example:**
```json
{
  "action": "join_channel",
  "channel": "new-project"
}
```

### 8. leave_channel
Leave a specific channel.

**Parameters:**
- `channel` (string, required): Channel ID or name

**Example:**
```json
{
  "action": "leave_channel",
  "channel": "general"
}
```

### 9. create_channel
Create a new channel.

**Parameters:**
- `channel_name` (string, required): Name for new channel (without #)
- `is_private` (boolean, optional): Whether channel should be private (default: false)

**Example:**
```json
{
  "action": "create_channel",
  "channel_name": "project-alpha",
  "is_private": false
}
```

### 10. archive_channel
Archive a specific channel.

**Parameters:**
- `channel` (string, required): Channel ID or name

**Example:**
```json
{
  "action": "archive_channel",
  "channel": "old-project"
}
```

### 11. list_users
List all users in the workspace.

**Parameters:**
- `limit` (integer, optional): Maximum number of results (1-1000, default: 100)

**Example:**
```json
{
  "action": "list_users",
  "limit": 100
}
```

### 12. get_user_info
Get information about a specific user.

**Parameters:**
- `user` (string, required): User ID or username

**Example:**
```json
{
  "action": "get_user_info",
  "user": "U1234567890"
}
```

### 13. get_user_presence
Get user's presence status.

**Parameters:**
- `user` (string, required): User ID or username

**Example:**
```json
{
  "action": "get_user_presence",
  "user": "U1234567890"
}
```

### 14. list_conversations
List conversations (channels, DMs, etc.).

**Parameters:**
- `types` (string, optional): Comma-separated list of conversation types (public_channel, private_channel, mpim, im, default: "public_channel,private_channel,mpim,im")
- `exclude_archived` (boolean, optional): Exclude archived conversations (default: true)
- `limit` (integer, optional): Maximum number of results (1-1000, default: 100)

**Example:**
```json
{
  "action": "list_conversations",
  "types": "public_channel,private_channel",
  "limit": 50
}
```

### 15. get_conversation_history
Get conversation history.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `limit` (integer, optional): Maximum number of results (1-1000, default: 100)
- `oldest` (string, optional): Start of time range (timestamp)
- `latest` (string, optional): End of time range (timestamp)

**Example:**
```json
{
  "action": "get_conversation_history",
  "channel": "general",
  "limit": 20
}
```

### 16. send_thread_reply
Send a reply in a message thread.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `thread_ts` (string, required): Thread timestamp for replies
- `message` (string, required): Message text to send

**Example:**
```json
{
  "action": "send_thread_reply",
  "channel": "general",
  "thread_ts": "1234567890.123456",
  "message": "This is a thread reply"
}
```

### 17. upload_file
Upload a file to Slack.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `file_path` (string, required): Path to file to upload
- `file_title` (string, optional): Title for uploaded file
- `file_comment` (string, optional): Comment for uploaded file

**Example:**
```json
{
  "action": "upload_file",
  "channel": "general",
  "file_path": "/path/to/document.pdf",
  "file_title": "Project Report",
  "file_comment": "Here's the latest project report"
}
```

### 18. get_file_info
Get information about a specific file.

**Parameters:**
- `file_id` (string, required): File ID for file operations

**Example:**
```json
{
  "action": "get_file_info",
  "file_id": "F1234567890"
}
```

### 19. list_files
List files in the workspace.

**Parameters:**
- `channel` (string, optional): Channel ID to filter files
- `user` (string, optional): User ID to filter files
- `count` (integer, optional): Number of results to return (1-100, default: 20)
- `page` (integer, optional): Page number for pagination (default: 1)

**Example:**
```json
{
  "action": "list_files",
  "count": 10,
  "page": 1
}
```

### 20. search_messages
Search for messages in the workspace.

**Parameters:**
- `query` (string, required): Search query for messages
- `count` (integer, optional): Number of results to return (1-100, default: 20)
- `page` (integer, optional): Page number for pagination (default: 1)

**Example:**
```json
{
  "action": "search_messages",
  "query": "project update",
  "count": 10
}
```

### 21. get_team_info
Get team/workspace information.

**Parameters:** None

**Example:**
```json
{
  "action": "get_team_info"
}
```

### 22. get_emoji_list
Get list of custom emojis in the workspace.

**Parameters:** None

**Example:**
```json
{
  "action": "get_emoji_list"
}
```

### 23. add_reaction
Add a reaction to a message.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `ts` (string, required): Message timestamp
- `reaction` (string, required): Emoji reaction (e.g., 'thumbsup')

**Example:**
```json
{
  "action": "add_reaction",
  "channel": "general",
  "ts": "1234567890.123456",
  "reaction": "thumbsup"
}
```

### 24. remove_reaction
Remove a reaction from a message.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `ts` (string, required): Message timestamp
- `reaction` (string, required): Emoji reaction to remove

**Example:**
```json
{
  "action": "remove_reaction",
  "channel": "general",
  "ts": "1234567890.123456",
  "reaction": "thumbsup"
}
```

### 25. get_reactions
Get reactions for a message.

**Parameters:**
- `channel` (string, required): Channel ID or name
- `ts` (string, required): Message timestamp

**Example:**
```json
{
  "action": "get_reactions",
  "channel": "general",
  "ts": "1234567890.123456"
}
```

## Response Format

All actions return a list containing a single dictionary with the following structure:

### Success Response
```json
[
  {
    "success": true,
    "data": {
      "ok": true,
      "channel": "C1234567890",
      "ts": "1234567890.123456",
      "message": {
        "text": "Hello from AI assistant!",
        "user": "U1234567890",
        "ts": "1234567890.123456"
      }
    }
  }
]
```

### Error Response
```json
[
  {
    "success": false,
    "error": "Slack API error: invalid_auth"
  }
]
```

## Error Handling

The tool handles various error scenarios:

1. **Missing Authentication**: Returns error when `SLACK_BOT_TOKEN` or `SLACK_USER_TOKEN` is not configured
2. **Invalid Parameters**: Returns error when required parameters are missing
3. **API Errors**: Returns Slack API error messages
4. **Network Errors**: Returns connection error messages
5. **File Errors**: Returns file not found or upload error messages

## Integration

### Environment Variables

Set the following environment variables for authentication:

```bash
# Bot Token (recommended for most operations)
export SLACK_BOT_TOKEN="xoxb-your-bot-token"

# User Token (for user-specific operations)
export SLACK_USER_TOKEN="xoxp-your-user-token"
```

### API Setup

1. **Create a Slack App**:
   - Go to https://api.slack.com/apps
   - Click "Create New App"
   - Choose "From scratch"
   - Enter app name and select workspace

2. **Configure Bot Token Scopes**:
   - Go to "OAuth & Permissions"
   - Add required scopes:
     - `chat:write` - Send messages
     - `channels:read` - Read channel information
     - `channels:write` - Join/leave channels
     - `users:read` - Read user information
     - `files:write` - Upload files
     - `reactions:write` - Add/remove reactions
     - `search:read` - Search messages

3. **Install App to Workspace**:
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the Bot User OAuth Token

### Rate Limits

Slack API has rate limits:
- **Tier 1**: 1 request per second
- **Tier 2**: 20 requests per minute
- **Tier 3**: 50 requests per minute
- **Tier 4**: 100 requests per minute

The tool handles rate limiting automatically by respecting Slack's rate limit headers.

## Testing

Run the comprehensive test suite:

```bash
# Test SlackTool specifically
python scripts/test_slack_tool.py

# Test all tools including SlackTool
python scripts/test_all_tools.py
```

## Use Cases

### 1. Team Communication
- Send automated notifications to channels
- Create project-specific channels
- Archive old channels

### 2. File Sharing
- Upload reports and documents
- Share files with specific channels
- Track file usage and information

### 3. User Management
- Get user information and presence
- List workspace members
- Monitor user activity

### 4. Message Management
- Search for specific messages
- Get conversation history
- Manage message threads

### 5. Reactions and Engagement
- Add reactions to messages
- Track message engagement
- Manage team interactions

## Advanced Features

### 1. Thread Management
The tool supports Slack's threading system for organized conversations:

```json
{
  "action": "send_message",
  "channel": "general",
  "message": "Main message",
  "thread_ts": "1234567890.123456"
}
```

### 2. File Upload with Metadata
Upload files with custom titles and comments:

```json
{
  "action": "upload_file",
  "channel": "general",
  "file_path": "/path/to/file.pdf",
  "file_title": "Custom Title",
  "file_comment": "File description"
}
```

### 3. Conversation Filtering
Filter conversations by type and status:

```json
{
  "action": "list_conversations",
  "types": "public_channel,private_channel",
  "exclude_archived": true
}
```

## Best Practices

1. **Use Bot Tokens**: Prefer bot tokens over user tokens for most operations
2. **Handle Rate Limits**: Implement proper error handling for rate limit responses
3. **Validate Inputs**: Always validate channel names and user IDs before API calls
4. **Error Handling**: Implement proper error handling for all API responses
5. **File Management**: Clean up temporary files after upload
6. **Security**: Never expose tokens in logs or error messages

## Troubleshooting

### Common Issues

1. **"invalid_auth" Error**:
   - Check if token is correctly set
   - Verify token has required scopes
   - Ensure token is not expired

2. **"channel_not_found" Error**:
   - Verify channel name or ID is correct
   - Check if bot has access to the channel
   - Ensure channel exists and is not archived

3. **"file_not_found" Error**:
   - Verify file path is correct
   - Check file permissions
   - Ensure file exists and is readable

4. **Rate Limit Errors**:
   - Implement exponential backoff
   - Reduce request frequency
   - Use bulk operations when possible

### Debug Mode

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

1. **Token Security**: Store tokens securely and never commit them to version control
2. **Scope Limitation**: Use minimal required scopes for your use case
3. **Input Validation**: Validate all user inputs before sending to Slack API
4. **Error Handling**: Don't expose sensitive information in error messages
5. **Rate Limiting**: Respect Slack's rate limits to avoid service disruption

## Performance Optimization

1. **Session Reuse**: The tool reuses HTTP sessions for better performance
2. **Batch Operations**: Use bulk operations when possible
3. **Caching**: Implement caching for frequently accessed data
4. **Connection Pooling**: Use connection pooling for high-volume operations

## Future Enhancements

Potential improvements for the SlackTool:

1. **Webhook Support**: Add support for incoming webhooks
2. **Event Subscriptions**: Implement real-time event handling
3. **Message Formatting**: Add support for rich message formatting
4. **Bulk Operations**: Add support for bulk message sending
5. **Analytics**: Add message analytics and reporting features
6. **Integration**: Add support for other Slack features like apps and workflows
