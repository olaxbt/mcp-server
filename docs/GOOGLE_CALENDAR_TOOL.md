# Google Calendar Tool Documentation

## Overview

The `GoogleCalendarTool` provides comprehensive access to Google Calendar data through the Google Calendar API v3, including event management, calendar operations, scheduling, and calendar analytics. This tool enables AI assistants to interact with Google Calendar for scheduling, event management, and calendar automation tasks.

## Features

### Available Actions

1. **list_calendars** - List all calendars
2. **get_calendar** - Get a specific calendar
3. **list_events** - List events from a calendar
4. **get_event** - Get a specific event
5. **create_event** - Create a new event
6. **update_event** - Update an existing event
7. **delete_event** - Delete an event
8. **get_free_busy** - Get free/busy information for calendars
9. **get_calendar_list** - Get the list of calendars
10. **create_calendar** - Create a new calendar
11. **delete_calendar** - Delete a calendar
12. **get_event_instances** - Get instances of a recurring event

### Supported Parameters

- **calendar_id** - Calendar ID (use 'primary' for primary calendar)
- **event_id** - Event ID
- **time_min** - Start time for event queries (ISO 8601 format)
- **time_max** - End time for event queries (ISO 8601 format)
- **summary** - Event summary/title
- **description** - Event description
- **location** - Event location
- **start_time** - Event start time (ISO 8601 format)
- **end_time** - Event end time (ISO 8601 format)
- **attendees** - List of attendee email addresses
- **max_results** - Maximum number of results to return (default: 10)
- **single_events** - Whether to expand recurring events (default: True)
- **order_by** - Order of events (startTime, updated) (default: startTime)

## Usage Examples

### 1. List All Calendars

```python
# List all calendars
result = await calendar.execute({
    "action": "list_calendars"
})
```

### 2. Get a Specific Calendar

```python
# Get primary calendar
result = await calendar.execute({
    "action": "get_calendar",
    "calendar_id": "primary"
})

# Get specific calendar
result = await calendar.execute({
    "action": "get_calendar",
    "calendar_id": "calendar_id_here"
})
```

### 3. List Events

```python
# List events from primary calendar
result = await calendar.execute({
    "action": "list_events",
    "calendar_id": "primary",
    "time_min": "2024-01-01T00:00:00Z",
    "time_max": "2024-12-31T23:59:59Z",
    "max_results": 10
})

# List events with specific parameters
result = await calendar.execute({
    "action": "list_events",
    "calendar_id": "primary",
    "max_results": 5,
    "single_events": True,
    "order_by": "startTime"
})
```

### 4. Get a Specific Event

```python
result = await calendar.execute({
    "action": "get_event",
    "calendar_id": "primary",
    "event_id": "event_id_here"
})
```

### 5. Create an Event

```python
# Create event with all details
result = await calendar.execute({
    "action": "create_event",
    "calendar_id": "primary",
    "summary": "Team Meeting",
    "description": "Weekly team sync meeting",
    "location": "Conference Room A",
    "start_time": "2024-12-25T10:00:00Z",
    "end_time": "2024-12-25T11:00:00Z",
    "attendees": ["team@example.com", "manager@example.com"]
})

# Create event with minimal parameters
result = await calendar.execute({
    "action": "create_event",
    "summary": "Quick Call",
    "start_time": "2024-12-26T14:00:00Z",
    "end_time": "2024-12-26T14:30:00Z"
})
```

### 6. Update an Event

```python
result = await calendar.execute({
    "action": "update_event",
    "calendar_id": "primary",
    "event_id": "event_id_here",
    "summary": "Updated Meeting Title",
    "description": "Updated meeting description",
    "location": "New Location"
})
```

### 7. Delete an Event

```python
result = await calendar.execute({
    "action": "delete_event",
    "calendar_id": "primary",
    "event_id": "event_id_here"
})
```

### 8. Get Free/Busy Information

```python
result = await calendar.execute({
    "action": "get_free_busy",
    "time_min": "2024-12-25T00:00:00Z",
    "time_max": "2024-12-25T23:59:59Z",
    "calendar_ids": ["primary", "work@example.com"]
})
```

### 9. Get Calendar List

```python
result = await calendar.execute({
    "action": "get_calendar_list"
})
```

### 10. Create a New Calendar

```python
result = await calendar.execute({
    "action": "create_calendar",
    "summary": "Work Calendar",
    "description": "Calendar for work-related events",
    "time_zone": "America/New_York"
})
```

### 11. Delete a Calendar

```python
result = await calendar.execute({
    "action": "delete_calendar",
    "calendar_id": "calendar_id_here"
})
```

### 12. Get Event Instances

```python
result = await calendar.execute({
    "action": "get_event_instances",
    "calendar_id": "primary",
    "event_id": "recurring_event_id_here",
    "time_min": "2024-01-01T00:00:00Z",
    "time_max": "2024-12-31T23:59:59Z"
})
```

## Response Format

### Success Response

```json
{
    "success": true,
    "action": "list_events",
    "calendar_id": "primary",
    "data": {
        "events": [...],
        "next_page_token": "token_here",
        "updated": "2024-01-15T10:30:00Z",
        "timestamp": "2024-01-15T10:30:00"
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": "Failed to list events: 401"
}
```

## Key Data Points

