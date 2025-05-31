"""
Interactive MCP Configuration Wizard command for create-sparc-py using click.
Implements listing, adding, and removing MCP servers via CLI prompts.
"""

import json
from pathlib import Path
from typing import Any, Dict
import click
from create_sparc_py.core.mcp_wizard_workflow import MCPWizardWorkflow
import sys

try:
    from rich import print as rich_print
    from rich.console import Console

    console = Console()
except ImportError:
    rich_print = None
    console = None

CONFIG_PATH = Path(".roo/mcp.json")


def load_config(config_path=CONFIG_PATH):
    if config_path.exists():
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def save_config(config, config_path=CONFIG_PATH):
    # Always ensure 'servers' key exists in the file
    to_save = config.copy()
    if not to_save or "mcpServers" not in to_save:
        to_save = {"mcpServers": {}}
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(to_save, f, indent=2)


def list_servers(config):
    servers = config.get("mcpServers", {})
    if not servers:
        click.echo("No MCP servers configured.")
        return
    click.echo("\nConfigured MCP Servers:")
    for server_id, server in servers.items():
        click.echo(f"- {server_id}: {server}")


def add_server(config):
    server_id = click.prompt("Server ID")
    command = click.prompt("Command (e.g., npx)")
    args = click.prompt("Arguments (comma-separated)")
    permissions = click.prompt("Permissions (comma-separated)")
    config.setdefault("mcpServers", {})[server_id] = {
        "command": command,
        "args": [a.strip() for a in args.split(",") if a.strip()],
        "permissions": [p.strip() for p in permissions.split(",") if p.strip()],
    }
    click.echo(f"Added/updated server: {server_id}")


@click.group()
def wizard():
    """Interactive MCP Configuration Wizard (click-based)"""
    # No-op group, do not print or pass
    return


@wizard.command()
def list():
    """List configured MCP servers."""
    config = load_config()
    list_servers(config)


@wizard.command()
def add():
    """Add a new MCP server."""
    config = load_config()
    add_server(config)
    save_config(config)


@wizard.command()
@click.option("--server-id", default=None, help="Server ID to remove")
def remove(server_id):
    """Remove a configured MCP server."""
    config = load_config()
    servers = config.get("mcpServers", {})
    if not servers:
        click.echo("No servers to remove.")
        save_config(config)
        return
    if server_id is None:
        choices = list(servers.keys())
        server_id = click.prompt(
            "Select server to remove",
            type=click.Choice(choices),
            show_choices=True,
        )
    if server_id not in servers:
        click.echo(f"Server ID '{server_id}' not found.")
        save_config(config)
        return
    del servers[server_id]
    if not servers:
        config.clear()
        config["mcpServers"] = {}
    click.echo(f"Removed server: {server_id}")
    save_config(config)


@wizard.command("audit-security")
def audit_security_cmd():
    """Run a security audit on the MCP configuration."""
    try:
        cwd = Path.cwd()
        config_path = cwd / ".roo" / "mcp.json"
        print(f"[DEBUG] CWD: {cwd}")
        print(f"[DEBUG] Looking for config at: {config_path}")
        workflow = MCPWizardWorkflow(project_path=cwd)
        result = workflow.audit_security()
        if not result["success"]:
            msg = f"[red]Error:[/red] {result['error']}" if rich_print else f"Error: {result['error']}"
            (console.print(msg) if console else click.echo(msg))
            sys.exit(1)
        if result["secure"]:
            msg = (
                "[green]✅ MCP configuration passed security audit.[/green]"
                if rich_print
                else "✅ MCP configuration passed security audit."
            )
            (console.print(msg) if console else click.echo(msg))
        else:
            msg = (
                f"[yellow]⚠️ Security issues detected: {len(result['issues'])} issues found[/yellow]"
                if rich_print
                else f"⚠️ Security issues detected: {len(result['issues'])} issues found"
            )
            (console.print(msg) if console else click.echo(msg))
            for issue in result["issues"]:
                sev = issue.get("severity", "info").capitalize()
                color = {"critical": "red", "warning": "yellow", "info": "blue"}.get(
                    issue.get("severity", "info"), "white"
                )
                if rich_print:
                    msg = f"[{color}]- {sev}: {issue['message']}[/] Recommendation: {issue.get('recommendation', '')}"
                else:
                    msg = f"- {sev}: {issue['message']}\n  Recommendation: {issue.get('recommendation', '')}"
                (console.print(msg) if console else click.echo(msg))
            if result.get("recommendations"):
                (console.print("\n[bold]Recommendations:[/bold]") if console else click.echo("\nRecommendations:"))
                for rec in result["recommendations"]:
                    title = rec.get("title", "")
                    steps = rec.get("steps", [])
                    (console.print(f"[bold]{title}[/bold]") if console else click.echo(title))
                    for step in steps:
                        (console.print(f"- {step}") if console else click.echo(f"- {step}"))
        sys.exit(0)
    except Exception as e:
        msg = f"[red]Unexpected error:[/red] {e}" if rich_print else f"Unexpected error: {e}"
        (console.print(msg) if console else click.echo(msg))
        sys.exit(1)


@wizard.command("validate-env")
def validate_env_cmd():
    """Validate environment variable references in MCP configuration."""
    try:
        cwd = Path.cwd()
        config_path = cwd / ".roo" / "mcp.json"
        print(f"[DEBUG] CWD: {cwd}")
        print(f"[DEBUG] Looking for config at: {config_path}")
        workflow = MCPWizardWorkflow(project_path=cwd)
        result = workflow.validate_env_var_references()
        if not result["success"]:
            msg = f"[red]Error:[/red] {result['error']}" if rich_print else f"Error: {result['error']}"
            (console.print(msg) if console else click.echo(msg))
            sys.exit(1)
        if result["valid"]:
            msg = (
                "[green]✅ All environment variable references are set.[/green]"
                if rich_print
                else "✅ All environment variable references are set."
            )
            (console.print(msg) if console else click.echo(msg))
        else:
            msg = (
                f"[yellow]⚠️ Missing environment variables: {', '.join(result['missingVariables'])}[/yellow]"
                if rich_print
                else f"⚠️ Missing environment variables: {', '.join(result['missingVariables'])}"
            )
            (console.print(msg) if console else click.echo(msg))
            for ref in result["references"]:
                if not ref["isSet"]:
                    msg = (
                        f"[red]- {ref['name']} (server: {ref['serverId']}) not set[/red]"
                        if rich_print
                        else f"- {ref['name']} (server: {ref['serverId']}) not set"
                    )
                    (console.print(msg) if console else click.echo(msg))
        sys.exit(0)
    except Exception as e:
        msg = f"[red]Unexpected error:[/red] {e}" if rich_print else f"Unexpected error: {e}"
        (console.print(msg) if console else click.echo(msg))
        sys.exit(1)


def run(args: Any) -> int:
    """
    Run the wizard command (interactive MCP configuration) using click.
    Args:
        args: Parsed command-line arguments (argparse.Namespace).
    Returns:
        Exit code (0 for success, non-zero for failure).
    """
    click_args = getattr(args, "wizard_args", [])
    try:
        wizard(standalone_mode=True, args=click_args)
        return 0
    except SystemExit as e:
        return e.code
