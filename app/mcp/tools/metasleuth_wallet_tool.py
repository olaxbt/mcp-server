import os
import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class MetaSleuthWalletTool(MCPTool):
    """Tool for advanced wallet analytics using MetaSleuth API"""

    @property
    def name(self) -> str:
        return "metasleuth_wallet"

    @property
    def description(self) -> str:
        return "Advanced wallet analytics, risk scoring, and transaction intelligence using MetaSleuth API"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["get_wallet_intel", "get_risk_score", "get_transaction_analysis", "get_behavior_patterns", "get_entity_connections", "get_compliance_check"]
                },
                "address": {
                    "type": "string",
                    "description": "Wallet address to analyze"
                },
                "api_key": {
                    "type": "string",
                    "description": "MetaSleuth API key (required)"
                },
                "timeframe": {
                    "type": "string",
                    "description": "Time period for analysis",
                    "enum": ["7d", "30d", "90d", "1y", "all"],
                    "default": "30d"
                },
                "include_metadata": {
                    "type": "boolean",
                    "description": "Include additional metadata in response",
                    "default": True
                }
            },
            "required": ["action", "address", "api_key"]
        }

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        action = arguments.get("action")
        address = arguments.get("address")
        api_key = arguments.get("api_key")
        timeframe = arguments.get("timeframe", "30d")
        include_metadata = arguments.get("include_metadata", True)
        
        if not api_key:
            return [{"type": "text", "text": "❌ Error: MetaSleuth API key is required"}]
        
        try:
            if action == "get_wallet_intel":
                return await self._get_wallet_intel(address, api_key, timeframe, include_metadata)
            elif action == "get_risk_score":
                return await self._get_risk_score(address, api_key, timeframe)
            elif action == "get_transaction_analysis":
                return await self._get_transaction_analysis(address, api_key, timeframe)
            elif action == "get_behavior_patterns":
                return await self._get_behavior_patterns(address, api_key, timeframe)
            elif action == "get_entity_connections":
                return await self._get_entity_connections(address, api_key, timeframe)
            elif action == "get_compliance_check":
                return await self._get_compliance_check(address, api_key)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"MetaSleuth wallet tool error: {str(e)}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]

    async def _get_wallet_intel(self, address: str, api_key: str, timeframe: str, include_metadata: bool) -> List[Dict[str, Any]]:
        """Get comprehensive wallet intelligence"""
        try:
            # MetaSleuth API endpoint for wallet intelligence
            url = f"https://api.metasleuth.com/v1/wallet/intelligence"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "address": address,
                "timeframe": timeframe,
                "include_metadata": include_metadata
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        intel = data.get("data", {})
                        
                        # Extract key intelligence data
                        risk_level = intel.get("risk_level", "Unknown")
                        activity_score = intel.get("activity_score", "N/A")
                        total_volume = intel.get("total_volume_usd", "0")
                        transaction_count = intel.get("transaction_count", 0)
                        first_seen = intel.get("first_seen", "Unknown")
                        last_active = intel.get("last_active", "Unknown")
                        
                        return [{
                            "type": "text", 
                            "text": f"🕵️ MetaSleuth Wallet Intelligence for {address[:10]}...\n\n"
                                   f"**Risk Level**: {risk_level}\n"
                                   f"**Activity Score**: {activity_score}\n"
                                   f"**Total Volume**: ${total_volume}\n"
                                   f"**Transaction Count**: {transaction_count}\n"
                                   f"**First Seen**: {first_seen}\n"
                                   f"**Last Active**: {last_active}\n"
                                   f"**Timeframe**: {timeframe}\n\n"
                                   f"*Data provided by MetaSleuth API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching wallet intelligence: {str(e)}"}]

    async def _get_risk_score(self, address: str, api_key: str, timeframe: str) -> List[Dict[str, Any]]:
        """Get comprehensive risk score for a wallet"""
        try:
            # MetaSleuth API endpoint for risk scoring
            url = f"https://api.metasleuth.com/v1/wallet/risk-score"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "address": address,
                "timeframe": timeframe
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        risk_data = data.get("data", {})
                        
                        overall_score = risk_data.get("overall_score", "N/A")
                        risk_category = risk_data.get("risk_category", "Unknown")
                        risk_factors = risk_data.get("risk_factors", [])
                        mitigation_suggestions = risk_data.get("mitigation_suggestions", [])
                        
                        risk_factors_text = "\n".join([f"• {factor}" for factor in risk_factors[:5]]) if risk_factors else "None identified"
                        mitigation_text = "\n".join([f"• {suggestion}" for suggestion in mitigation_suggestions[:3]]) if mitigation_suggestions else "No specific suggestions"
                        
                        return [{
                            "type": "text", 
                            "text": f"⚠️ MetaSleuth Risk Score for {address[:10]}...\n\n"
                                   f"**Overall Risk Score**: {overall_score}/100\n"
                                   f"**Risk Category**: {risk_category}\n"
                                   f"**Timeframe**: {timeframe}\n\n"
                                   f"**Risk Factors**:\n{risk_factors_text}\n\n"
                                   f"**Mitigation Suggestions**:\n{mitigation_text}\n\n"
                                   f"*Data provided by MetaSleuth API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching risk score: {str(e)}"}]

    async def _get_transaction_analysis(self, address: str, api_key: str, timeframe: str) -> List[Dict[str, Any]]:
        """Get detailed transaction analysis"""
        try:
            # MetaSleuth API endpoint for transaction analysis
            url = f"https://api.metasleuth.com/v1/wallet/transaction-analysis"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "address": address,
                "timeframe": timeframe
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        analysis = data.get("data", {})
                        
                        # Extract analysis data
                        total_inflow = analysis.get("total_inflow_usd", "0")
                        total_outflow = analysis.get("total_outflow_usd", "0")
                        net_flow = analysis.get("net_flow_usd", "0")
                        avg_transaction_size = analysis.get("avg_transaction_size_usd", "0")
                        suspicious_transactions = analysis.get("suspicious_transactions", 0)
                        high_risk_interactions = analysis.get("high_risk_interactions", 0)
                        
                        return [{
                            "type": "text", 
                            "text": f"📊 MetaSleuth Transaction Analysis for {address[:10]}...\n\n"
                                   f"**Timeframe**: {timeframe}\n"
                                   f"**Total Inflow**: ${total_inflow}\n"
                                   f"**Total Outflow**: ${total_outflow}\n"
                                   f"**Net Flow**: ${net_flow}\n"
                                   f"**Average TX Size**: ${avg_transaction_size}\n"
                                   f"**Suspicious TXs**: {suspicious_transactions}\n"
                                   f"**High-Risk Interactions**: {high_risk_interactions}\n\n"
                                   f"*Data provided by MetaSleuth API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching transaction analysis: {str(e)}"}]

    async def _get_behavior_patterns(self, address: str, api_key: str, timeframe: str) -> List[Dict[str, Any]]:
        """Get behavioral pattern analysis"""
        try:
            # MetaSleuth API endpoint for behavior patterns
            url = f"https://api.metasleuth.com/v1/wallet/behavior-patterns"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "address": address,
                "timeframe": timeframe
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        patterns = data.get("data", {})
                        
                        # Extract pattern data
                        trading_pattern = patterns.get("trading_pattern", "Unknown")
                        activity_timing = patterns.get("activity_timing", "Unknown")
                        preferred_protocols = patterns.get("preferred_protocols", [])
                        risk_tolerance = patterns.get("risk_tolerance", "Unknown")
                        behavioral_score = patterns.get("behavioral_score", "N/A")
                        
                        protocols_text = "\n".join([f"• {protocol}" for protocol in preferred_protocols[:5]]) if preferred_protocols else "None identified"
                        
                        return [{
                            "type": "text", 
                            "text": f"🧠 MetaSleuth Behavior Patterns for {address[:10]}...\n\n"
                                   f"**Timeframe**: {timeframe}\n"
                                   f"**Trading Pattern**: {trading_pattern}\n"
                                   f"**Activity Timing**: {activity_timing}\n"
                                   f"**Risk Tolerance**: {risk_tolerance}\n"
                                   f"**Behavioral Score**: {behavioral_score}/100\n\n"
                                   f"**Preferred Protocols**:\n{protocols_text}\n\n"
                                   f"*Data provided by MetaSleuth API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching behavior patterns: {str(e)}"}]

    async def _get_entity_connections(self, address: str, api_key: str, timeframe: str) -> List[Dict[str, Any]]:
        """Get entity connection analysis"""
        try:
            # MetaSleuth API endpoint for entity connections
            url = f"https://api.metasleuth.com/v1/wallet/entity-connections"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "address": address,
                "timeframe": timeframe
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        connections = data.get("data", {})
                        
                        # Extract connection data
                        total_connections = connections.get("total_connections", 0)
                        high_risk_connections = connections.get("high_risk_connections", 0)
                        known_entities = connections.get("known_entities", [])
                        connection_strength = connections.get("connection_strength", "Unknown")
                        
                        entities_text = "\n".join([f"• {entity}" for entity in known_entities[:5]]) if known_entities else "None identified"
                        
                        return [{
                            "type": "text", 
                            "text": f"🔗 MetaSleuth Entity Connections for {address[:10]}...\n\n"
                                   f"**Timeframe**: {timeframe}\n"
                                   f"**Total Connections**: {total_connections}\n"
                                   f"**High-Risk Connections**: {high_risk_connections}\n"
                                   f"**Connection Strength**: {connection_strength}\n\n"
                                   f"**Known Entities**:\n{entities_text}\n\n"
                                   f"*Data provided by MetaSleuth API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching entity connections: {str(e)}"}]

    async def _get_compliance_check(self, address: str, api_key: str) -> List[Dict[str, Any]]:
        """Get compliance and regulatory check results"""
        try:
            # MetaSleuth API endpoint for compliance checks
            url = f"https://api.metasleuth.com/v1/wallet/compliance-check"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            params = {
                "address": address
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        compliance = data.get("data", {})
                        
                        # Extract compliance data
                        overall_status = compliance.get("overall_status", "Unknown")
                        sanctions_check = compliance.get("sanctions_check", "Unknown")
                        regulatory_flags = compliance.get("regulatory_flags", [])
                        compliance_score = compliance.get("compliance_score", "N/A")
                        last_updated = compliance.get("last_updated", "Unknown")
                        
                        flags_text = "\n".join([f"• {flag}" for flag in regulatory_flags[:5]]) if regulatory_flags else "None identified"
                        
                        return [{
                            "type": "text", 
                            "text": f"📋 MetaSleuth Compliance Check for {address[:10]}...\n\n"
                                   f"**Overall Status**: {overall_status}\n"
                                   f"**Sanctions Check**: {sanctions_check}\n"
                                   f"**Compliance Score**: {compliance_score}/100\n"
                                   f"**Last Updated**: {last_updated}\n\n"
                                   f"**Regulatory Flags**:\n{flags_text}\n\n"
                                   f"*Data provided by MetaSleuth API*"
                        }]
                    else:
                        error_text = await response.text()
                        return [{"type": "text", "text": f"❌ API Error: {response.status} - {error_text}"}]
                        
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error fetching compliance check: {str(e)}"}]
