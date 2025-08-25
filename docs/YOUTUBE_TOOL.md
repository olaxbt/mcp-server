# YouTube Tool Documentation

## Overview

The `YouTubeTool` provides comprehensive access to YouTube data through the YouTube Data API v3, including video search, channel analytics, trending videos, comments analysis, and video statistics. This tool enables AI assistants to gather real-time YouTube data for content analysis, trend monitoring, and social media insights.

## Features

### Available Actions

1. **search_videos** - Search for YouTube videos with various filters
2. **get_video_details** - Get detailed information about a specific video
3. **get_channel_info** - Get information about a YouTube channel
4. **get_trending_videos** - Get trending videos for a specific region
5. **get_video_comments** - Get comments for a specific video
6. **get_video_statistics** - Get detailed statistics for a specific video
7. **get_playlist_videos** - Get videos from a specific playlist
8. **get_channel_videos** - Get videos uploaded by a specific channel
9. **get_video_categories** - Get video categories for a specific region
10. **search_channels** - Search for YouTube channels

### Supported Parameters

- **query** - Search query for videos or channels
- **video_id** - YouTube video ID (e.g., "dQw4w9WgXcQ")
- **channel_id** - YouTube channel ID (e.g., "UC-lHJZR3Gqxm24_Vd_AJ5Yw")
- **playlist_id** - YouTube playlist ID
- **region_code** - Country code for region-specific results (default: "US")
- **max_results** - Maximum number of results to return (default: 10)
- **order** - Order of results (relevance, date, rating, viewCount, title)
- **video_category_id** - Video category ID for filtering
- **published_after** - Filter videos published after this date (ISO 8601 format)
- **published_before** - Filter videos published before this date (ISO 8601 format)
- **video_duration** - Video duration filter (short, medium, long)
- **video_definition** - Video definition filter (high, standard)
- **video_embeddable** - Filter for embeddable videos
- **video_license** - Video license filter (youtube, creativeCommon)
- **video_syndicated** - Filter for syndicated videos
- **video_type** - Video type filter (any, episode, movie)

## Usage Examples

### 1. Search for Videos

```python
# Basic video search
result = await youtube.execute({
    "action": "search_videos",
    "query": "cryptocurrency",
    "max_results": 10,
    "region_code": "US"
})

# Advanced search with filters
result = await youtube.execute({
    "action": "search_videos",
    "query": "bitcoin",
    "max_results": 5,
    "order": "viewCount",
    "video_duration": "medium",
    "video_definition": "high",
    "published_after": "2024-01-01T00:00:00Z"
})
```

### 2. Get Video Details

```python
result = await youtube.execute({
    "action": "get_video_details",
    "video_id": "dQw4w9WgXcQ"
})
```

### 3. Get Channel Information

```python
result = await youtube.execute({
    "action": "get_channel_info",
    "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw"
})
```

### 4. Get Trending Videos

```python
result = await youtube.execute({
    "action": "get_trending_videos",
    "region_code": "US",
    "max_results": 10
})
```

### 5. Get Video Comments

```python
result = await youtube.execute({
    "action": "get_video_comments",
    "video_id": "dQw4w9WgXcQ",
    "max_results": 20,
    "order": "relevance"
})
```

### 6. Get Video Statistics

```python
result = await youtube.execute({
    "action": "get_video_statistics",
    "video_id": "dQw4w9WgXcQ"
})
```

### 7. Get Playlist Videos

```python
result = await youtube.execute({
    "action": "get_playlist_videos",
    "playlist_id": "PLrAXtmRdnEQy6nuLMHjMZOz59Oq8WGfwR",
    "max_results": 10
})
```

### 8. Get Channel Videos

```python
result = await youtube.execute({
    "action": "get_channel_videos",
    "channel_id": "UC-lHJZR3Gqxm24_Vd_AJ5Yw",
    "max_results": 10,
    "order": "date"
})
```

### 9. Get Video Categories

```python
result = await youtube.execute({
    "action": "get_video_categories",
    "region_code": "US"
})
```

### 10. Search for Channels

```python
result = await youtube.execute({
    "action": "search_channels",
    "query": "cryptocurrency",
    "max_results": 10,
    "order": "relevance"
})
```

