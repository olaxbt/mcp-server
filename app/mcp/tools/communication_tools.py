

import asyncio
import logging
import time
import aiohttp
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .mcp_tool import MCPTool

logger = logging.getLogger(__name__)


class GmailTool(MCPTool):
    def __init__(self):
        self.session = None
        self.gmail_api_url = "https://gmail.googleapis.com/gmail/v1/users/me"

    @property
    def name(self) -> str:
        return "gmail"

    @property
    def description(self) -> str:
        return "Access Gmail data including email search, sending emails, managing labels, and email management"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "search_emails",
                        "get_email",
                        "send_email",
                        "get_labels",
                        "create_label",
                        "delete_label",
                        "get_threads",
                        "get_attachments",
                        "mark_as_read",
                        "mark_as_unread",
                        "move_to_trash",
                        "get_profile"
                    ]
                },
                "api_key": {
                    "type": "string",
                    "description": "Gmail API key (required)"
                },
                "access_token": {
                    "type": "string",
                    "description": "Gmail access token (required)"
                },
                "query": {
                    "type": "string",
                    "description": "Search query for emails (Gmail search syntax)"
                },
                "email_id": {
                    "type": "string",
                    "description": "Gmail message ID"
                },
                "thread_id": {
                    "type": "string",
                    "description": "Gmail thread ID"
                },
                "to": {
                    "type": "string",
                    "description": "Recipient email address"
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject"
                },
                "body": {
                    "type": "string",
                    "description": "Email body content"
                },
                "label_name": {
                    "type": "string",
                    "description": "Label name for creation or management"
                },
                "label_id": {
                    "type": "string",
                    "description": "Label ID for deletion"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "include_spam_trash": {
                    "type": "boolean",
                    "description": "Include spam and trash in search",
                    "default": False
                }
            },
            "required": ["action", "api_key", "access_token"]
        }

    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            access_token = arguments.get("access_token")
            
            if not api_key or not access_token:
                return [{"type": "text", "text": "❌ Error: Gmail API key and access token are required. Please provide both credentials."}]

            if action == "search_emails":
                result = await self._search_emails(**arguments)
            elif action == "get_email":
                result = await self._get_email(**arguments)
            elif action == "send_email":
                result = await self._send_email(**arguments)
            elif action == "get_labels":
                result = await self._get_labels(**arguments)
            elif action == "create_label":
                result = await self._create_label(**arguments)
            elif action == "delete_label":
                result = await self._delete_label(**arguments)
            elif action == "get_threads":
                result = await self._get_threads(**arguments)
            elif action == "get_attachments":
                result = await self._get_attachments(**arguments)
            elif action == "mark_as_read":
                result = await self._mark_as_read(**arguments)
            elif action == "mark_as_unread":
                result = await self._mark_as_unread(**arguments)
            elif action == "move_to_trash":
                result = await self._move_to_trash(**arguments)
            elif action == "get_profile":
                result = await self._get_profile(**arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}

            return [result]
        finally:
            await self._cleanup_session()

    async def _search_emails(self, **kwargs) -> dict:
        """Search for emails using Gmail search syntax."""
        try:
            query = kwargs.get("query", "")
            max_results = kwargs.get("max_results", 10)
            include_spam_trash = kwargs.get("include_spam_trash", False)

            session = await self._get_session()

            url = f"{self.gmail_api_url}/messages"
            params = {
                "q": query,
                "maxResults": max_results,
                "includeSpamTrash": str(include_spam_trash).lower()
            }

            access_token = kwargs.get("access_token")
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"

            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "query": query,
                        "data": {
                            "messages": data.get("messages", []),
                            "next_page_token": data.get("nextPageToken"),
                            "result_size_estimate": data.get("resultSizeEstimate"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to search emails: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to search emails: {str(e)}"
            }

    async def _get_email(self, **kwargs) -> dict:
        """Get detailed information about a specific email."""
        try:
            email_id = kwargs.get("email_id")
            if not email_id:
                return {
                    "success": False,
                    "error": "email_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/messages/{email_id}"
            params = {"format": "full"}

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "email_id": email_id,
                        "data": {
                            "email": data,
                            "headers": data.get("payload", {}).get("headers", []),
                            "body": data.get("payload", {}).get("body", {}),
                            "parts": data.get("payload", {}).get("parts", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get email: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get email: {str(e)}"
            }

    async def _send_email(self, **kwargs) -> dict:
        """Send an email."""
        try:
            to = kwargs.get("to")
            subject = kwargs.get("subject")
            body = kwargs.get("body")

            if not all([to, subject, body]):
                return {
                    "success": False,
                    "error": "to, subject, and body parameters are required"
                }

            session = await self._get_session()

            # Create email message
            message = {
                "raw": self._create_email_message(to, subject, body)
            }

            url = f"{self.gmail_api_url}/messages/send"

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=message, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "to": to,
                        "subject": subject,
                        "data": {
                            "message_id": data.get("id"),
                            "thread_id": data.get("threadId"),
                            "label_ids": data.get("labelIds", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to send email: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send email: {str(e)}"
            }

    async def _get_labels(self, **kwargs) -> dict:
        """Get all Gmail labels."""
        try:
            session = await self._get_session()

            url = f"{self.gmail_api_url}/labels"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "labels": data.get("labels", []),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get labels: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get labels: {str(e)}"
            }

    async def _create_label(self, **kwargs) -> dict:
        """Create a new Gmail label."""
        try:
            label_name = kwargs.get("label_name")
            if not label_name:
                return {
                    "success": False,
                    "error": "label_name parameter is required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/labels"
            label_data = {
                "name": label_name,
                "labelListVisibility": "labelShow",
                "messageListVisibility": "show"
            }

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=label_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "label_name": label_name,
                        "data": {
                            "label": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to create label: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create label: {str(e)}"
            }

    async def _delete_label(self, **kwargs) -> dict:
        """Delete a Gmail label."""
        try:
            label_id = kwargs.get("label_id")
            if not label_id:
                return {
                    "success": False,
                    "error": "label_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/labels/{label_id}"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    return {
                        "success": True,
                        "label_id": label_id,
                        "message": "Label deleted successfully",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to delete label: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete label: {str(e)}"
            }

    async def _get_threads(self, **kwargs) -> dict:
        """Get email threads."""
        try:
            query = kwargs.get("query", "")
            max_results = kwargs.get("max_results", 10)

            session = await self._get_session()

            url = f"{self.gmail_api_url}/threads"
            params = {
                "q": query,
                "maxResults": max_results
            }

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "query": query,
                        "data": {
                            "threads": data.get("threads", []),
                            "next_page_token": data.get("nextPageToken"),
                            "result_size_estimate": data.get("resultSizeEstimate"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get threads: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get threads: {str(e)}"
            }

    async def _get_attachments(self, **kwargs) -> dict:
        """Get email attachments."""
        try:
            email_id = kwargs.get("email_id")
            attachment_id = kwargs.get("attachment_id")

            if not email_id or not attachment_id:
                return {
                    "success": False,
                    "error": "email_id and attachment_id parameters are required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/messages/{email_id}/attachments/{attachment_id}"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "email_id": email_id,
                        "attachment_id": attachment_id,
                        "data": {
                            "attachment": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get attachment: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get attachment: {str(e)}"
            }

    async def _mark_as_read(self, **kwargs) -> dict:
        """Mark an email as read."""
        try:
            email_id = kwargs.get("email_id")
            if not email_id:
                return {
                    "success": False,
                    "error": "email_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/messages/{email_id}/modify"
            modify_data = {
                "removeLabelIds": ["UNREAD"]
            }

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=modify_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "email_id": email_id,
                        "data": {
                            "message": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to mark as read: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to mark as read: {str(e)}"
            }

    async def _mark_as_unread(self, **kwargs) -> dict:
        """Mark an email as unread."""
        try:
            email_id = kwargs.get("email_id")
            if not email_id:
                return {
                    "success": False,
                    "error": "email_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/messages/{email_id}/modify"
            modify_data = {
                "addLabelIds": ["UNREAD"]
            }

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=modify_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "email_id": email_id,
                        "data": {
                            "message": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to mark as unread: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to mark as unread: {str(e)}"
            }

    async def _move_to_trash(self, **kwargs) -> dict:
        """Move an email to trash."""
        try:
            email_id = kwargs.get("email_id")
            if not email_id:
                return {
                    "success": False,
                    "error": "email_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.gmail_api_url}/messages/{email_id}/trash"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "email_id": email_id,
                        "data": {
                            "message": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to move to trash: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to move to trash: {str(e)}"
            }

    async def _get_profile(self, **kwargs) -> dict:
        """Get Gmail profile information."""
        try:
            session = await self._get_session()

            url = f"{self.gmail_api_url}/profile"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "profile": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get profile: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get profile: {str(e)}"
            }

    def _create_email_message(self, to: str, subject: str, body: str) -> str:
        """Create a base64 encoded email message."""
        import base64
        from email.mime.text import MIMEText

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject

        return base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')


class GoogleCalendarTool(MCPTool):
    def __init__(self):
        self.session = None
        self.calendar_api_url = "https://www.googleapis.com/calendar/v3"

    @property
    def name(self) -> str:
        return "google_calendar"

    @property
    def description(self) -> str:
        return "Access Google Calendar data including events, calendars, scheduling, and calendar management"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "list_calendars",
                        "get_calendar",
                        "list_events",
                        "get_event",
                        "create_event",
                        "update_event",
                        "delete_event",
                        "get_free_busy",
                        "get_calendar_list",
                        "create_calendar",
                        "delete_calendar",
                        "get_event_instances"
                    ]
                },
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID (use 'primary' for primary calendar)"
                },
                "event_id": {
                    "type": "string",
                    "description": "Event ID"
                },
                "time_min": {
                    "type": "string",
                    "description": "Start time for event queries (ISO 8601 format)"
                },
                "time_max": {
                    "type": "string",
                    "description": "End time for event queries (ISO 8601 format)"
                },
                "summary": {
                    "type": "string",
                    "description": "Event summary/title"
                },
                "description": {
                    "type": "string",
                    "description": "Event description"
                },
                "location": {
                    "type": "string",
                    "description": "Event location"
                },
                "start_time": {
                    "type": "string",
                    "description": "Event start time (ISO 8601 format)"
                },
                "end_time": {
                    "type": "string",
                    "description": "Event end time (ISO 8601 format)"
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of attendee email addresses"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 10
                },
                "single_events": {
                    "type": "boolean",
                    "description": "Whether to expand recurring events",
                    "default": True
                },
                "order_by": {
                    "type": "string",
                    "description": "Order of events (startTime, updated)",
                    "default": "startTime"
                },
                "api_key": {
                    "type": "string",
                    "description": "Google Calendar API key (required)"
                },
                "access_token": {
                    "type": "string",
                    "description": "Google Calendar access token (required)"
                }
            },
            "required": ["action", "api_key", "access_token"]
        }

    async def _get_session(self):
        """Get or create aiohttp session."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _cleanup_session(self):
        """Clean up aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            action = arguments.get("action")
            api_key = arguments.get("api_key")
            access_token = arguments.get("access_token")
            
            if not api_key or not access_token:
                return [{"type": "text", "text": "❌ Error: Google Calendar API key and access token are required. Please provide both credentials."}]

            if action == "list_calendars":
                result = await self._list_calendars(**arguments)
            elif action == "get_calendar":
                result = await self._get_calendar(**arguments)
            elif action == "list_events":
                result = await self._list_events(**arguments)
            elif action == "get_event":
                result = await self._get_event(**arguments)
            elif action == "create_event":
                result = await self._create_event(**arguments)
            elif action == "update_event":
                result = await self._update_event(**arguments)
            elif action == "delete_event":
                result = await self._delete_event(**arguments)
            elif action == "get_free_busy":
                result = await self._get_free_busy(**arguments)
            elif action == "get_calendar_list":
                result = await self._get_calendar_list(**arguments)
            elif action == "create_calendar":
                result = await self._create_calendar(**arguments)
            elif action == "delete_calendar":
                result = await self._delete_calendar(**arguments)
            elif action == "get_event_instances":
                result = await self._get_event_instances(**arguments)
            else:
                result = {"type": "text", "text": f"❌ Error: Unknown action: {action}"}

            return [result]
        finally:
            await self._cleanup_session()

    async def _list_calendars(self, **kwargs) -> dict:
        """List all calendars."""
        try:
            session = await self._get_session()

            url = f"{self.calendar_api_url}/users/me/calendarList"

            access_token = kwargs.get("access_token")
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "calendars": data.get("items", []),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to list calendars: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list calendars: {str(e)}"
            }

    async def _get_calendar(self, **kwargs) -> dict:
        """Get a specific calendar."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")

            session = await self._get_session()

            url = f"{self.calendar_api_url}/calendars/{calendar_id}"

            access_token = kwargs.get("access_token")
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "data": {
                            "calendar": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get calendar: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get calendar: {str(e)}"
            }

    async def _list_events(self, **kwargs) -> dict:
        """List events from a calendar."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")
            time_min = kwargs.get("time_min")
            time_max = kwargs.get("time_max")
            max_results = kwargs.get("max_results", 10)
            single_events = kwargs.get("single_events", True)
            order_by = kwargs.get("order_by", "startTime")

            session = await self._get_session()

            url = f"{self.calendar_api_url}/calendars/{calendar_id}/events"
            params = {
                "maxResults": max_results,
                "singleEvents": str(single_events).lower(),
                "orderBy": order_by
            }

            if time_min:
                params["timeMin"] = time_min
            if time_max:
                params["timeMax"] = time_max

            access_token = kwargs.get("access_token")
            headers = {}
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"

            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "data": {
                            "events": data.get("items", []),
                            "next_page_token": data.get("nextPageToken"),
                            "updated": data.get("updated"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to list events: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to list events: {str(e)}"
            }

    async def _get_event(self, **kwargs) -> dict:
        """Get a specific event."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")
            event_id = kwargs.get("event_id")

            if not event_id:
                return {
                    "success": False,
                    "error": "event_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.calendar_api_url}/calendars/{calendar_id}/events/{event_id}"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "event_id": event_id,
                        "data": {
                            "event": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get event: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get event: {str(e)}"
            }

    async def _create_event(self, **kwargs) -> dict:
        """Create a new event."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")
            summary = kwargs.get("summary")
            description = kwargs.get("description")
            location = kwargs.get("location")
            start_time = kwargs.get("start_time")
            end_time = kwargs.get("end_time")
            attendees = kwargs.get("attendees", [])

            if not all([summary, start_time, end_time]):
                return {
                    "success": False,
                    "error": "summary, start_time, and end_time parameters are required"
                }

            session = await self._get_session()

            event_data = {
                "summary": summary,
                "description": description,
                "location": location,
                "start": {
                    "dateTime": start_time,
                    "timeZone": "UTC"
                },
                "end": {
                    "dateTime": end_time,
                    "timeZone": "UTC"
                }
            }

            if attendees:
                event_data["attendees"] = [{"email": email} for email in attendees]

            url = f"{self.calendar_api_url}/calendars/{calendar_id}/events"

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=event_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "data": {
                            "event": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to create event: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create event: {str(e)}"
            }

    async def _update_event(self, **kwargs) -> dict:
        """Update an existing event."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")
            event_id = kwargs.get("event_id")
            summary = kwargs.get("summary")
            description = kwargs.get("description")
            location = kwargs.get("location")
            start_time = kwargs.get("start_time")
            end_time = kwargs.get("end_time")
            attendees = kwargs.get("attendees", [])

            if not event_id:
                return {
                    "success": False,
                    "error": "event_id parameter is required"
                }

            session = await self._get_session()

            event_data = {}
            if summary:
                event_data["summary"] = summary
            if description:
                event_data["description"] = description
            if location:
                event_data["location"] = location
            if start_time:
                event_data["start"] = {
                    "dateTime": start_time,
                    "timeZone": "UTC"
                }
            if end_time:
                event_data["end"] = {
                    "dateTime": end_time,
                    "timeZone": "UTC"
                }
            if attendees:
                event_data["attendees"] = [{"email": email} for email in attendees]

            url = f"{self.calendar_api_url}/calendars/{calendar_id}/events/{event_id}"

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.put(url, json=event_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "event_id": event_id,
                        "data": {
                            "event": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to update event: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update event: {str(e)}"
            }

    async def _delete_event(self, **kwargs) -> dict:
        """Delete an event."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")
            event_id = kwargs.get("event_id")

            if not event_id:
                return {
                    "success": False,
                    "error": "event_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.calendar_api_url}/calendars/{calendar_id}/events/{event_id}"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "event_id": event_id,
                        "message": "Event deleted successfully",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to delete event: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete event: {str(e)}"
            }

    async def _get_free_busy(self, **kwargs) -> dict:
        """Get free/busy information for calendars."""
        try:
            time_min = kwargs.get("time_min")
            time_max = kwargs.get("time_max")
            calendar_ids = kwargs.get("calendar_ids", ["primary"])

            if not all([time_min, time_max]):
                return {
                    "success": False,
                    "error": "time_min and time_max parameters are required"
                }

            session = await self._get_session()

            url = f"{self.calendar_api_url}/freeBusy"

            free_busy_data = {
                "timeMin": time_min,
                "timeMax": time_max,
                "items": [{"id": cal_id} for cal_id in calendar_ids]
            }

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=free_busy_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "free_busy": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get free/busy: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get free/busy: {str(e)}"
            }

    async def _get_calendar_list(self, **kwargs) -> dict:
        """Get the list of calendars."""
        try:
            session = await self._get_session()

            url = f"{self.calendar_api_url}/users/me/calendarList"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "calendars": data.get("items", []),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get calendar list: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get calendar list: {str(e)}"
            }

    async def _create_calendar(self, **kwargs) -> dict:
        """Create a new calendar."""
        try:
            summary = kwargs.get("summary")
            description = kwargs.get("description")
            time_zone = kwargs.get("time_zone", "UTC")

            if not summary:
                return {
                    "success": False,
                    "error": "summary parameter is required"
                }

            session = await self._get_session()

            calendar_data = {
                "summary": summary,
                "description": description,
                "timeZone": time_zone
            }

            url = f"{self.calendar_api_url}/calendars"

            headers = {"Content-Type": "application/json"}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.post(url, json=calendar_data, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "data": {
                            "calendar": data,
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to create calendar: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create calendar: {str(e)}"
            }

    async def _delete_calendar(self, **kwargs) -> dict:
        """Delete a calendar."""
        try:
            calendar_id = kwargs.get("calendar_id")

            if not calendar_id:
                return {
                    "success": False,
                    "error": "calendar_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.calendar_api_url}/calendars/{calendar_id}"

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.delete(url, headers=headers) as response:
                if response.status == 204:
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "message": "Calendar deleted successfully",
                        "timestamp": datetime.now().isoformat()
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to delete calendar: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete calendar: {str(e)}"
            }

    async def _get_event_instances(self, **kwargs) -> dict:
        """Get instances of a recurring event."""
        try:
            calendar_id = kwargs.get("calendar_id", "primary")
            event_id = kwargs.get("event_id")
            time_min = kwargs.get("time_min")
            time_max = kwargs.get("time_max")
            max_results = kwargs.get("max_results", 10)

            if not event_id:
                return {
                    "success": False,
                    "error": "event_id parameter is required"
                }

            session = await self._get_session()

            url = f"{self.calendar_api_url}/calendars/{calendar_id}/events/{event_id}/instances"
            params = {"maxResults": max_results}

            if time_min:
                params["timeMin"] = time_min
            if time_max:
                params["timeMax"] = time_max

            headers = {}
            if self.access_token:
                headers["Authorization"] = f"Bearer {self.access_token}"

            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "calendar_id": calendar_id,
                        "event_id": event_id,
                        "data": {
                            "instances": data.get("items", []),
                            "next_page_token": data.get("nextPageToken"),
                            "timestamp": datetime.now().isoformat()
                        }
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Failed to get event instances: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get event instances: {str(e)}"
            }






