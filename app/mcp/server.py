import asyncio
import logging
from typing import Any, Dict, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .service_manager import ServiceManager
from .router import MCPRouter
from .config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServer:
    def __init__(self):
        self.app = FastAPI(
            title=config.server_name,
            description="Modern MCP Server with Modular Service Architecture",
            version=config.server_version
        )
        
        # Initialize core components
        self.service_manager = ServiceManager()
        self.router = MCPRouter(self.service_manager.registry)
        
        self.setup_middleware()
        self.setup_routes()
    
    def setup_middleware(self):
        """Setup CORS and other middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "https://internal-dev.olaxbt.xyz",
                "https://olaxbt.xyz",
                "https://www.olaxbt.xyz",
                "http://localhost:5173",  # For local development
                "http://localhost:3000",  # For local development
            ],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],
            allow_headers=[
                "Accept",
                "Accept-Language",
                "Content-Language",
                "Content-Type",
                "Authorization",
                "X-Requested-With",
                "Origin",
                "Access-Control-Request-Method",
                "Access-Control-Request-Headers"
            ],
            allow_origin_regex=r"https://.*\.olaxbt\.xyz",  # Allow all subdomains
            expose_headers=["Content-Length", "Content-Type"],
            max_age=86400,  # Cache preflight requests for 24 hours
        )
    
    def setup_routes(self):
        """Setup all API routes"""
        @self.app.on_event("startup")
        async def startup_event():
            await self.setup_services()
        
        @self.app.on_event("shutdown")
        async def shutdown_event():
            await self.service_manager.shutdown()
        
        @self.app.options("/{full_path:path}")
        async def options_handler(full_path: str):
            """Handle CORS preflight requests"""
            return {"message": "CORS preflight handled"}
        
        @self.app.get("/")
        async def root():
            return {
                "message": f"{config.server_name} v{config.server_version}", 
                "status": "running",
                "architecture": "modular"
            }
        
        @self.app.get("/health")
        async def health():
            return await self.router.get_health_status()
        
        @self.app.get("/ping")
        async def ping():
            return {
                "message": "pong",
                "timestamp": asyncio.get_event_loop().time(),
                "status": "ok"
            }
        
        @self.app.get("/services")
        async def list_services():
            return await self.service_manager.get_all_service_statuses()
        
        @self.app.get("/tools")
        async def list_tools():
            all_tools = await self.service_manager.registry.list_all_tools()
            local_tool_names = list(self.router.local_tools.keys())
            return {
                "gateway_tools": all_tools,
                "local_tool_names": local_tool_names,
                "total": len(all_tools) + len(local_tool_names)
            }
        
        @self.app.get("/statistics")
        async def get_statistics():
            """Get detailed statistics about services and tools"""
            return await self.service_manager.get_statistics()
        
        # Service Management Endpoints
        @self.app.post("/services/reload/{service_id}")
        async def reload_service(service_id: str):
            """Reload a specific service"""
            try:
                success = await self.service_manager.registry.reload_service(service_id)
                if success:
                    return {"message": f"Service {service_id} reloaded successfully", "status": "success"}
                else:
                    raise HTTPException(status_code=400, detail=f"Failed to reload service {service_id}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/services/load")
        async def load_services_from_config():
            """Load services from configuration file"""
            try:
                success = await self.service_manager.reload_configuration()
                if success:
                    return {"message": "Services reloaded successfully", "status": "success"}
                else:
                    raise HTTPException(status_code=500, detail="Failed to reload services")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/services/add")
        async def add_service(service_config: Dict[str, Any]):
            """Add a new service dynamically"""
            try:
                service_id = await self.service_manager.add_service(service_config)
                if service_id:
                    return {
                        "message": f"Service {service_id} added successfully",
                        "service_id": service_id,
                        "status": "success"
                    }
                else:
                    raise HTTPException(status_code=400, detail="Failed to add service")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.delete("/services/{service_id}")
        async def remove_service(service_id: str):
            """Remove a service"""
            try:
                success = await self.service_manager.remove_service(service_id)
                if success:
                    return {"message": f"Service {service_id} removed successfully", "status": "success"}
                else:
                    raise HTTPException(status_code=400, detail=f"Failed to remove service {service_id}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/services/{service_id}/enable")
        async def enable_service(service_id: str):
            """Enable a disabled service"""
            try:
                success = await self.service_manager.enable_service(service_id)
                if success:
                    return {"message": f"Service {service_id} enabled successfully", "status": "success"}
                else:
                    raise HTTPException(status_code=400, detail=f"Failed to enable service {service_id}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/services/{service_id}/disable")
        async def disable_service(service_id: str):
            """Disable a service"""
            try:
                success = await self.service_manager.disable_service(service_id)
                if success:
                    return {"message": f"Service {service_id} disabled successfully", "status": "success"}
                else:
                    raise HTTPException(status_code=400, detail=f"Failed to disable service {service_id}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/services/{service_id}/status")
        async def get_service_status(service_id: str):
            """Get detailed status of a specific service"""
            try:
                status = await self.service_manager.get_service_status(service_id)
                if status:
                    return status
                else:
                    raise HTTPException(status_code=404, detail=f"Service {service_id} not found")
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        # Standard MCP Protocol endpoints
        @self.app.post("/mcp")
        async def standard_mcp_post_endpoint(request: Request):
            """Standard MCP endpoint for POST requests"""
            try:
                body = await request.json()
                response = await self.router.route_mcp_request(body)
                return response
            except Exception as e:
                logger.error(f"Error processing MCP request: {e}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "jsonrpc": "2.0",
                        "id": "error",
                        "error": {
                            "code": "internal_error",
                            "message": str(e)
                        }
                    }
                )
        
        @self.app.get("/mcp")
        async def standard_mcp_get_endpoint():
            """Standard MCP endpoint for GET requests (SSE connections)"""
            from fastapi.responses import StreamingResponse
            
            async def event_stream():
                yield "data: {\"type\": \"connected\", \"message\": \"MCP SSE connection established\"}\n\n"
                
                # Keep connection alive
                while True:
                    await asyncio.sleep(30)
                    yield "data: {\"type\": \"ping\", \"timestamp\": \"" + str(asyncio.get_event_loop().time()) + "\"}\n\n"
            
            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        
        # Server-Sent Events endpoint
        @self.app.get("/sse")
        async def sse_endpoint():
            """SSE endpoint for streaming MCP responses"""
            from fastapi.responses import StreamingResponse
            
            async def event_stream():
                yield "data: {\"type\": \"connected\", \"message\": \"SSE connection established\"}\n\n"
                
                # Keep connection alive
                while True:
                    await asyncio.sleep(30)
                    yield "data: {\"type\": \"ping\", \"timestamp\": \"" + str(asyncio.get_event_loop().time()) + "\"}\n\n"
            
            return StreamingResponse(
                event_stream(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Access-Control-Allow-Origin": "*"
                }
            )
        
        # Custom API endpoint (for backward compatibility)
        @self.app.post("/api/mcp/olaxbt-gateway")
        async def custom_mcp_endpoint(request: Request):
            """Custom MCP endpoint for specific clients"""
            try:
                body = await request.json()
                method = body.get("method")
                
                if method == "tools/list":
                    return await self.router.handle_list_tools(body)
                elif method == "tools/call":
                    return await self.router.handle_call_tool(body)
                elif method == "services/list":
                    return await self.router.handle_list_services(body)
                else:
                    return JSONResponse(
                        status_code=400,
                        content={
                            "jsonrpc": "2.0",
                            "id": body.get("id"),
                            "error": {
                                "code": "method_not_found",
                                "message": f"Unknown method: {method}"
                            }
                        }
                    )
            except Exception as e:
                logger.error(f"Error processing MCP request: {e}")
                return JSONResponse(
                    status_code=500,
                    content={
                        "jsonrpc": "2.0",
                        "id": "error",
                        "error": {
                            "code": "internal_error",
                            "message": str(e)
                        }
                    }
                )
        
        # Legacy MCP Protocol endpoints (for backward compatibility)
        @self.app.post("/mcp/tools/list")
        async def mcp_list_tools():
            """MCP Protocol: List all available tools"""
            try:
                tools = await self.service_manager.registry.list_all_tools()
                local_tools = []
                
                for tool_name, tool in self.router.local_tools.items():
                    local_tools.append({
                        "name": tool_name,
                        "description": tool.description,
                        "inputSchema": tool.input_schema
                    })
                
                return {
                    "jsonrpc": "2.0",
                    "id": "tools_list",
                    "result": {"tools": tools + local_tools}
                }
            except Exception as e:
                logger.error(f"Error listing tools: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/mcp/tools/call")
        async def mcp_call_tool(request: Dict[str, Any]):
            """MCP Protocol: Call a specific tool"""
            try:
                method = request.get("method")
                if method != "tools/call":
                    raise HTTPException(status_code=400, detail="Invalid method")
                
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = request.get("arguments", {})
                
                if not tool_name:
                    raise HTTPException(status_code=400, detail="Tool name is required")
                
                # Check if it's a local tool
                if tool_name in self.router.local_tools:
                    tool = self.router.local_tools[tool_name]
                    result = await tool.execute(arguments)
                    formatted_result = self.router.format_tool_result_for_mcp(result, tool_name)
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id", "tool_call"),
                        "result": formatted_result
                    }
                
                # Route to registry for remote tools
                try:
                    result = await self.service_manager.registry.route_tool_call(tool_name, arguments)
                    formatted_result = self.router.format_tool_result_for_mcp(result, tool_name)
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id", "tool_call"),
                        "result": formatted_result
                    }
                except ValueError as e:
                    raise HTTPException(status_code=404, detail=str(e))
                
            except Exception as e:
                logger.error(f"Error calling tool: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/mcp/services/list")
        async def mcp_list_services():
            """MCP Protocol: List all available services"""
            try:
                services = await self.service_manager.registry.list_services()
                return {
                    "jsonrpc": "2.0",
                    "id": "services_list",
                    "result": {"services": services}
                }
            except Exception as e:
                logger.error(f"Error listing services: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def setup_services(self):
        """Setup and load all MCP services"""
        logger.info("Setting up MCP services...")
        
        try:
            # Initialize service manager
            success = await self.service_manager.initialize()
            if success:
                logger.info("Service Manager initialized successfully")
                
                # List all registered services
                services = await self.service_manager.registry.list_services()
                logger.info(f"Total registered services: {len(services)}")
                
                for service in services:
                    logger.info(f"  - {service['name']}: {service['status']}")
            else:
                logger.error("Failed to initialize Service Manager")
                
        except Exception as e:
            logger.error(f"Error setting up services: {e}")

# Create the FastAPI app instance
app = MCPServer().app
