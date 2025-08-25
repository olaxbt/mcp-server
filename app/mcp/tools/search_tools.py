"""
Search Tools
Contains web search and search engine integration tools
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional
from duckduckgo_search import DDGS

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class DuckDuckGoSearchTool(MCPTool):
    def __init__(self):
        self.ddgs = DDGS()
        self.last_search_time = 0
        self.min_search_interval = 3  # Minimum 3 seconds between searches
    
    @property
    def name(self) -> str:
        return "duckduckgo_search"
    
    @property
    def description(self) -> str:
        return "Search the web using DuckDuckGo search engine. Returns relevant search results including titles, links, and snippets."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 5, max: 20)",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20
                },
                "region": {
                    "type": "string",
                    "description": "Search region (e.g., 'us-en', 'uk-en', 'de-de')",
                    "default": "us-en"
                },
                "time": {
                    "type": "string",
                    "description": "Time filter for results (e.g., 'd' for day, 'w' for week, 'm' for month, 'y' for year)",
                    "enum": ["d", "w", "m", "y"],
                    "default": None
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            query = arguments.get("query", "")
            max_results = min(arguments.get("max_results", 5), 20)
            region = arguments.get("region", "us-en")
            time_filter = arguments.get("time")
            
            if not query:
                return [{"error": "Query parameter is required"}]
            
            logger.info(f"Executing DuckDuckGo search: {query}")
            
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                None, 
                self._perform_search, 
                query, 
                max_results, 
                region, 
                time_filter
            )
            
            return results
            
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return [{"error": f"Search failed: {str(e)}"}]
    
    def _perform_search(self, query: str, max_results: int, region: str, time_filter: Optional[str]) -> List[Dict[str, Any]]:
        try:
            # Rate limiting to avoid DuckDuckGo rate limit errors
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            
            if time_since_last_search < self.min_search_interval:
                sleep_time = self.min_search_interval - time_since_last_search
                logger.info(f"Rate limiting: waiting {sleep_time:.2f} seconds before search")
                time.sleep(sleep_time)
            
            self.last_search_time = time.time()
            
            logger.info(f"Starting DuckDuckGo search for: {query}")
            
            # Use proper DuckDuckGo search with error handling
            try:
                # Create a new DDGS instance for each search to avoid connection issues
                ddgs = DDGS()
                
                search_kwargs = {
                    "keywords": query,
                    "max_results": max_results,
                    "region": region
                }
                
                if time_filter:
                    search_kwargs["time"] = time_filter
                
                logger.info(f"Search kwargs: {search_kwargs}")
                
                # Execute the search
                search_results = list(ddgs.text(**search_kwargs))
                
                logger.info(f"Raw search results count: {len(search_results)}")
                
                # Process results safely
                processed_results = []
                for result in search_results:
                    if result and isinstance(result, dict):
                        processed_results.append({
                            "title": result.get("title", ""),
                            "link": result.get("link", ""),
                            "snippet": result.get("body", ""),
                            "source": result.get("source", ""),
                            "published_date": result.get("published", "")
                        })
                
                logger.info(f"Processed {len(processed_results)} results")
                
                if not processed_results:
                    return [{"error": "No valid search results found"}]
                
                return processed_results
                
            except Exception as search_error:
                logger.error(f"DuckDuckGo search execution error: {search_error}")
                # Try alternative search method
                try:
                    logger.info("Trying alternative search method...")
                    ddgs = DDGS()
                    # Use simpler search without region/time filters
                    simple_results = list(ddgs.text(keywords=query, max_results=max_results))
                    
                    processed_results = []
                    for result in simple_results:
                        if result and isinstance(result, dict):
                            processed_results.append({
                                "title": result.get("title", ""),
                                "link": result.get("link", ""),
                                "snippet": result.get("body", ""),
                                "source": result.get("source", ""),
                                "published_date": result.get("published", "")
                            })
                    
                    if processed_results:
                        logger.info(f"Alternative search successful: {len(processed_results)} results")
                        return processed_results
                    else:
                        return [{"error": "Alternative search also failed"}]
                        
                except Exception as alt_error:
                    logger.error(f"Alternative search also failed: {alt_error}")
                    return [{"error": f"Search failed: {str(search_error)}"}]
            
        except Exception as e:
            logger.error(f"Search execution error: {e}")
            return [{"error": f"Search execution failed: {str(e)}"}]

class WebSearchTool(MCPTool):
    def __init__(self):
        self.ddgs = DDGS()
        self.last_search_time = 0
        self.min_search_interval = 3  # Minimum 3 seconds between searches
    
    @property
    def name(self) -> str:
        return "web_search"
    
    @property
    def description(self) -> str:
        return "Enhanced web search tool supporting multiple search types including news, images, and videos."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "search_type": {
                    "type": "string",
                    "description": "Type of search to perform",
                    "enum": ["text", "news", "images", "videos"],
                    "default": "text"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5,
                    "minimum": 1,
                    "maximum": 20
                },
                "region": {
                    "type": "string",
                    "description": "Search region",
                    "default": "us-en"
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            query = arguments.get("query", "")
            search_type = arguments.get("search_type", "text")
            max_results = min(arguments.get("max_results", 5), 20)
            region = arguments.get("region", "us-en")
            
            if not query:
                return [{"error": "Query parameter is required"}]
            
            logger.info(f"Executing {search_type} search: {query}")
            
            loop = asyncio.get_event_loop()
            
            if search_type == "news":
                results = await loop.run_in_executor(
                    None, self._search_news, query, max_results, region
                )
            elif search_type == "images":
                results = await loop.run_in_executor(
                    None, self._search_images, query, max_results, region
                )
            elif search_type == "videos":
                results = await loop.run_in_executor(
                    None, self._search_videos, query, max_results, region
                )
            else:
                results = await loop.run_in_executor(
                    None, self._search_text, query, max_results, region
                )
            
            return results
            
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return [{"error": f"Search failed: {str(e)}"}]
    
    def _search_text(self, query: str, max_results: int, region: str) -> List[Dict[str, Any]]:
        try:
            # Rate limiting to avoid DuckDuckGo rate limit errors
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            
            if time_since_last_search < self.min_search_interval:
                sleep_time = self.min_search_interval - time_since_last_search
                logger.info(f"Rate limiting: waiting {sleep_time:.2f} seconds before search")
                time.sleep(sleep_time)
            
            self.last_search_time = time.time()
            
            logger.info(f"Starting text search for: {query}")
            
            # Create new DDGS instance for each search
            ddgs = DDGS()
            
            # Get search results and handle potential errors
            search_response = ddgs.text(keywords=query, max_results=max_results, region=region)
            
            # Check if we got a valid response
            if not search_response:
                return [{"error": "No search results returned"}]
            
            # Convert to list safely
            try:
                results = list(search_response)
            except Exception as list_error:
                logger.error(f"Error converting search results to list: {list_error}")
                return [{"error": f"Error processing search results: {str(list_error)}"}]
            
            # Process results safely
            processed_results = []
            for r in results:
                if r and isinstance(r, dict):
                    processed_results.append({
                        "title": r.get("title", ""),
                        "link": r.get("link", ""),
                        "snippet": r.get("body", ""),
                        "source": r.get("source", ""),
                        "type": "text"
                    })
            
            if not processed_results:
                return [{"error": "No valid search results found"}]
            
            logger.info(f"Text search successful: {len(processed_results)} results")
            return processed_results
            
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return [{"error": f"Text search failed: {str(e)}"}]
    
    def _search_news(self, query: str, max_results: int, region: str) -> List[Dict[str, Any]]:
        try:
            # Rate limiting
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            
            if time_since_last_search < self.min_search_interval:
                sleep_time = self.min_search_interval - time_since_last_search
                time.sleep(sleep_time)
            
            self.last_search_time = time.time()
            
            ddgs = DDGS()
            results = list(ddgs.news(keywords=query, max_results=max_results, region=region))
            return [
                {
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("body", ""),
                    "source": r.get("source", ""),
                    "published_date": r.get("date", ""),
                    "type": "news"
                }
                for r in results if r and isinstance(r, dict)
            ]
        except Exception as e:
            return [{"error": f"News search failed: {str(e)}"}]
    
    def _search_images(self, query: str, max_results: int, region: str) -> List[Dict[str, Any]]:
        try:
            # Rate limiting
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            
            if time_since_last_search < self.min_search_interval:
                sleep_time = self.min_search_interval - time_since_last_search
                time.sleep(sleep_time)
            
            self.last_search_time = time.time()
            
            ddgs = DDGS()
            results = list(ddgs.images(keywords=query, max_results=max_results, region=region))
            return [
                {
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "image_url": r.get("image", ""),
                    "source": r.get("source", ""),
                    "type": "image"
                }
                for r in results if r and isinstance(r, dict)
            ]
        except Exception as e:
            return [{"error": f"Image search failed: {str(e)}"}]
    
    def _search_videos(self, query: str, max_results: int, region: str) -> List[Dict[str, Any]]:
        try:
            # Rate limiting
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            
            if time_since_last_search < self.min_search_interval:
                sleep_time = self.min_search_interval - time_since_last_search
                time.sleep(sleep_time)
            
            self.last_search_time = time.time()
            
            ddgs = DDGS()
            results = list(ddgs.videos(keywords=query, max_results=max_results, region=region))
            return [
                {
                    "title": r.get("title", ""),
                    "link": r.get("link", ""),
                    "snippet": r.get("description", ""),
                    "thumbnail": r.get("image", ""),
                    "duration": r.get("duration", ""),
                    "type": "video"
                }
                for r in results if r and isinstance(r, dict)
            ]
        except Exception as e:
            return [{"error": f"Video search failed: {str(e)}"}]
