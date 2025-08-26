"""
Tool Validation and Error Handling Utilities
Provides systematic validation and error handling for all MCP tools
"""

import logging
from typing import Dict, Any, List, Optional
from functools import wraps

logger = logging.getLogger(__name__)

class ToolValidator:
    """Validates tool parameters and provides consistent error handling"""
    
    @staticmethod
    def validate_required_params(params: Dict[str, Any], required: List[str], tool_name: str) -> Optional[str]:
        """Validate that all required parameters are present"""
        missing = [param for param in required if param not in params or params[param] is None or params[param] == ""]
        if missing:
            return f"Missing required parameters for {tool_name}: {', '.join(missing)}"
        return None
    
    @staticmethod
    def validate_param_types(params: Dict[str, Any], schema: Dict[str, Any], tool_name: str) -> Optional[str]:
        """Validate parameter types according to schema"""
        for param_name, param_value in params.items():
            if param_name in schema.get("properties", {}):
                expected_type = schema["properties"][param_name].get("type")
                if expected_type == "integer" and not isinstance(param_value, int):
                    try:
                        params[param_name] = int(param_value)
                    except (ValueError, TypeError):
                        return f"Parameter '{param_name}' must be an integer for {tool_name}"
                elif expected_type == "number" and not isinstance(param_value, (int, float)):
                    try:
                        params[param_name] = float(param_value)
                    except (ValueError, TypeError):
                        return f"Parameter '{param_name}' must be a number for {tool_name}"
                elif expected_type == "boolean" and not isinstance(param_value, bool):
                    if isinstance(param_value, str):
                        if param_value.lower() in ["true", "1", "yes"]:
                            params[param_name] = True
                        elif param_value.lower() in ["false", "0", "no"]:
                            params[param_name] = False
                        else:
                            return f"Parameter '{param_name}' must be a boolean for {tool_name}"
        return None
    
    @staticmethod
    def sanitize_params(params: Dict[str, Any], tool_name: str) -> Dict[str, Any]:
        """Sanitize and normalize parameters"""
        sanitized = {}
        for key, value in params.items():
            if isinstance(value, str):
                # Trim whitespace and convert empty strings to None
                sanitized[key] = value.strip() if value.strip() else None
            else:
                sanitized[key] = value
        return sanitized

def handle_tool_errors(func):
    """Decorator for consistent error handling across all tools"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return [{"error": f"Tool execution failed: {str(e)}"}]
    return wrapper

def validate_tool_params(required_params: List[str], schema: Dict[str, Any] = None):
    """Decorator for parameter validation"""
    def decorator(func):
        @wraps(func)
        async def wrapper(self, arguments: Dict[str, Any], *args, **kwargs):
            try:
                # Sanitize parameters
                arguments = ToolValidator.sanitize_params(arguments, func.__name__)
                
                # Validate required parameters
                missing_error = ToolValidator.validate_required_params(arguments, required_params, func.__name__)
                if missing_error:
                    return [{"error": missing_error}]
                
                # Validate parameter types if schema provided
                if schema:
                    type_error = ToolValidator.validate_param_types(arguments, schema, func.__name__)
                    if type_error:
                        return [{"error": type_error}]
                
                # Execute the tool
                return await func(self, arguments, *args, **kwargs)
                
            except Exception as e:
                logger.error(f"Parameter validation error in {func.__name__}: {e}")
                return [{"error": f"Parameter validation failed: {str(e)}"}]
        return wrapper
    return decorator

# Common parameter schemas for different tool types
SEARCH_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {"type": "string"},
        "max_results": {"type": "integer"},
        "time_filter": {"type": "string"},
        "include_sentiment": {"type": "boolean"}
    }
}

CRYPTO_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "coin_id": {"type": "string"},
        "currency": {"type": "string"},
        "include_market_data": {"type": "boolean"}
    }
}

PORTFOLIO_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "portfolio_id": {"type": "string"},
        "name": {"type": "string"},
        "coin_id": {"type": "string"},
        "amount": {"type": "number"},
        "purchase_price": {"type": "number"}
    }
}
