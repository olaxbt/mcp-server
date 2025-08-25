"""
Base MCP Tool Class
Defines the interface that all MCP tools must implement
"""

import os
import aiohttp
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class MCPTool(ABC):
    """Abstract base class for all MCP tools"""
    
    def __init__(self):
        self.session = None
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return the tool description"""
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """Return the input schema for the tool"""
        pass
    
    @abstractmethod
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the tool with the given arguments"""
        pass
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        """Clean up aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None
