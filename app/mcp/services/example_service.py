import logging
from typing import Any, Dict, List
from .base_service import BaseMCPService

logger = logging.getLogger(__name__)

class ExampleService(BaseMCPService):
    """Example MCP service template for demonstration"""
    
    def __init__(self):
        super().__init__()
        self.service_name = "Example Service"
        self.service_description = "A template service showing how to create new MCP services"
        self.base_url = "http://localhost:3010"
    
    async def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools for this service"""
        return [
            {
                "name": "example_hello",
                "description": "A simple hello world tool",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name to greet",
                            "default": "World"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "example_calculate",
                "description": "Perform basic mathematical calculations",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "Mathematical operation",
                            "enum": ["add", "subtract", "multiply", "divide"]
                        },
                        "a": {
                            "type": "number",
                            "description": "First number"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number"
                        }
                    },
                    "required": ["operation", "a", "b"]
                }
            },
            {
                "name": "example_info",
                "description": "Get information about this service",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        ]
    
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool with given arguments"""
        try:
            if tool_name == "example_hello":
                return await self._hello_world(arguments)
            elif tool_name == "example_calculate":
                return await self._calculate(arguments)
            elif tool_name == "example_info":
                return await self._get_info()
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def _hello_world(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Hello world tool implementation"""
        name = arguments.get("name", "World")
        return {
            "message": f"Hello, {name}!",
            "timestamp": "2024-01-01T00:00:00Z",
            "service": self.service_name
        }
    
    async def _calculate(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate tool implementation"""
        operation = arguments.get("operation")
        a = arguments.get("a")
        b = arguments.get("b")
        
        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {"error": "Division by zero"}
            result = a / b
        else:
            return {"error": f"Unknown operation: {operation}"}
        
        return {
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
            "service": self.service_name
        }
    
    async def _get_info(self) -> Dict[str, Any]:
        """Get service information"""
        return {
            "service_name": self.service_name,
            "description": self.service_description,
            "base_url": self.base_url,
            "tools_available": len(await self.get_tools()),
            "status": "active",
            "version": "1.0.0"
        }