class SlackTool(MCPTool):
    """Slack API integration tool for messaging, channel management, and team collaboration"""
    
    def __init__(self):
        self.session = None
        # Note: Slack tokens will be provided by user
        self.base_url = "https://slack.com/api"
    
    @property
    def name(self) -> str:
        return "slack"
    
    @property
    def description(self) -> str:
        return "Slack API integration for messaging, channel management, user operations, and team collaboration"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "send_message",
                        "send_direct_message",
                        "get_channel_history",
                        "get_direct_message_history",
                        "list_channels",
                        "get_channel_info",
                        "join_channel",
                        "leave_channel",
                        "create_channel",
                        "archive_channel",
                        "list_users",
                        "get_user_info",
                        "get_user_presence",
                        "list_conversations",
                        "get_conversation_history",
                        "send_thread_reply",
                        "upload_file",
                        "get_file_info",
                        "list_files",
                        "search_messages",
                        "get_team_info",
                        "get_emoji_list",
                        "add_reaction",
                        "remove_reaction",
                        "get_reactions"
                    ],
                    "description": "The action to perform"
                },
                "channel": {
                    "type": "string",
                    "description": "Channel ID or name (with #)"
                },
                "user": {
                    "type": "string",
                    "description": "User ID or username"
                },
                "message": {
                    "type": "string",
                    "description": "Message text to send"
                },
                "thread_ts": {
                    "type": "string",
                    "description": "Thread timestamp for replies"
                },
                "ts": {
                    "type": "string",
                    "description": "Message timestamp"
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 1000,
                    "default": 100,
                    "description": "Maximum number of results to return"
                },
                "oldest": {
                    "type": "string",
                    "description": "Start of time range (timestamp)"
                },
                "latest": {
                    "type": "string",
                    "description": "End of time range (timestamp)"
                },
                "inclusive": {
                    "type": "boolean",
                    "default": False,
                    "description": "Include messages with oldest or latest timestamps"
                },
                "channel_name": {
                    "type": "string",
                    "description": "Name for new channel (without #)"
                },
                "is_private": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether channel should be private"
                },
                "query": {
                    "type": "string",
                    "description": "Search query for messages or files"
                },
                "count": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 20,
                    "description": "Number of results to return"
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "description": "Page number for pagination"
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to file to upload"
                },
                "file_title": {
                    "type": "string",
                    "description": "Title for uploaded file"
                },
                "file_comment": {
                    "type": "string",
                    "description": "Comment for uploaded file"
                },
                "file_id": {
                    "type": "string",
                    "description": "File ID for file operations"
                },
                "reaction": {
                    "type": "string",
                    "description": "Emoji reaction (e.g., 'thumbsup')"
                },
                "types": {
                    "type": "string",
                    "description": "Comma-separated list of conversation types (public_channel, private_channel, mpim, im)"
                },
                "exclude_archived": {
                    "type": "boolean",
                    "default": True,
                    "description": "Exclude archived conversations"
                },
                "bot_token": {
                    "type": "string",
                    "description": "Slack Bot Token (required)"
                },
                "user_token": {
                    "type": "string",
                    "description": "Slack User Token (required)"
                }
            },
            "required": ["action", "bot_token", "user_token"]
        }
    
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
    
    async def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make authenticated request to Slack API"""
        try:
            session = await self._get_session()
            
            bot_token = kwargs.get("bot_token")
            user_token = kwargs.get("user_token")
            
            if not bot_token and not user_token:
                return {"type": "text", "text": "❌ Error: Slack tokens not configured. Please provide both bot_token and user_token."}
            
            # Use bot token if available, otherwise user token
            token = bot_token or user_token
            
            url = f"{self.base_url}/{endpoint}"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8"
            }
            
            if method.upper() == "GET":
                if params is None:
                    params = {}
                params["token"] = token
                async with session.get(url, headers=headers, params=params) as response:
                    return await self._handle_response(response)
            elif method.upper() == "POST":
                if data is None:
                    data = {}
                data["token"] = token
                async with session.post(url, headers=headers, json=data) as response:
                    return await self._handle_response(response)
            else:
                return {"type": "text", "text": f"❌ Error: Unsupported HTTP method: {method}"}
                
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    async def _handle_response(self, response) -> Dict[str, Any]:
        """Handle API response"""
        try:
            if response.status == 200:
                data = await response.json()
                if data.get("ok"):
                    return {"success": True, "data": data}
                else:
                    return {"success": False, "error": f"Slack API error: {data.get('error', 'Unknown error')}"}
            else:
                error_text = await response.text()
                return {"success": False, "error": f"HTTP {response.status}: {error_text}"}
        except Exception as e:
            return {"success": False, "error": f"Response parsing failed: {str(e)}"}
    
    async def _send_message(self, **kwargs) -> List[Dict[str, Any]]:
        """Send a message to a channel"""
        channel = kwargs.get("channel")
        message = kwargs.get("message")
        thread_ts = kwargs.get("thread_ts")
        
        if not channel or not message:
            return [{"success": False, "error": "channel and message parameters are required"}]
        
        data = {
            "channel": channel,
            "text": message
        }
        
        if thread_ts:
            data["thread_ts"] = thread_ts
        
        result = await self._make_request("POST", "chat.postMessage", data=data)
        return [result]
    
    async def _send_direct_message(self, **kwargs) -> List[Dict[str, Any]]:
        """Send a direct message to a user"""
        user = kwargs.get("user")
        message = kwargs.get("message")
        
        if not user or not message:
            return [{"success": False, "error": "user and message parameters are required"}]
        
        # First, open a DM with the user
        open_dm_data = {"users": user}
        open_result = await self._make_request("POST", "conversations.open", data=open_dm_data)
        
        if not open_result.get("success"):
            return [open_result]
        
        channel_id = open_result["data"]["channel"]["id"]
        
        # Send the message
        message_data = {
            "channel": channel_id,
            "text": message
        }
        
        result = await self._make_request("POST", "chat.postMessage", data=message_data)
        return [result]
    
    async def _get_channel_history(self, **kwargs) -> List[Dict[str, Any]]:
        """Get message history for a channel"""
        channel = kwargs.get("channel")
        limit = min(kwargs.get("limit", 100), 1000)
        oldest = kwargs.get("oldest")
        latest = kwargs.get("latest")
        inclusive = kwargs.get("inclusive", False)
        
        if not channel:
            return [{"success": False, "error": "channel parameter is required"}]
        
        params = {
            "channel": channel,
            "limit": limit,
            "inclusive": inclusive
        }
        
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        
        result = await self._make_request("GET", "conversations.history", params=params)
        return [result]
    
    async def _get_direct_message_history(self, **kwargs) -> List[Dict[str, Any]]:
        """Get message history for a direct message conversation"""
        user = kwargs.get("user")
        limit = min(kwargs.get("limit", 100), 1000)
        oldest = kwargs.get("oldest")
        latest = kwargs.get("latest")
        
        if not user:
            return [{"success": False, "error": "user parameter is required"}]
        
        # First, open a DM with the user
        open_dm_data = {"users": user}
        open_result = await self._make_request("POST", "conversations.open", data=open_dm_data)
        
        if not open_result.get("success"):
            return [open_result]
        
        channel_id = open_result["data"]["channel"]["id"]
        
        # Get conversation history
        params = {
            "channel": channel_id,
            "limit": limit
        }
        
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        
        result = await self._make_request("GET", "conversations.history", params=params)
        return [result]
    
    async def _list_channels(self, **kwargs) -> List[Dict[str, Any]]:
        """List all channels"""
        exclude_archived = kwargs.get("exclude_archived", True)
        limit = min(kwargs.get("limit", 100), 1000)
        
        params = {
            "limit": limit,
            "exclude_archived": exclude_archived
        }
        
        result = await self._make_request("GET", "conversations.list", params=params)
        return [result]
    
    async def _get_channel_info(self, **kwargs) -> List[Dict[str, Any]]:
        """Get information about a specific channel"""
        channel = kwargs.get("channel")
        
        if not channel:
            return [{"success": False, "error": "channel parameter is required"}]
        
        params = {"channel": channel}
        result = await self._make_request("GET", "conversations.info", params=params)
        return [result]
    
    async def _join_channel(self, **kwargs) -> List[Dict[str, Any]]:
        """Join a channel"""
        channel = kwargs.get("channel")
        
        if not channel:
            return [{"success": False, "error": "channel parameter is required"}]
        
        data = {"name": channel}
        result = await self._make_request("POST", "conversations.join", data=data)
        return [result]
    
    async def _leave_channel(self, **kwargs) -> List[Dict[str, Any]]:
        """Leave a channel"""
        channel = kwargs.get("channel")
        
        if not channel:
            return [{"success": False, "error": "channel parameter is required"}]
        
        data = {"channel": channel}
        result = await self._make_request("POST", "conversations.leave", data=data)
        return [result]
    
    async def _create_channel(self, **kwargs) -> List[Dict[str, Any]]:
        """Create a new channel"""
        channel_name = kwargs.get("channel_name")
        is_private = kwargs.get("is_private", False)
        
        if not channel_name:
            return [{"success": False, "error": "channel_name parameter is required"}]
        
        data = {
            "name": channel_name,
            "is_private": is_private
        }
        
        result = await self._make_request("POST", "conversations.create", data=data)
        return [result]
    
    async def _archive_channel(self, **kwargs) -> List[Dict[str, Any]]:
        """Archive a channel"""
        channel = kwargs.get("channel")
        
        if not channel:
            return [{"success": False, "error": "channel parameter is required"}]
        
        data = {"channel": channel}
        result = await self._make_request("POST", "conversations.archive", data=data)
        return [result]
    
    async def _list_users(self, **kwargs) -> List[Dict[str, Any]]:
        """List all users"""
        limit = min(kwargs.get("limit", 100), 1000)
        
        params = {"limit": limit}
        result = await self._make_request("GET", "users.list", params=params)
        return [result]
    
    async def _get_user_info(self, **kwargs) -> List[Dict[str, Any]]:
        """Get information about a specific user"""
        user = kwargs.get("user")
        
        if not user:
            return [{"success": False, "error": "user parameter is required"}]
        
        params = {"user": user}
        result = await self._make_request("GET", "users.info", params=params)
        return [result]
    
    async def _get_user_presence(self, **kwargs) -> List[Dict[str, Any]]:
        """Get user's presence status"""
        user = kwargs.get("user")
        
        if not user:
            return [{"success": False, "error": "user parameter is required"}]
        
        params = {"user": user}
        result = await self._make_request("GET", "users.getPresence", params=params)
        return [result]
    
    async def _list_conversations(self, **kwargs) -> List[Dict[str, Any]]:
        """List conversations (channels, DMs, etc.)"""
        types = kwargs.get("types", "public_channel,private_channel,mpim,im")
        exclude_archived = kwargs.get("exclude_archived", True)
        limit = min(kwargs.get("limit", 100), 1000)
        
        params = {
            "types": types,
            "exclude_archived": exclude_archived,
            "limit": limit
        }
        
        result = await self._make_request("GET", "conversations.list", params=params)
        return [result]
    
    async def _get_conversation_history(self, **kwargs) -> List[Dict[str, Any]]:
        """Get conversation history"""
        channel = kwargs.get("channel")
        limit = min(kwargs.get("limit", 100), 1000)
        oldest = kwargs.get("oldest")
        latest = kwargs.get("latest")
        
        if not channel:
            return [{"success": False, "error": "channel parameter is required"}]
        
        params = {
            "channel": channel,
            "limit": limit
        }
        
        if oldest:
            params["oldest"] = oldest
        if latest:
            params["latest"] = latest
        
        result = await self._make_request("GET", "conversations.history", params=params)
        return [result]
    
    async def _send_thread_reply(self, **kwargs) -> List[Dict[str, Any]]:
        """Send a reply in a thread"""
        channel = kwargs.get("channel")
        thread_ts = kwargs.get("thread_ts")
        message = kwargs.get("message")
        
        if not channel or not thread_ts or not message:
            return [{"success": False, "error": "channel, thread_ts, and message parameters are required"}]
        
        data = {
            "channel": channel,
            "thread_ts": thread_ts,
            "text": message
        }
        
        result = await self._make_request("POST", "chat.postMessage", data=data)
        return [result]
    
    async def _upload_file(self, **kwargs) -> List[Dict[str, Any]]:
        """Upload a file to Slack"""
        channel = kwargs.get("channel")
        file_path = kwargs.get("file_path")
        file_title = kwargs.get("file_title")
        file_comment = kwargs.get("file_comment")
        
        if not channel or not file_path:
            return [{"success": False, "error": "channel and file_path parameters are required"}]
        
        try:
            session = await self._get_session()
            
            if not self.bot_token and not self.user_token:
                return [{"success": False, "error": "Slack tokens not configured"}]
            
            token = self.bot_token or self.user_token
            
            url = f"{self.base_url}/files.upload"
            
            # Prepare form data
            form_data = aiohttp.FormData()
            form_data.add_field('token', token)
            form_data.add_field('channels', channel)
            
            if file_title:
                form_data.add_field('title', file_title)
            if file_comment:
                form_data.add_field('initial_comment', file_comment)
            
            # Add file
            with open(file_path, 'rb') as f:
                form_data.add_field('file', f, filename=os.path.basename(file_path))
            
            async with session.post(url, data=form_data) as response:
                result = await self._handle_response(response)
                return [result]
                
        except FileNotFoundError:
            return [{"success": False, "error": f"File not found: {file_path}"}]
        except Exception as e:
            return [{"success": False, "error": f"File upload failed: {str(e)}"}]
    
    async def _get_file_info(self, **kwargs) -> List[Dict[str, Any]]:
        """Get information about a specific file"""
        file_id = kwargs.get("file_id")
        
        if not file_id:
            return [{"success": False, "error": "file_id parameter is required"}]
        
        params = {"file": file_id}
        result = await self._make_request("GET", "files.info", params=params)
        return [result]
    
    async def _list_files(self, **kwargs) -> List[Dict[str, Any]]:
        """List files"""
        channel = kwargs.get("channel")
        user = kwargs.get("user")
        count = min(kwargs.get("count", 20), 100)
        page = kwargs.get("page", 1)
        
        params = {
            "count": count,
            "page": page
        }
        
        if channel:
            params["channel"] = channel
        if user:
            params["user"] = user
        
        result = await self._make_request("GET", "files.list", params=params)
        return [result]
    
    async def _search_messages(self, **kwargs) -> List[Dict[str, Any]]:
        """Search for messages"""
        query = kwargs.get("query")
        count = min(kwargs.get("count", 20), 100)
        page = kwargs.get("page", 1)
        
        if not query:
            return [{"success": False, "error": "query parameter is required"}]
        
        params = {
            "query": query,
            "count": count,
            "page": page
        }
        
        result = await self._make_request("GET", "search.messages", params=params)
        return [result]
    
    async def _get_team_info(self, **kwargs) -> List[Dict[str, Any]]:
        """Get team information"""
        result = await self._make_request("GET", "team.info")
        return [result]
    
    async def _get_emoji_list(self, **kwargs) -> List[Dict[str, Any]]:
        """Get list of custom emojis"""
        result = await self._make_request("GET", "emoji.list")
        return [result]
    
    async def _add_reaction(self, **kwargs) -> List[Dict[str, Any]]:
        """Add a reaction to a message"""
        channel = kwargs.get("channel")
        timestamp = kwargs.get("ts")
        reaction = kwargs.get("reaction")
        
        if not channel or not timestamp or not reaction:
            return [{"success": False, "error": "channel, ts, and reaction parameters are required"}]
        
        data = {
            "channel": channel,
            "timestamp": timestamp,
            "name": reaction
        }
        
        result = await self._make_request("POST", "reactions.add", data=data)
        return [result]
    
    async def _remove_reaction(self, **kwargs) -> List[Dict[str, Any]]:
        """Remove a reaction from a message"""
        channel = kwargs.get("channel")
        timestamp = kwargs.get("ts")
        reaction = kwargs.get("reaction")
        
        if not channel or not timestamp or not reaction:
            return [{"success": False, "error": "channel, ts, and reaction parameters are required"}]
        
        data = {
            "channel": channel,
            "timestamp": timestamp,
            "name": reaction
        }
        
        result = await self._make_request("POST", "reactions.remove", data=data)
        return [result]
    
    async def _get_reactions(self, **kwargs) -> List[Dict[str, Any]]:
        """Get reactions for a message"""
        channel = kwargs.get("channel")
        timestamp = kwargs.get("ts")
        
        if not channel or not timestamp:
            return [{"success": False, "error": "channel and ts parameters are required"}]
        
        params = {
            "channel": channel,
            "timestamp": timestamp
        }
        
        result = await self._make_request("GET", "reactions.get", params=params)
        return [result]
    
    async def execute(self, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute Slack API operations"""
        try:
            action = arguments.get("action")
            bot_token = arguments.get("bot_token")
            user_token = arguments.get("user_token")
            
            if not bot_token or not user_token:
                return [{"type": "text", "text": "❌ Error: Both Slack Bot Token and User Token are required. Please provide both credentials."}]
            
            if action == "send_message":
                return await self._send_message(**arguments)
            elif action == "send_direct_message":
                return await self._send_direct_message(**arguments)
            elif action == "get_channel_history":
                return await self._get_channel_history(**arguments)
            elif action == "get_direct_message_history":
                return await self._get_direct_message_history(**arguments)
            elif action == "list_channels":
                return await self._list_channels(**arguments)
            elif action == "get_channel_info":
                return await self._get_channel_info(**arguments)
            elif action == "join_channel":
                return await self._join_channel(**arguments)
            elif action == "leave_channel":
                return await self._leave_channel(**arguments)
            elif action == "create_channel":
                return await self._create_channel(**arguments)
            elif action == "archive_channel":
                return await self._archive_channel(**arguments)
            elif action == "list_users":
                return await self._list_users(**arguments)
            elif action == "get_user_info":
                return await self._get_user_info(**arguments)
            elif action == "get_user_presence":
                return await self._get_user_presence(**arguments)
            elif action == "list_conversations":
                return await self._list_conversations(**arguments)
            elif action == "get_conversation_history":
                return await self._get_conversation_history(**arguments)
            elif action == "send_thread_reply":
                return await self._send_thread_reply(**arguments)
            elif action == "upload_file":
                return await self._upload_file(**arguments)
            elif action == "get_file_info":
                return await self._get_file_info(**arguments)
            elif action == "list_files":
                return await self._list_files(**arguments)
            elif action == "search_messages":
                return await self._search_messages(**arguments)
            elif action == "get_team_info":
                return await self._get_team_info(**arguments)
            elif action == "get_emoji_list":
                return await self._get_emoji_list(**arguments)
            elif action == "add_reaction":
                return await self._add_reaction(**arguments)
            elif action == "remove_reaction":
                return await self._remove_reaction(**arguments)
            elif action == "get_reactions":
                return await self._get_reactions(**arguments)
            else:
                return [{"type": "text", "text": f"❌ Error: Unknown action: {action}"}]
                
        except Exception as e:
            return [{"type": "text", "text": f"❌ Error: Execution error: {str(e)}"}]
        finally:
            await self._cleanup_session()
