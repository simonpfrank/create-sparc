import argparse
from create_sparc_py.cli.commands.help_markdown import get_help_markdown
from rich.console import Console
from rich.markdown import Markdown


def create_parser() -> argparse.ArgumentParser:
    class MarkdownHelpParser(argparse.ArgumentParser):
        def __init__(self, *args, **kwargs):
            self.command_name = kwargs.pop("command_name", None)
            super().__init__(*args, **kwargs)

        def print_help(self, file=None):
            if getattr(self, "command_name", None):
                help_md = get_help_markdown(self.command_name)
                if not help_md.startswith("No help available"):
                    console = Console()
                    console.print(Markdown(help_md))
                    return
            super().print_help(file=file)

    parser = MarkdownHelpParser(
        prog="create-sparc-py",
        description="Python scaffolding tool using the SPARC methodology",
        epilog="For more information, visit: https://github.com/yourusername/create-sparc-py",
        command_name=None,
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        help="Commands to run",
        parser_class=MarkdownHelpParser,
    )

    def add_subparser_with_markdown(name, help_text, add_args_fn):
        subparser = subparsers.add_parser(
            name,
            help=help_text,
        )
        subparser.command_name = name
        add_args_fn(subparser)
        return subparser

    def _add_init_args(parser):
        from create_sparc_py.cli.commands import init_command

        parser.add_argument("name", help="Name of the project to create")
        parser.add_argument(
            "-t",
            "--template",
            default="default",
            help="Template to use (default: 'default')",
        )
        parser.add_argument("-d", "--directory", help="Directory to create the project in (default: <name>)")
        parser.set_defaults(func=init_command)

    def _add_add_args(parser):
        from create_sparc_py.cli.commands import add_command

        parser.add_argument("component", help="Component to add")
        parser.add_argument("name", help="Name of the component")
        parser.add_argument(
            "-d",
            "--directory",
            help="Directory to add the component to (default: current directory)",
        )
        parser.set_defaults(func=add_command)

    def _add_help_args(parser):
        from create_sparc_py.cli.commands import help_command

        parser.add_argument("command", nargs="?", help="Command to show help for")
        parser.set_defaults(func=help_command)

    def _add_wizard_args(parser):
        from create_sparc_py.cli.commands import wizard_command

        parser.add_argument(
            "wizard_args",
            nargs=argparse.REMAINDER,
            help="Arguments for the wizard subcommands (e.g., list, add, audit-security, etc.)",
        )
        parser.set_defaults(func=wizard_command)

    def _add_mcp_args(parser):
        from create_sparc_py.cli.commands import configure_mcp_command

        parser.add_argument(
            "mcp_args",
            nargs=argparse.REMAINDER,
            help="Arguments for the configure-mcp subcommands (e.g., add, remove, update, list, etc.)",
        )
        parser.set_defaults(func=configure_mcp_command)

    def _add_aigi_args(parser):
        from create_sparc_py.cli.commands import aigi_command

        parser.add_argument(
            "aigi_args",
            nargs=argparse.REMAINDER,
            help="Arguments for the aigi subcommands (e.g., init, etc.)",
        )
        parser.set_defaults(func=aigi_command)

    def _add_minimal_args(parser):
        from create_sparc_py.cli.commands import minimal_command

        parser.add_argument(
            "minimal_args",
            nargs=argparse.REMAINDER,
            help="Arguments for the minimal subcommands (e.g., init, etc.)",
        )
        parser.set_defaults(func=minimal_command)

    def _add_registry_args(parser):
        from create_sparc_py.cli.commands.registry_command import registry_command

        parser.add_argument(
            "registry_args",
            nargs=argparse.REMAINDER,
            help="Arguments for the registry subcommands (e.g., list, get, post, auth, etc.)",
        )
        parser.set_defaults(func=registry_command)

    add_subparser_with_markdown("init", "Initialize a new project using a template", _add_init_args)
    add_subparser_with_markdown("add", "Add a component to an existing project", _add_add_args)
    add_subparser_with_markdown("help", "Show help for a command", _add_help_args)
    add_subparser_with_markdown("wizard", "Run the project creation wizard", _add_wizard_args)
    add_subparser_with_markdown("configure-mcp", "Configure Multi-Cloud Provider settings", _add_mcp_args)
    add_subparser_with_markdown("aigi", "AI-Guided Implementation commands", _add_aigi_args)
    add_subparser_with_markdown("minimal", "Create a minimal Roo mode framework", _add_minimal_args)
    add_subparser_with_markdown("registry", "Registry client commands", _add_registry_args)
    return parser