## Response Format

### Success Response

```json
{
    "success": true,
    "action": "search_videos",
    "query": "cryptocurrency",
    "region_code": "US",
    "data": {
        "videos": [...],
        "total_results": 1000000,
        "results_per_page": 10,
        "next_page_token": "CAUQAA",
        "timestamp": "2024-01-15T10:30:00"
    }
}
```

### Error Response

```json
{
    "success": false,
    "error": "Failed to search videos: 403"
}
```

## Key Data Points

### Video Information
- **Video ID** - Unique identifier for the video
- **Title** - Video title
- **Description** - Video description
- **Thumbnail URLs** - Various thumbnail sizes
- **Channel Information** - Channel ID, title, and details
- **Published Date** - When the video was published
- **Duration** - Video length
- **View Count** - Number of views
- **Like/Dislike Count** - Engagement metrics
- **Comment Count** - Number of comments
- **Tags** - Video tags
- **Category** - Video category

### Channel Information
- **Channel ID** - Unique identifier for the channel
- **Channel Title** - Channel name
- **Description** - Channel description
- **Subscriber Count** - Number of subscribers
- **Video Count** - Number of videos uploaded
- **View Count** - Total channel views
- **Custom URL** - Channel's custom URL
- **Thumbnail** - Channel thumbnail
- **Country** - Channel's country
- **Created Date** - When the channel was created

### Comment Information
- **Comment ID** - Unique identifier for the comment
- **Author** - Comment author information
- **Text** - Comment text content
- **Published Date** - When the comment was published
- **Like Count** - Number of likes on the comment
- **Reply Count** - Number of replies
- **Parent ID** - Parent comment ID (for replies)

## Integration

### Environment Variables

Set the following environment variable to enable YouTube API access:

```bash
export YOUTUBE_API_KEY="your_youtube_api_key_here"
```

### API Key Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API Key)
5. Set the API key as an environment variable

### Rate Limits

The YouTube Data API v3 has the following quotas:
- **Queries per day**: 10,000 units
- **Queries per 100 seconds per user**: 3,000 units
- **Queries per 100 seconds**: 50,000 units

Different API calls consume different amounts of quota:
- Search: 100 units
- Videos: 1 unit
- Channels: 1 unit
- CommentThreads: 1 unit
- PlaylistItems: 1 unit
- VideoCategories: 1 unit

## Testing

### Individual Tool Testing

Run the dedicated test script:

```bash
python scripts/test_youtube_tool.py
```

### Comprehensive Testing

Include YouTubeTool in the comprehensive test suite:

```bash
python scripts/test_all_tools.py
```

### Test Coverage

The test suite covers:
- ✅ All 10 available actions
- ✅ Parameter validation
- ✅ Error handling
- ✅ Different regions and filters
- ✅ API response parsing
- ✅ Session management

## Error Handling

The tool handles various error scenarios:

1. **Missing API Key** - Returns error when YOUTUBE_API_KEY is not set
2. **Invalid Parameters** - Validates required parameters and returns descriptive errors
3. **API Errors** - Handles HTTP status codes and API-specific errors
4. **Network Issues** - Gracefully handles connection timeouts and network failures
5. **Rate Limiting** - Respects YouTube API rate limits

## Use Cases

### Content Analysis
- Analyze trending videos in specific categories
- Monitor video performance metrics
- Track channel growth and engagement

### Social Media Monitoring
- Monitor comments and sentiment
- Track viral content
- Analyze content trends

### Market Research
- Research competitor channels
- Analyze content strategies
- Monitor industry trends

### Content Creation
- Research popular topics
- Analyze successful content
- Identify content gaps

## Notes

- **API Key Required**: The tool requires a valid YouTube Data API v3 key
- **Real Data**: Uses actual YouTube API data when available
- **Rate Limiting**: Respects YouTube API quotas and rate limits
- **Error Handling**: Returns descriptive error messages for troubleshooting
- **Session Management**: Efficiently manages HTTP sessions for API calls
- **Comprehensive Coverage**: Supports all major YouTube Data API v3 endpoints
