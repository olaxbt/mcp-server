"""
MetaSleuth Wallet Tool for MCP
Provides wallet analytics using MetaSleuth API from BlockSec
"""

import aiohttp
import json
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class MetaSleuthWalletTool(MCPTool):
    """Tool for advanced wallet analytics using MetaSleuth API from BlockSec"""

    @property
    def name(self) -> str:
        return "metasleuth_wallet"

    @property
    def description(self) -> str:
        return "Advanced wallet analytics and compliance checking using MetaSleuth API from BlockSec"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_address_labels", "get_compliance_risk"]
                },
                "address": {
                    "type": "string",
                    "description": "Wallet address to analyze"
                },
                "api_key": {
                    "type": "string",
                    "description": "MetaSleuth API key (required) - Get from BlockSec account"
                },
                "chain_id": {
                    "type": "integer",
                    "description": "Chain ID (1=Ethereum, 56=BSC, 137=Polygon, etc.)",
                    "default": 1
                }
            },
            "required": ["action", "address", "api_key"]
        }

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        address = arguments.get("address")
        api_key = arguments.get("api_key")
        chain_id = arguments.get("chain_id", 1)
        
        if not api_key:
            return [{"type": "text", "text": "❌ Error: MetaSleuth API key is required"}]
        
        try:
            if action == "get_address_labels":
                return await self._get_address_labels(address, api_key, chain_id)
            elif action == "get_compliance_risk":
                return await self._get_compliance_risk(address, api_key, chain_id)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"MetaSleuth wallet tool error: {str(e)}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _get_address_labels(self, address: str, api_key: str, chain_id: int) -> List[Dict[str, Any]]:
        """Get address labels and information using MetaSleuth Address Label API"""
        try:
            # MetaSleuth Address Label API endpoint
            url = "https://aml.blocksec.com/address-label/api/v3/labels"
            headers = {
                "API-KEY": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "chain_id": chain_id,
                "address": address
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        # Extract address information
                        labels = response_data.get("data", {}).get("labels", [])
                        risk_score = response_data.get("data", {}).get("risk_score", "Unknown")
                        address_type = response_data.get("data", {}).get("type", "Unknown")
                        
                        result_text = f"""🏷️ **Address Label Information**

**Address:** `{address}`
**Chain ID:** {chain_id}
**Address Type:** {address_type}
**Risk Score:** {risk_score}

**Labels:**"""
                        
                        if labels:
                            for label in labels:
                                label_name = label.get("label", "Unknown")
                                label_type = label.get("type", "Unknown")
                                confidence = label.get("confidence", "Unknown")
                                result_text += f"\n• **{label_name}** ({label_type}) - Confidence: {confidence}"
                        else:
                            result_text += "\n• No specific labels found"
                        
                        result_text += f"\n\n*Data provided by [MetaSleuth API](https://docs.metasleuth.io/)*"
                        
                        return [{"type": "text", "text": result_text}]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ Error fetching address labels: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching address labels: {str(e)}"}]

    async def _get_compliance_risk(self, address: str, api_key: str, chain_id: int) -> List[Dict[str, Any]]:
        """Get compliance risk assessment using MetaSleuth Compliance API"""
        try:
            # MetaSleuth Compliance API endpoint
            url = "https://aml.blocksec.com/compliance/api/v1/risk"
            headers = {
                "API-KEY": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "chain_id": chain_id,
                "address": address
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        
                        # Extract compliance information
                        risk_score = response_data.get("data", {}).get("risk_score", "Unknown")
                        risk_level = response_data.get("data", {}).get("risk_level", "Unknown")
                        factors = response_data.get("data", {}).get("risk_factors", [])
                        recommendation = response_data.get("data", {}).get("recommendation", "No specific recommendation")
                        
                        result_text = f"""⚖️ **Compliance Risk Assessment**

**Address:** `{address}`
**Chain ID:** {chain_id}
**Risk Score:** {risk_score}/5
**Risk Level:** {risk_level}

**Risk Factors:**"""
                        
                        if factors:
                            for factor in factors:
                                factor_name = factor.get("factor", "Unknown")
                                factor_impact = factor.get("impact", "Unknown")
                                result_text += f"\n• **{factor_name}** - Impact: {factor_impact}"
                        else:
                            result_text += "\n• No specific risk factors identified"
                        
                        result_text += f"\n\n**Recommendation:** {recommendation}"
                        result_text += f"\n\n*Data provided by [MetaSleuth API](https://docs.metasleuth.io/)*"
                        
                        return [{"type": "text", "text": result_text}]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ Error fetching compliance risk: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching compliance risk: {str(e)}"}]