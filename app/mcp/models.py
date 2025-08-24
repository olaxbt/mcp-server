from typing import Any, Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field

class MCPRequest(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[Union[str, int]] = None
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[Union[str, int]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPError(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: Optional[Union[str, int]] = None
    error: Dict[str, Any] = Field(
        description="Error object containing code and message"
    )
    
    def dict(self, **kwargs):
        return {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
            "error": self.error
        }

class MCPToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]

class MCPToolResult(BaseModel):
    content: List[Dict[str, Any]]

class MCPListToolsRequest(MCPRequest):
    method: Literal["tools/list"] = "tools/list"

class MCPListToolsResponse(MCPResponse):
    result: Dict[str, List[Dict[str, Any]]] = Field(
        description="List of available tools"
    )
    
    def dict(self, **kwargs):
        return {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
            "result": self.result
        }

class MCPCallToolRequest(MCPRequest):
    method: Literal["tools/call"] = "tools/call"
    params: Dict[str, Any] = Field(
        description="Tool call parameters including name and arguments"
    )

class MCPCallToolResponse(MCPResponse):
    result: MCPToolResult
    
    def dict(self, **kwargs):
        return {
            "jsonrpc": self.jsonrpc,
            "id": self.id,
            "result": self.result.dict()
        }
