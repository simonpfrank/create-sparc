"""
Registry client for create-sparc-py (stub).
"""

from typing import Any, Dict, Optional
from create_sparc_py.utils import logger


class RegistryClient:
    """
    Client for remote template/component registry (stub).
    """

    def __init__(self):
        self.authenticated = False

    def get(self, path: str) -> Dict[str, Any]:
        logger.info(f"[RegistryClient] GET {path}")
        # Stub: return fake data
        return {"status": "ok", "path": path}

    def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[RegistryClient] POST {path} with data: {data}")
        # Stub: return fake response
        return {"status": "posted", "path": path, "data": data}

    def authenticate(self, credentials: Optional[Dict[str, Any]] = None) -> bool:
        logger.info(f"[RegistryClient] AUTHENTICATE with credentials: {credentials}")
        self.authenticated = True
        return True


# Singleton instance
registry_client = RegistryClient()
