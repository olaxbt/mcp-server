# Reddit Tool Documentation

## Overview

The `RedditTool` is a comprehensive MCP tool for interacting with Reddit's API to fetch posts, comments, subreddit data, and user information. It provides access to Reddit's OAuth API endpoints for searching content, retrieving user data, analyzing community engagement, and monitoring trending topics.

## Features

### Core Functionality
- **Post Search**: Search for posts across Reddit using keywords and filters
- **Subreddit Data**: Get posts, comments, and information from specific subreddits
- **User Analytics**: Retrieve user posts, comments, and profile information
- **Trending Content**: Access hot, new, top, and rising posts
- **Community Insights**: Get subreddit information and trending communities
- **Comment Analysis**: Fetch comments for specific posts

### Available Actions

1. **`search_posts`** - Search for posts across Reddit
2. **`get_subreddit_posts`** - Get posts from a specific subreddit
3. **`get_post_comments`** - Get comments for a specific post
4. **`get_user_posts`** - Get posts submitted by a user
5. **`get_user_comments`** - Get comments made by a user
6. **`get_subreddit_info`** - Get information about a subreddit
7. **`get_user_info`** - Get information about a user
8. **`get_trending_subreddits`** - Get popular/trending subreddits
9. **`get_hot_posts`** - Get hot posts from front page
10. **`get_new_posts`** - Get new posts from front page
11. **`get_top_posts`** - Get top posts from front page
12. **`get_rising_posts`** - Get rising posts from front page

## Usage Examples

### Search Posts
```python
# Search for cryptocurrency-related posts
result = await reddit_tool.execute({
    "action": "search_posts",
    "query": "cryptocurrency",
    "limit": 10,
    "time_filter": "day"
})
```

### Get Subreddit Posts
```python
# Get hot posts from r/cryptocurrency
result = await reddit_tool.execute({
    "action": "get_subreddit_posts",
    "subreddit": "cryptocurrency",
    "sort": "hot",
    "limit": 20,
    "time_filter": "week"
})
```

### Get Post Comments
```python
# Get comments for a specific post
result = await reddit_tool.execute({
    "action": "get_post_comments",
    "post_id": "abc123",
    "limit": 50
})
```

### Get User Posts
```python
# Get posts by a specific user
result = await reddit_tool.execute({
    "action": "get_user_posts",
    "username": "username",
    "limit": 15,
    "time_filter": "month"
})
```

### Get Subreddit Information
```python
# Get information about a subreddit
result = await reddit_tool.execute({
    "action": "get_subreddit_info",
    "subreddit": "cryptocurrency"
})
```

### Get Trending Subreddits
```python
# Get popular subreddits
result = await reddit_tool.execute({
    "action": "get_trending_subreddits",
    "limit": 25
})
```

### Get Front Page Posts
```python
# Get hot posts from front page
result = await reddit_tool.execute({
    "action": "get_hot_posts",
    "limit": 10
})

# Get top posts from front page
result = await reddit_tool.execute({
    "action": "get_top_posts",
    "limit": 10,
    "time_filter": "week"
})
```

## Response Format

### Success Response
```json
[
    {
        "success": true,
        "data": {
            "data": {
                "children": [
                    {
                        "data": {
                            "id": "abc123",
                            "title": "Post Title",
                            "selftext": "Post content",
                            "author": "username",
                            "subreddit": "cryptocurrency",
                            "score": 100,
                            "upvote_ratio": 0.95,
                            "num_comments": 50,
                            "created_utc": 1640995200,
                            "url": "https://reddit.com/r/cryptocurrency/comments/abc123",
                            "permalink": "/r/cryptocurrency/comments/abc123/post_title/"
                        }
                    }
                ],
                "after": "t3_abc123",
                "before": null
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
        "error": "Failed to authenticate with Reddit API"
    }
]
```

## Key Data Points

### Post Data
- **Post ID**: Unique identifier for the post
- **Title**: Post title
- **Content**: Post text content (selftext)
- **Author**: Username of the post author
- **Subreddit**: Subreddit where the post was made
- **Score**: Upvotes minus downvotes
- **Upvote Ratio**: Percentage of upvotes
- **Comment Count**: Number of comments
- **Created Time**: Unix timestamp of creation
- **URL**: Direct link to the post
- **Permalink**: Reddit permalink

### Comment Data
- **Comment ID**: Unique identifier for the comment
- **Body**: Comment text content
- **Author**: Username of the comment author
- **Score**: Upvotes minus downvotes
- **Created Time**: Unix timestamp of creation
- **Parent ID**: ID of parent comment/post
- **Depth**: Nesting level of the comment

### User Data
- **Username**: Reddit username
- **Created Time**: Account creation date
- **Link Karma**: Karma from link posts
- **Comment Karma**: Karma from comments
- **Is Gold**: Gold member status
- **Is Mod**: Moderator status
- **Verified Email**: Email verification status

### Subreddit Data
- **Name**: Subreddit name
- **Display Name**: Display name
- **Description**: Subreddit description
- **Subscribers**: Number of subscribers
- **Active Users**: Currently active users
- **Created Time**: Subreddit creation date
- **Is NSFW**: Adult content flag
- **Is Private**: Private subreddit flag

## Integration

### Environment Variables
```bash
# Required for API access
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=MCP-Reddit-Tool/1.0
```

