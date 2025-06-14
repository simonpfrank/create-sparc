import os
from pathlib import Path
from typing import Any, Dict, Optional
import shutil
import datetime
from .mcp_validation import (
    validate_server_id,
    validate_api_key,
    validate_permissions,
    validate_server_config,
    validate_env_var_reference,
)
from .mcp_security import MCPSecurity


class MCPWizardWorkflow:
    """
    Orchestrates the MCP Configuration Wizard workflow, including registry, config, security, and file management.
    """

    def __init__(self, project_path: Optional[Path] = None):
        self.project_path = Path(project_path or os.getcwd())
        self.mcp_config_path = self.project_path / ".roo" / "mcp.json"
        self.roomodes_path = self.project_path / ".roomodes"
        self.registry_url = "https://registry.example.com/api/v1/mcp"  # TODO: Make configurable
        self.cache_enabled = True
        self.security = MCPSecurity()
        # TODO: Initialize registry client, file manager, config generator, security modules

    def initialize(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Initialize workflow, ensure directories, set up clients."""
        try:
            # Allow override of paths via options
            opts = options or {}
            if "project_path" in opts:
                self.project_path = Path(opts["project_path"])
            if "mcp_config_path" in opts:
                self.mcp_config_path = Path(opts["mcp_config_path"])
            if "roomodes_path" in opts:
                self.roomodes_path = Path(opts["roomodes_path"])
            # Ensure .roo directory exists
            roo_dir = self.mcp_config_path.parent
            roo_dir.mkdir(parents=True, exist_ok=True)
            # Ensure .roomodes file exists (touch if not)
            if not self.roomodes_path.exists():
                self.roomodes_path.touch()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def discover_servers(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Discover available MCP servers from registry."""
        # TODO: Implement server discovery
        return {"success": True, "servers": []}

    def get_server_details(self, server_id: str) -> Dict[str, Any]:
        """Get details for a specific server from registry."""
        # TODO: Implement server details fetch
        return {"success": True, "server": {}}

    def configure_server(self, server_id: str, user_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Configure a server with user parameters."""
        # TODO: Implement server configuration
        return {"success": True}

    def update_server_config(self, server_id: str, user_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Update server configuration."""
        # TODO: Implement server update
        return {"success": True}

    def remove_server(self, server_id: str) -> Dict[str, Any]:
        """Remove a configured server."""
        # TODO: Implement server removal
        return {"success": True}

    def list_configured_servers(self) -> Dict[str, Any]:
        """List all configured servers from local config."""
        try:
            if not self.mcp_config_path.exists():
                return {"success": True, "servers": []}
            import json

            with open(self.mcp_config_path, "r") as f:
                config = json.load(f)
            servers = config.get("mcpServers", {})
            return {"success": True, "servers": list(servers.keys()), "details": servers}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def validate_configuration(self) -> Dict[str, Any]:
        """Validate the MCP configuration file using advanced validation logic."""
        try:
            import json

            if not self.mcp_config_path.exists():
                return {"success": False, "errors": ["Config file does not exist."]}
            with open(self.mcp_config_path, "r") as f:
                config = json.load(f)
            errors = []
            if "mcpServers" not in config or not isinstance(config["mcpServers"], dict):
                errors.append("Missing or invalid 'mcpServers' key.")
            for server_id, server in config.get("mcpServers", {}).items():
                id_result = validate_server_id(server_id)
                if not id_result["valid"]:
                    errors.append(f"Server ID '{server_id}': {id_result['error']}")
                server_result = validate_server_config(server)
                if not server_result["valid"]:
                    for err in server_result["errors"]:
                        errors.append(f"Server '{server_id}': {err}")
            return {"success": len(errors) == 0, "errors": errors}
        except Exception as e:
            return {"success": False, "errors": [str(e)]}

    def backup_configuration(self) -> Dict[str, Any]:
        """Backup current configuration files (.roo/mcp.json and .roomodes) to .roo/backups/ with a timestamp."""
        try:
            backup_dir = self.project_path / ".roo" / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            backup_paths = {}
            # Backup mcp.json
            if self.mcp_config_path.exists():
                mcp_backup = backup_dir / f"mcp_{timestamp}.json"
                shutil.copy2(self.mcp_config_path, mcp_backup)
                backup_paths["mcp.json"] = str(mcp_backup)
            # Backup .roomodes
            if self.roomodes_path.exists():
                roomodes_backup = backup_dir / f"roomodes_{timestamp}"
                shutil.copy2(self.roomodes_path, roomodes_backup)
                backup_paths[".roomodes"] = str(roomodes_backup)
            if not backup_paths:
                return {"success": False, "error": "No config files to backup."}
            return {"success": True, "backupPaths": backup_paths}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def restore_configuration(self, backup_paths: Dict[str, Any]) -> Dict[str, Any]:
        """Restore configuration files from the given backup paths (dict with keys 'mcp.json' and/or '.roomodes')."""
        try:
            restored = {}
            # Restore mcp.json
            mcp_backup = backup_paths.get("mcp.json")
            if mcp_backup:
                shutil.copy2(mcp_backup, self.mcp_config_path)
                restored["mcp.json"] = str(self.mcp_config_path)
            # Restore .roomodes
            roomodes_backup = backup_paths.get(".roomodes")
            if roomodes_backup:
                shutil.copy2(roomodes_backup, self.roomodes_path)
                restored[".roomodes"] = str(self.roomodes_path)
            if not restored:
                return {"success": False, "error": "No valid backup paths provided."}
            return {"success": True, "restored": restored}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def configure_server_workflow(
        self, server_id: str, user_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform the full configuration workflow for a server."""
        # TODO: Implement full workflow (backup, configure, validate, restore on error)
        return {"success": True}

    def audit_security(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform a security audit on the MCP configuration using MCPSecurity."""
        import json

        config = None
        try:
            if not self.mcp_config_path.exists():
                return {"success": False, "error": "Config file does not exist."}
            with open(self.mcp_config_path, "r") as f:
                config = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"Failed to load config: {e}"}
        results = self.security.audit_configuration(config)
        # Always return a dict with 'success' key
        results["success"] = True
        return results

    def validate_env_var_references(self, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Validate environment variable references in the MCP configuration."""
        import json
        import os

        config = None
        try:
            if not self.mcp_config_path.exists():
                return {"success": False, "error": "Config file does not exist."}
            with open(self.mcp_config_path, "r") as f:
                config = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"Failed to load config: {e}"}

        results = {"success": True, "valid": True, "missingVariables": [], "references": []}
        servers = config.get("mcpServers", {})
        for server_id, server in servers.items():
            args = server.get("args", [])
            if isinstance(args, list):
                for arg in args:
                    if isinstance(arg, str) and "${env:" in arg:
                        import re

                        matches = re.findall(r"\${env:([A-Za-z0-9_]+)}", arg)
                        for env_var in matches:
                            is_set = env_var in os.environ
                            results["references"].append(
                                {"name": env_var, "isSet": is_set, "serverId": server_id, "value": arg}
                            )
                            if not is_set:
                                results["missingVariables"].append(env_var)
                                results["valid"] = False
        return results

    def detect_dangerous_command(self, command: str) -> list:
        """Detect potentially dangerous commands."""
        issues = []
        dangerous_commands = ["rm", "sudo", "chmod", "chown", "eval"]
        if any(cmd in command for cmd in dangerous_commands):
            issues.append(
                {
                    "severity": "critical",
                    "message": f"Potentially dangerous command: {command}",
                    "recommendation": "Avoid using system-level commands that could modify the system.",
                }
            )
        if any(x in command for x in ["$", "`", ";"]):
            issues.append(
                {
                    "severity": "critical",
                    "message": f"Potential command injection vulnerability: {command}",
                    "recommendation": "Avoid using shell metacharacters in commands.",
                }
            )
        return issues

    def validate_env_var_reference(self, reference: str) -> dict:
        import re, os

        env_var_pattern = r"^\${env:([A-Za-z0-9_]+)}$"
        match = re.match(env_var_pattern, reference)
        if not match:
            return {"valid": False, "error": "Invalid environment variable reference format. Use ${env:VARIABLE_NAME}"}
        var = match.group(1)
        is_set = var in os.environ
        return {
            "valid": True,
            "variableName": var,
            "isSet": is_set,
            "warning": None if is_set else f"Environment variable {var} is not set",
        }

    def validate_permission_scope(self, always_allow, server_id):
        issues = []
        high_risk = [
            "admin",
            "delete",
            "write",
            "execute",
            "deploy",
            "manage",
            "create",
            "update",
            "remove",
            "modify",
            "execute_sql",
            "execute_query",
        ]
        if not always_allow or not isinstance(always_allow, list):
            return issues
        granted = [p for p in always_allow if any(risk in p for risk in high_risk)]
        if granted:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"High-risk permissions granted to server '{server_id}': {', '.join(granted)}",
                    "recommendation": "Review and limit permissions to only what is necessary",
                }
            )
        if "*" in always_allow:
            issues.append(
                {
                    "severity": "critical",
                    "message": f"Wildcard permission granted to server '{server_id}'",
                    "recommendation": "Replace wildcard with specific required permissions",
                }
            )
        if len(always_allow) > 10:
            issues.append(
                {
                    "severity": "info",
                    "message": f"Server '{server_id}' has a large number of permissions ({len(always_allow)})",
                    "recommendation": "Review and consolidate permissions where possible",
                }
            )
        return issues

    def secure_configuration(self, config: dict) -> dict:
        """Auto-fix common security issues in the config."""
        import copy

        secured = copy.deepcopy(config)
        applied_fixes = []
        for server_id, server in secured.get("mcpServers", {}).items():
            # Remove wildcard permissions
            if "alwaysAllow" in server and isinstance(server["alwaysAllow"], list):
                if "*" in server["alwaysAllow"]:
                    server["alwaysAllow"] = [p for p in server["alwaysAllow"] if p != "*"]
                    applied_fixes.append(
                        {
                            "type": "permission",
                            "message": f"Removed wildcard permission from server '{server_id}'",
                            "location": f"mcpServers.{server_id}.alwaysAllow",
                        }
                    )
            # Suggest env var for hardcoded sensitive values
            args = server.get("args", [])
            sensitive_patterns = ["token", "key", "secret", "password", "credential", "auth", "access"]
            for i, arg in enumerate(args):
                if isinstance(arg, str) and arg.startswith("--"):
                    param_name = arg[2:]
                    if i + 1 < len(args):
                        param_value = args[i + 1]
                        if any(pat in param_name.lower() for pat in sensitive_patterns):
                            if isinstance(param_value, str) and "${env:" not in param_value:
                                env_var = f"{server_id.upper()}_{param_name.upper().replace('-', '_')}"
                                args[i + 1] = f"${{env:{env_var}}}"
                                applied_fixes.append(
                                    {
                                        "type": "credential",
                                        "message": f"Replaced hardcoded value for '{param_name}' in server '{server_id}' with env var reference.",
                                        "location": f"mcpServers.{server_id}.args[{i+1}]",
                                    }
                                )
        return {"securedConfig": secured, "appliedFixes": applied_fixes}

    def calculate_integrity_hash(self, config: dict) -> str:
        import hashlib, json

        config_str = json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()

    def verify_integrity(self, config: dict, expected_hash: str) -> bool:
        return self.calculate_integrity_hash(config) == expected_hash
