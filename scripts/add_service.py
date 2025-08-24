#!/usr/bin/env python3
"""
Script to demonstrate adding new MCP services using the modular architecture.
This script shows how easy it is to add services without modifying the core server code.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from mcp.service_manager import ServiceManager

async def add_example_service():
    """Add the example service to demonstrate the modular architecture"""
    
    # Initialize service manager
    service_manager = ServiceManager()
    
    try:
        # Initialize the service manager
        success = await service_manager.initialize()
        if not success:
            print("❌ Failed to initialize service manager")
            return
        
        print("✅ Service manager initialized successfully")
        
        # Example service configuration
        example_service_config = {
            "id": "example",
            "name": "Example Service",
            "description": "A demonstration service added dynamically",
            "module": "app.mcp.services.example_service",
            "class": "ExampleService",
            "enabled": True,
            "category": "general",
            "url": "http://localhost:3010",
            "metadata": {
                "type": "demonstration",
                "features": ["hello_world", "calculations", "info"]
            }
        }
        
        # Add the service
        print("🔄 Adding example service...")
        service_id = await service_manager.add_service(example_service_config)
        
        if service_id:
            print(f"✅ Service '{service_id}' added successfully!")
            
            # Get service status
            status = await service_manager.get_service_status(service_id)
            if status:
                print(f"📊 Service Status:")
                print(f"   Name: {status['name']}")
                print(f"   Status: {status['status']}")
                print(f"   Tools: {len(status['tools'])}")
                print(f"   Category: {status['category']}")
            
            # Get overall statistics
            stats = await service_manager.get_statistics()
            print(f"\n📈 Overall Statistics:")
            print(f"   Total Services: {stats['services']['total_services']}")
            print(f"   Online Services: {stats['services']['online_services']}")
            print(f"   Total Tools: {stats['services']['total_tools']}")
            
        else:
            print("❌ Failed to add service")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Shutdown the service manager
        await service_manager.shutdown()

async def list_all_services():
    """List all currently registered services"""
    
    service_manager = ServiceManager()
    
    try:
        await service_manager.initialize()
        
        print("📋 Currently Registered Services:")
        print("=" * 50)
        
        services = await service_manager.get_all_service_statuses()
        
        if not services:
            print("No services registered")
            return
        
        for service in services:
            status_emoji = "🟢" if service['status'] == 'online' else "🔴"
            print(f"{status_emoji} {service['name']} ({service['id']})")
            print(f"   Status: {service['status']}")
            print(f"   Category: {service['category']}")
            print(f"   Tools: {len(service['tools'])}")
            print(f"   Enabled: {service['enabled']}")
            print()
            
    except Exception as e:
        print(f"❌ Error listing services: {e}")
    
    finally:
        await service_manager.shutdown()

async def main():
    """Main function to demonstrate service management"""
    
    print("🚀 MCP Service Management Demo")
    print("=" * 40)
    
    # List current services
    await list_all_services()
    
    print("\n" + "=" * 40)
    
    # Add example service
    await add_example_service()
    
    print("\n" + "=" * 40)
    
    # List services again to show the new addition
    await list_all_services()

if __name__ == "__main__":
    asyncio.run(main())