### API Setup
1. **Create Reddit App**:
   - Visit [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Click "Create App" or "Create Another App"
   - Select "script" as the app type
   - Fill in the required information

2. **Get Credentials**:
   - Note the Client ID (under the app name)
   - Note the Client Secret (labeled "secret")
   - Set a User Agent string

3. **API Permissions**:
   - The script app type provides read-only access
   - No additional OAuth scopes required for basic functionality

### OAuth 2.0 Flow
- **Client Credentials Flow**: Used for script applications
- **Read-Only Access**: No user authentication required
- **Rate Limiting**: 60 requests per minute for script apps

### Rate Limits
- **Script Apps**: 60 requests per minute
- **Web Apps**: 60 requests per minute
- **Installed Apps**: 60 requests per minute
- **User-Agent**: Must be unique and descriptive

## Testing

### Individual Tool Testing
```bash
python scripts/test_reddit_tool.py
```

### Comprehensive Testing
```bash
python scripts/test_all_tools.py
```

### Test Coverage
- ✅ Tool instantiation
- ✅ All 12 actions tested
- ✅ Parameter validation
- ✅ Error handling
- ✅ API response parsing
- ✅ Authentication handling

## Error Handling

### Common Error Codes
- **401 Unauthorized**: Invalid or missing credentials
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Reddit API error

### Error Response Format
```json
[
    {
        "success": false,
        "error": "Failed to [action]: [status_code]"
    }
]
```

### Parameter Validation
- **Required Parameters**: Validates presence of required fields
- **Parameter Types**: Ensures correct data types
- **Value Ranges**: Validates numeric ranges (e.g., limit: 1-100)
- **Enum Values**: Validates enum parameters (e.g., time_filter, sort)

## Reddit Search Syntax

### Basic Search
- **Keywords**: `cryptocurrency`, `bitcoin`
- **Exact Phrase**: `"artificial intelligence"`
- **Subreddit**: `subreddit:cryptocurrency`
- **Author**: `author:username`
- **Title Only**: `title:cryptocurrency`

### Advanced Filters
- **Time Range**: `timestamp:1640995200..1641081600`
- **Score**: `score:>100`
- **Comments**: `num_comments:>50`
- **Domain**: `domain:youtube.com`
- **URL**: `url:reddit.com`

### Boolean Operators
- **AND**: `cryptocurrency AND bitcoin`
- **OR**: `cryptocurrency OR bitcoin`
- **NOT**: `cryptocurrency -bitcoin`

## Use Cases

### Content Discovery
- Find trending posts in specific communities
- Discover popular content across subreddits
- Monitor new posts in target subreddits
- Track rising content before it goes viral

### Community Analysis
- Analyze subreddit activity and engagement
- Monitor user participation and contributions
- Track community growth and trends
- Identify influential users and content

### Market Research
- Monitor discussions about products/services
- Track sentiment in relevant communities
- Identify emerging trends and topics
- Analyze competitor mentions and discussions

### Social Media Monitoring
- Track brand mentions and discussions
- Monitor customer feedback and complaints
- Analyze public sentiment and opinions
- Identify potential PR issues or opportunities

### Content Strategy
- Research trending topics and hashtags
- Analyze successful content patterns
- Monitor audience engagement metrics
- Track content performance over time

## Advanced Features

### Pagination
- Use `after` parameter for paginated results
- Implement cursor-based navigation
- Handle rate limiting gracefully
- Cache frequently requested data

### Real-time Monitoring
- Set up polling for new posts
- Monitor specific subreddits for activity
- Track trending topics in real-time
- Implement webhook-like functionality

### Data Analytics
- Aggregate engagement metrics
- Calculate sentiment scores
- Generate trend reports
- Create user influence scores

## Best Practices

### Rate Limiting
- Implement exponential backoff
- Cache frequently requested data
- Use bulk endpoints when possible
- Monitor rate limit headers

### Error Handling
- Implement retry logic for transient errors
- Log errors for debugging
- Provide meaningful error messages
- Handle network timeouts

### Data Management
- Store historical data locally
- Implement data validation
- Use appropriate data structures
- Optimize for query performance

### Security
- Secure API credentials storage
- Implement credential rotation
- Monitor API usage
- Follow OAuth 2.0 best practices

## Troubleshooting

### Common Issues
1. **401 Unauthorized**: Check Client ID and Secret validity
2. **403 Forbidden**: Verify app permissions and User-Agent
3. **429 Rate Limited**: Implement backoff strategy
4. **Network Errors**: Check connectivity and timeouts

### Debug Tips
- Enable detailed logging
- Test with minimal parameters
- Verify API endpoint URLs
- Check response headers

### Support Resources
- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [Reddit API Status](https://www.redditstatus.com/)
- [Reddit Developer Community](https://www.reddit.com/r/redditdev/)
- [Rate Limiting Guide](https://github.com/reddit-archive/reddit/wiki/API)

## Examples

### Complete Workflow Example
```python
# Initialize Reddit tool
reddit_tool = RedditTool()

# Search for cryptocurrency posts
search_result = await reddit_tool.execute({
    "action": "search_posts",
    "query": "bitcoin price",
    "limit": 10,
    "time_filter": "day"
})

# Get subreddit information
subreddit_info = await reddit_tool.execute({
    "action": "get_subreddit_info",
    "subreddit": "cryptocurrency"
})

# Get trending posts
trending_posts = await reddit_tool.execute({
    "action": "get_hot_posts",
    "limit": 5
})

# Process results
if search_result[0]["success"]:
    posts = search_result[0]["data"]["data"]["children"]
    for post in posts:
        print(f"Title: {post['data']['title']}")
        print(f"Score: {post['data']['score']}")
        print(f"Comments: {post['data']['num_comments']}")
        print("---")
```

### Error Handling Example
```python
try:
    result = await reddit_tool.execute({
        "action": "search_posts",
        "query": "cryptocurrency"
    })
    
    if result[0]["success"]:
        # Process successful result
        data = result[0]["data"]
        # ... process data
    else:
        # Handle error
        error = result[0]["error"]
        print(f"Reddit API error: {error}")
        
except Exception as e:
    print(f"Tool execution error: {str(e)}")
```
