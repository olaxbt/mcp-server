import logging
from typing import Any, Dict, List, Optional
from fastapi.responses import JSONResponse

from .service_registry import ServiceRegistry
from .utils.tool_registry import ToolRegistry
from .tool_configs.tool_config import get_tool_config, get_tool_required_params, get_tool_schema
from .tools import (
    DuckDuckGoSearchTool,
    WebSearchTool,
    CryptoPriceTool,
    DeFiProtocolTool,
    PortfolioTrackerTool,
    CryptoNewsTool,
    NFTMarketplaceTool,
    MarketAnalysisTool,
    NotificationTool,
    APYCalculatorTool,
    JupiterTool,
    RaydiumTool,
    LunarCrushTool,
    CoinDeskTool,
    AaveTool,
    PumpNewsTool,
    PumpFunTool,
    GMGNTool,
    MerklTool,
    YouTubeTool,
    GmailTool,
    GoogleCalendarTool,
    TwitterTool,
    RedditTool,
    OpenWeatherTool,
    GoogleMapsTool,
    JiraTool,
    SlackTool,
    CurrencyConverterTool
)

logger = logging.getLogger(__name__)

class MCPRouter:
    """Handles MCP protocol routing and request processing"""
    
    def __init__(self, service_registry: ServiceRegistry):
        self.registry = service_registry
        self.tool_registry = ToolRegistry()
        
        # Initialize tools
        self.local_tools = {
            "duckduckgo_search": DuckDuckGoSearchTool(),
            "web_search": WebSearchTool(),
            "crypto_price": CryptoPriceTool(),
            "defi_protocol": DeFiProtocolTool(),
            "portfolio_tracker": PortfolioTrackerTool(),
            "crypto_news": CryptoNewsTool(),
            "nft_marketplace": NFTMarketplaceTool(),
            "market_analysis": MarketAnalysisTool(),
            "notification": NotificationTool(),
            "apy_calculator": APYCalculatorTool(),
            "jupiter": JupiterTool(),
            "raydium": RaydiumTool(),
            "lunarcrush": LunarCrushTool(),
            "coindesk": CoinDeskTool(),
            "aave": AaveTool(),
            "pumpnews": PumpNewsTool(),
            "pumpfun": PumpFunTool(),
            "gmgn": GMGNTool(),
            "merkl": MerklTool(),
            "youtube": YouTubeTool(),
            "gmail": GmailTool(),
            "google_calendar": GoogleCalendarTool(),
            "twitter": TwitterTool(),
            "reddit": RedditTool(),
            "openweather": OpenWeatherTool(),
            "googlemaps": GoogleMapsTool(),
            "jira": JiraTool(),
            "slack": SlackTool(),
            "currency_converter": CurrencyConverterTool()
        }
        
        # Register all tools with validation rules
        self._register_all_tools()
    
    def _register_all_tools(self):
        """Register all tools with the tool registry for validation and formatting"""
        for tool_name, tool_instance in self.local_tools.items():
            config = get_tool_config(tool_name)
            required_params = config.get("required_params", [])
            schema = config.get("schema", {})
            
            self.tool_registry.register_tool(
                tool_name=tool_name,
                tool_instance=tool_instance,
                required_params=required_params,
                schema=schema
            )
            logger.info(f"Registered tool: {tool_name} with validation rules")
    
    def format_tool_result_for_mcp(self, result: List[Dict[str, Any]], tool_name: str) -> Dict[str, Any]:
        """Format tool results using the new systematic tool registry"""
        try:
            return self.tool_registry._format_tool_response(tool_name, result)
        except Exception as e:
            logger.error(f"Error formatting tool result for {tool_name}: {e}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"❌ Error formatting results for {tool_name}: {str(e)}"
                    }
                ]
            }
    
    async def handle_initialize(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize MCP request"""
        try:
            logger.info(f"Starting initialize handler for message: {message}")
            
            params = message.get("params", {})
            client_name = params.get("clientInfo", {}).get("name", "Unknown Client")
            client_version = params.get("clientInfo", {}).get("version", "1.0.0")
            
            logger.info(f"MCP Client initialized: {client_name} v{client_version}")
            
            response = {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                        "resources": {},
                        "prompts": {}
                    },
                    "serverInfo": {
                        "name": "OlaXBT MCP Server",
                        "version": "1.0.0"
                    }
                }
            }
            
            logger.info(f"Initialize response prepared: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error in handle_initialize: {e}")
            error_response = {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "internal_error",
                    "message": str(e)
                }
            }
            logger.error(f"Initialize error response: {error_response}")
            return error_response
    
    async def handle_list_tools(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list MCP request"""
        try:
            tools = await self.registry.list_all_tools()
            local_tools = []
            
            for tool_name, tool in self.local_tools.items():
                local_tools.append({
                    "name": tool_name,
                    "description": tool.description,
                    "inputSchema": tool.input_schema
                })
            
            all_tools = tools + local_tools
            
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {"tools": all_tools}
            }
        except Exception as e:
            logger.error(f"Error in handle_list_tools: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "internal_error",
                    "message": str(e)
                }
            }
    
    async def handle_call_tool(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call MCP request"""
        try:
            params = message.get("params", {})
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                return {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "error": {
                        "code": "invalid_params",
                        "message": "Tool name is required"
                    }
                }
            
            # Check if it's a local tool
            if tool_name in self.local_tools:
                tool = self.local_tools[tool_name]
                result = await tool.execute(arguments)
                formatted_result = self.format_tool_result_for_mcp(result, tool_name)
                return {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": formatted_result
                }
            
            # Route to registry for remote tools
            try:
                result = await self.registry.route_tool_call(tool_name, arguments)
                formatted_result = self.format_tool_result_for_mcp(result, tool_name)
                return {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": formatted_result
                }
            except ValueError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "error": {
                        "code": "tool_not_found",
                        "message": str(e)
                    }
                }
            
        except Exception as e:
            logger.error(f"Error in handle_call_tool: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "tool_execution_error",
                    "message": str(e)
                }
            }
    
    async def handle_list_services(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle services/list MCP request"""
        try:
            services = await self.registry.list_services()
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {"services": services}
            }
        except Exception as e:
            logger.error(f"Error in handle_list_services: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "internal_error",
                    "message": str(e)
                }
            }
    
    async def handle_list_prompts(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle prompts/list MCP request"""
        try:
            # For now, return an empty list since we don't have prompts yet
            # You can add prompts later if needed
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {"prompts": []}
            }
        except Exception as e:
            logger.error(f"Error in handle_list_prompts: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "internal_error",
                    "message": str(e)
                }
            }
    
    async def handle_cancel_notification(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle notifications/cancel MCP request"""
        try:
            # For now, just acknowledge the cancellation
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {"cancelled": True}
            }
        except Exception as e:
            logger.error(f"Error in handle_cancel_notification: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "internal_error",
                    "message": str(e)
                }
            }
    
    async def handle_initialized_notification(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle notifications/initialized MCP request"""
        try:
            logger.info("MCP Client initialization completed")
            
            # For notifications, we don't need to return a result
            # Just acknowledge receipt
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "result": {"initialized": True}
            }
        except Exception as e:
            logger.error(f"Error in handle_initialized_notification: {e}")
            return {
                "jsonrpc": "2.0",
                "id": message.get("id"),
                "error": {
                    "code": "internal_error",
                    "message": str(e)
                }
            }
    
    async def route_mcp_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Route MCP requests to appropriate handlers"""
        method = message.get("method")
        request_id = message.get("id")
        
        logger.info(f"MCP Request received: {method} (ID: {request_id})")
        
        # Route to appropriate handler
        if method == "initialize":
            response = await self.handle_initialize(message)
        elif method == "tools/list":
            response = await self.handle_list_tools(message)
        elif method == "tools/call":
            response = await self.handle_call_tool(message)
        elif method == "services/list":
            response = await self.handle_list_services(message)
        elif method == "prompts/list":
            response = await self.handle_list_prompts(message)
        elif method == "notifications/cancel":
            response = await self.handle_cancel_notification(message)
        elif method == "notifications/initialized":
            response = await self.handle_initialized_notification(message)
        else:
            logger.warning(f"Unknown MCP method: {method}")
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": "method_not_found",
                    "message": f"Unknown method: {method}"
                }
            }
        
        logger.info(f"MCP Response sent: {response}")
        return response
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status of the router and services"""
        try:
            # Get service statistics
            service_stats = await self.registry.get_service_statistics()
            
            # Check local tools
            local_tools_status = {}
            for tool_name, tool in self.local_tools.items():
                try:
                    # Simple health check for local tools
                    local_tools_status[tool_name] = "healthy"
                except Exception as e:
                    local_tools_status[tool_name] = f"unhealthy: {str(e)}"
            
            return {
                "status": "healthy",
                "router": "operational",
                "local_tools": local_tools_status,
                "services": service_stats,
                "total_tools": service_stats.get("total_tools", 0) + len(self.local_tools)
            }
            
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
