# Gmail Tool Documentation

## Overview

The `GmailTool` provides comprehensive access to Gmail data through the Gmail API, including email search, sending emails, managing labels, and email management. This tool enables AI assistants to interact with Gmail accounts for email automation, organization, and communication tasks.

## Features

### Available Actions

1. **search_emails** - Search for emails using Gmail search syntax
2. **get_email** - Get detailed information about a specific email
3. **send_email** - Send an email to recipients
4. **get_labels** - Get all Gmail labels
5. **create_label** - Create a new Gmail label
6. **delete_label** - Delete a Gmail label
7. **get_threads** - Get email threads
8. **get_attachments** - Get email attachments
9. **mark_as_read** - Mark an email as read
10. **mark_as_unread** - Mark an email as unread
11. **move_to_trash** - Move an email to trash
12. **get_profile** - Get Gmail profile information

### Supported Parameters

- **query** - Search query for emails (Gmail search syntax)
- **email_id** - Gmail message ID
- **thread_id** - Gmail thread ID
- **to** - Recipient email address
- **subject** - Email subject
- **body** - Email body content
- **label_name** - Label name for creation or management
- **label_id** - Label ID for deletion
- **max_results** - Maximum number of results to return (default: 10)
- **include_spam_trash** - Include spam and trash in search (default: False)

## Usage Examples

### 1. Search for Emails

```python
# Basic email search
result = await gmail.execute({
    "action": "search_emails",
    "query": "is:unread",
    "max_results": 10
})

# Advanced search with filters
result = await gmail.execute({
    "action": "search_emails",
    "query": "from:important@example.com subject:urgent",
    "max_results": 5,
    "include_spam_trash": False
})
```

### 2. Get Email Details

```python
result = await gmail.execute({
    "action": "get_email",
    "email_id": "message_id_here"
})
```

### 3. Send an Email

```python
result = await gmail.execute({
    "action": "send_email",
    "to": "recipient@example.com",
    "subject": "Important Message",
    "body": "This is the email content."
})
```

### 4. Get All Labels

```python
result = await gmail.execute({
    "action": "get_labels"
})
```

### 5. Create a New Label

```python
result = await gmail.execute({
    "action": "create_label",
    "label_name": "Important"
})
```

### 6. Delete a Label

```python
result = await gmail.execute({
    "action": "delete_label",
    "label_id": "label_id_here"
})
```

### 7. Get Email Threads

```python
result = await gmail.execute({
    "action": "get_threads",
    "query": "important",
    "max_results": 10
})
```

### 8. Get Email Attachments

```python
result = await gmail.execute({
    "action": "get_attachments",
    "email_id": "message_id_here",
    "attachment_id": "attachment_id_here"
})
```

### 9. Mark Email as Read

```python
result = await gmail.execute({
    "action": "mark_as_read",
    "email_id": "message_id_here"
})
```

### 10. Mark Email as Unread

```python
result = await gmail.execute({
    "action": "mark_as_unread",
    "email_id": "message_id_here"
})
```

### 11. Move Email to Trash

```python
result = await gmail.execute({
    "action": "move_to_trash",
    "email_id": "message_id_here"
})
```

### 12. Get Profile Information

```python
result = await gmail.execute({
    "action": "get_profile"
})
```

## Response Format

### Success Response

```json
{
    "success": true,
    "action": "search_emails",
    "query": "is:unread",
    "data": {
        "messages": [...],
        "next_page_token": "token_here",
        "result_size_estimate": 100,
        "timestamp": "2024-01-15T10:30:00"
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": "Failed to search emails: 401"
}
```

## Key Data Points

### Email Information
- **Message ID** - Unique identifier for the email
- **Thread ID** - Thread identifier for conversation grouping
- **Headers** - Email headers (From, To, Subject, Date, etc.)
- **Body** - Email body content
- **Parts** - Multipart email content
- **Label IDs** - Associated labels
- **Snippet** - Email preview text

### Label Information
- **Label ID** - Unique identifier for the label
- **Label Name** - Display name of the label
- **Message List Visibility** - Visibility in message list
- **Label List Visibility** - Visibility in label list
- **Type** - Label type (system, user)

