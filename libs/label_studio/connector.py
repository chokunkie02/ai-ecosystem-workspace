"""
Label Studio REST API Connector Client Library
Provides helper class LabelStudioConnector to create projects, import tasks, and fetch annotations.
"""

import os
from typing import Any, Dict, List, Optional
import httpx


class LabelStudioConnector:
    """
    Label Studio REST API Connector for project management, task importing, and data synchronization.
    """

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize Label Studio API Client.
        """
        self.url = (url or os.getenv("LABEL_STUDIO_URL", "http://localhost:8080")).rstrip("/")
        self.api_key = api_key or os.getenv("LABEL_STUDIO_API_KEY", "")
        self.headers = {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json",
        }
        self.timeout = timeout

    async def create_project(
        self,
        title: str,
        description: str = "",
        label_config: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new project in Label Studio.
        """
        default_config = (
            "<View><Text name='text' value='$text'/><Choices name='sentiment' toName='text'>"
            "<Choice value='Positive'/><Choice value='Negative'/></Choices></View>"
        )
        payload = {
            "title": title,
            "description": description,
            "label_config": label_config or default_config,
        }
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.url}/api/projects/",
                json=payload,
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_projects(self) -> List[Dict[str, Any]]:
        """
        Retrieve list of all active projects.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.url}/api/projects/",
                headers=self.headers,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("results", data) if isinstance(data, dict) else data

    async def get_project(self, project_id: int) -> Dict[str, Any]:
        """
        Get details of a specific project.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.url}/api/projects/{project_id}/",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def import_tasks(
        self, project_id: int, tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Import annotation tasks into specified project.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.url}/api/projects/{project_id}/import",
                json=tasks,
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def get_tasks(self, project_id: int) -> List[Dict[str, Any]]:
        """
        Fetch all tasks and annotations for specified project.
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                f"{self.url}/api/projects/{project_id}/tasks",
                headers=self.headers,
            )
            resp.raise_for_status()
            return resp.json()

    async def sync_data(
        self, project_id: int, source_type: str = "s3", config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Trigger cloud storage data sync or create storage connection for project.
        """
        endpoint = f"{self.url}/api/storages/{source_type}/"
        payload = {"project": project_id, **(config or {})}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                endpoint,
                json=payload,
                headers=self.headers,
            )
            if resp.status_code in (200, 201):
                return resp.json()
            return {"status": "sync_requested", "project_id": project_id, "source_type": source_type}
