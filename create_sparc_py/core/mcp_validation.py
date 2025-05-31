import os
import re
from typing import List, Dict, Any, Optional


def validate_server_id(server_id: str) -> Dict[str, Any]:
    """Validate server ID."""
    if not server_id:
        return {"valid": False, "error": "Server ID is required"}
    if not re.match(r"^[a-zA-Z0-9-_]+$", server_id):
        return {"valid": False, "error": "Server ID must contain only letters, numbers, hyphens, and underscores"}
    return {"valid": True}


def validate_api_key(api_key: str) -> Dict[str, Any]:
    """Validate API key."""
    if not api_key:
        return {"valid": False, "error": "API key is required"}
    if api_key.startswith("${env:") and api_key.endswith("}"):
        return {"valid": True, "is_env_var": True}
    if len(api_key) < 8:
        return {"valid": False, "error": "API key is too short"}
    return {
        "valid": True,
        "is_env_var": False,
        "warning": "Consider using an environment variable reference for security",
    }


def validate_permissions(
    permissions: List[str], recommended_permissions: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Validate permissions."""
    if not isinstance(permissions, list):
        return {"valid": False, "error": "Permissions must be an array"}
    if len(permissions) == 0:
        return {"valid": True, "warning": "No permissions specified. The server may have limited functionality."}
    if recommended_permissions:
        extra_permissions = [p for p in permissions if p not in recommended_permissions]
        if extra_permissions:
            return {
                "valid": True,
                "warning": f"The following permissions are beyond recommended: {', '.join(extra_permissions)}",
            }
    return {"valid": True}


def validate_server_config(server_config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate server configuration."""
    errors = []
    if not server_config.get("command"):
        errors.append("Server command is required")
    if not isinstance(server_config.get("args"), list):
        errors.append("Server arguments must be an array")
    sensitive_patterns = [
        re.compile(r"^[A-Za-z0-9-_]{20,}$"),
        re.compile(r"^sk-[A-Za-z0-9]{20,}$"),
        re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"),
    ]
    args = server_config.get("args", [])
    if isinstance(args, list):
        for arg in args:
            if isinstance(arg, str):
                for pattern in sensitive_patterns:
                    if pattern.match(arg) and not arg.startswith("${env:"):
                        errors.append(
                            "Potential sensitive information detected in arguments. Use environment variable references instead."
                        )
                        break
    if "alwaysAllow" in server_config and not isinstance(server_config["alwaysAllow"], list):
        errors.append("alwaysAllow must be an array of permission strings")
    return {"valid": len(errors) == 0, "errors": errors}


def validate_env_var_reference(reference: str) -> Dict[str, Any]:
    """Validate environment variable reference and check if set."""
    env_var_pattern = re.compile(r"^\${env:([A-Za-z0-9_]+)}$")
    match = env_var_pattern.match(reference)
    if not match:
        return {"valid": False, "error": "Invalid environment variable reference format. Use ${env:VARIABLE_NAME}"}
    variable_name = match.group(1)
    is_set = variable_name in os.environ
    return {
        "valid": True,
        "variable_name": variable_name,
        "is_set": is_set,
        "warning": None if is_set else f"Environment variable {variable_name} is not set",
    }
