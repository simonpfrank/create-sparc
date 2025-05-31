import re
from typing import Dict, Any, List


class MCPSecurity:
    """Security features for the MCP Configuration Wizard."""

    sensitive_patterns = [
        re.compile(r"^[A-Za-z0-9-_]{20,}$"),
        re.compile(r"^sk-[A-Za-z0-9]{20,}$"),
        re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"),
        re.compile(r"^Bearer\s+[A-Za-z0-9-_]+$"),
        re.compile(r"^[A-Za-z0-9+/]{40,}={0,2}$"),
    ]
    sensitive_param_names = [
        "key",
        "apikey",
        "api-key",
        "token",
        "secret",
        "password",
        "credential",
        "auth",
        "authorization",
        "access-token",
        "refresh-token",
    ]
    high_risk_permissions = [
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
    dangerous_commands = ["rm", "sudo", "chmod", "chown", "eval"]

    def audit_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Audit MCP configuration for security issues."""
        results = {"secure": True, "issues": [], "recommendations": []}
        if not config or "mcpServers" not in config:
            results["secure"] = False
            results["issues"].append({"severity": "error", "message": "Invalid or empty configuration"})
            return results
        for server_id, server_config in config["mcpServers"].items():
            # Require 'command' field for each server
            if (
                "command" not in server_config
                or not isinstance(server_config["command"], str)
                or not server_config["command"].strip()
            ):
                results["secure"] = False
                results["issues"].append(
                    {
                        "severity": "error",
                        "message": f"Missing or invalid command for server '{server_id}'",
                        "location": f"mcpServers.{server_id}.command",
                        "recommendation": "Specify a valid command string",
                    }
                )
            results["issues"].extend(self.detect_hardcoded_credentials(server_config, server_id))
            results["issues"].extend(self.validate_permission_scope(server_config, server_id))
            results["issues"].extend(self.validate_command_security(server_config, server_id))
        if results["issues"]:
            results["secure"] = False
        results["recommendations"] = self.generate_recommendations(results["issues"])
        return results

    def detect_hardcoded_credentials(self, server_config: Dict[str, Any], server_id: str) -> List[Dict[str, Any]]:
        issues = []
        args = server_config.get("args", [])
        if not isinstance(args, list):
            return issues
        for i, arg in enumerate(args):
            if isinstance(arg, str) and arg.startswith("--"):
                param_name = arg[2:].lower()
                if i + 1 < len(args):
                    param_value = args[i + 1]
                    is_sensitive = any(name in param_name for name in self.sensitive_param_names)
                    is_hardcoded = is_sensitive and isinstance(param_value, str) and "${env:" not in param_value
                    if is_hardcoded:
                        issues.append(
                            {
                                "severity": "critical",
                                "message": f"Hardcoded sensitive value detected in server '{server_id}'",
                                "location": f"mcpServers.{server_id}.args",
                                "recommendation": f"Replace with environment variable reference: ${{env:{server_id.upper()}_{param_name.upper().replace('-', '_')}}}",
                            }
                        )
            elif isinstance(arg, str):
                for pattern in self.sensitive_patterns:
                    if pattern.match(arg) and "${env:" not in arg:
                        issues.append(
                            {
                                "severity": "critical",
                                "message": f"Potential sensitive value detected in server '{server_id}' arguments",
                                "location": f"mcpServers.{server_id}.args",
                                "recommendation": "Replace with environment variable reference",
                            }
                        )
                        break
        return issues

    def validate_permission_scope(self, server_config: Dict[str, Any], server_id: str) -> List[Dict[str, Any]]:
        issues = []
        always_allow = server_config.get("alwaysAllow", [])
        if not isinstance(always_allow, list):
            return issues
        granted_high_risk = [p for p in always_allow if any(risk in p for risk in self.high_risk_permissions)]
        if granted_high_risk:
            issues.append(
                {
                    "severity": "warning",
                    "message": f"High-risk permissions granted to server '{server_id}': {', '.join(granted_high_risk)}",
                    "location": f"mcpServers.{server_id}.alwaysAllow",
                    "recommendation": "Review and limit permissions to only what is necessary",
                }
            )
        if "*" in always_allow:
            issues.append(
                {
                    "severity": "critical",
                    "message": f"Wildcard permission granted to server '{server_id}'",
                    "location": f"mcpServers.{server_id}.alwaysAllow",
                    "recommendation": "Replace wildcard with specific required permissions",
                }
            )
        if len(always_allow) > 10:
            issues.append(
                {
                    "severity": "info",
                    "message": f"Server '{server_id}' has a large number of permissions ({len(always_allow)})",
                    "location": f"mcpServers.{server_id}.alwaysAllow",
                    "recommendation": "Review and consolidate permissions where possible",
                }
            )
        return issues

    def validate_command_security(self, server_config: Dict[str, Any], server_id: str) -> List[Dict[str, Any]]:
        issues = []
        command = server_config.get("command")
        if not command or not isinstance(command, str):
            issues.append(
                {
                    "severity": "error",
                    "message": f"Missing or invalid command for server '{server_id}'",
                    "location": f"mcpServers.{server_id}.command",
                    "recommendation": "Specify a valid command string",
                }
            )
            return issues
        if any(cmd in command for cmd in self.dangerous_commands):
            issues.append(
                {
                    "severity": "critical",
                    "message": f"Potentially dangerous command for server '{server_id}': {command}",
                    "location": f"mcpServers.{server_id}.command",
                    "recommendation": "Avoid using system-level commands that could modify the system",
                }
            )
        if any(sym in command for sym in ["$", "`", ";"]):
            issues.append(
                {
                    "severity": "critical",
                    "message": f"Potential command injection vulnerability in server '{server_id}'",
                    "location": f"mcpServers.{server_id}.command",
                    "recommendation": "Avoid using shell metacharacters in commands",
                }
            )
        return issues

    def generate_recommendations(self, issues: List[Dict[str, Any]]) -> List[dict]:
        recommendations = []
        # Group issues by type
        credential_issues = [
            i for i in issues if "Hardcoded" in i.get("message", "") or "sensitive" in i.get("message", "")
        ]
        permission_issues = [i for i in issues if i.get("location", "").endswith("alwaysAllow")]
        command_issues = [i for i in issues if i.get("location", "").endswith("command")]
        if credential_issues:
            recommendations.append(
                {
                    "title": "Secure Credential Management",
                    "steps": [
                        "Use environment variable references (${env:VARIABLE_NAME}) for all sensitive information",
                        "Never hardcode API keys, tokens, or passwords in configuration files",
                        "Consider using a secrets management solution for production environments",
                    ],
                }
            )
        if permission_issues:
            recommendations.append(
                {
                    "title": "Permission Scope Management",
                    "steps": [
                        "Follow the principle of least privilege - grant only permissions that are necessary",
                        "Avoid using wildcard (*) permissions",
                        "Regularly audit and review granted permissions",
                    ],
                }
            )
        if command_issues:
            recommendations.append(
                {
                    "title": "Command Security",
                    "steps": [
                        'Use specific package versions instead of "latest" to prevent supply chain attacks',
                        "Avoid commands that could modify the system or execute arbitrary code",
                        "Validate all inputs to prevent command injection",
                    ],
                }
            )
        return recommendations
