"""
Registry client for create-sparc-py (stub).
"""

import requests
import os
import json
from typing import Any, Dict, Optional
from create_sparc_py.utils import logger


class RegistryClient:
    """
    Client for remote template/component registry.
    """

    def __init__(self, base_url: Optional[str] = None, token: Optional[str] = None, mock: bool = False):
        self.base_url = base_url or os.environ.get("SPARC_REGISTRY_URL", "https://registry.example.com/api/v1")
        self.token = token or os.environ.get("SPARC_REGISTRY_TOKEN")
        # Enable mock mode if env var is set
        self.mock = mock or os.environ.get("SPARC_REGISTRY_MOCK") == "1"
        self._mock_data = {"templates": ["minimal_roo", "sparc_default"], "components": ["api", "database"]}
        self.authenticated = False

    def set_mock_data(self, path: str, data: Any):
        """Set mock data for a given path (for tests)."""
        self._mock_data[path] = data

    def get(self, path: str) -> Any:
        if self.mock:
            # If path is a known resource, return the list directly
            if path in self._mock_data:
                return self._mock_data[path]
            # For unknown paths, return a dict with 'item': path (for test parity)
            return {"item": path}
        url = f"{self.base_url}/{path}"
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            logger.info(f"[RegistryClient] GET {url}")
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"RegistryClient GET error: {e}")
            return {"error": str(e), "status": "error"}

    def post(self, path: str, data: Any) -> Any:
        if self.mock:
            return {"posted": True, "path": path, "data": data}
        url = f"{self.base_url}/{path}"
        headers = (
            {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            if self.token
            else {"Content-Type": "application/json"}
        )
        try:
            logger.info(f"[RegistryClient] POST {url} with data: {data}")
            resp = requests.post(url, headers=headers, data=json.dumps(data))
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"RegistryClient POST error: {e}")
            return {"error": str(e), "status": "error"}

    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        if self.mock:
            api_key = credentials.get("api_key")
            return api_key == "good"
        api_key = credentials.get("api_key")
        if not api_key:
            return False
        self.token = api_key
        self.authenticated = True
        return True

    def _get_auth_headers(self) -> Dict[str, str]:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers


# Singleton instance
registry_client = RegistryClient()
