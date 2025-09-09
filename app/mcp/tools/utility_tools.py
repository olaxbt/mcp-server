

import asyncio
import logging
import time
import aiohttp
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)





class OpenWeatherTool(MCPTool):
    """OpenWeatherMap API integration tool for weather data and forecasting"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0"
    
    @property
    def name(self) -> str:
        return "openweather"
    
    @property
    def description(self) -> str:
        return "OpenWeatherMap API integration for current weather, forecasts, and weather alerts"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_current_weather",
                        "get_weather_forecast",
                        "get_weather_alerts",
                        "get_air_pollution",
                        "get_geocoding",
                        "get_reverse_geocoding",
                        "get_weather_history"
                    ],
                    "description": "The action to perform"
                },
                "location": {
                    "type": "string",
                    "description": "City name, coordinates (lat,lon), or location query"
                },
                "latitude": {
                    "type": "number",
                    "description": "Latitude coordinate"
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude coordinate"
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial", "standard"],
                    "default": "metric",
                    "description": "Units for temperature and measurements"
                },
                "lang": {
                    "type": "string",
                    "default": "en",
                    "description": "Language for weather descriptions"
                },
                "days": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 16,
                    "default": 5,
                    "description": "Number of days for forecast (max 16)"
                },
                "exclude": {
                    "type": "string",
                    "description": "Exclude parts from response (current,minutely,hourly,daily,alerts)"
                },
                "api_key": {
                    "type": "string",
                    "description": "OpenWeatherMap API key (required)"
                }
            },
            "required": ["action", "api_key"]
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
    
    async def _make_request(self, url: str, params: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:
        """Make request to OpenWeatherMap API"""
        try:
            session = await self._get_session()
            
            if not api_key:
                return {"success": False, "error": "OpenWeatherMap API key is required"}
            
            # Add API key to params
            if params is None:
                params = {}
            params["appid"] = api_key
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"success": True, "data": data}
                else:
                    error_text = await response.text()
                    return {"success": False, "error": f"API error {response.status}: {error_text}"}
                    
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    async def _get_current_weather(self, **kwargs) -> List[Dict[str, Any]]:
        """Get current weather data"""
        location = kwargs.get("location")
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        units = kwargs.get("units", "metric")
        lang = kwargs.get("lang", "en")
        
        if not location and (lat is None or lon is None):
            return [{"success": False, "error": "location or latitude/longitude parameters are required"}]
        
        params = {
            "units": units,
            "lang": lang
        }
        
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            params["q"] = location
        
        url = f"{self.base_url}/weather"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def _get_weather_forecast(self, **kwargs) -> List[Dict[str, Any]]:
        """Get weather forecast data"""
        location = kwargs.get("location")
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        units = kwargs.get("units", "metric")
        lang = kwargs.get("lang", "en")
        days = min(kwargs.get("days", 5), 16)
        exclude = kwargs.get("exclude")
        
        if not location and (lat is None or lon is None):
            return [{"success": False, "error": "location or latitude/longitude parameters are required"}]
        
        params = {
            "units": units,
            "lang": lang,
            "cnt": days
        }
        
        if exclude:
            params["exclude"] = exclude
        
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            params["q"] = location
        
        url = f"{self.base_url}/forecast"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def _get_weather_alerts(self, **kwargs) -> List[Dict[str, Any]]:
        """Get weather alerts"""
        location = kwargs.get("location")
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        units = kwargs.get("units", "metric")
        lang = kwargs.get("lang", "en")
        
        if not location and (lat is None or lon is None):
            return [{"success": False, "error": "location or latitude/longitude parameters are required"}]
        
        params = {
            "units": units,
            "lang": lang,
            "exclude": "current,minutely,hourly,daily"
        }
        
        if lat is not None and lon is not None:
            params["lat"] = lat
            params["lon"] = lon
        else:
            params["q"] = location
        
        url = f"{self.base_url}/onecall"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def _get_air_pollution(self, **kwargs) -> List[Dict[str, Any]]:
        """Get air pollution data"""
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        
        if lat is None or lon is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        params = {
            "lat": lat,
            "lon": lon
        }
        
        url = f"{self.base_url}/air_pollution"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def _get_geocoding(self, **kwargs) -> List[Dict[str, Any]]:
        """Get geocoding data for a location"""
        location = kwargs.get("location")
        limit = kwargs.get("limit", 5)
        lang = kwargs.get("lang", "en")
        
        if not location:
            return [{"success": False, "error": "location parameter is required"}]
        
        params = {
            "q": location,
            "limit": limit,
            "lang": lang
        }
        
        url = f"{self.geo_url}/direct"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def _get_reverse_geocoding(self, **kwargs) -> List[Dict[str, Any]]:
        """Get reverse geocoding data"""
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        limit = kwargs.get("limit", 5)
        lang = kwargs.get("lang", "en")
        
        if lat is None or lon is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        params = {
            "lat": lat,
            "lon": lon,
            "limit": limit,
            "lang": lang
        }
        
        url = f"{self.geo_url}/reverse"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def _get_weather_history(self, **kwargs) -> List[Dict[str, Any]]:
        """Get historical weather data"""
        lat = kwargs.get("latitude")
        lon = kwargs.get("longitude")
        dt = kwargs.get("dt")  # Unix timestamp
        units = kwargs.get("units", "metric")
        lang = kwargs.get("lang", "en")
        
        if lat is None or lon is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        if not dt:
            return [{"success": False, "error": "dt (timestamp) parameter is required"}]
        
        params = {
            "lat": lat,
            "lon": lon,
            "dt": dt,
            "units": units,
            "lang": lang
        }
        
        url = f"{self.base_url}/onecall/timemachine"
        api_key = kwargs.get("api_key")
        result = await self._make_request(url, params, api_key)
        return [result]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute OpenWeatherMap API operations"""
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: OpenWeatherMap API key is required. Please provide your API key."}]
            
            if action == "get_current_weather":
                return await self._get_current_weather(**arguments)
            elif action == "get_weather_forecast":
                return await self._get_weather_forecast(**arguments)
            elif action == "get_weather_alerts":
                return await self._get_weather_alerts(**arguments)
            elif action == "get_air_pollution":
                return await self._get_air_pollution(**arguments)
            elif action == "get_geocoding":
                return await self._get_geocoding(**arguments)
            elif action == "get_reverse_geocoding":
                return await self._get_reverse_geocoding(**arguments)
            elif action == "get_weather_history":
                return await self._get_weather_history(**arguments)
            else:
                return [{"type": "text", "text": f"❌ Error: Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: Execution error: {str(e)}"}]
        finally:
            await self._cleanup_session()


