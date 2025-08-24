import asyncio
import logging
from typing import Any, Dict, List, Optional, Type
from pathlib import Path
import importlib
import inspect

from .services.base_service import BaseMCPService

logger = logging.getLogger(__name__)

class ServiceRegistry:
    """Central registry for managing all MCP services"""
    
    def __init__(self):
        self.services: Dict[str, BaseMCPService] = {}
        self.service_configs: Dict[str, Dict[str, Any]] = {}
        self.tool_routing: Dict[str, str] = {}  # tool_name -> service_id
        self.service_health: Dict[str, bool] = {}
        
    async def register_service(self, service_id: str, service_instance: BaseMCPService, config: Dict[str, Any]) -> bool:
        """Register a service instance with configuration"""
        try:
            # Validate service instance
            if not isinstance(service_instance, BaseMCPService):
                logger.error(f"Service {service_id} must inherit from BaseMCPService")
                return False
            
            # Store service and config
            self.services[service_id] = service_instance
            self.service_configs[service_id] = config
            self.service_health[service_id] = True
            
            # Register tools
            tools = await service_instance.get_tools()
            for tool in tools:
                tool_name = tool.get("name")
                if tool_name:
                    self.tool_routing[tool_name] = service_id
                    logger.info(f"Registered tool '{tool_name}' -> service '{service_id}'")
            
            logger.info(f"Successfully registered service: {service_id} with {len(tools)} tools")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register service {service_id}: {e}")
            return False
    
    async def unregister_service(self, service_id: str) -> bool:
        """Unregister a service and clean up its tools"""
        try:
            if service_id not in self.services:
                return False
            
            # Remove tool routing
            tools_to_remove = [
                tool_name for tool_name, service in self.tool_routing.items() 
                if service == service_id
            ]
            for tool_name in tools_to_remove:
                del self.tool_routing[tool_name]
            
            # Remove service
            del self.services[service_id]
            del self.service_configs[service_id]
            del self.service_health[service_id]
            
            logger.info(f"Unregistered service: {service_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to unregister service {service_id}: {e}")
            return False
    
    async def get_service(self, service_id: str) -> Optional[BaseMCPService]:
        """Get a service instance by ID"""
        return self.services.get(service_id)
    
    async def get_service_config(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get service configuration by ID"""
        return self.service_configs.get(service_id)
    
    async def list_services(self) -> List[Dict[str, Any]]:
        """List all registered services with their status"""
        services_list = []
        for service_id, service in self.services.items():
            config = self.service_configs.get(service_id, {})
            health_status = await self.check_service_health(service_id)
            
            services_list.append({
                "id": service_id,
                "name": config.get("name", service_id),
                "description": config.get("description", ""),
                "url": config.get("url", ""),
                "status": health_status,
                "tools": list(await service.list_tool_names()),
                "metadata": config.get("metadata", {}),
                "category": config.get("category", "general")
            })
        
        return services_list
    
    async def list_all_tools(self) -> List[Dict[str, Any]]:
        """List all available tools across all services"""
        all_tools = []
        for service_id, service in self.services.items():
            if self.service_health.get(service_id, False):
                try:
                    tools = await service.get_tools()
                    for tool in tools:
                        config = self.service_configs.get(service_id, {})
                        all_tools.append({
                            "name": tool.get("name", ""),
                            "description": tool.get("description", ""),
                            "input_schema": tool.get("input_schema", {}),
                            "service_id": service_id,
                            "service_name": config.get("name", service_id),
                            "category": config.get("category", "general")
                        })
                except Exception as e:
                    logger.error(f"Error getting tools from service {service_id}: {e}")
                    continue
        
        return all_tools
    
    async def route_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Route a tool call to the appropriate service"""
        service_id = self.tool_routing.get(tool_name)
        if not service_id:
            raise ValueError(f"Tool '{tool_name}' not found in any service")
        
        service = self.services.get(service_id)
        if not service:
            raise ValueError(f"Service '{service_id}' not found")
        
        # Validate arguments
        validation = await service.validate_arguments(tool_name, arguments)
        if not validation.get("valid", False):
            raise ValueError(f"Invalid arguments for tool '{tool_name}': {validation.get('error')}")
        
        # Execute tool
        result = await service.execute_tool(tool_name, arguments)
        return result
    
    async def check_service_health(self, service_id: str) -> str:
        """Check health status of a specific service"""
        if service_id not in self.services:
            return "not_found"
        
        try:
            service = self.services[service_id]
            health = await service.health_check()
            
            if health.get("status") == "healthy":
                self.service_health[service_id] = True
                return "online"
            else:
                self.service_health[service_id] = False
                return "unhealthy"
                
        except Exception as e:
            logger.error(f"Health check failed for {service_id}: {e}")
            self.service_health[service_id] = False
            return "offline"
    
    async def check_all_services_health(self) -> Dict[str, str]:
        """Check health of all services"""
        health_status = {}
        for service_id in self.services.keys():
            health_status[service_id] = await self.check_service_health(service_id)
        return health_status
    
    async def get_service_by_tool(self, tool_name: str) -> Optional[BaseMCPService]:
        """Get service instance that provides a specific tool"""
        service_id = self.tool_routing.get(tool_name)
        if service_id:
            return self.services.get(service_id)
        return None
    
    async def reload_service(self, service_id: str) -> bool:
        """Reload a service (useful for development)"""
        try:
            if service_id not in self.services:
                return False
            
            # Get current config
            config = self.service_configs[service_id]
            
            # Unregister and re-register
            await self.unregister_service(service_id)
            
            # Recreate service instance
            service_class = config.get("class")
            if service_class and inspect.isclass(service_class):
                service_instance = service_class()
                return await self.register_service(service_id, service_instance, config)
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to reload service {service_id}: {e}")
            return False
    
    async def get_service_statistics(self) -> Dict[str, Any]:
        """Get statistics about all services"""
        total_services = len(self.services)
        total_tools = len(self.tool_routing)
        
        # Count tools by category
        tools_by_category = {}
        for service_id, config in self.service_configs.items():
            category = config.get("category", "general")
            if category not in tools_by_category:
                tools_by_category[category] = 0
            
            service = self.services.get(service_id)
            if service:
                try:
                    tool_count = len(await service.list_tool_names())
                    tools_by_category[category] += tool_count
                except:
                    continue
        
        # Health statistics
        health_stats = await self.check_all_services_health()
        online_services = sum(1 for status in health_stats.values() if status == "online")
        
        return {
            "total_services": total_services,
            "online_services": online_services,
            "total_tools": total_tools,
            "tools_by_category": tools_by_category,
            "health_summary": health_stats
        }
