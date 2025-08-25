"""
Solana Ecosystem Tools
Contains Jupiter DEX aggregator and Raydium DEX tools for Solana
"""

import asyncio
import logging
import time
import aiohttp
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class YouTubeTool(MCPTool):
    def __init__(self):
        self.session = None
        self.youtube_api_url = "https://www.googleapis.com/youtube/v3"
        self.api_key = os.getenv("YOUTUBE_API_KEY")

    @property
    def name(self) -> str:
        return "youtube"

    @property
    def description(self) -> str:
        return "Access YouTube data including video search, channel analytics, trending videos, comments analysis, and video statistics"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "search_videos",
                        "get_video_details",
                        "get_channel_info",
                        "get_trending_videos",
                        "get_video_comments",
                        "get_video_statistics",
                        "get_playlist_videos",
                        "get_channel_videos",
                        "get_video_categories",
                        "search_channels"
                    ]
                },
                "query": {
                    "type": "string",
                    "description": "Search query for videos or channels"
                },
                "video_id": {
                    "type": "string",
                    "description": "YouTube video ID"
                },
                "channel_id": {
                    "type": "string",
                    "description": "YouTube channel ID"
                },
                "playlist_id": {
                    "type": "string",
                    "description": "YouTube playlist ID"
                },
                "region_code": {
                    "type": "string",
                    "description": "Country code for region-specific results (e.g., US, GB, CA)",
                    "default": "US"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "order": {
                    "type": "string",
                    "description": "Order of results (relevance, date, rating, viewCount, title)",
                    "default": "relevance"
                },
                "video_category_id": {
                    "type": "string",
                    "description": "Video category ID for filtering"
                },
                "published_after": {
                    "type": "string",
                    "description": "Filter videos published after this date (ISO 8601 format)"
                },
                "published_before": {
                    "type": "string",
                    "description": "Filter videos published before this date (ISO 8601 format)"
                },
                "video_duration": {
                    "type": "string",
                    "description": "Video duration filter (short, medium, long)",
                    "enum": ["short", "medium", "long"]
                },
                "video_definition": {
                    "type": "string",
                    "description": "Video definition filter (high, standard)",
                    "enum": ["high", "standard"]
                },
                "video_embeddable": {
                    "type": "boolean",
                    "description": "Filter for embeddable videos"
                },
                "video_license": {
                    "type": "string",
                    "description": "Video license filter (youtube, creativeCommon)",
                    "enum": ["youtube", "creativeCommon"]
                },
                "video_syndicated": {
                    "type": "boolean",
                    "description": "Filter for syndicated videos"
                },
                "video_type": {
                    "type": "string",
                    "description": "Video type filter (any, episode, movie)",
                    "enum": ["any", "episode", "movie"]
                }
            },
            "required": ["action"]
        }

    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")

            if action == "search_videos":
                result = await self._search_videos(**arguments)
            elif action == "get_video_details":
                result = await self._get_video_details(**arguments)
            elif action == "get_channel_info":
                result = await self._get_channel_info(**arguments)
            elif action == "get_trending_videos":
                result = await self._get_trending_videos(**arguments)
            elif action == "get_video_comments":
                result = await self._get_video_comments(**arguments)
            elif action == "get_video_statistics":
                result = await self._get_video_statistics(**arguments)
            elif action == "get_playlist_videos":
                result = await self._get_playlist_videos(**arguments)
            elif action == "get_channel_videos":
                result = await self._get_channel_videos(**arguments)
            elif action == "get_video_categories":
                result = await self._get_video_categories(**arguments)
            elif action == "search_channels":
                result = await self._search_channels(**arguments)
            else:
                result = {"error": f"Unknown action: {action}"}

            return [result]
        finally:
            await self._cleanup_session()

    async def _search_videos(self, **kwargs) -> dict:
        """Search for YouTube videos."""
        try:
            query = kwargs.get("query")
            if not query:
                return {
                    "success": False,
                    "error": "query parameter is required"
                }

            max_results = kwargs.get("max_results", 10)
            order = kwargs.get("order", "relevance")
            region_code = kwargs.get("region_code", "US")
            video_category_id = kwargs.get("video_category_id")
            published_after = kwargs.get("published_after")
            published_before = kwargs.get("published_before")
            video_duration = kwargs.get("video_duration")
            video_definition = kwargs.get("video_definition")
            video_embeddable = kwargs.get("video_embeddable")
            video_license = kwargs.get("video_license")
            video_syndicated = kwargs.get("video_syndicated")
            video_type = kwargs.get("video_type")

            session = await self._get_session()

            url = f"{self.youtube_api_url}/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "video",
                "maxResults": max_results,
                "order": order,
                "regionCode": region_code
            }

            if video_category_id:
                params["videoCategoryId"] = video_category_id
            if published_after:
                params["publishedAfter"] = published_after
            if published_before:
                params["publishedBefore"] = published_before
            if video_duration:
                params["videoDuration"] = video_duration
            if video_definition:
                params["videoDefinition"] = video_definition
            if video_embeddable is not None:
                params["videoEmbeddable"] = video_embeddable
            if video_license:
                params["videoLicense"] = video_license
            if video_syndicated is not None:
                params["videoSyndicated"] = video_syndicated
            if video_type:
                params["videoType"] = video_type

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "query": query,
                        "region_code": region_code,
                        "order": order,
                        "data": {
                            "videos": data.get("items", []),
                            "total_results": data.get("pageInfo", {}).get("totalResults"),
                            "results_per_page": data.get("pageInfo", {}).get("resultsPerPage"),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to search videos: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search videos: {str(e)}"
            }

    async def _get_video_details(self, **kwargs) -> dict:
        """Get detailed information about a specific video."""
        try:
            video_id = kwargs.get("video_id")
            if not video_id:
                return {
                    "success": False,
                    "error": "video_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.youtube_api_url}/videos"
            params = {
                "part": "snippet,statistics,contentDetails,status",
                "id": video_id
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    if items:
                        video = items[0]
                        return {
                            "success": True,
                            "video_id": video_id,
                            "data": {
                                "video": video,
                                "snippet": video.get("snippet", {}),
                                "statistics": video.get("statistics", {}),
                                "content_details": video.get("contentDetails", {}),
                                "status": video.get("status", {}),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Video not found"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get video details: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get video details: {str(e)}"
            }

    async def _get_channel_info(self, **kwargs) -> dict:
        """Get information about a YouTube channel."""
        try:
            channel_id = kwargs.get("channel_id")
            if not channel_id:
                return {
                    "success": False,
                    "error": "channel_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.youtube_api_url}/channels"
            params = {
                "part": "snippet,statistics,brandingSettings,contentDetails",
                "id": channel_id
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    if items:
                        channel = items[0]
                        return {
                            "success": True,
                            "channel_id": channel_id,
                            "data": {
                                "channel": channel,
                                "snippet": channel.get("snippet", {}),
                                "content_details": channel.get("contentDetails", {}),
                                "statistics": channel.get("statistics", {}),
                                "branding_settings": channel.get("brandingSettings", {}),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Channel not found"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get channel info: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get channel info: {str(e)}"
            }

    async def _get_trending_videos(self, **kwargs) -> dict:
        """Get trending videos for a specific region."""
        try:
            region_code = kwargs.get("region_code", "US")
            max_results = kwargs.get("max_results", 10)
            video_category_id = kwargs.get("video_category_id")

            session = await self._get_session()

            url = f"{self.youtube_api_url}/videos"
            params = {
                "part": "snippet,statistics,contentDetails",
                "chart": "mostPopular",
                "regionCode": region_code,
                "maxResults": max_results
            }

            if video_category_id:
                params["videoCategoryId"] = video_category_id

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "region_code": region_code,
                        "data": {
                            "trending_videos": data.get("items", []),
                            "total_results": data.get("pageInfo", {}).get("totalResults"),
                            "results_per_page": data.get("pageInfo", {}).get("resultsPerPage"),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get trending videos: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get trending videos: {str(e)}"
            }

    async def _get_video_comments(self, **kwargs) -> dict:
        """Get comments for a specific video."""
        try:
            video_id = kwargs.get("video_id")
            if not video_id:
                return {
                    "success": False,
                    "error": "video_id parameter is required"
                }

            max_results = kwargs.get("max_results", 10)
            order = kwargs.get("order", "relevance")

            session = await self._get_session()

            url = f"{self.youtube_api_url}/commentThreads"
            params = {
                "part": "snippet,replies",
                "videoId": video_id,
                "maxResults": max_results,
                "order": order
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "video_id": video_id,
                        "order": order,
                        "data": {
                            "comments": data.get("items", []),
                            "total_results": data.get("pageInfo", {}).get("totalResults"),
                            "results_per_page": data.get("pageInfo", {}).get("resultsPerPage"),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get video comments: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get video comments: {str(e)}"
            }

    async def _get_video_statistics(self, **kwargs) -> dict:
        """Get detailed statistics for a specific video."""
        try:
            video_id = kwargs.get("video_id")
            if not video_id:
                return {
                    "success": False,
                    "error": "video_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.youtube_api_url}/videos"
            params = {
                "part": "statistics",
                "id": video_id
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    if items:
                        statistics = items[0].get("statistics", {})
                        return {
                            "success": True,
                            "video_id": video_id,
                            "data": {
                                "statistics": statistics,
                                "view_count": statistics.get("viewCount"),
                                "like_count": statistics.get("likeCount"),
                                "dislike_count": statistics.get("dislikeCount"),
                                "comment_count": statistics.get("commentCount"),
                                "favorite_count": statistics.get("favoriteCount"),
                                "timestamp": datetime.now().isoformat()
                            }
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Video not found"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get video statistics: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get video statistics: {str(e)}"
            }

    async def _get_playlist_videos(self, **kwargs) -> dict:
        """Get videos from a specific playlist."""
        try:
            playlist_id = kwargs.get("playlist_id")
            if not playlist_id:
                return {
                    "success": False,
                    "error": "playlist_id parameter is required"
                }

            max_results = kwargs.get("max_results", 10)

            session = await self._get_session()

            url = f"{self.youtube_api_url}/playlistItems"
            params = {
                "part": "snippet,contentDetails",
                "playlistId": playlist_id,
                "maxResults": max_results
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "playlist_id": playlist_id,
                        "data": {
                            "playlist_videos": data.get("items", []),
                            "total_results": data.get("pageInfo", {}).get("totalResults"),
                            "results_per_page": data.get("pageInfo", {}).get("resultsPerPage"),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get playlist videos: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get playlist videos: {str(e)}"
            }

    async def _get_channel_videos(self, **kwargs) -> dict:
        """Get videos uploaded by a specific channel."""
        try:
            channel_id = kwargs.get("channel_id")
            if not channel_id:
                return {
                    "success": False,
                    "error": "channel_id parameter is required"
                }

            max_results = kwargs.get("max_results", 10)
            order = kwargs.get("order", "date")

            session = await self._get_session()

            # First get the uploads playlist ID
            url = f"{self.youtube_api_url}/channels"
            params = {
                "part": "contentDetails",
                "id": channel_id
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    items = data.get("items", [])
                    if items:
                        uploads_playlist_id = items[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
                        
                        # Now get the videos from the uploads playlist
                        playlist_url = f"{self.youtube_api_url}/playlistItems"
                        playlist_params = {
                            "part": "snippet,contentDetails",
                            "playlistId": uploads_playlist_id,
                            "maxResults": max_results,
                            "order": order
                        }

                        if self.api_key:
                            playlist_params["key"] = self.api_key

                        async with session.get(playlist_url, params=playlist_params) as playlist_response:
                            if playlist_response.status == 200:
                                playlist_data = await playlist_response.json()
                                return {
                                    "success": True,
                                    "channel_id": channel_id,
                                    "uploads_playlist_id": uploads_playlist_id,
                                    "order": order,
                                    "data": {
                                        "channel_videos": playlist_data.get("items", []),
                                        "total_results": playlist_data.get("pageInfo", {}).get("totalResults"),
                                        "results_per_page": playlist_data.get("pageInfo", {}).get("resultsPerPage"),
                                        "next_page_token": playlist_data.get("nextPageToken"),
                                        "timestamp": datetime.now().isoformat()
                                    }
                                }
                            else:
                                return {
                                    "success": False,
                                    "error": f"Failed to get channel videos: {playlist_response.status}"
                                }
                    else:
                        return {
                            "success": False,
                            "error": "Channel not found"
                        }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get channel info: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get channel videos: {str(e)}"
            }

    async def _get_video_categories(self, **kwargs) -> dict:
        """Get video categories for a specific region."""
        try:
            region_code = kwargs.get("region_code", "US")

            session = await self._get_session()

            url = f"{self.youtube_api_url}/videoCategories"
            params = {
                "part": "snippet",
                "regionCode": region_code
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "region_code": region_code,
                        "data": {
                            "categories": data.get("items", []),
                            "total_results": data.get("pageInfo", {}).get("totalResults"),
                            "results_per_page": data.get("pageInfo", {}).get("resultsPerPage"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get video categories: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get video categories: {str(e)}"
            }

    async def _search_channels(self, **kwargs) -> dict:
        """Search for YouTube channels."""
        try:
            query = kwargs.get("query")
            if not query:
                return {
                    "success": False,
                    "error": "query parameter is required"
                }

            max_results = kwargs.get("max_results", 10)
            order = kwargs.get("order", "relevance")
            region_code = kwargs.get("region_code", "US")

            session = await self._get_session()

            url = f"{self.youtube_api_url}/search"
            params = {
                "part": "snippet",
                "q": query,
                "type": "channel",
                "maxResults": max_results,
                "order": order,
                "regionCode": region_code
            }

            if self.api_key:
                params["key"] = self.api_key

            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "query": query,
                        "region_code": region_code,
                        "order": order,
                        "data": {
                            "channels": data.get("items", []),
                            "total_results": data.get("pageInfo", {}).get("totalResults"),
                            "results_per_page": data.get("pageInfo", {}).get("resultsPerPage"),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to search channels: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search channels: {str(e)}"
            }

class TwitterTool(MCPTool):
    """Tool for interacting with Twitter/X API to fetch tweets, user data, and social metrics."""
    
    def __init__(self):
        self.session = None
        self.twitter_api_url = "https://api.twitter.com/2"
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    
    @property
    def name(self) -> str:
        return "twitter"
    
    @property
    def description(self) -> str:
        return "Tool for fetching Twitter/X data including tweets, user profiles, trends, and social metrics"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "search_tweets",
                        "get_user_tweets",
                        "get_user_profile",
                        "get_tweet_details",
                        "get_trending_topics",
                        "get_user_followers",
                        "get_user_following",
                        "get_tweet_likes",
                        "get_tweet_retweets",
                        "get_user_mentions",
                        "get_hashtag_tweets",
                        "get_user_timeline"
                    ],
                    "description": "The action to perform"
                },
                "query": {
                    "type": "string",
                    "description": "Search query for tweets"
                },
                "username": {
                    "type": "string",
                    "description": "Twitter username (without @)"
                },
                "user_id": {
                    "type": "string",
                    "description": "Twitter user ID"
                },
                "tweet_id": {
                    "type": "string",
                    "description": "Tweet ID"
                },
                "hashtag": {
                    "type": "string",
                    "description": "Hashtag to search (without #)"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 10, max: 100)"
                },
                "since_id": {
                    "type": "string",
                    "description": "Return results with an ID greater than this value"
                },
                "until_id": {
                    "type": "string",
                    "description": "Return results with an ID less than this value"
                },
                "start_time": {
                    "type": "string",
                    "description": "Start time for search (ISO 8601 format)"
                },
                "end_time": {
                    "type": "string",
                    "description": "End time for search (ISO 8601 format)"
                },
                "woeid": {
                    "type": "integer",
                    "description": "Where On Earth ID for trending topics"
                }
            },
            "required": ["action"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Twitter tool action."""
        action = arguments.get("action")
        
        try:
            session = await self._get_session()
            
            if action == "search_tweets":
                return await self._search_tweets(session, **arguments)
            elif action == "get_user_tweets":
                return await self._get_user_tweets(session, **arguments)
            elif action == "get_user_profile":
                return await self._get_user_profile(session, **arguments)
            elif action == "get_tweet_details":
                return await self._get_tweet_details(session, **arguments)
            elif action == "get_trending_topics":
                return await self._get_trending_topics(session, **arguments)
            elif action == "get_user_followers":
                return await self._get_user_followers(session, **arguments)
            elif action == "get_user_following":
                return await self._get_user_following(session, **arguments)
            elif action == "get_tweet_likes":
                return await self._get_tweet_likes(session, **arguments)
            elif action == "get_tweet_retweets":
                return await self._get_tweet_retweets(session, **arguments)
            elif action == "get_user_mentions":
                return await self._get_user_mentions(session, **arguments)
            elif action == "get_hashtag_tweets":
                return await self._get_hashtag_tweets(session, **arguments)
            elif action == "get_user_timeline":
                return await self._get_user_timeline(session, **arguments)
            else:
                return [{"error": f"Unknown action: {action}"}]
        finally:
            await self._cleanup_session()
    
    async def _search_tweets(self, session, **kwargs):
        """Search for tweets."""
        query = kwargs.get("query")
        if not query:
            return [{"success": False, "error": "query parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        since_id = kwargs.get("since_id")
        until_id = kwargs.get("until_id")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        
        params = {
            "query": query,
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,author_id,public_metrics,entities,context_annotations,lang"
        }
        
        if since_id:
            params["since_id"] = since_id
        if until_id:
            params["until_id"] = until_id
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/tweets/search/recent", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to search tweets: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to search tweets: {str(e)}"}]
    
    async def _get_user_tweets(self, session, **kwargs):
        """Get tweets from a specific user."""
        user_id = kwargs.get("user_id")
        username = kwargs.get("username")
        
        if not user_id and not username:
            return [{"success": False, "error": "user_id or username parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        since_id = kwargs.get("since_id")
        until_id = kwargs.get("until_id")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        
        # First get user ID if username provided
        if username and not user_id:
            user_response = await self._get_user_profile(session, username=username)
            if not user_response or len(user_response) == 0 or not user_response[0].get("success"):
                return user_response
            user_id = user_response[0]["data"]["data"]["id"]
        
        params = {
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,public_metrics,entities,context_annotations,lang"
        }
        
        if since_id:
            params["since_id"] = since_id
        if until_id:
            params["until_id"] = until_id
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/users/{user_id}/tweets", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get user tweets: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get user tweets: {str(e)}"}]
    
    async def _get_user_profile(self, session, **kwargs):
        """Get user profile information."""
        user_id = kwargs.get("user_id")
        username = kwargs.get("username")
        
        if not user_id and not username:
            return [{"success": False, "error": "user_id or username parameter is required"}]
        
        params = {
            "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        }
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            if username:
                url = f"{self.twitter_api_url}/users/by/username/{username}"
            else:
                url = f"{self.twitter_api_url}/users/{user_id}"
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get user profile: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get user profile: {str(e)}"}]
    
    async def _get_tweet_details(self, session, **kwargs):
        """Get detailed information about a specific tweet."""
        tweet_id = kwargs.get("tweet_id")
        if not tweet_id:
            return [{"success": False, "error": "tweet_id parameter is required"}]
        
        params = {
            "tweet.fields": "created_at,author_id,public_metrics,entities,context_annotations,lang,referenced_tweets",
            "expansions": "author_id,referenced_tweets.id",
            "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        }
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/tweets/{tweet_id}", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get tweet details: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get tweet details: {str(e)}"}]
    
    async def _get_trending_topics(self, session, **kwargs):
        """Get trending topics."""
        woeid = kwargs.get("woeid", 1)  # Default to worldwide
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/trends/place/{woeid}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get trending topics: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get trending topics: {str(e)}"}]
    
    async def _get_user_followers(self, session, **kwargs):
        """Get user's followers."""
        user_id = kwargs.get("user_id")
        username = kwargs.get("username")
        
        if not user_id and not username:
            return [{"success": False, "error": "user_id or username parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        
        # First get user ID if username provided
        if username and not user_id:
            user_response = await self._get_user_profile(session, username=username)
            if not user_response or len(user_response) == 0 or not user_response[0].get("success"):
                return user_response
            user_id = user_response[0]["data"]["data"]["id"]
        
        params = {
            "max_results": min(max_results, 100),
            "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        }
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/users/{user_id}/followers", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get user followers: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get user followers: {str(e)}"}]
    
    async def _get_user_following(self, session, **kwargs):
        """Get users that a specific user is following."""
        user_id = kwargs.get("user_id")
        username = kwargs.get("username")
        
        if not user_id and not username:
            return [{"success": False, "error": "user_id or username parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        
        # First get user ID if username provided
        if username and not user_id:
            user_response = await self._get_user_profile(session, username=username)
            if not user_response or len(user_response) == 0 or not user_response[0].get("success"):
                return user_response
            user_id = user_response[0]["data"]["data"]["id"]
        
        params = {
            "max_results": min(max_results, 100),
            "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        }
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/users/{user_id}/following", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get user following: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get user following: {str(e)}"}]
    
    async def _get_tweet_likes(self, session, **kwargs):
        """Get users who liked a specific tweet."""
        tweet_id = kwargs.get("tweet_id")
        if not tweet_id:
            return [{"success": False, "error": "tweet_id parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        
        params = {
            "max_results": min(max_results, 100),
            "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        }
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/tweets/{tweet_id}/liking_users", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get tweet likes: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get tweet likes: {str(e)}"}]
    
    async def _get_tweet_retweets(self, session, **kwargs):
        """Get users who retweeted a specific tweet."""
        tweet_id = kwargs.get("tweet_id")
        if not tweet_id:
            return [{"success": False, "error": "tweet_id parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        
        params = {
            "max_results": min(max_results, 100),
            "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        }
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/tweets/{tweet_id}/retweeted_by", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get tweet retweets: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get tweet retweets: {str(e)}"}]
    
    async def _get_user_mentions(self, session, **kwargs):
        """Get tweets that mention a specific user."""
        user_id = kwargs.get("user_id")
        username = kwargs.get("username")
        
        if not user_id and not username:
            return [{"success": False, "error": "user_id or username parameter is required"}]
        
        max_results = kwargs.get("max_results", 10)
        since_id = kwargs.get("since_id")
        until_id = kwargs.get("until_id")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        
        # First get user ID if username provided
        if username and not user_id:
            user_response = await self._get_user_profile(session, username=username)
            if not user_response or len(user_response) == 0 or not user_response[0].get("success"):
                return user_response
            user_id = user_response[0]["data"]["data"]["id"]
        
        params = {
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,author_id,public_metrics,entities,context_annotations,lang"
        }
        
        if since_id:
            params["since_id"] = since_id
        if until_id:
            params["until_id"] = until_id
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/users/{user_id}/mentions", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get user mentions: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get user mentions: {str(e)}"}]
    
    async def _get_hashtag_tweets(self, session, **kwargs):
        """Get tweets with a specific hashtag."""
        hashtag = kwargs.get("hashtag")
        if not hashtag:
            return [{"success": False, "error": "hashtag parameter is required"}]
        
        # Remove # if present
        hashtag = hashtag.lstrip("#")
        
        max_results = kwargs.get("max_results", 10)
        since_id = kwargs.get("since_id")
        until_id = kwargs.get("until_id")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        
        params = {
            "query": f"#{hashtag}",
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,author_id,public_metrics,entities,context_annotations,lang"
        }
        
        if since_id:
            params["since_id"] = since_id
        if until_id:
            params["until_id"] = until_id
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/tweets/search/recent", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get hashtag tweets: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get hashtag tweets: {str(e)}"}]
    
    async def _get_user_timeline(self, session, **kwargs):
        """Get user's home timeline (requires user context)."""
        max_results = kwargs.get("max_results", 10)
        since_id = kwargs.get("since_id")
        until_id = kwargs.get("until_id")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        
        params = {
            "max_results": min(max_results, 100),
            "tweet.fields": "created_at,author_id,public_metrics,entities,context_annotations,lang"
        }
        
        if since_id:
            params["since_id"] = since_id
        if until_id:
            params["until_id"] = until_id
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        headers = {"Authorization": f"Bearer {self.bearer_token}"} if self.bearer_token else {}
        
        try:
            async with session.get(f"{self.twitter_api_url}/tweets", params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{"success": True, "data": data}]
                else:
                    return [{"success": False, "error": f"Failed to get user timeline: {response.status}"}]
        except Exception as e:
            return [{"success": False, "error": f"Failed to get user timeline: {str(e)}"}]


class RedditTool(MCPTool):
    """Reddit API integration tool for fetching posts, comments, and subreddit data"""
    
    def __init__(self):
        self.session = None
        self.reddit_api_url = "https://oauth.reddit.com"
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "MCP-Reddit-Tool/1.0")
        self.access_token = None
    
    @property
    def name(self) -> str:
        return "reddit"
    
    @property
    def description(self) -> str:
        return "Reddit API integration for fetching posts, comments, subreddit data, and user information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "search_posts",
                        "get_subreddit_posts",
                        "get_post_comments",
                        "get_user_posts",
                        "get_user_comments",
                        "get_subreddit_info",
                        "get_user_info",
                        "get_trending_subreddits",
                        "get_hot_posts",
                        "get_new_posts",
                        "get_top_posts",
                        "get_rising_posts"
                    ],
                    "description": "The action to perform"
                },
                "query": {
                    "type": "string",
                    "description": "Search query for posts"
                },
                "subreddit": {
                    "type": "string",
                    "description": "Subreddit name (without r/)"
                },
                "username": {
                    "type": "string",
                    "description": "Reddit username"
                },
                "post_id": {
                    "type": "string",
                    "description": "Reddit post ID"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 25,
                    "description": "Number of results to return (max 100)"
                },
                "time_filter": {
                    "type": "string",
                    "enum": ["hour", "day", "week", "month", "year", "all"],
                    "default": "day",
                    "description": "Time filter for posts"
                },
                "sort": {
                    "type": "string",
                    "enum": ["hot", "new", "top", "rising"],
                    "default": "hot",
                    "description": "Sort order for posts"
                }
            },
            "required": ["action"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def _get_access_token(self):
        """Get Reddit OAuth access token"""
        if not self.client_id or not self.client_secret:
            return None
        
        try:
            session = await self._get_session()
            auth_url = "https://www.reddit.com/api/v1/access_token"
            
            # Use client credentials flow
            auth_data = aiohttp.FormData()
            auth_data.add_field('grant_type', 'client_credentials')
            
            auth_headers = {
                'User-Agent': self.user_agent
            }
            
            async with session.post(
                auth_url,
                data=auth_data,
                headers=auth_headers,
                auth=aiohttp.BasicAuth(self.client_id, self.client_secret)
            ) as response:
                if response.status == 200:
                    token_data = await response.json()
                    self.access_token = token_data.get('access_token')
                    return self.access_token
                else:
                    return None
        except Exception as e:
            return None
    
    async def _make_reddit_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make authenticated request to Reddit API"""
        try:
            session = await self._get_session()
            
            # Get access token if not available
            if not self.access_token:
                await self._get_access_token()
            
            if not self.access_token:
                return {"success": False, "error": "Failed to authenticate with Reddit API"}
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'User-Agent': self.user_agent
            }
            
            url = f"{self.reddit_api_url}{endpoint}"
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"success": True, "data": data}
                else:
                    return {"success": False, "error": f"Reddit API error: {response.status}"}
                    
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    async def _search_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Search for posts"""
        query = kwargs.get("query")
        if not query:
            return [{"success": False, "error": "query parameter is required"}]
        
        limit = min(kwargs.get("limit", 25), 100)
        time_filter = kwargs.get("time_filter", "day")
        
        params = {
            'q': query,
            'limit': limit,
            't': time_filter,
            'type': 'link'
        }
        
        result = await self._make_reddit_request('/search', params)
        return [result]
    
    async def _get_subreddit_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get posts from a subreddit"""
        subreddit = kwargs.get("subreddit")
        if not subreddit:
            return [{"success": False, "error": "subreddit parameter is required"}]
        
        limit = min(kwargs.get("limit", 25), 100)
        sort = kwargs.get("sort", "hot")
        time_filter = kwargs.get("time_filter", "day")
        
        params = {
            'limit': limit,
            't': time_filter
        }
        
        endpoint = f'/r/{subreddit}/{sort}'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_post_comments(self, **kwargs) -> List[Dict[str, Any]]:
        """Get comments for a post"""
        post_id = kwargs.get("post_id")
        if not post_id:
            return [{"success": False, "error": "post_id parameter is required"}]
        
        limit = min(kwargs.get("limit", 25), 100)
        
        params = {
            'limit': limit,
            'depth': 1
        }
        
        endpoint = f'/comments/{post_id}'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_user_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get posts by a user"""
        username = kwargs.get("username")
        if not username:
            return [{"success": False, "error": "username parameter is required"}]
        
        limit = min(kwargs.get("limit", 25), 100)
        time_filter = kwargs.get("time_filter", "day")
        
        params = {
            'limit': limit,
            't': time_filter
        }
        
        endpoint = f'/user/{username}/submitted'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_user_comments(self, **kwargs) -> List[Dict[str, Any]]:
        """Get comments by a user"""
        username = kwargs.get("username")
        if not username:
            return [{"success": False, "error": "username parameter is required"}]
        
        limit = min(kwargs.get("limit", 25), 100)
        time_filter = kwargs.get("time_filter", "day")
        
        params = {
            'limit': limit,
            't': time_filter
        }
        
        endpoint = f'/user/{username}/comments'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_subreddit_info(self, **kwargs) -> List[Dict[str, Any]]:
        """Get subreddit information"""
        subreddit = kwargs.get("subreddit")
        if not subreddit:
            return [{"success": False, "error": "subreddit parameter is required"}]
        
        endpoint = f'/r/{subreddit}/about'
        result = await self._make_reddit_request(endpoint)
        return [result]
    
    async def _get_user_info(self, **kwargs) -> List[Dict[str, Any]]:
        """Get user information"""
        username = kwargs.get("username")
        if not username:
            return [{"success": False, "error": "username parameter is required"}]
        
        endpoint = f'/user/{username}/about'
        result = await self._make_reddit_request(endpoint)
        return [result]
    
    async def _get_trending_subreddits(self, **kwargs) -> List[Dict[str, Any]]:
        """Get trending subreddits"""
        limit = min(kwargs.get("limit", 25), 100)
        
        params = {
            'limit': limit
        }
        
        endpoint = '/subreddits/popular'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_hot_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get hot posts from front page"""
        limit = min(kwargs.get("limit", 25), 100)
        
        params = {
            'limit': limit
        }
        
        endpoint = '/hot'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_new_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get new posts from front page"""
        limit = min(kwargs.get("limit", 25), 100)
        
        params = {
            'limit': limit
        }
        
        endpoint = '/new'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_top_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get top posts from front page"""
        limit = min(kwargs.get("limit", 25), 100)
        time_filter = kwargs.get("time_filter", "day")
        
        params = {
            'limit': limit,
            't': time_filter
        }
        
        endpoint = '/top'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def _get_rising_posts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get rising posts from front page"""
        limit = min(kwargs.get("limit", 25), 100)
        
        params = {
            'limit': limit
        }
        
        endpoint = '/rising'
        result = await self._make_reddit_request(endpoint, params)
        return [result]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute Reddit API operations"""
        try:
            action = arguments.get("action")
            
            if action == "search_posts":
                return await self._search_posts(**arguments)
            elif action == "get_subreddit_posts":
                return await self._get_subreddit_posts(**arguments)
            elif action == "get_post_comments":
                return await self._get_post_comments(**arguments)
            elif action == "get_user_posts":
                return await self._get_user_posts(**arguments)
            elif action == "get_user_comments":
                return await self._get_user_comments(**arguments)
            elif action == "get_subreddit_info":
                return await self._get_subreddit_info(**arguments)
            elif action == "get_user_info":
                return await self._get_user_info(**arguments)
            elif action == "get_trending_subreddits":
                return await self._get_trending_subreddits(**arguments)
            elif action == "get_hot_posts":
                return await self._get_hot_posts(**arguments)
            elif action == "get_new_posts":
                return await self._get_new_posts(**arguments)
            elif action == "get_top_posts":
                return await self._get_top_posts(**arguments)
            elif action == "get_rising_posts":
                return await self._get_rising_posts(**arguments)
            else:
                return [{"success": False, "error": f"Unknown action: {action}"}]
                
        except Exception as e:
            return [{"success": False, "error": f"Execution error: {str(e)}"}]
        finally:
            await self._cleanup_session()

