"""
Tool Registry and Response Formatter
Automatically handles validation, error handling, and response formatting for all MCP tools
"""

import logging
from typing import Dict, Any, List, Optional
from .tool_validator import ToolValidator, handle_tool_errors, validate_tool_params

logger = logging.getLogger(__name__)

class ToolRegistry:
    """Central registry for all MCP tools with automatic validation and formatting"""
    
    def __init__(self):
        self.tools = {}
        self.response_formatters = {}
        self._register_default_formatters()
    
    def register_tool(self, tool_name: str, tool_instance, required_params: List[str] = None, schema: Dict[str, Any] = None):
        """Register a tool with validation rules"""
        self.tools[tool_name] = {
            "instance": tool_instance,
            "required_params": required_params or [],
            "schema": schema or {},
            "validator": ToolValidator()
        }
        logger.info(f"Registered tool: {tool_name}")
    
    def _register_default_formatters(self):
        """Register default response formatters for different tool types"""
        # Crypto tools
        self.response_formatters.update({
            "crypto_price": self._format_crypto_price,
            "crypto_news": self._format_crypto_news,
            "market_analysis": self._format_market_analysis,
            "portfolio_tracker": self._format_portfolio_tracker,
            "defi_protocol": self._format_defi_protocol,
            "apy_calculator": self._format_apy_calculator,
            "nft_marketplace": self._format_nft_marketplace,
            "jupiter": self._format_jupiter,
            "raydium": self._format_raydium,
            "aave": self._format_aave,
            "lunarcrush": self._format_lunarcrush,
            "coindesk": self._format_coindesk,
            "pumpnews": self._format_pumpnews,
            "pumpfun": self._format_pumpfun,
            "gmgn": self._format_gmgn,
            "merkl": self._format_merkl,
        })
        
        # Search tools
        self.response_formatters.update({
            "duckduckgo_search": self._format_search_results,
            "web_search": self._format_search_results,
        })
        
        # Social tools
        self.response_formatters.update({
            "youtube": self._format_social_results,
            "twitter": self._format_social_results,
            "reddit": self._format_social_results,
        })
        
        # Communication tools
        self.response_formatters.update({
            "gmail": self._format_communication_results,
            "google_calendar": self._format_communication_results,
            "slack": self._format_communication_results,
        })
        
        # Utility tools
        self.response_formatters.update({
            "openweather": self._format_weather_results,
            "googlemaps": self._format_maps_results,
            "jira": self._format_jira_results,
            "currency_converter": self._format_currency_results,
            "notification": self._format_notification_results,
        })
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with automatic validation and formatting"""
        try:
            if tool_name not in self.tools:
                return self._format_error(f"Tool '{tool_name}' not found")
            
            tool_info = self.tools[tool_name]
            tool_instance = tool_info["instance"]
            
            # Validate parameters
            validation_error = self._validate_tool_params(tool_name, arguments, tool_info)
            if validation_error:
                return self._format_error(validation_error)
            
            # Execute tool
            result = await tool_instance.execute(arguments)
            
            # Format response
            return self._format_tool_response(tool_name, result)
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return self._format_error(f"Tool execution failed: {str(e)}")
    
    def _validate_tool_params(self, tool_name: str, arguments: Dict[str, Any], tool_info: Dict[str, Any]) -> Optional[str]:
        """Validate tool parameters"""
        validator = tool_info["validator"]
        required_params = tool_info["required_params"]
        schema = tool_info["schema"]
        
        # Sanitize parameters
        arguments = validator.sanitize_params(arguments, tool_name)
        
        # Check required parameters
        missing_error = validator.validate_required_params(arguments, required_params, tool_name)
        if missing_error:
            return missing_error
        
        # Validate parameter types
        if schema:
            type_error = validator.validate_param_types(arguments, schema, tool_name)
            if type_error:
                return type_error
        
        return None
    
    def _format_tool_response(self, tool_name: str, result: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Format tool response using appropriate formatter"""
        try:
            if not result:
                return self._format_error(f"No results found for {tool_name}")
            
            # Check for errors in result
            if any("error" in item for item in result):
                error_items = [item for item in result if "error" in item]
                return self._format_error(f"Tool execution errors: {', '.join(item['error'] for item in error_items)}")
            
            # Use specific formatter if available
            if tool_name in self.response_formatters:
                formatter = self.response_formatters[tool_name]
                formatted_text = formatter(result, tool_name)
            else:
                # Use generic formatter
                formatted_text = self._format_generic_results(result, tool_name)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": formatted_text
                    }
                ]
            }
            
        except Exception as e:
            logger.error(f"Error formatting response for {tool_name}: {e}")
            return self._format_error(f"Response formatting failed: {str(e)}")
    
    def _format_error(self, error_message: str) -> Dict[str, Any]:
        """Format error messages consistently"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"❌ Error: {error_message}"
                }
            ]
        }
    
    # Specific formatters for different tool types
    def _format_crypto_price(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        """Format cryptocurrency price data"""
        formatted_text = f"Cryptocurrency Price Data:\n\n"
        for i, item in enumerate(result, 1):
            formatted_text += f"{i}. **{item.get('coin_id', 'Unknown').title()}**\n"
            formatted_text += f"   Price: ${item.get('price', 'N/A'):,}\n"
            formatted_text += f"   Currency: {item.get('currency', 'N/A').upper()}\n"
            if item.get('include_market_data'):
                formatted_text += f"   Market Cap: ${item.get('market_cap', 'N/A'):,}\n"
                formatted_text += f"   24h Volume: ${item.get('volume_24h', 'N/A'):,}\n"
                formatted_text += f"   24h Change: {item.get('change_24h', 'N/A')}%\n"
            formatted_text += f"   Last Updated: {item.get('last_updated', 'N/A')}\n\n"
        return formatted_text.strip()
    
    def _format_crypto_news(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        """Format cryptocurrency news results"""
        formatted_text = f"Cryptocurrency News:\n\n"
        for i, item in enumerate(result, 1):
            formatted_text += f"{i}. **{item.get('title', 'No title')}**\n"
            formatted_text += f"   Source: {item.get('source', 'Unknown source')}\n"
            formatted_text += f"   Published: {item.get('published_date', 'Unknown date')}\n"
            formatted_text += f"   Summary: {item.get('snippet', 'No description')}\n"
            if item.get('sentiment'):
                formatted_text += f"   Sentiment: {item.get('sentiment', 'Unknown')}\n"
            formatted_text += "\n"
        return formatted_text.strip()
    
    def _format_search_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        """Format search results"""
        formatted_text = f"Search Results:\n\n"
        for i, item in enumerate(result, 1):
            formatted_text += f"{i}. **{item.get('title', 'No title')}**\n"
            formatted_text += f"   URL: {item.get('link', 'No link')}\n"
            formatted_text += f"   Source: {item.get('source', 'Unknown source')}\n"
            formatted_text += f"   Description: {item.get('snippet', 'No description')}\n\n"
        return formatted_text.strip()
    
    def _format_generic_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        """Generic formatter for other tools"""
        formatted_text = f"Results for {tool_name}:\n\n"
        for i, item in enumerate(result, 1):
            if isinstance(item, dict):
                for key, value in item.items():
                    if key != "error":
                        formatted_text += f"   {key.replace('_', ' ').title()}: {value}\n"
                formatted_text += "\n"
            else:
                formatted_text += f"{i}. {str(item)}\n\n"
        return formatted_text.strip()
    
    # Add other specific formatters as needed...
    def _format_market_analysis(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_portfolio_tracker(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_defi_protocol(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_apy_calculator(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_nft_marketplace(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_jupiter(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_raydium(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_aave(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_lunarcrush(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_coindesk(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_pumpnews(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_pumpfun(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_gmgn(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_merkl(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_social_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_communication_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_weather_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_maps_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_jira_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_currency_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
    
    def _format_notification_results(self, result: List[Dict[str, Any]], tool_name: str) -> str:
        return self._format_generic_results(result, tool_name)