class GoogleMapsTool(MCPTool):
    """Google Maps API integration for geocoding, directions, and places search"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://maps.googleapis.com/maps/api"
    
    @property
    def name(self) -> str:
        return "googlemaps"
    
    @property
    def description(self) -> str:
        return "Google Maps API integration for geocoding, directions, places search, and location services"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "geocode",
                        "reverse_geocode", 
                        "get_directions",
                        "search_places",
                        "get_place_details",
                        "get_nearby_places",
                        "get_distance_matrix",
                        "get_elevation",
                        "get_timezone"
                    ],
                    "description": "The action to perform"
                },
                "address": {
                    "type": "string",
                    "description": "Address for geocoding"
                },
                "latitude": {
                    "type": "number",
                    "description": "Latitude coordinate"
                },
                "longitude": {
                    "type": "number", 
                    "description": "Longitude coordinate"
                },
                "origin": {
                    "type": "string",
                    "description": "Starting location for directions (address or coordinates)"
                },
                "destination": {
                    "type": "string",
                    "description": "Ending location for directions (address or coordinates)"
                },
                "waypoints": {
                    "type": "string",
                    "description": "Intermediate waypoints for directions (comma-separated)"
                },
                "mode": {
                    "type": "string",
                    "enum": ["driving", "walking", "bicycling", "transit"],
                    "description": "Travel mode for directions",
                    "default": "driving"
                },
                "query": {
                    "type": "string",
                    "description": "Search query for places"
                },
                "place_id": {
                    "type": "string",
                    "description": "Google Place ID for place details"
                },
                "radius": {
                    "type": "number",
                    "description": "Search radius in meters for nearby places",
                    "default": 5000
                },
                "type": {
                    "type": "string",
                    "description": "Place type filter (restaurant, hotel, etc.)"
                },
                "language": {
                    "type": "string",
                    "description": "Language code for results",
                    "default": "en"
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": "Units for distance calculations",
                    "default": "metric"
                },
                "origins": {
                    "type": "string",
                    "description": "Starting points for distance matrix (comma-separated)"
                },
                "destinations": {
                    "type": "string",
                    "description": "Ending points for distance matrix (comma-separated)"
                },
                "timestamp": {
                    "type": "number",
                    "description": "Unix timestamp for timezone lookup"
                },
                "keyword": {
                    "type": "string",
                    "description": "Keyword for nearby places search"
                },
                "api_key": {
                    "type": "string",
                    "description": "Google Maps API key (required)"
                }
            },
            "required": ["action", "api_key"]
        }
    
    def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _cleanup_session(self):
        """Close aiohttp session"""
        if self.session:
            asyncio.create_task(self.session.close())
            self.session = None
    
    async def _make_request(self, endpoint: str, params: Dict[str, Any], api_key: str = None) -> Dict[str, Any]:
        """Make request to Google Maps API"""
        if not api_key:
            return {"success": False, "error": "Google Maps API key is required"}
        
        try:
            session = self._get_session()
            params["key"] = api_key
            
            url = f"{self.base_url}/{endpoint}"
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "OK":
                        return {"success": True, "data": data}
                    else:
                        return {"success": False, "error": f"API Error: {data.get('status')} - {data.get('error_message', 'Unknown error')}"}
                else:
                    return {"success": False, "error": f"HTTP {response.status}: {response.reason}"}
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    async def _geocode(self, address: str, language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Convert address to coordinates"""
        if not address:
            return [{"success": False, "error": "address parameter is required"}]
        
        params = {
            "address": address,
            "language": language
        }
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("geocode/json", params, api_key)
        return [result]
    
    async def _reverse_geocode(self, latitude: float, longitude: float, language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Convert coordinates to address"""
        if latitude is None or longitude is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        params = {
            "latlng": f"{latitude},{longitude}",
            "language": language
        }
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("geocode/json", params, api_key)
        return [result]
    
    async def _get_directions(self, origin: str, destination: str, waypoints: str = None, 
                             mode: str = "driving", language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Get directions between two points"""
        if not origin or not destination:
            return [{"success": False, "error": "origin and destination parameters are required"}]
        
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "language": language
        }
        
        if waypoints:
            params["waypoints"] = waypoints
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("directions/json", params, api_key)
        return [result]
    
    async def _search_places(self, query: str, latitude: float = None, longitude: float = None,
                            radius: int = 5000, type: str = None, language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Search for places"""
        if not query:
            return [{"success": False, "error": "query parameter is required"}]
        
        params = {
            "query": query,
            "language": language
        }
        
        if latitude is not None and longitude is not None:
            params["location"] = f"{latitude},{longitude}"
            params["radius"] = radius
        
        if type:
            params["type"] = type
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("place/textsearch/json", params, api_key)
        return [result]
    
    async def _get_place_details(self, place_id: str, language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Get detailed information about a place"""
        if not place_id:
            return [{"success": False, "error": "place_id parameter is required"}]
        
        params = {
            "place_id": place_id,
            "language": language
        }
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("place/details/json", params, api_key)
        return [result]
    
    async def _get_nearby_places(self, latitude: float, longitude: float, radius: int = 5000,
                                type: str = None, keyword: str = None, language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Get nearby places"""
        if latitude is None or longitude is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "language": language
        }
        
        if type:
            params["type"] = type
        if keyword:
            params["keyword"] = keyword
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("place/nearbysearch/json", params, api_key)
        return [result]
    
    async def _get_distance_matrix(self, origins: str, destinations: str, mode: str = "driving",
                                  units: str = "metric", language: str = "en", **kwargs) -> List[Dict[str, Any]]:
        """Get distance and duration matrix"""
        if not origins or not destinations:
            return [{"success": False, "error": "origins and destinations parameters are required"}]
        
        params = {
            "origins": origins,
            "destinations": destinations,
            "mode": mode,
            "units": units,
            "language": language
        }
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("distancematrix/json", params, api_key)
        return [result]
    
    async def _get_elevation(self, latitude: float, longitude: float, **kwargs) -> List[Dict[str, Any]]:
        """Get elevation for coordinates"""
        if latitude is None or longitude is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        params = {
            "locations": f"{latitude},{longitude}"
        }
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("elevation/json", params, api_key)
        return [result]
    
    async def _get_timezone(self, latitude: float, longitude: float, timestamp: int = None, **kwargs) -> List[Dict[str, Any]]:
        """Get timezone information for coordinates"""
        if latitude is None or longitude is None:
            return [{"success": False, "error": "latitude and longitude parameters are required"}]
        
        params = {
            "location": f"{latitude},{longitude}"
        }
        
        if timestamp:
            params["timestamp"] = timestamp
        
        api_key = kwargs.get("api_key")
        result = await self._make_request("timezone/json", params, api_key)
        return [result]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Google Maps tool action"""
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Google Maps API key is required. Please provide your API key."}]
            
            if action == "geocode":
                return await self._geocode(
                    arguments.get("address"),
                    arguments.get("language", "en")
                )
            elif action == "reverse_geocode":
                return await self._reverse_geocode(
                    arguments.get("latitude"),
                    arguments.get("longitude"),
                    arguments.get("language", "en")
                )
            elif action == "get_directions":
                return await self._get_directions(
                    arguments.get("origin"),
                    arguments.get("destination"),
                    arguments.get("waypoints"),
                    arguments.get("mode", "driving"),
                    arguments.get("language", "en")
                )
            elif action == "search_places":
                return await self._search_places(
                    arguments.get("query"),
                    arguments.get("latitude"),
                    arguments.get("longitude"),
                    arguments.get("radius", 5000),
                    arguments.get("type"),
                    arguments.get("language", "en")
                )
            elif action == "get_place_details":
                return await self._get_place_details(
                    arguments.get("place_id"),
                    arguments.get("language", "en")
                )
            elif action == "get_nearby_places":
                return await self._get_nearby_places(
                    arguments.get("latitude"),
                    arguments.get("longitude"),
                    arguments.get("radius", 5000),
                    arguments.get("type"),
                    arguments.get("keyword"),
                    arguments.get("language", "en")
                )
            elif action == "get_distance_matrix":
                return await self._get_distance_matrix(
                    arguments.get("origins"),
                    arguments.get("destinations"),
                    arguments.get("mode", "driving"),
                    arguments.get("units", "metric"),
                    arguments.get("language", "en")
                )
            elif action == "get_elevation":
                return await self._get_elevation(
                    arguments.get("latitude"),
                    arguments.get("longitude")
                )
            elif action == "get_timezone":
                return await self._get_timezone(
                    arguments.get("latitude"),
                    arguments.get("longitude"),
                    arguments.get("timestamp")
                )
            else:
                return [{"type": "text", "text": f"❌ Error: Unknown action: {action}"}]
        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: Execution error: {str(e)}"}]
        finally:
            self._cleanup_session()


class JiraTool(MCPTool):
    """Jira API integration tool for project management and issue tracking"""
    
    def __init__(self):
        self.session = None
        self.base_url = None
        # Note: JIRA credentials will be provided by user
    
    @property
    def name(self) -> str:
        return "jira"
    
    @property
    def description(self) -> str:
        return "Jira API integration for project management, issue tracking, and workflow management"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_issues",
                        "get_issue",
                        "create_issue",
                        "update_issue",
                        "delete_issue",
                        "get_projects",
                        "get_project",
                        "get_boards",
                        "get_sprints",
                        "get_workflows",
                        "get_users",
                        "get_user",
                        "search_issues",
                        "get_issue_comments",
                        "add_comment",
                        "get_attachments",
                        "get_issue_links",
                        "get_issue_watchers",
                        "get_project_components",
                        "get_project_versions"
                    ],
                    "description": "The action to perform"
                },
                "issue_key": {
                    "type": "string",
                    "description": "Jira issue key (e.g., PROJ-123)"
                },
                "project_key": {
                    "type": "string",
                    "description": "Jira project key"
                },
                "jql": {
                    "type": "string",
                    "description": "JQL (Jira Query Language) search string"
                },
                "summary": {
                    "type": "string",
                    "description": "Issue summary/title"
                },
                "description": {
                    "type": "string",
                    "description": "Issue description"
                },
                "issue_type": {
                    "type": "string",
                    "description": "Issue type (Bug, Task, Story, etc.)"
                },
                "priority": {
                    "type": "string",
                    "description": "Issue priority (Highest, High, Medium, Low, Lowest)"
                },
                "assignee": {
                    "type": "string",
                    "description": "Assignee username or account ID"
                },
                "reporter": {
                    "type": "string",
                    "description": "Reporter username or account ID"
                },
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of labels for the issue"
                },
                "components": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of component names"
                },
                "fix_versions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of fix version names"
                },
                "fields": {
                    "type": "object",
                    "description": "Additional fields to set on the issue"
                },
                "max_results": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 50,
                    "description": "Maximum number of results to return"
                },
                "start_at": {
                    "type": "integer",
                    "default": 0,
                    "description": "Starting index for pagination"
                },
                "board_id": {
                    "type": "integer",
                    "description": "Board ID for sprint operations"
                },
                "sprint_id": {
                    "type": "integer",
                    "description": "Sprint ID"
                },
                "comment_body": {
                    "type": "string",
                    "description": "Comment text content"
                },
                "username": {
                    "type": "string",
                    "description": "Username or account ID for user operations"
                },
                "expand": {
                    "type": "string",
                    "description": "Fields to expand in response"
                },
                "jira_domain": {
                    "type": "string",
                    "description": "JIRA domain (e.g., 'company' for company.atlassian.net)"
                },
                "jira_username": {
                    "type": "string",
                    "description": "JIRA username or email (required)"
                },
                "jira_api_token": {
                    "type": "string",
                    "description": "JIRA API token (required)"
                }
            },
            "required": ["action", "jira_domain", "jira_username", "jira_api_token"]
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
    
    async def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Jira API"""
        try:
            session = await self._get_session()
            
            jira_username = kwargs.get("jira_username")
            jira_api_token = kwargs.get("jira_api_token")
            base_url = kwargs.get("base_url") or self.base_url
            
            if not base_url or not jira_username or not jira_api_token:
                return {"type": "text", "text": "❌ Error: JIRA credentials not configured. Please provide domain, username, and API token."}
            
            url = f"{base_url}/{endpoint}"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            # Basic auth with username and API token
            auth = aiohttp.BasicAuth(jira_username, jira_api_token)
            
            if method.upper() == "GET":
                async with session.get(url, headers=headers, auth=auth, params=params) as response:
                    return await self._handle_response(response)
            elif method.upper() == "POST":
                async with session.post(url, headers=headers, auth=auth, json=data, params=params) as response:
                    return await self._handle_response(response)
            elif method.upper() == "PUT":
                async with session.put(url, headers=headers, auth=auth, json=data, params=params) as response:
                    return await self._handle_response(response)
            elif method.upper() == "DELETE":
                async with session.delete(url, headers=headers, auth=auth, params=params) as response:
                    return await self._handle_response(response)
            else:
                return {"type": "text", "text": f"❌ Error: Unsupported HTTP method: {method}"}
                
        except Exception as e:
            return {"type": "text", "text": f"❌ Error: Request failed: {str(e)}"}
    
    async def _handle_response(self, response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            if response.status == 204:  # No content (e.g., successful delete)
                return {"success": True, "data": None}
            elif response.status in [200, 201]:
                data = await response.json()
                return {"success": True, "data": data}
            else:
                error_text = await response.text()
                return {"success": False, "error": f"API error {response.status}: {error_text}"}
        except Exception as e:
            return {"success": False, "error": f"Response parsing failed: {str(e)}"}
    
    async def _get_issues(self, **kwargs) -> List[Dict[str, Any]]:
        """Get issues from a project"""
        project_key = kwargs.get("project_key")
        max_results = min(kwargs.get("max_results", 50), 100)
        start_at = kwargs.get("start_at", 0)
        expand = kwargs.get("expand", "names,schema")
        
        if not project_key:
            return [{"success": False, "error": "project_key parameter is required"}]
        
        params = {
            "jql": f"project = {project_key}",
            "maxResults": max_results,
            "startAt": start_at,
            "expand": expand
        }
        
        result = await self._make_request("GET", "search", params=params)
        return [result]
    
    async def _get_issue(self, **kwargs) -> List[Dict[str, Any]]:
        """Get a specific issue by key"""
        issue_key = kwargs.get("issue_key")
        expand = kwargs.get("expand", "names,schema")
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        params = {"expand": expand} if expand else {}
        result = await self._make_request("GET", f"issue/{issue_key}", params=params)
        return [result]
    
    async def _create_issue(self, **kwargs) -> List[Dict[str, Any]]:
        """Create a new issue"""
        project_key = kwargs.get("project_key")
        summary = kwargs.get("summary")
        description = kwargs.get("description")
        issue_type = kwargs.get("issue_type", "Task")
        priority = kwargs.get("priority")
        assignee = kwargs.get("assignee")
        reporter = kwargs.get("reporter")
        labels = kwargs.get("labels", [])
        components = kwargs.get("components", [])
        fix_versions = kwargs.get("fix_versions", [])
        fields = kwargs.get("fields", {})
        
        if not project_key or not summary:
            return [{"success": False, "error": "project_key and summary parameters are required"}]
        
        # Build issue data
        issue_data = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "issuetype": {"name": issue_type}
            }
        }
        
        if description:
            issue_data["fields"]["description"] = {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}]
                    }
                ]
            }
        
        if priority:
            issue_data["fields"]["priority"] = {"name": priority}
        
        if assignee:
            issue_data["fields"]["assignee"] = {"name": assignee}
        
        if reporter:
            issue_data["fields"]["reporter"] = {"name": reporter}
        
        if labels:
            issue_data["fields"]["labels"] = labels
        
        if components:
            issue_data["fields"]["components"] = [{"name": comp} for comp in components]
        
        if fix_versions:
            issue_data["fields"]["fixVersions"] = [{"name": version} for version in fix_versions]
        
        # Add any additional fields
        issue_data["fields"].update(fields)
        
        result = await self._make_request("POST", "issue", data=issue_data)
        return [result]
    
    async def _update_issue(self, **kwargs) -> List[Dict[str, Any]]:
        """Update an existing issue"""
        issue_key = kwargs.get("issue_key")
        fields = kwargs.get("fields", {})
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        if not fields:
            return [{"success": False, "error": "fields parameter is required"}]
        
        issue_data = {"fields": fields}
        result = await self._make_request("PUT", f"issue/{issue_key}", data=issue_data)
        return [result]
    
    async def _delete_issue(self, **kwargs) -> List[Dict[str, Any]]:
        """Delete an issue"""
        issue_key = kwargs.get("issue_key")
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        result = await self._make_request("DELETE", f"issue/{issue_key}")
        return [result]
    
    async def _get_projects(self, **kwargs) -> List[Dict[str, Any]]:
        """Get all projects"""
        expand = kwargs.get("expand", "lead,issueTypes")
        result = await self._make_request("GET", "project", params={"expand": expand})
        return [result]
    
    async def _get_project(self, **kwargs) -> List[Dict[str, Any]]:
        """Get a specific project"""
        project_key = kwargs.get("project_key")
        expand = kwargs.get("expand", "lead,issueTypes")
        
        if not project_key:
            return [{"success": False, "error": "project_key parameter is required"}]
        
        result = await self._make_request("GET", f"project/{project_key}", params={"expand": expand})
        return [result]
    
    async def _get_boards(self, **kwargs) -> List[Dict[str, Any]]:
        """Get all boards"""
        result = await self._make_request("GET", "board")
        return [result]
    
    async def _get_sprints(self, **kwargs) -> List[Dict[str, Any]]:
        """Get sprints for a board"""
        board_id = kwargs.get("board_id")
        state = kwargs.get("state", "active")  # active, future, closed
        
        if not board_id:
            return [{"success": False, "error": "board_id parameter is required"}]
        
        params = {"state": state}
        result = await self._make_request("GET", f"board/{board_id}/sprint", params=params)
        return [result]
    
    async def _get_workflows(self, **kwargs) -> List[Dict[str, Any]]:
        """Get workflows"""
        result = await self._make_request("GET", "workflow")
        return [result]
    
    async def _get_users(self, **kwargs) -> List[Dict[str, Any]]:
        """Get users"""
        max_results = min(kwargs.get("max_results", 50), 100)
        start_at = kwargs.get("start_at", 0)
        
        params = {
            "maxResults": max_results,
            "startAt": start_at
        }
        
        result = await self._make_request("GET", "users/search", params=params)
        return [result]
    
    async def _get_user(self, **kwargs) -> List[Dict[str, Any]]:
        """Get a specific user"""
        username = kwargs.get("username")
        
        if not username:
            return [{"success": False, "error": "username parameter is required"}]
        
        result = await self._make_request("GET", f"user", params={"accountId": username})
        return [result]
    
    async def _search_issues(self, **kwargs) -> List[Dict[str, Any]]:
        """Search issues using JQL"""
        jql = kwargs.get("jql")
        max_results = min(kwargs.get("max_results", 50), 100)
        start_at = kwargs.get("start_at", 0)
        expand = kwargs.get("expand", "names,schema")
        
        if not jql:
            return [{"success": False, "error": "jql parameter is required"}]
        
        params = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at,
            "expand": expand
        }
        
        result = await self._make_request("GET", "search", params=params)
        return [result]
    
    async def _get_issue_comments(self, **kwargs) -> List[Dict[str, Any]]:
        """Get comments for an issue"""
        issue_key = kwargs.get("issue_key")
        max_results = min(kwargs.get("max_results", 50), 100)
        start_at = kwargs.get("start_at", 0)
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        params = {
            "maxResults": max_results,
            "startAt": start_at
        }
        
        result = await self._make_request("GET", f"issue/{issue_key}/comment", params=params)
        return [result]
    
    async def _add_comment(self, **kwargs) -> List[Dict[str, Any]]:
        """Add a comment to an issue"""
        issue_key = kwargs.get("issue_key")
        comment_body = kwargs.get("comment_body")
        
        if not issue_key or not comment_body:
            return [{"success": False, "error": "issue_key and comment_body parameters are required"}]
        
        comment_data = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment_body}]
                    }
                ]
            }
        }
        
        result = await self._make_request("POST", f"issue/{issue_key}/comment", data=comment_data)
        return [result]
    
    async def _get_attachments(self, **kwargs) -> List[Dict[str, Any]]:
        """Get attachments for an issue"""
        issue_key = kwargs.get("issue_key")
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        result = await self._make_request("GET", f"issue/{issue_key}/attachments")
        return [result]
    
    async def _get_issue_links(self, **kwargs) -> List[Dict[str, Any]]:
        """Get issue links for an issue"""
        issue_key = kwargs.get("issue_key")
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        result = await self._make_request("GET", f"issue/{issue_key}/remotelink")
        return [result]
    
    async def _get_issue_watchers(self, **kwargs) -> List[Dict[str, Any]]:
        """Get watchers for an issue"""
        issue_key = kwargs.get("issue_key")
        
        if not issue_key:
            return [{"success": False, "error": "issue_key parameter is required"}]
        
        result = await self._make_request("GET", f"issue/{issue_key}/watchers")
        return [result]
    
    async def _get_project_components(self, **kwargs) -> List[Dict[str, Any]]:
        """Get components for a project"""
        project_key = kwargs.get("project_key")
        
        if not project_key:
            return [{"success": False, "error": "project_key parameter is required"}]
        
        result = await self._make_request("GET", f"project/{project_key}/components")
        return [result]
    
    async def _get_project_versions(self, **kwargs) -> List[Dict[str, Any]]:
        """Get versions for a project"""
        project_key = kwargs.get("project_key")
        
        if not project_key:
            return [{"success": False, "error": "project_key parameter is required"}]
        
        result = await self._make_request("GET", f"project/{project_key}/versions")
        return [result]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute Jira API operations"""
        try:
            action = arguments.get("action")
            jira_domain = arguments.get("jira_domain")
            jira_username = arguments.get("jira_username")
            jira_api_token = arguments.get("jira_api_token")
            
            if not jira_domain or not jira_username or not jira_api_token:
                return [{"type": "text", "text": "❌ Error: JIRA domain, username, and API token are required. Please provide all credentials."}]
            
            # Set base URL dynamically
            base_url = f"https://{jira_domain}.atlassian.net/rest/api/3"
            self.base_url = base_url
            
            # Add base_url to arguments for _make_request
            arguments["base_url"] = base_url
            
            if action == "get_issues":
                return await self._get_issues(**arguments)
            elif action == "get_issue":
                return await self._get_issue(**arguments)
            elif action == "create_issue":
                return await self._create_issue(**arguments)
            elif action == "update_issue":
                return await self._update_issue(**arguments)
            elif action == "delete_issue":
                return await self._delete_issue(**arguments)
            elif action == "get_projects":
                return await self._get_projects(**arguments)
            elif action == "get_project":
                return await self._get_project(**arguments)
            elif action == "get_boards":
                return await self._get_boards(**arguments)
            elif action == "get_sprints":
                return await self._get_sprints(**arguments)
            elif action == "get_workflows":
                return await self._get_workflows(**arguments)
            elif action == "get_users":
                return await self._get_user(**arguments)
            elif action == "get_user":
                return await self._get_user(**arguments)
            elif action == "search_issues":
                return await self._search_issues(**arguments)
            elif action == "get_issue_comments":
                return await self._get_issue_comments(**arguments)
            elif action == "add_comment":
                return await self._add_comment(**arguments)
            elif action == "get_attachments":
                return await self._get_attachments(**arguments)
            elif action == "get_issue_links":
                return await self._get_issue_links(**arguments)
            elif action == "get_issue_watchers":
                return await self._get_issue_watchers(**arguments)
            elif action == "get_project_components":
                return await self._get_project_components(**arguments)
            elif action == "get_project_versions":
                return await self._get_project_versions(**arguments)
            else:
                return [{"type": "text", "text": f"❌ Error: Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: Execution error: {str(e)}"}]
        finally:
            await self._cleanup_session()
