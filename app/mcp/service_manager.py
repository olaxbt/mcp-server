import asyncio
import logging
from typing import Any, Dict, List, Optional
from pathlib import Path
import json
import yaml

from .service_registry import ServiceRegistry
from .service_loader import ServiceLoader

logger = logging.getLogger(__name__)

class ServiceManager:
    """High-level service management interface"""
    
    def __init__(self, config_path: str = "app/mcp/services_config.yaml"):
        self.config_path = config_path
        self.registry = ServiceRegistry()
        self.loader = ServiceLoader(self.registry)
        self.config_cache = {}
        self.auto_reload_enabled = False
        
    async def initialize(self) -> bool:
        """Initialize the service manager and load all services"""
        try:
            logger.info("Initializing Service Manager...")
            
            # Load configuration
            if not await self.load_configuration():
                logger.error("Failed to load configuration")
                return False
            
            # Load services from config
            loaded_services = await self.loader.load_services_from_config(self.config_path)
            
            if loaded_services:
                logger.info(f"Successfully loaded {len(loaded_services)} services")
            else:
                logger.warning("No services loaded from configuration, trying auto-discovery")
                
                # Fallback to auto-discovery
                services_dir = "app/mcp/services"
                discovered_services = await self.loader.load_services_from_directory(services_dir)
                if discovered_services:
                    logger.info(f"Auto-discovered {len(discovered_services)} services")
                else:
                    logger.warning("No services discovered automatically")
            
            # Start health monitoring if enabled
            if self.config_cache.get('settings', {}).get('auto_discovery', True):
                await self.start_health_monitoring()
            
            logger.info("Service Manager initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Service Manager: {e}")
            return False
    
    async def load_configuration(self) -> bool:
        """Load service configuration from file"""
        try:
            config_path = Path(self.config_path)
            if not config_path.exists():
                logger.error(f"Configuration file not found: {config_path}")
                return False
            
            # Load configuration
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                with open(config_path, 'r') as f:
                    self.config_cache = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                with open(config_path, 'r') as f:
                    self.config_cache = json.load(f)
            else:
                logger.error(f"Unsupported configuration file format: {config_path.suffix}")
                return False
            
            logger.info(f"Configuration loaded from {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return False
    
    async def reload_configuration(self) -> bool:
        """Reload configuration and restart services"""
        try:
            logger.info("Reloading configuration...")
            
            # Stop health monitoring
            await self.stop_health_monitoring()
            
            # Unregister all services
            services = await self.registry.list_services()
            for service in services:
                await self.registry.unregister_service(service['id'])
            
            # Reload configuration
            if not await self.load_configuration():
                return False
            
            # Reload services
            loaded_services = await self.loader.load_services_from_config(self.config_path)
            
            # Restart health monitoring
            if self.config_cache.get('settings', {}).get('auto_discovery', True):
                await self.start_health_monitoring()
            
            logger.info(f"Configuration reloaded, {len(loaded_services)} services loaded")
            return True
            
        except Exception as e:
            logger.error(f"Error reloading configuration: {e}")
            return False
    
    async def add_service(self, service_config: Dict[str, Any]) -> Optional[str]:
        """Add a new service dynamically"""
        try:
            # Validate configuration
            validation = await self.loader.validate_service_config(service_config)
            if not validation.get('valid', False):
                logger.error(f"Invalid service configuration: {validation.get('errors')}")
                return None
            
            # Load and register service
            service_id = await self.loader.load_service(service_config)
            if service_id:
                logger.info(f"Service {service_id} added successfully")
                
                # Update configuration cache
                if 'services' not in self.config_cache:
                    self.config_cache['services'] = []
                self.config_cache['services'].append(service_config)
                
                return service_id
            else:
                logger.error("Failed to add service")
                return None
                
        except Exception as e:
            logger.error(f"Error adding service: {e}")
            return None
    
    async def remove_service(self, service_id: str) -> bool:
        """Remove a service"""
        try:
            # Unregister service
            success = await self.registry.unregister_service(service_id)
            if success:
                # Remove from configuration cache
                if 'services' in self.config_cache:
                    self.config_cache['services'] = [
                        s for s in self.config_cache['services'] 
                        if s.get('id') != service_id
                    ]
                
                logger.info(f"Service {service_id} removed successfully")
                return True
            else:
                logger.error(f"Failed to remove service {service_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing service {service_id}: {e}")
            return False
    
    async def enable_service(self, service_id: str) -> bool:
        """Enable a disabled service"""
        try:
            # Find service in configuration
            if 'services' in self.config_cache:
                for service in self.config_cache['services']:
                    if service.get('id') == service_id:
                        service['enabled'] = True
                        
                        # Reload the service
                        await self.registry.unregister_service(service_id)
                        await self.loader.load_service(service)
                        
                        logger.info(f"Service {service_id} enabled successfully")
                        return True
            
            logger.error(f"Service {service_id} not found in configuration")
            return False
            
        except Exception as e:
            logger.error(f"Error enabling service {service_id}: {e}")
            return False
    
    async def disable_service(self, service_id: str) -> bool:
        """Disable a service"""
        try:
            # Find service in configuration
            if 'services' in self.config_cache:
                for service in self.config_cache['services']:
                    if service.get('id') == service_id:
                        service['enabled'] = False
                        
                        # Unregister the service
                        await self.registry.unregister_service(service_id)
                        
                        logger.info(f"Service {service_id} disabled successfully")
                        return True
            
            logger.error(f"Service {service_id} not found in configuration")
            return False
            
        except Exception as e:
            logger.error(f"Error disabling service {service_id}: {e}")
            return False
    
    async def get_service_status(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a specific service"""
        try:
            service = await self.registry.get_service(service_id)
            if not service:
                return None
            
            config = await self.registry.get_service_config(service_id)
            health_status = await self.registry.check_service_health(service_id)
            
            return {
                "id": service_id,
                "name": config.get("name", service_id),
                "description": config.get("description", ""),
                "status": health_status,
                "enabled": config.get("enabled", True),
                "category": config.get("category", "general"),
                "tools": await service.list_tool_names(),
                "metadata": config.get("metadata", {}),
                "url": config.get("url", "")
            }
            
        except Exception as e:
            logger.error(f"Error getting service status for {service_id}: {e}")
            return None
    
    async def get_all_service_statuses(self) -> List[Dict[str, Any]]:
        """Get status of all services"""
        try:
            services = await self.registry.list_services()
            statuses = []
            
            for service in services:
                status = await self.get_service_status(service['id'])
                if status:
                    statuses.append(status)
            
            return statuses
            
        except Exception as e:
            logger.error(f"Error getting all service statuses: {e}")
            return []
    
    async def start_health_monitoring(self) -> None:
        """Start automatic health monitoring of services"""
        if self.auto_reload_enabled:
            return
        
        self.auto_reload_enabled = True
        asyncio.create_task(self._health_monitor_loop())
        logger.info("Health monitoring started")
    
    async def stop_health_monitoring(self) -> None:
        """Stop automatic health monitoring"""
        self.auto_reload_enabled = False
        logger.info("Health monitoring stopped")
    
    async def _health_monitor_loop(self) -> None:
        """Health monitoring loop"""
        while self.auto_reload_enabled:
            try:
                # Check all services health
                health_status = await self.registry.check_all_services_health()
                
                # Log any offline services
                for service_id, status in health_status.items():
                    if status == "offline":
                        logger.warning(f"Service {service_id} is offline")
                
                # Wait for next check
                interval = self.config_cache.get('settings', {}).get('health_check_interval', 30)
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in health monitoring: {e}")
                await asyncio.sleep(10)
    
    async def save_configuration(self, output_path: Optional[str] = None) -> bool:
        """Save current configuration to file"""
        try:
            if not output_path:
                output_path = self.config_path
            
            output_path = Path(output_path)
            
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save configuration
            if output_path.suffix.lower() in ['.yaml', '.yml']:
                with open(output_path, 'w') as f:
                    yaml.dump(self.config_cache, f, default_flow_style=False, indent=2)
            elif output_path.suffix.lower() == '.json':
                with open(output_path, 'w') as f:
                    json.dump(self.config_cache, f, indent=2)
            else:
                logger.error(f"Unsupported output format: {output_path.suffix}")
                return False
            
            logger.info(f"Configuration saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about all services"""
        try:
            service_stats = await self.registry.get_service_statistics()
            
            # Add manager-specific stats
            stats = {
                "manager": {
                    "auto_reload_enabled": self.auto_reload_enabled,
                    "config_file": self.config_path,
                    "config_loaded": bool(self.config_cache)
                },
                "services": service_stats,
                "configuration": {
                    "total_configured": len(self.config_cache.get('services', [])),
                    "enabled_services": len([
                        s for s in self.config_cache.get('services', [])
                        if s.get('enabled', True)
                    ]),
                    "categories": list(self.config_cache.get('categories', {}).keys())
                }
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {"error": str(e)}
    
    async def shutdown(self) -> None:
        """Shutdown the service manager"""
        try:
            logger.info("Shutting down Service Manager...")
            
            # Stop health monitoring
            await self.stop_health_monitoring()
            
            # Unregister all services
            services = await self.registry.list_services()
            for service in services:
                await self.registry.unregister_service(service['id'])
            
            logger.info("Service Manager shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
