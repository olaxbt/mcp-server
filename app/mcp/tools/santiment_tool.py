"""
Santiment MCP Tool
Access social sentiment and market intelligence data from Santiment API
"""

import aiohttp
import json
import asyncio
from typing import Dict, Any, List, Optional
from .mcp_tool import MCPTool
import logging

logger = logging.getLogger(__name__)

class SantimentTool(MCPTool):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.santiment.net/graphql"
        self._session = None
    
    @property
    def name(self) -> str:
        return "santiment"
    
    @property
    def description(self) -> str:
        return "Access social sentiment and market intelligence data from Santiment API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_social_volume",
                        "get_social_dominance",
                        "get_sentiment_positive_negative",
                        "get_development_activity",
                        "get_network_growth",
                        "get_daily_active_addresses",
                        "get_transaction_volume",
                        "get_network_realized_value",
                        "get_mvrv_ratio",
                        "get_fear_greed_index",
                        "get_top_social_gainers",
                        "get_top_social_losers",
                        "get_emerging_trends",
                        "get_whale_transactions",
                        "get_exchange_flows"
                    ],
                    "description": "The action to perform"
                },
                "slug": {
                    "type": "string",
                    "description": "Asset slug (e.g., bitcoin, ethereum)",
                    "default": "bitcoin"
                },
                "from_date": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD)",
                    "default": "2024-01-01"
                },
                "to_date": {
                    "type": "string",
                    "description": "End date (YYYY-MM-DD)",
                    "default": "2024-01-15"
                },
                "interval": {
                    "type": "string",
                    "enum": ["1h", "1d", "1w"],
                    "description": "Data interval",
                    "default": "1d"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 100
                },
                "api_key": {
                    "type": "string",
                    "description": "Santiment API key (required for all endpoints)",
                    "default": ""
                }
            },
            "required": ["action"]
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def _make_request(self, query: str, variables: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:
        """Make GraphQL request to Santiment API"""
        session = await self._get_session()
        
        headers = {
            "Content-Type": "application/json"
        }
        
        if api_key and api_key.strip():
            headers["Authorization"] = f"Apikey {api_key.strip()}"
        else:
            return {"error": "API key is required for Santiment API"}
        
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        try:
            async with session.post(self.base_url, json=payload, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Santiment API request failed: {e}")
            return {"error": f"Santiment API request failed: {e}"}
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_social_volume":
                return await self._get_social_volume(arguments)
            elif action == "get_social_dominance":
                return await self._get_social_dominance(arguments)
            elif action == "get_sentiment_positive_negative":
                return await self._get_sentiment_positive_negative(arguments)
            elif action == "get_development_activity":
                return await self._get_development_activity(arguments)
            elif action == "get_network_growth":
                return await self._get_network_growth(arguments)
            elif action == "get_daily_active_addresses":
                return await self._get_daily_active_addresses(arguments)
            elif action == "get_transaction_volume":
                return await self._get_transaction_volume(arguments)
            elif action == "get_network_realized_value":
                return await self._get_network_realized_value(arguments)
            elif action == "get_mvrv_ratio":
                return await self._get_mvrv_ratio(arguments)
            elif action == "get_fear_greed_index":
                return await self._get_fear_greed_index(arguments)
            elif action == "get_top_social_gainers":
                return await self._get_top_social_gainers(arguments)
            elif action == "get_top_social_losers":
                return await self._get_top_social_losers(arguments)
            elif action == "get_emerging_trends":
                return await self._get_emerging_trends(arguments)
            elif action == "get_whale_transactions":
                return await self._get_whale_transactions(arguments)
            elif action == "get_exchange_flows":
                return await self._get_exchange_flows(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _get_social_volume(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get social volume data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getSocialVolume($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "social_volume") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Social Volume for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching social volume: {e}")
            return [{"type": "text", "text": f"❌ Error fetching social volume: {str(e)}"}]
    
    async def _get_social_dominance(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get social dominance data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getSocialDominance($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "social_dominance") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Social Dominance for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching social dominance: {e}")
            return [{"type": "text", "text": f"❌ Error fetching social dominance: {str(e)}"}]
    
    async def _get_sentiment_positive_negative(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get sentiment data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getSentiment($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "sentiment_positive_negative") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Sentiment for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching sentiment: {e}")
            return [{"type": "text", "text": f"❌ Error fetching sentiment: {str(e)}"}]
    
    async def _get_development_activity(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get development activity data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getDevelopmentActivity($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "dev_activity") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Development Activity for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching development activity: {e}")
            return [{"type": "text", "text": f"❌ Error fetching development activity: {str(e)}"}]
    
    async def _get_network_growth(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get network growth data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getNetworkGrowth($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "network_growth") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Network Growth for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching network growth: {e}")
            return [{"type": "text", "text": f"❌ Error fetching network growth: {str(e)}"}]
    
    async def _get_daily_active_addresses(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get daily active addresses data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getDailyActiveAddresses($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "daily_active_addresses") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Daily Active Addresses for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching daily active addresses: {e}")
            return [{"type": "text", "text": f"❌ Error fetching daily active addresses: {str(e)}"}]
    
    async def _get_transaction_volume(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get transaction volume data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getTransactionVolume($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "transaction_volume") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Transaction Volume for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching transaction volume: {e}")
            return [{"type": "text", "text": f"❌ Error fetching transaction volume: {str(e)}"}]
    
    async def _get_network_realized_value(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get network realized value data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getNetworkRealizedValue($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "network_realized_value") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Network Realized Value for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching network realized value: {e}")
            return [{"type": "text", "text": f"❌ Error fetching network realized value: {str(e)}"}]
    
    async def _get_mvrv_ratio(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get MVRV ratio data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getMVRVRatio($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "mvrv_ratio") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment MVRV Ratio for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching MVRV ratio: {e}")
            return [{"type": "text", "text": f"❌ Error fetching MVRV ratio: {str(e)}"}]
    
    async def _get_fear_greed_index(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get fear & greed index data"""
        api_key = args.get("api_key")
        
        query = """
        query getFearGreedIndex {
          getMetric(metric: "fear_greed_index") {
            timeseriesData(
              slug: "bitcoin"
              from: "2024-01-01T00:00:00Z"
              to: "2024-01-15T23:59:59Z"
              interval: "1d"
            ) {
              datetime
              value
            }
          }
        }
        """
        
        try:
            data = await self._make_request(query, {}, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Fear & Greed Index:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching fear & greed index: {e}")
            return [{"type": "text", "text": f"❌ Error fetching fear & greed index: {str(e)}"}]
    
    async def _get_top_social_gainers(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top social gainers data"""
        api_key = args.get("api_key")
        
        query = """
        query getTopSocialGainers {
          getMetric(metric: "top_social_gainers") {
            timeseriesData(
              slug: "bitcoin"
              from: "2024-01-01T00:00:00Z"
              to: "2024-01-15T23:59:59Z"
              interval: "1d"
            ) {
              datetime
              value
            }
          }
        }
        """
        
        try:
            data = await self._make_request(query, {}, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Top Social Gainers:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching top social gainers: {e}")
            return [{"type": "text", "text": f"❌ Error fetching top social gainers: {str(e)}"}]
    
    async def _get_top_social_losers(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get top social losers data"""
        api_key = args.get("api_key")
        
        query = """
        query getTopSocialLosers {
          getMetric(metric: "top_social_losers") {
            timeseriesData(
              slug: "bitcoin"
              from: "2024-01-01T00:00:00Z"
              to: "2024-01-15T23:59:59Z"
              interval: "1d"
            ) {
              datetime
              value
            }
          }
        }
        """
        
        try:
            data = await self._make_request(query, {}, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Top Social Losers:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching top social losers: {e}")
            return [{"type": "text", "text": f"❌ Error fetching top social losers: {str(e)}"}]
    
    async def _get_emerging_trends(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get emerging trends data"""
        api_key = args.get("api_key")
        
        query = """
        query getEmergingTrends {
          getMetric(metric: "emerging_trends") {
            timeseriesData(
              slug: "bitcoin"
              from: "2024-01-01T00:00:00Z"
              to: "2024-01-15T23:59:59Z"
              interval: "1d"
            ) {
              datetime
              value
            }
          }
        }
        """
        
        try:
            data = await self._make_request(query, {}, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Emerging Trends:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching emerging trends: {e}")
            return [{"type": "text", "text": f"❌ Error fetching emerging trends: {str(e)}"}]
    
    async def _get_whale_transactions(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get whale transactions data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getWhaleTransactions($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "whale_transactions") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Whale Transactions for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching whale transactions: {e}")
            return [{"type": "text", "text": f"❌ Error fetching whale transactions: {str(e)}"}]
    
    async def _get_exchange_flows(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get exchange flows data"""
        slug = args.get("slug", "bitcoin")
        from_date = args.get("from_date", "2024-01-01")
        to_date = args.get("to_date", "2024-01-15")
        interval = args.get("interval", "1d")
        api_key = args.get("api_key")
        
        query = """
        query getExchangeFlows($slug: String!, $from: DateTime!, $to: DateTime!, $interval: String!) {
          getMetric(metric: "exchange_flows") {
            timeseriesData(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            ) {
              datetime
              value
            }
          }
        }
        """
        
        variables = {
            "slug": slug,
            "from": f"{from_date}T00:00:00Z",
            "to": f"{to_date}T23:59:59Z",
            "interval": interval
        }
        
        try:
            data = await self._make_request(query, variables, api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Santiment Exchange Flows for {slug}:\n\n{json.dumps(data, indent=2)}"}]
        except Exception as e:
            logger.error(f"Error fetching exchange flows: {e}")
            return [{"type": "text", "text": f"❌ Error fetching exchange flows: {str(e)}"}]