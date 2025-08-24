import os
from typing import Optional, List
from pydantic import BaseModel

class MCPServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 3000
    debug: bool = False
    
    server_name: str = "OLAXBT MCP Server"
    server_version: str = "2.0.0"
    
    default_search_region: str = "us-en"
    max_search_results: int = 20
    search_timeout: int = 30
    
    log_level: str = "INFO"
    log_file: Optional[str] = "logs/mcp_server.log"
    
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    
    @classmethod
    def from_env(cls) -> "MCPServerConfig":
        return cls(
            host=os.getenv("MCP_HOST", "0.0.0.0"),
            port=int(os.getenv("MCP_PORT", "3000")),
            debug=os.getenv("MCP_DEBUG", "false").lower() == "true",
            server_name=os.getenv("MCP_SERVER_NAME", "OLAXBT MCP Server"),
            server_version=os.getenv("MCP_SERVER_VERSION", "2.0.0"),
            default_search_region=os.getenv("MCP_DEFAULT_SEARCH_REGION", "us-en"),
            max_search_results=int(os.getenv("MCP_MAX_SEARCH_RESULTS", "20")),
            search_timeout=int(os.getenv("MCP_SEARCH_TIMEOUT", "30")),
            log_level=os.getenv("MCP_LOG_LEVEL", "INFO"),
            log_file=os.getenv("MCP_LOG_FILE", "logs/mcp_server.log"),
        )

config = MCPServerConfig.from_env()
