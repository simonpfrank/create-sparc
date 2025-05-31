import os
from pathlib import Path
from typing import Any, Dict, Optional
import shutil
import datetime


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
        """Validate the MCP configuration file."""
        try:
            import json

            if not self.mcp_config_path.exists():
                return {"success": False, "errors": ["Config file does not exist."]}
            with open(self.mcp_config_path, "r") as f:
                config = json.load(f)
            errors = []
            if "mcpServers" not in config or not isinstance(config["mcpServers"], dict):
                errors.append("Missing or invalid 'mcpServers' key.")
            # Additional validation can be added here (e.g., check server fields)
            for server_id, server in config.get("mcpServers", {}).items():
                if not isinstance(server, dict):
                    errors.append(f"Server '{server_id}' is not a valid object.")
                # Example: check for required fields
                for field in ["command", "args", "permissions"]:
                    if field not in server:
                        errors.append(f"Server '{server_id}' missing required field: {field}")
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
        """Perform a security audit on the MCP configuration."""
        import json

        config = None
        try:
            if not self.mcp_config_path.exists():
                return {"success": False, "error": "Config file does not exist."}
            with open(self.mcp_config_path, "r") as f:
                config = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"Failed to load config: {e}"}

        issues = []
        recommendations = []
        secure = True
        sensitive_patterns = ["token", "key", "secret", "password", "credential", "auth", "access"]

        def is_sensitive(name):
            return any(pat in name.lower() for pat in sensitive_patterns)

        # Scan each server
        servers = config.get("mcpServers", {})
        for server_id, server in servers.items():
            # Check for hardcoded sensitive values in args
            args = server.get("args", [])
            if isinstance(args, list):
                for i, arg in enumerate(args):
                    if isinstance(arg, str) and arg.startswith("--"):
                        param_name = arg[2:]
                        if i + 1 < len(args):
                            param_value = args[i + 1]
                            if is_sensitive(param_name):
                                if isinstance(param_value, str) and "${env:" not in param_value:
                                    secure = False
                                    env_var = f"{server_id.upper()}_{param_name.upper().replace('-', '_')}"
                                    issues.append(
                                        {
                                            "severity": "critical",
                                            "message": f"Hardcoded sensitive value for '{param_name}' in server '{server_id}'.",
                                            "recommendation": f"Replace with environment variable reference: ${{env:{env_var}}}",
                                        }
                                    )
            # Check for wildcard permissions
            always_allow = server.get("alwaysAllow", [])
            if isinstance(always_allow, list) and "*" in always_allow:
                secure = False
                issues.append(
                    {
                        "severity": "warning",
                        "message": f"Wildcard permission '*' found in alwaysAllow for server '{server_id}'.",
                        "recommendation": "Remove wildcard permissions and specify only required permissions.",
                    }
                )
        if not issues:
            recommendations.append(
                {
                    "title": "Best Practices",
                    "steps": [
                        "Use environment variable references (${env:VARNAME}) for all sensitive information.",
                        "Avoid wildcard permissions in alwaysAllow.",
                        "Review server arguments for hardcoded secrets.",
                    ],
                }
            )
        return {"success": True, "secure": secure, "issues": issues, "recommendations": recommendations}

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
