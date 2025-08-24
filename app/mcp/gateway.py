import logging
from typing import Any, Dict, List
import aiohttp

logger = logging.getLogger(__name__)

class MCPGateway:
    def __init__(self):
        self.servers = {}
        self.tool_routing = {}
        self.server_health = {}
        
    async def register_server(self, server_id: str, server_info: Dict[str, Any]) -> bool:
        try:
            server = {
                "id": server_id,
                "name": server_info.get("name", server_id),
                "description": server_info.get("description", ""),
                "url": server_info.get("url", ""),
                "status": "online",
                "tools": server_info.get("tools", []),
                "metadata": server_info.get("metadata", {})
            }
            
            self.servers[server_id] = server
            self.server_health[server_id] = True
            
            for tool in server["tools"]:
                self.tool_routing[tool] = server_id
                
            logger.info(f"Registered server: {server_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register server {server_id}: {e}")
            return False
    
    async def unregister_server(self, server_id: str) -> bool:
        if server_id in self.servers:
            server = self.servers[server_id]
            for tool in server["tools"]:
                self.tool_routing.pop(tool, None)
            
            del self.servers[server_id]
            del self.server_health[server_id]
            return True
        return False
    
    async def get_server_status(self, server_id: str):
        if server_id not in self.servers:
            return None
            
        try:
            server = self.servers[server_id]
            async with aiohttp.ClientSession() as session:
                # Try to get server info or health check
                health_url = f"{server['url']}/health"
                try:
                    async with session.get(health_url, timeout=5) as response:
                        if response.status == 200:
                            self.server_health[server_id] = True
                            return "online"
                        else:
                            self.server_health[server_id] = False
                            return "error"
                except:
                    # If health endpoint doesn't exist, try to list tools
                    tools_url = f"{server['url']}/mcp/tools/list"
                    try:
                        async with session.post(tools_url, json={
                            "jsonrpc": "2.0",
                            "id": "health_check",
                            "method": "tools/list"
                        }, timeout=5) as response:
                            if response.status == 200:
                                self.server_health[server_id] = True
                                return "online"
                            else:
                                self.server_health[server_id] = False
                                return "error"
                    except:
                        self.server_health[server_id] = False
                        return "offline"
                        
        except Exception as e:
            logger.error(f"Health check failed for {server_id}: {e}")
            self.server_health[server_id] = False
            return "offline"
    
    async def list_all_tools(self) -> List[Dict[str, Any]]:
        all_tools = []
        for server_id, server in self.servers.items():
            if self.server_health.get(server_id, False):
                for tool in server["tools"]:
                    all_tools.append({
                        "name": tool,
                        "server_id": server_id,
                        "server_name": server["name"],
                        "description": f"Tool from {server['name']}"
                    })
        return all_tools
    
    async def route_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name not in self.tool_routing:
            return {"error": f"Tool '{tool_name}' not found"}
            
        server_id = self.tool_routing[tool_name]
        if not self.server_health.get(server_id, False):
            return {"error": f"Server for tool '{tool_name}' is offline"}
            
        server = self.servers[server_id]
        
        try:
            async with aiohttp.ClientSession() as session:
                # Use MCP protocol format
                payload = {
                    "jsonrpc": "2.0",
                    "id": "gateway_call",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    }
                }
                
                # Try MCP endpoint first
                mcp_url = f"{server['url']}/mcp/tools/call"
                try:
                    async with session.post(
                        mcp_url,
                        json=payload,
                        timeout=30
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            return result.get("result", {"error": "No result from server"})
                        else:
                            # Fallback to legacy endpoint
                            pass
                except:
                    pass
                
                # Fallback to legacy endpoint
                legacy_url = f"{server['url']}/tools/call"
                async with session.post(
                    legacy_url,
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("result", {"error": "No result from server"})
                    else:
                        return {"error": f"Server error: {response.status}"}
                        
        except Exception as e:
            logger.error(f"Tool call failed for {tool_name}: {e}")
            return {"error": f"Tool call failed: {str(e)}"}
    
    async def list_servers(self) -> List[Dict[str, Any]]:
        server_list = []
        for server_id, server in self.servers.items():
            status = await self.get_server_status(server_id)
            server_list.append({
                "id": server_id,
                "name": server["name"],
                "description": server["description"],
                "url": server["url"],
                "status": status or "unknown",
                "tools": server["tools"],
                "metadata": server["metadata"]
            })
        return server_list