### Thread Information
- **Thread ID** - Unique identifier for the thread
- **History ID** - History identifier for changes
- **Messages** - Messages in the thread
- **Snippet** - Thread preview text

## Integration

### Environment Variables

Set the following environment variables to enable Gmail API access:

```bash
export GMAIL_ACCESS_TOKEN="your_gmail_access_token_here"
export GMAIL_API_KEY="your_gmail_api_key_here"  # Optional
```

### API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API
4. Create OAuth 2.0 credentials
5. Set up OAuth consent screen
6. Generate access tokens for your application
7. Set the access token as an environment variable

### OAuth 2.0 Scopes

The Gmail API requires the following scopes:
- `https://www.googleapis.com/auth/gmail.readonly` - Read-only access
- `https://www.googleapis.com/auth/gmail.modify` - Read and modify access
- `https://www.googleapis.com/auth/gmail.compose` - Compose and send emails
- `https://www.googleapis.com/auth/gmail.send` - Send emails
- `https://www.googleapis.com/auth/gmail.labels` - Manage labels

### Rate Limits

The Gmail API has the following quotas:
- **Queries per day**: 1,000,000,000
- **Queries per 100 seconds per user**: 250
- **Queries per 100 seconds**: 1,000

## Testing

### Individual Tool Testing

Run the dedicated test script:

```bash
python scripts/test_gmail_tool.py
```

### Comprehensive Testing

Include GmailTool in the comprehensive test suite:

```bash
python scripts/test_all_tools.py
```

### Test Coverage

The test suite covers:
- ✅ All 12 available actions
- ✅ Parameter validation
- ✅ Error handling
- ✅ Gmail search syntax
- ✅ Email management operations
- ✅ Session management

## Error Handling

The tool handles various error scenarios:

1. **Missing Access Token** - Returns error when GMAIL_ACCESS_TOKEN is not set
2. **Invalid Parameters** - Validates required parameters and returns descriptive errors
3. **API Errors** - Handles HTTP status codes and API-specific errors
4. **Network Issues** - Gracefully handles connection timeouts and network failures
5. **Authentication Errors** - Handles OAuth token expiration and invalid tokens

## Gmail Search Syntax

The tool supports Gmail's powerful search syntax:

### Basic Search Operators
- `from:email@example.com` - Emails from specific sender
- `to:email@example.com` - Emails to specific recipient
- `subject:keyword` - Emails with keyword in subject
- `has:attachment` - Emails with attachments
- `is:unread` - Unread emails
- `is:read` - Read emails
- `is:starred` - Starred emails
- `is:important` - Important emails

### Advanced Search Operators
- `after:2024/01/01` - Emails after specific date
- `before:2024/12/31` - Emails before specific date
- `larger:10M` - Emails larger than 10MB
- `smaller:1M` - Emails smaller than 1MB
- `filename:pdf` - Emails with PDF attachments
- `label:important` - Emails with specific label

## Use Cases

### Email Automation
- Auto-respond to specific emails
- Process incoming emails based on criteria
- Organize emails into labels automatically
- Archive old emails

### Email Management
- Search and filter emails efficiently
- Manage email labels and organization
- Mark emails as read/unread
- Move emails to trash

### Communication
- Send automated emails
- Compose and send bulk emails
- Reply to emails programmatically
- Forward emails to other addresses

### Email Analysis
- Analyze email patterns
- Extract email metadata
- Process email attachments
- Generate email reports

## Notes

- **Access Token Required**: The tool requires a valid Gmail API access token
- **Real Data**: Uses actual Gmail API data when available
- **OAuth 2.0**: Requires proper OAuth 2.0 setup and token management
- **Rate Limiting**: Respects Gmail API quotas and rate limits
- **Error Handling**: Returns descriptive error messages for troubleshooting
- **Session Management**: Efficiently manages HTTP sessions for API calls
- **Search Syntax**: Supports full Gmail search syntax for powerful filtering
- **Security**: Handles sensitive email data securely
