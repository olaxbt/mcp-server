# Twitter Tool Documentation

## Overview

The `TwitterTool` is a comprehensive MCP tool for interacting with Twitter/X API to fetch tweets, user data, and social metrics. It provides access to Twitter's v2 API endpoints for searching tweets, retrieving user profiles, analyzing engagement metrics, and monitoring trending topics.

## Features

### Core Functionality
- **Tweet Search**: Search for tweets using keywords, hashtags, and advanced filters
- **User Profiles**: Get detailed user information including followers, following, and profile data
- **Tweet Analytics**: Retrieve engagement metrics (likes, retweets, replies)
- **Trending Topics**: Monitor trending topics by location
- **User Timeline**: Access user tweets and mentions
- **Hashtag Analysis**: Search tweets by specific hashtags

### Available Actions

1. **`search_tweets`** - Search for tweets with query filters
2. **`get_user_tweets`** - Get tweets from a specific user
3. **`get_user_profile`** - Retrieve user profile information
4. **`get_tweet_details`** - Get detailed information about a specific tweet
5. **`get_trending_topics`** - Get trending topics by location
6. **`get_user_followers`** - Get user's followers list
7. **`get_user_following`** - Get users that a specific user is following
8. **`get_tweet_likes`** - Get users who liked a specific tweet
9. **`get_tweet_retweets`** - Get users who retweeted a specific tweet
10. **`get_user_mentions`** - Get tweets that mention a specific user
11. **`get_hashtag_tweets`** - Get tweets with a specific hashtag
12. **`get_user_timeline`** - Get user's home timeline

## Usage Examples

### Search Tweets
```python
# Search for cryptocurrency-related tweets
result = await twitter_tool.execute({
    "action": "search_tweets",
    "query": "cryptocurrency",
    "max_results": 10,
    "start_time": "2024-01-01T00:00:00Z"
})
```

### Get User Profile
```python
# Get user profile by username
result = await twitter_tool.execute({
    "action": "get_user_profile",
    "username": "elonmusk"
})

# Get user profile by user ID
result = await twitter_tool.execute({
    "action": "get_user_profile",
    "user_id": "44196397"
})
```

### Get User Tweets
```python
# Get recent tweets from a user
result = await twitter_tool.execute({
    "action": "get_user_tweets",
    "username": "elonmusk",
    "max_results": 20
})
```

### Get Trending Topics
```python
# Get worldwide trending topics
result = await twitter_tool.execute({
    "action": "get_trending_topics",
    "woeid": 1  # Worldwide
})
```

### Get Tweet Details
```python
# Get detailed information about a specific tweet
result = await twitter_tool.execute({
    "action": "get_tweet_details",
    "tweet_id": "1234567890123456789"
})
```

### Get Hashtag Tweets
```python
# Search tweets with a specific hashtag
result = await twitter_tool.execute({
    "action": "get_hashtag_tweets",
    "hashtag": "cryptocurrency",
    "max_results": 15
})
```

## Response Format

### Success Response
```json
[
    {
        "success": true,
        "data": {
            "data": [
                {
                    "id": "1234567890123456789",
                    "text": "Tweet content here",
                    "created_at": "2024-01-01T12:00:00.000Z",
                    "author_id": "44196397",
                    "public_metrics": {
                        "retweet_count": 100,
                        "reply_count": 50,
                        "like_count": 1000,
                        "quote_count": 25
                    }
                }
            ],
            "meta": {
                "result_count": 1,
                "newest_id": "1234567890123456789",
                "oldest_id": "1234567890123456789",
                "next_token": "next_token_here"
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
        "error": "Failed to search tweets: 401"
    }
]
```

## Key Data Points

### Tweet Data
- **Tweet ID**: Unique identifier for the tweet
- **Text**: Tweet content
- **Created At**: Timestamp of tweet creation
- **Author ID**: User ID of the tweet author
- **Public Metrics**: Engagement statistics (likes, retweets, replies, quotes)
- **Entities**: URLs, mentions, hashtags, and media
- **Context Annotations**: Topic classifications
- **Language**: Tweet language code

