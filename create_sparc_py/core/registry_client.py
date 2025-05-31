"""
Registry client for create-sparc-py (stub).
"""

import requests
from typing import Any, Dict, Optional
from create_sparc_py.utils import logger


class RegistryClient:
    """
    Client for remote template/component registry.
    """

    def __init__(self, base_url: Optional[str] = None, mock: bool = False):
        self.base_url = base_url or "https://registry.example.com/api/v1"
        self.authenticated = False
        self.token = None
        self.mock = mock
        self._mock_data = {}

    def set_mock_data(self, path: str, data: Any):
        """Set mock data for a given path (for tests)."""
        self._mock_data[path] = data

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """GET a resource from the registry (real or mock)."""
        if self.mock:
            return self._mock_data.get(path, {"error": "Not found in mock registry", "status": "error"})
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        all_headers = self._get_auth_headers()
        if headers:
            all_headers.update(headers)
        try:
            logger.info(f"[RegistryClient] GET {url}")
            resp = requests.get(url, headers=all_headers, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            return {"error": str(e), "status": "error", "code": e.response.status_code if e.response else None}
        except Exception as e:
            logger.error(f"RegistryClient GET error: {e}")
            return {"error": str(e), "status": "error"}

    def post(
        self, path: str, data: Dict[str, Any], headers: Optional[Dict[str, str]] = None, timeout: int = 10
    ) -> Dict[str, Any]:
        """POST data to the registry (real or mock)."""
        if self.mock:
            self._mock_data[path] = data
            return {"mock": True, "posted": True, "data": data}
        url = self.base_url.rstrip("/") + "/" + path.lstrip("/")
        all_headers = self._get_auth_headers()
        if headers:
            all_headers.update(headers)
        try:
            logger.info(f"[RegistryClient] POST {url} with data: {data}")
            resp = requests.post(url, headers=all_headers, json=data, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            return {"error": str(e), "status": "error", "code": e.response.status_code if e.response else None}
        except Exception as e:
            logger.error(f"RegistryClient POST error: {e}")
            return {"error": str(e), "status": "error"}

    def authenticate(self, credentials: Optional[Dict[str, Any]] = None, timeout: int = 10) -> bool:
        """Authenticate with the registry using credentials (e.g., API key)."""
        if self.mock:
            self.token = "mock-token"
            self.authenticated = True
            return True
        if not credentials or "api_key" not in credentials:
            logger.error("No credentials provided for registry authentication.")
            return False
        try:
            url = self.base_url.rstrip("/") + "/auth"
            resp = requests.post(url, json=credentials, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            self.token = data.get("token")
            self.authenticated = True if self.token else False
            logger.info(f"RegistryClient authenticated: {self.authenticated}")
            return self.authenticated
        except Exception as e:
            logger.error(f"RegistryClient AUTH error: {e}")
            self.authenticated = False
            return False

    def _get_auth_headers(self) -> Dict[str, str]:
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers


# Singleton instance
registry_client = RegistryClient()