### Calendar Information
- **Calendar ID** - Unique identifier for the calendar
- **Summary** - Calendar name/title
- **Description** - Calendar description
- **Time Zone** - Calendar timezone
- **Access Role** - User's access role to the calendar
- **Primary** - Whether this is the primary calendar
- **Selected** - Whether the calendar is selected

### Event Information
- **Event ID** - Unique identifier for the event
- **Summary** - Event title
- **Description** - Event description
- **Location** - Event location
- **Start Time** - Event start date and time
- **End Time** - Event end date and time
- **Attendees** - List of event attendees
- **Organizer** - Event organizer information
- **Status** - Event status (confirmed, tentative, cancelled)
- **Recurrence** - Recurrence rules for recurring events
- **Reminders** - Event reminders
- **Conference Data** - Video conference information

### Free/Busy Information
- **Calendar ID** - Calendar identifier
- **Busy Periods** - List of busy time periods
- **Free Periods** - Available time slots
- **Time Range** - Query time range

## Integration

### Environment Variables

Set the following environment variables to enable Google Calendar API access:

```bash
export GOOGLE_CALENDAR_ACCESS_TOKEN="your_google_calendar_access_token_here"
export GOOGLE_CALENDAR_API_KEY="your_google_calendar_api_key_here"  # Optional
```

### API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials
5. Set up OAuth consent screen
6. Generate access tokens for your application
7. Set the access token as an environment variable

### OAuth 2.0 Scopes

The Google Calendar API requires the following scopes:
- `https://www.googleapis.com/auth/calendar.readonly` - Read-only access
- `https://www.googleapis.com/auth/calendar.events` - Read and write access to events
- `https://www.googleapis.com/auth/calendar` - Full access to calendars
- `https://www.googleapis.com/auth/calendar.settings.readonly` - Read-only access to settings

### Rate Limits

The Google Calendar API has the following quotas:
- **Queries per day**: 1,000,000,000
- **Queries per 100 seconds per user**: 500
- **Queries per 100 seconds**: 10,000

## Testing

### Individual Tool Testing

Run the dedicated test script:

```bash
python scripts/test_google_calendar_tool.py
```

### Comprehensive Testing

Include GoogleCalendarTool in the comprehensive test suite:

```bash
python scripts/test_all_tools.py
```

### Test Coverage

The test suite covers:
- ✅ All 12 available actions
- ✅ Parameter validation
- ✅ Error handling
- ✅ Event management operations
- ✅ Calendar operations
- ✅ Session management

## Error Handling

The tool handles various error scenarios:

1. **Missing Access Token** - Returns error when GOOGLE_CALENDAR_ACCESS_TOKEN is not set
2. **Invalid Parameters** - Validates required parameters and returns descriptive errors
3. **API Errors** - Handles HTTP status codes and API-specific errors
4. **Network Issues** - Gracefully handles connection timeouts and network failures
5. **Authentication Errors** - Handles OAuth token expiration and invalid tokens

## Date and Time Formats

The tool uses ISO 8601 format for all date and time parameters:

### Examples
- `2024-12-25T10:00:00Z` - December 25, 2024 at 10:00 AM UTC
- `2024-12-25T10:00:00-05:00` - December 25, 2024 at 10:00 AM EST
- `2024-12-25` - December 25, 2024 (all day event)

## Use Cases

### Event Management
- Create and manage calendar events
- Schedule meetings and appointments
- Set up recurring events
- Update event details and attendees
- Cancel or reschedule events

### Calendar Operations
- List and manage multiple calendars
- Create new calendars for different purposes
- Delete unused calendars
- Get calendar information and settings

### Scheduling
- Check availability across multiple calendars
- Find free time slots for meetings
- Coordinate schedules with attendees
- Set up meeting reminders

### Calendar Analytics
- Analyze calendar usage patterns
- Track meeting frequency and duration
- Generate calendar reports
- Monitor calendar activity

### Automation
- Auto-schedule recurring meetings
- Create events from external data
- Sync calendars across platforms
- Generate calendar summaries

## Advanced Features

### Recurring Events
- Create events that repeat daily, weekly, monthly, or yearly
- Get instances of recurring events
- Update recurring event patterns
- Handle exceptions to recurring events

### Attendee Management
- Add and remove attendees from events
- Send calendar invitations
- Track attendee responses
- Manage attendee permissions

### Conference Integration
- Add video conference links to events
- Integrate with Google Meet, Zoom, or other platforms
- Generate conference URLs automatically
- Manage conference settings

### Reminders and Notifications
- Set up event reminders
- Configure notification preferences
- Send reminder emails
- Manage notification timing

## Notes

- **Access Token Required**: The tool requires a valid Google Calendar API access token
- **Real Data**: Uses actual Google Calendar API data when available
- **OAuth 2.0**: Requires proper OAuth 2.0 setup and token management
- **Rate Limiting**: Respects Google Calendar API quotas and rate limits
- **Error Handling**: Returns descriptive error messages for troubleshooting
- **Session Management**: Efficiently manages HTTP sessions for API calls
- **Time Zones**: Handles timezone conversions automatically
- **Recurring Events**: Supports complex recurring event patterns
- **Security**: Handles sensitive calendar data securely
- **Multi-Calendar**: Supports operations across multiple calendars
