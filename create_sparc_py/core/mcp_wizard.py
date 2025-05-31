import json
from pathlib import Path
from typing import Any, Dict, Optional

CONFIG_PATH = Path(".roo/mcp.json")


class MCPWizard:
    """
    Interactive Multi-Cloud Provider (MCP) configuration wizard.
    """

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or CONFIG_PATH
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {"mcpServers": {}}

    def save_config(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def run(self):
        """
        Run the interactive MCP configuration wizard.
        """
        print("MCP Configuration Wizard")
        while True:
            print("\nOptions: [list, add, remove, exit]")
            choice = input("Choose an option: ").strip().lower()
            if choice == "list":
                self.list_servers()
            elif choice == "add":
                self.add_server()
            elif choice == "remove":
                self.remove_server()
            elif choice == "exit":
                break
            else:
                print("Unknown option.")

    def list_servers(self):
        servers = self.config.get("mcpServers", {})
        if not servers:
            print("No MCP servers configured.")
            return
        print("Configured MCP Servers:")
        for server_id, server in servers.items():
            print(f"- {server_id}: {server}")

    def add_server(self, server_id=None, command=None, args=None, permissions=None):
        if server_id is None:
            server_id = input("Server ID: ").strip()
        if command is None:
            command = input("Command (e.g., npx): ").strip()
        if args is None:
            args = input("Arguments (comma-separated): ").strip()
        if permissions is None:
            permissions = input("Permissions (comma-separated): ").strip()
        self.config.setdefault("mcpServers", {})[server_id] = {
            "command": command,
            "args": [a.strip() for a in args.split(",") if a.strip()],
            "permissions": [p.strip() for p in permissions.split(",") if p.strip()],
        }
        self.save_config()
        print(f"Added/updated server: {server_id}")

    def remove_server(self, server_id=None):
        servers = self.config.get("mcpServers", {})
        if not servers:
            print("No servers to remove.")
            return
        if server_id is None:
            print("Servers:", ", ".join(servers.keys()))
            server_id = input("Server ID to remove: ").strip()
        if server_id not in servers:
            print(f"Server ID '{server_id}' not found.")
            return
        del servers[server_id]
        self.save_config()
        print(f"Removed server: {server_id}")

    def configure(self, options: Optional[Dict[str, Any]] = None):
        """
        Configure MCP with the given options (programmatic, for tests or automation).
        """
        if not options:
            return
        self.config.setdefault("mcpServers", {})
        for server_id, server_data in options.get("mcpServers", {}).items():
            self.config["mcpServers"][server_id] = server_data
        self.save_config()

    def generate_config(self, config: Optional[Dict[str, Any]] = None):
        """
        Generate MCP configuration files based on user input or provided config.
        """
        if config:
            self.config = config
        self.save_config()
