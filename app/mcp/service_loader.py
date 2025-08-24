import asyncio
import logging
import importlib
import inspect
from typing import Any, Dict, List, Optional, Type
from pathlib import Path
import json
import yaml

from .service_registry import ServiceRegistry
from .services.base_service import BaseMCPService

logger = logging.getLogger(__name__)

class ServiceLoader:
    """Dynamic service loader for MCP services"""
    
    def __init__(self, registry: ServiceRegistry):
        self.registry = registry
        self.service_modules = {}
        self.config_cache = {}
        
    async def load_services_from_config(self, config_path: str) -> List[str]:
        """Load services from a configuration file"""
        try:
            config_path = Path(config_path)
            if not config_path.exists():
                logger.error(f"Configuration file not found: {config_path}")
                return []
            
            # Load configuration
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                with open(config_path, 'r') as f:
                    config = json.load(f)
            else:
                logger.error(f"Unsupported configuration file format: {config_path.suffix}")
                return []
            
            # Load services
            loaded_services = []
            services_config = config.get('services', [])
            
            for service_config in services_config:
                try:
                    service_id = await self.load_service(service_config)
                    if service_id:
                        loaded_services.append(service_id)
                except Exception as e:
                    logger.error(f"Failed to load service from config: {e}")
                    continue
            
            logger.info(f"Loaded {len(loaded_services)} services from configuration")
            return loaded_services
            
        except Exception as e:
            logger.error(f"Error loading services from config: {e}")
            return []
    
    async def load_service(self, service_config: Dict[str, Any]) -> Optional[str]:
        """Load a single service from configuration"""
        try:
            service_id = service_config.get('id')
            if not service_id:
                logger.error("Service configuration missing 'id' field")
                return None
            
            # Check if service is enabled
            if not service_config.get('enabled', True):
                logger.info(f"Service {service_id} is disabled, skipping")
                return None
            
            # Load service class
            service_class = await self.load_service_class(service_config)
            if not service_class:
                return None
            
            # Create service instance
            service_instance = await self.create_service_instance(service_class, service_config)
            if not service_instance:
                return None
            
            # Register service
            success = await self.registry.register_service(service_id, service_instance, service_config)
            if success:
                logger.info(f"Successfully loaded service: {service_id}")
                return service_id
            else:
                logger.error(f"Failed to register service: {service_id}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading service: {e}")
            return None
    
    async def load_service_class(self, service_config: Dict[str, Any]) -> Optional[Type[BaseMCPService]]:
        """Load service class from module path"""
        try:
            module_path = service_config.get('module')
            class_name = service_config.get('class')
            
            if not module_path or not class_name:
                logger.error(f"Service configuration missing 'module' or 'class' field")
                return None
            
            # Import module
            try:
                module = importlib.import_module(module_path)
            except ImportError as e:
                logger.error(f"Failed to import module {module_path}: {e}")
                return None
            
            # Get class
            service_class = getattr(module, class_name, None)
            if not service_class:
                logger.error(f"Class {class_name} not found in module {module_path}")
                return None
            
            # Validate class
            if not inspect.isclass(service_class):
                logger.error(f"{class_name} is not a class")
                return None
            
            if not issubclass(service_class, BaseMCPService):
                logger.error(f"{class_name} must inherit from BaseMCPService")
                return None
            
            return service_class
            
        except Exception as e:
            logger.error(f"Error loading service class: {e}")
            return None
    
    async def create_service_instance(self, service_class: Type[BaseMCPService], service_config: Dict[str, Any]) -> Optional[BaseMCPService]:
        """Create service instance with configuration"""
        try:
            # Get constructor parameters
            init_params = service_config.get('init_params', {})
            
            # Create instance
            if init_params:
                service_instance = service_class(**init_params)
            else:
                service_instance = service_class()
            
            # Set service attributes if they exist
            if hasattr(service_instance, 'service_name'):
                service_instance.service_name = service_config.get('name', service_instance.service_name)
            
            if hasattr(service_instance, 'service_description'):
                service_instance.service_description = service_config.get('description', service_instance.service_description)
            
            if hasattr(service_instance, 'base_url'):
                service_instance.base_url = service_config.get('url', service_instance.base_url)
            
            return service_instance
            
        except Exception as e:
            logger.error(f"Error creating service instance: {e}")
            return None
    
    async def load_services_from_directory(self, services_dir: str) -> List[str]:
        """Load services from a directory containing service modules"""
        try:
            services_dir = Path(services_dir)
            if not services_dir.exists() or not services_dir.is_dir():
                logger.error(f"Services directory not found: {services_dir}")
                return []
            
            loaded_services = []
            
            # Look for Python files in the directory
            for py_file in services_dir.glob("*.py"):
                if py_file.name.startswith('_') or py_file.name == '__init__.py':
                    continue
                
                try:
                    # Import the module
                    module_name = f"{services_dir.name}.{py_file.stem}"
                    module = importlib.import_module(module_name)
                    
                    # Look for classes that inherit from BaseMCPService
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (inspect.isclass(attr) and 
                            issubclass(attr, BaseMCPService) and 
                            attr != BaseMCPService):
                            
                            # Create basic config
                            service_config = {
                                'id': attr_name.lower(),
                                'name': getattr(attr, 'service_name', attr_name),
                                'description': getattr(attr, 'service_description', f'Service {attr_name}'),
                                'module': module_name,
                                'class': attr_name,
                                'enabled': True,
                                'category': 'auto_discovered'
                            }
                            
                            # Try to load the service
                            service_id = await self.load_service(service_config)
                            if service_id:
                                loaded_services.append(service_id)
                
                except Exception as e:
                    logger.error(f"Error loading service from {py_file}: {e}")
                    continue
            
            logger.info(f"Auto-discovered and loaded {len(loaded_services)} services from directory")
            return loaded_services
            
        except Exception as e:
            logger.error(f"Error loading services from directory: {e}")
            return []
    
    async def reload_service(self, service_id: str) -> bool:
        """Reload a specific service"""
        try:
            # Get current config
            config = await self.registry.get_service_config(service_id)
            if not config:
                logger.error(f"Service {service_id} not found in registry")
                return False
            
            # Unregister current service
            await self.registry.unregister_service(service_id)
            
            # Reload service
            new_service_id = await self.load_service(config)
            if new_service_id and new_service_id == service_id:
                logger.info(f"Successfully reloaded service: {service_id}")
                return True
            else:
                logger.error(f"Failed to reload service: {service_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error reloading service {service_id}: {e}")
            return False
    
    async def get_available_service_modules(self) -> List[str]:
        """Get list of available service modules"""
        return list(self.service_modules.keys())
    
    async def validate_service_config(self, service_config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate service configuration"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['id', 'module', 'class']
        for field in required_fields:
            if field not in service_config:
                errors.append(f"Missing required field: {field}")
        
        # Validate module path
        if 'module' in service_config:
            try:
                importlib.import_module(service_config['module'])
            except ImportError:
                errors.append(f"Cannot import module: {service_config['module']}")
        
        # Validate class name
        if 'module' in service_config and 'class' in service_config:
            try:
                module = importlib.import_module(service_config['module'])
                if not hasattr(module, service_config['class']):
                    errors.append(f"Class {service_config['class']} not found in module {service_config['module']}")
            except ImportError:
                pass  # Already caught above
        
        # Optional validations
        if 'url' in service_config and not service_config['url'].startswith(('http://', 'https://')):
            warnings.append("URL should start with http:// or https://")
        
        if 'category' in service_config and service_config['category'] not in ['defi', 'gaming', 'nft', 'trading', 'analytics', 'general']:
            warnings.append("Category should be one of: defi, gaming, nft, trading, analytics, general")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
