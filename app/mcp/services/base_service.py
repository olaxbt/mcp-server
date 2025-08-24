import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class BaseMCPService(ABC):
    def __init__(self):
        self.service_name: str = ""
        self.service_description: str = ""
        self.base_url: str = ""
        self.tools: List[Dict[str, Any]] = []
        
    @abstractmethod
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools for this service"""
        pass
    
    @abstractmethod
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool with given arguments"""
        pass
    
    async def get_service_info(self) -> Dict[str, Any]:
        """Get service metadata and information"""
        return {
            "name": self.service_name,
            "description": self.service_description,
            "base_url": self.base_url,
            "tools_count": len(await self.get_tools()),
            "status": "active"
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Check service health status"""
        try:
            tools = await self.get_tools()
            return {
                "status": "healthy",
                "tools_available": len(tools),
                "service_name": self.service_name
            }
        except Exception as e:
            logger.error(f"Health check failed for {self.service_name}: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "service_name": self.service_name
            }
    
    def get_tool_schema(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get input schema for a specific tool"""
        tools = asyncio.run(self.get_tools())
        for tool in tools:
            if tool["name"] == tool_name:
                return tool.get("input_schema")
        return None
    
    async def list_tool_names(self) -> List[str]:
        """Get list of tool names available in this service"""
        tools = await self.get_tools()
        return [tool["name"] for tool in tools]
    
    async def validate_arguments(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tool arguments against schema"""
        schema = self.get_tool_schema(tool_name)
        if not schema:
            return {"valid": False, "error": f"Tool '{tool_name}' not found"}
        
        required_fields = schema.get("required", [])
        missing_fields = [field for field in required_fields if field not in arguments]
        
        if missing_fields:
            return {
                "valid": False, 
                "error": f"Missing required fields: {missing_fields}",
                "required": required_fields
            }
        
        return {"valid": True, "arguments": arguments}
