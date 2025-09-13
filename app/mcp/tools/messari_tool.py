"""
Messari MCP Tool
Access on-chain metrics and research data from Messari API
"""

import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class MessariTool(MCPTool):
    def __init__(self):
        super().__init__()
        self.base_url = "https://data.messari.io/api/v1"
    
    @property
    def name(self) -> str:
        return "messari"
    
    @property
    def description(self) -> str:
        return "Access on-chain metrics and research data from Messari API"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_asset_metrics",
                        "get_asset_profile",
                        "get_asset_market_data",
                        "get_asset_timeseries",
                        "get_all_assets",
                        "get_news",
                        "get_asset_news",
                        "get_asset_events",
                        "get_asset_governance",
                        "get_asset_research",
                        "get_token_unlocks",
                        "get_governance_proposals",
                        "get_market_data",
                        "get_asset_screener"
                    ],
                    "description": "The action to perform"
                },
                "asset_key": {
                    "type": "string",
                    "description": "Asset key (e.g., btc, eth)",
                    "default": "btc"
                },
                "metric_id": {
                    "type": "string",
                    "description": "Metric ID for timeseries data",
                    "default": "price"
                },
                "start": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD)",
                    "default": "2024-01-01"
                },
                "end": {
                    "type": "string",
                    "description": "End date (YYYY-MM-DD)",
                    "default": "2024-01-15"
                },
                "api_key": {
                    "type": "string",
                    "description": "Messari API key (required for most endpoints)",
                    "default": ""
                },
                "limit": {
                    "type": "integer",
                    "description": "Limit number of results (for get_all_assets)",
                    "default": 100
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        
        try:
            if action == "get_asset_metrics":
                return await self._get_asset_metrics(arguments)
            elif action == "get_asset_profile":
                return await self._get_asset_profile(arguments)
            elif action == "get_asset_market_data":
                return await self._get_asset_market_data(arguments)
            elif action == "get_asset_timeseries":
                return await self._get_asset_timeseries(arguments)
            elif action == "get_all_assets":
                return await self._get_all_assets(arguments)
            elif action == "get_news":
                return await self._get_news(arguments)
            elif action == "get_asset_news":
                return await self._get_asset_news(arguments)
            elif action == "get_asset_events":
                return await self._get_asset_events(arguments)
            elif action == "get_asset_governance":
                return await self._get_asset_governance(arguments)
            elif action == "get_asset_research":
                return await self._get_asset_research(arguments)
            elif action == "get_token_unlocks":
                return await self._get_token_unlocks(arguments)
            elif action == "get_governance_proposals":
                return await self._get_governance_proposals(arguments)
            elif action == "get_market_data":
                return await self._get_market_data(arguments)
            elif action == "get_asset_screener":
                return await self._get_asset_screener(arguments)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Messari API error: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    def _get_valid_api_key(self, api_key: str) -> str:
        """Get valid API key or None if empty/invalid"""
        return api_key if api_key and api_key.strip() else None

    async def _make_request(self, endpoint: str, params: Dict[str, Any] = None, api_key: str = None) -> Dict[str, Any]:
        """Make API request to Messari"""
        url = f"{self.base_url}{endpoint}"
        session = await self._get_session()
        
        headers = {}
        valid_api_key = self._get_valid_api_key(api_key)
        if valid_api_key:
            headers['x-messari-api-key'] = valid_api_key
            
        try:
            async with session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Messari API request failed: {e}")
            return {"error": f"Messari API request failed: {e}"}
    
    async def _get_asset_metrics(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset metrics"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/metrics", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Metrics for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset metrics: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset metrics: {str(e)}"}]
    
    async def _get_asset_profile(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset profile"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/profile", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Profile for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset profile: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset profile: {str(e)}"}]
    
    async def _get_asset_market_data(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset market data"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/metrics/market-data", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Market Data for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset market data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset market data: {str(e)}"}]
    
    async def _get_asset_timeseries(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset timeseries data"""
        asset_key = args.get("asset_key", "btc")
        metric_id = args.get("metric_id", "price")
        start = args.get("start", "2024-01-01")
        end = args.get("end", "2024-01-15")
        api_key = args.get("api_key")
        
        try:
            params = {
                "metric_id": metric_id,
                "start": start,
                "end": end
            }
            data = await self._make_request(f"/assets/{asset_key}/metrics/{metric_id}/time-series", params, api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Timeseries for {asset_key.upper()} ({metric_id}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset timeseries: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset timeseries: {str(e)}"}]
    
    async def _get_all_assets(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all assets"""
        api_key = args.get("api_key")
        limit = args.get("limit", 100)
        
        try:
            # Add limit as query parameter
            params = {"limit": limit} if limit else {}
            data = await self._make_request("/assets", api_key=api_key, params=params)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari All Assets (limit: {limit}):\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching all assets: {e}")
            return [{"type": "text", "text": f"❌ Error fetching all assets: {str(e)}"}]
    
    async def _get_news(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get news"""
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request("/news", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari News:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return [{"type": "text", "text": f"❌ Error fetching news: {str(e)}"}]
    
    async def _get_asset_news(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset news"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/news/{asset_key}", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset News for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset news: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset news: {str(e)}"}]

    async def _get_asset_events(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset events"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/events", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Events for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset events: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset events: {str(e)}"}]

    async def _get_asset_governance(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset governance data"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/governance", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Governance for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset governance: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset governance: {str(e)}"}]

    async def _get_asset_research(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset research reports"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/research", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Research for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset research: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset research: {str(e)}"}]

    async def _get_token_unlocks(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get token unlock data"""
        asset_key = args.get("asset_key", "btc")
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request(f"/assets/{asset_key}/token-unlocks", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Token Unlocks for {asset_key.upper()}:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching token unlocks: {e}")
            return [{"type": "text", "text": f"❌ Error fetching token unlocks: {str(e)}"}]

    async def _get_governance_proposals(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get governance proposals"""
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request("/governance/proposals", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Governance Proposals:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching governance proposals: {e}")
            return [{"type": "text", "text": f"❌ Error fetching governance proposals: {str(e)}"}]

    async def _get_market_data(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get market data"""
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request("/market-data", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Market Data:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching market data: {e}")
            return [{"type": "text", "text": f"❌ Error fetching market data: {str(e)}"}]

    async def _get_asset_screener(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get asset screener data"""
        api_key = args.get("api_key")
        
        try:
            data = await self._make_request("/asset-screener", api_key=api_key)
            if "error" in data:
                return [{"type": "text", "text": f"❌ Error: {data['error']}"}]
            
            return [{"type": "text", "text": f"✅ Messari Asset Screener:\n\n{data}"}]
        except Exception as e:
            logger.error(f"Error fetching asset screener: {e}")
            return [{"type": "text", "text": f"❌ Error fetching asset screener: {str(e)}"}]