### User Data
- **User ID**: Unique identifier for the user
- **Username**: Twitter handle
- **Name**: Display name
- **Description**: User bio
- **Location**: User location
- **Profile Image URL**: Avatar image
- **Verified**: Account verification status
- **Public Metrics**: Follower/following counts
- **Created At**: Account creation date
- **Protected**: Account privacy status

### Engagement Metrics
- **Like Count**: Number of likes
- **Retweet Count**: Number of retweets
- **Reply Count**: Number of replies
- **Quote Count**: Number of quote tweets
- **Follower Count**: Number of followers
- **Following Count**: Number of accounts followed

## Integration

### Environment Variables
```bash
# Required for API access
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

### API Setup
1. **Create Twitter Developer Account**:
   - Visit [Twitter Developer Portal](https://developer.twitter.com/)
   - Apply for a developer account
   - Create a new app/project

2. **Generate Bearer Token**:
   - Navigate to your app's "Keys and Tokens" section
   - Generate a Bearer Token
   - Copy the token to your environment variables

3. **API Permissions**:
   - Ensure your app has read permissions
   - For user timeline access, additional OAuth 2.0 setup may be required

### OAuth 2.0 Scopes
- **Tweet Read**: Access to read tweets and user data
- **Users Read**: Access to user profile information
- **Offline Access**: For background data collection

### Rate Limits
- **Standard API**: 300 requests per 15-minute window
- **Academic Research**: 500,000 requests per 15-minute window
- **Enterprise API**: Custom limits based on plan

## Testing

### Individual Tool Testing
```bash
python scripts/test_twitter_tool.py
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
- **401 Unauthorized**: Invalid or missing Bearer Token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource doesn't exist
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Twitter API error

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
- **Value Ranges**: Validates numeric ranges (e.g., max_results: 1-100)
- **Format Validation**: Validates date formats and IDs

## Twitter Search Syntax

### Basic Search
- **Keywords**: `cryptocurrency`, `bitcoin`
- **Exact Phrase**: `"artificial intelligence"`
- **Hashtags**: `#cryptocurrency`, `#AI`
- **Mentions**: `@elonmusk`

### Advanced Filters
- **From User**: `from:elonmusk`
- **To User**: `to:elonmusk`
- **Mentioning User**: `@elonmusk`
- **Date Range**: `since:2024-01-01 until:2024-01-31`
- **Language**: `lang:en`
- **Has Media**: `has:media`
- **Has Links**: `has:links`
- **Is Retweet**: `is:retweet`
- **Is Reply**: `is:reply`

### Boolean Operators
- **AND**: `cryptocurrency AND bitcoin`
- **OR**: `cryptocurrency OR bitcoin`
- **NOT**: `cryptocurrency -bitcoin`

## Use Cases

### Social Media Monitoring
- Track brand mentions and sentiment
- Monitor competitor activity
- Analyze trending topics
- Measure campaign performance

### Market Research
- Analyze public sentiment about products
- Track industry conversations
- Monitor influencer activity
- Identify emerging trends

### Content Strategy
- Research trending hashtags
- Analyze successful content
- Monitor audience engagement
- Track content performance

### Crisis Management
- Monitor negative mentions
- Track sentiment changes
- Identify potential issues
- Measure response effectiveness

## Advanced Features

### Pagination
- Use `next_token` for paginated results
- Implement cursor-based navigation
- Handle rate limiting gracefully

### Real-time Monitoring
- Set up webhook endpoints
- Use streaming API for real-time data
- Implement event-driven architecture

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
- Secure API token storage
- Implement token rotation
- Monitor API usage
- Follow OAuth 2.0 best practices

## Troubleshooting

### Common Issues
1. **401 Unauthorized**: Check Bearer Token validity
2. **403 Forbidden**: Verify API permissions
3. **429 Rate Limited**: Implement backoff strategy
4. **Network Errors**: Check connectivity and timeouts

### Debug Tips
- Enable detailed logging
- Test with minimal parameters
- Verify API endpoint URLs
- Check response headers

### Support Resources
- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [API Status Page](https://api.twitter.com/1.1/help/configuration.json)
- [Developer Community](https://twittercommunity.com/)
- [Rate Limiting Guide](https://developer.twitter.com/en/docs/twitter-api/rate-limits)
