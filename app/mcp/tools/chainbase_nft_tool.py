import asyncio
import logging
import aiohttp
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class ChainbaseNFTTool(MCPTool):
    """Chainbase NFT MCP tool for accessing NFT metadata and collection information"""
    
    def __init__(self):
        self.session = None
        self.base_url = "https://api.chainbase.online/v1"
        
    @property
    def name(self) -> str:
        return "chainbase_nft"
    
    @property
    def description(self) -> str:
        return "Access Chainbase NFT data including metadata, owners, rarity, and collection information"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "get_nft_metadata",
                        "get_nft_owners_by_collection",
                        "get_nft_owner_by_token",
                        "get_nft_rarity",
                        "get_nft_owner_history",
                        "get_nft_transfers",
                        "get_collection_items",
                        "get_collection_metadata"
                    ],
                    "description": "Action to perform"
                },
                "api_key": {
                    "type": "string",
                    "description": "Chainbase API key (required)"
                },
                "chain_id": {
                    "type": "string",
                    "description": "Chain network ID"
                },
                "contract_address": {
                    "type": "string",
                    "description": "NFT contract address"
                },
                "token_id": {
                    "type": "string",
                    "description": "NFT token ID"
                },
                "limit": {
                    "type": "integer",
                    "default": 10,
                    "description": "Maximum number of results"
                }
            },
            "required": ["action", "api_key", "chain_id", "contract_address"]
        }
    
    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _cleanup_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            chain_id = arguments.get("chain_id")
            contract_address = arguments.get("contract_address")
            token_id = arguments.get("token_id")
            limit = arguments.get("limit", 10)
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Chainbase API key is required. Please provide your API key."}]
            
            if action == "get_nft_metadata":
                if not token_id:
                    result = {"type": "text", "text": "❌ Error: Token ID is required for get_nft_metadata"}
                else:
                    result = await self._get_nft_metadata(chain_id, contract_address, token_id, api_key)
            elif action == "get_nft_owners_by_collection":
                result = await self._get_nft_owners_by_collection(chain_id, contract_address, limit, api_key)
            elif action == "get_nft_owner_by_token":
                if not token_id:
                    result = {"type": "text", "text": "❌ Error: Token ID is required for get_nft_owner_by_token"}
                else:
                    result = await self._get_nft_owner_by_token(chain_id, contract_address, token_id, api_key)
            elif action == "get_nft_rarity":
                if not token_id:
                    result = {"type": "text", "text": "❌ Error: Token ID is required for get_nft_rarity"}
                else:
                    result = await self._get_nft_rarity(chain_id, contract_address, token_id, api_key)
            elif action == "get_nft_owner_history":
                if not token_id:
                    result = {"type": "text", "text": "❌ Error: Token ID is required for get_nft_owner_history"}
                else:
                    result = await self._get_nft_owner_history(chain_id, contract_address, token_id, api_key)
            elif action == "get_nft_transfers":
                result = await self._get_nft_transfers(chain_id, contract_address, limit, api_key)
            elif action == "get_collection_items":
                result = await self._get_collection_items(chain_id, contract_address, limit, api_key)
            elif action == "get_collection_metadata":
                result = await self._get_collection_metadata(chain_id, contract_address, api_key)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}
            
            return [result]
        finally:
            await self._cleanup_session()
    
    async def _get_nft_metadata(self, chain_id: str, contract_address: str, token_id: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/metadata"
            params = {"chain_id": chain_id, "contract_address": contract_address, "token_id": token_id}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "token_id": token_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get NFT metadata: {str(e)}"}
    
    async def _get_nft_owners_by_collection(self, chain_id: str, contract_address: str, limit: int, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/owners"
            params = {"chain_id": chain_id, "contract_address": contract_address, "limit": limit}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get NFT owners: {str(e)}"}
    
    async def _get_nft_owner_by_token(self, chain_id: str, contract_address: str, token_id: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/owner"
            params = {"chain_id": chain_id, "contract_address": contract_address, "token_id": token_id}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "token_id": token_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get NFT owner: {str(e)}"}
    
    async def _get_nft_rarity(self, chain_id: str, contract_address: str, token_id: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/rarity"
            params = {"chain_id": chain_id, "contract_address": contract_address, "token_id": token_id}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "token_id": token_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get NFT rarity: {str(e)}"}
    
    async def _get_nft_owner_history(self, chain_id: str, contract_address: str, token_id: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/owner/history"
            params = {"chain_id": chain_id, "contract_address": contract_address, "token_id": token_id}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "token_id": token_id,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get NFT owner history: {str(e)}"}
    
    async def _get_nft_transfers(self, chain_id: str, contract_address: str, limit: int, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/transfers"
            params = {"chain_id": chain_id, "contract_address": contract_address, "limit": limit}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get NFT transfers: {str(e)}"}
    
    async def _get_collection_items(self, chain_id: str, contract_address: str, limit: int, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/collection/items"
            params = {"chain_id": chain_id, "contract_address": contract_address, "limit": limit}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get collection items: {str(e)}"}
    
    async def _get_collection_metadata(self, chain_id: str, contract_address: str, api_key: str) -> dict:
        try:
            url = f"{self.base_url}/nft/collection/metadata"
            params = {"chain_id": chain_id, "contract_address": contract_address}
            headers = {"x-api-key": api_key}
            
            session = await self._get_session()
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": data,
                        "chain_id": chain_id,
                        "contract_address": contract_address,
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {"success": False, "error": f"API request failed with status {response.status}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to get collection metadata: {str(e)}"}
