import aiohttp
import logging
from typing import Dict, Any, List
from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)

class ApolloTool(MCPTool):
    """Tool for accessing Apollo.io business intelligence and lead generation APIs"""
    
    @property
    def name(self) -> str:
        return "apollo"
    
    @property
    def description(self) -> str:
        return "Access Apollo.io business intelligence data including people search, organization search, job postings, company information, and news articles."
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "search_people",
                        "search_organizations", 
                        "get_job_postings",
                        "get_organization_info",
                        "search_news_articles"
                    ]
                },
                "api_key": {
                    "type": "string",
                    "description": "Apollo API key (required)"
                },
                "query": {
                    "type": "string",
                    "description": "Search query or keywords"
                },
                "company_name": {
                    "type": "string", 
                    "description": "Company name for search or organization ID"
                },
                "job_title": {
                    "type": "string",
                    "description": "Job title for people search"
                },
                "industry": {
                    "type": "string",
                    "description": "Industry filter"
                },
                "location": {
                    "type": "string",
                    "description": "Location filter (city, state, country)"
                },
                "company_size": {
                    "type": "string",
                    "description": "Company size filter (1-10, 11-50, 51-200, etc.)"
                },
                "seniority": {
                    "type": "string",
                    "description": "Seniority level (VP, Director, Manager, etc.)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results",
                    "default": 10
                }
            },
            "required": ["action", "api_key"]
        }
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the Apollo tool"""
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            
            if not api_key:
                return [{"type": "text", "text": "❌ Error: Apollo API key is required. Please provide your API key."}]
            
            if action == "search_people":
                return await self._search_people(arguments, api_key)
            elif action == "search_organizations":
                return await self._search_organizations(arguments, api_key)
            elif action == "get_job_postings":
                return await self._get_job_postings(arguments, api_key)
            elif action == "get_organization_info":
                return await self._get_organization_info(arguments, api_key)
            elif action == "search_news_articles":
                return await self._search_news_articles(arguments, api_key)
            else:
                return [{"type": "text", "text": f"❌ Unknown action: {action}"}]
                
        except Exception as e:
            logger.error(f"Error in Apollo tool: {e}")
            return [{"type": "text", "text": f"❌ Error: {str(e)}"}]
    
    async def _search_people(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Search for people using Apollo People Search API"""
        url = "https://api.apollo.io/api/v1/mixed_people/search"
        
        # Build search parameters
        search_params = {}
        if arguments.get("query"):
            search_params["q_keywords"] = arguments["query"]
        if arguments.get("job_title"):
            search_params["q_titles"] = [arguments["job_title"]]
        if arguments.get("company_name"):
            search_params["q_organization_name"] = arguments["company_name"]
        if arguments.get("industry"):
            search_params["q_organization_industries"] = [arguments["industry"]]
        if arguments.get("location"):
            search_params["q_organization_locations"] = [arguments["location"]]
        if arguments.get("company_size"):
            search_params["q_organization_size_ranges"] = [arguments["company_size"]]
        if arguments.get("seniority"):
            search_params["q_seniority_levels"] = [arguments["seniority"]]
        
        payload = {
            "api_key": api_key,
            "page": 1,
            "per_page": arguments.get("limit", 10),
            **search_params
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    people = data.get("people", [])
                    
                    if not people:
                        return [{"type": "text", "text": "🔍 No people found matching your search criteria."}]
                    
                    result = f"✅ Found {len(people)} people:\n\n"
                    for person in people:
                        result += f"👤 **{person.get('name', 'N/A')}**\n"
                        result += f"   Title: {person.get('title', 'N/A')}\n"
                        result += f"   Company: {person.get('organization_name', 'N/A')}\n"
                        result += f"   Location: {person.get('location', 'N/A')}\n"
                        result += f"   LinkedIn: {person.get('linkedin_url', 'N/A')}\n\n"
                    
                    return [{"type": "text", "text": result}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to search people: {response.status} - {await response.text()}"}]
    
    async def _search_organizations(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Search for organizations using Apollo Organization Search API"""
        url = "https://api.apollo.io/api/v1/mixed_companies/search"
        
        # Build search parameters
        search_params = {}
        if arguments.get("query"):
            search_params["q_keywords"] = arguments["query"]
        if arguments.get("company_name"):
            search_params["q_name"] = arguments["company_name"]
        if arguments.get("industry"):
            search_params["q_industries"] = [arguments["industry"]]
        if arguments.get("location"):
            search_params["q_locations"] = [arguments["location"]]
        if arguments.get("company_size"):
            search_params["q_size_ranges"] = [arguments["company_size"]]
        
        payload = {
            "api_key": api_key,
            "page": 1,
            "per_page": arguments.get("limit", 10),
            **search_params
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    organizations = data.get("organizations", [])
                    
                    if not organizations:
                        return [{"type": "text", "text": "🔍 No organizations found matching your search criteria."}]
                    
                    result = f"✅ Found {len(organizations)} organizations:\n\n"
                    for org in organizations:
                        result += f"🏢 **{org.get('name', 'N/A')}**\n"
                        result += f"   Industry: {org.get('industry', 'N/A')}\n"
                        result += f"   Size: {org.get('size_range', 'N/A')}\n"
                        result += f"   Location: {org.get('location', 'N/A')}\n"
                        result += f"   Website: {org.get('website_url', 'N/A')}\n"
                        result += f"   LinkedIn: {org.get('linkedin_url', 'N/A')}\n\n"
                    
                    return [{"type": "text", "text": result}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to search organizations: {response.status} - {await response.text()}"}]
    
    async def _get_job_postings(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Get job postings for an organization using Apollo Job Postings API"""
        company_name = arguments.get("company_name")
        if not company_name:
            return [{"type": "text", "text": "❌ Company name is required to get job postings."}]
        
        # First, search for the organization to get its ID
        org_id = await self._get_organization_id(company_name, api_key)
        if not org_id:
            return [{"type": "text", "text": f"❌ Could not find organization: {company_name}"}]
        
        url = f"https://api.apollo.io/api/v1/organizations/{org_id}/job_postings"
        
        payload = {
            "api_key": api_key,
            "page": 1,
            "per_page": arguments.get("limit", 10)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    job_postings = data.get("job_postings", [])
                    
                    if not job_postings:
                        return [{"type": "text", "text": f"🔍 No job postings found for {company_name}."}]
                    
                    result = f"✅ Found {len(job_postings)} job postings at {company_name}:\n\n"
                    for job in job_postings:
                        result += f"💼 **{job.get('title', 'N/A')}**\n"
                        result += f"   Location: {job.get('location', 'N/A')}\n"
                        result += f"   Type: {job.get('employment_type', 'N/A')}\n"
                        result += f"   Posted: {job.get('posted_date', 'N/A')}\n"
                        result += f"   URL: {job.get('url', 'N/A')}\n\n"
                    
                    return [{"type": "text", "text": result}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get job postings: {response.status} - {await response.text()}"}]
    
    async def _get_organization_info(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Get complete organization information using Apollo Organization Info API"""
        company_name = arguments.get("company_name")
        if not company_name:
            return [{"type": "text", "text": "❌ Company name is required to get organization info."}]
        
        # First, search for the organization to get its ID
        org_id = await self._get_organization_id(company_name, api_key)
        if not org_id:
            return [{"type": "text", "text": f"❌ Could not find organization: {company_name}"}]
        
        url = f"https://api.apollo.io/api/v1/organizations/{org_id}"
        
        payload = {
            "api_key": api_key
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    organization = data.get("organization", {})
                    
                    if not organization:
                        return [{"type": "text", "text": f"❌ No organization information found for {company_name}."}]
                    
                    result = f"🏢 **Complete Organization Information for {organization.get('name', 'N/A')}**\n\n"
                    result += f"📊 **Company Details:**\n"
                    result += f"   Industry: {organization.get('industry', 'N/A')}\n"
                    result += f"   Size: {organization.get('size_range', 'N/A')}\n"
                    result += f"   Founded: {organization.get('founded_year', 'N/A')}\n"
                    result += f"   Revenue: {organization.get('estimated_annual_revenue', 'N/A')}\n\n"
                    
                    result += f"📍 **Location:**\n"
                    result += f"   Address: {organization.get('address', 'N/A')}\n"
                    result += f"   City: {organization.get('city', 'N/A')}\n"
                    result += f"   State: {organization.get('state', 'N/A')}\n"
                    result += f"   Country: {organization.get('country', 'N/A')}\n\n"
                    
                    result += f"🌐 **Online Presence:**\n"
                    result += f"   Website: {organization.get('website_url', 'N/A')}\n"
                    result += f"   LinkedIn: {organization.get('linkedin_url', 'N/A')}\n"
                    result += f"   Twitter: {organization.get('twitter_url', 'N/A')}\n\n"
                    
                    result += f"📈 **Business Info:**\n"
                    result += f"   Description: {organization.get('description', 'N/A')}\n"
                    result += f"   Keywords: {', '.join(organization.get('keywords', []))}\n"
                    
                    return [{"type": "text", "text": result}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to get organization info: {response.status} - {await response.text()}"}]
    
    async def _search_news_articles(self, arguments: Dict[str, Any], api_key: str) -> List[Dict[str, Any]]:
        """Search for news articles using Apollo News Articles Search API"""
        url = "https://api.apollo.io/api/v1/news_articles/search"
        
        # Build search parameters
        search_params = {}
        if arguments.get("query"):
            search_params["q_keywords"] = arguments["query"]
        if arguments.get("company_name"):
            search_params["q_organization_name"] = arguments["company_name"]
        if arguments.get("industry"):
            search_params["q_organization_industries"] = [arguments["industry"]]
        
        payload = {
            "api_key": api_key,
            "page": 1,
            "per_page": arguments.get("limit", 10),
            **search_params
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("news_articles", [])
                    
                    if not articles:
                        return [{"type": "text", "text": "🔍 No news articles found matching your search criteria."}]
                    
                    result = f"📰 Found {len(articles)} news articles:\n\n"
                    for article in articles:
                        result += f"📄 **{article.get('title', 'N/A')}**\n"
                        result += f"   Source: {article.get('source', 'N/A')}\n"
                        result += f"   Published: {article.get('published_date', 'N/A')}\n"
                        result += f"   Summary: {article.get('summary', 'N/A')[:200]}...\n"
                        result += f"   URL: {article.get('url', 'N/A')}\n\n"
                    
                    return [{"type": "text", "text": result}]
                else:
                    return [{"type": "text", "text": f"❌ Failed to search news articles: {response.status} - {await response.text()}"}]
    
    async def _get_organization_id(self, company_name: str, api_key: str) -> str:
        """Helper method to get organization ID from company name"""
        url = "https://api.apollo.io/api/v1/mixed_companies/search"
        
        payload = {
            "api_key": api_key,
            "q_name": company_name,
            "page": 1,
            "per_page": 1
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        organizations = data.get("organizations", [])
                        if organizations:
                            return organizations[0].get("id")
        except Exception as e:
            logger.error(f"Error getting organization ID: {e}")
        
        return None
