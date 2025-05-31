"""
Unit tests for the CLI module.
"""

import pytest
from unittest.mock import patch

from create_sparc_py.cli import run

# Import command modules directly for patching
from create_sparc_py.cli.commands import (
    add_command,
    aigi_command,
    configure_mcp_command,
    help_command,
    init_command,
    minimal_command,
    wizard_command,
)

# Explicitly import minimal_command before patching (for debugging ModuleNotFoundError)
try:
    from create_sparc_py.cli.commands import minimal_command as minimal_command_check

    print("Successfully imported minimal_command for check.")
except ModuleNotFoundError as e:
    print(f"ModuleNotFoundError during explicit import check: {e}")
    # Re-raise to ensure the test fails if the import still fails
    raise


def test_run_init_command_stub(capsys):
    """
    Test that the init command stub is called correctly.
    """
    with patch("create_sparc_py.cli.commands.init_command") as mock_init_run:
        mock_init_run.return_value = 0

        # Simulate running the command
        exit_code = run(["create-sparc-py", "init", "test_project"])

        # Assert that the init command's run function was called with correct arguments
        mock_init_run.assert_called_once()
        called_args = mock_init_run.call_args[0][0]
        assert called_args.name == "test_project"
        assert called_args.template == "default"
        assert called_args.directory is None

        # Assert the exit code is 0
        assert exit_code == 0

        # Capture and assert output (optional, depends on stub implementation)
        # captured = capsys.readouterr()
        # assert "Init command executed with args:" in captured.out


def test_run_add_command_stub(capsys):
    """
    Test that the add command stub is called correctly.
    """
    with patch("create_sparc_py.cli.commands.add_command") as mock_add_run:
        mock_add_run.return_value = 0

        # Simulate running the command
        exit_code = run(["create-sparc-py", "add", "component_name", "component_name"])

        # Assert that the add command's run function was called with correct arguments
        mock_add_run.assert_called_once()
        called_args = mock_add_run.call_args[0][0]
        assert called_args.component == "component_name"
        assert called_args.name == "component_name"
        assert called_args.directory is None

        # Assert the exit code is 0
        assert exit_code == 0

        # Capture and assert output (optional)
        # captured = capsys.readouterr()
        # assert "Add command executed with args:" in captured.out


def test_run_help_command_stub(capsys):
    """
    Test that the help command stub is called correctly.
    """
    with patch("create_sparc_py.cli.commands.help_command") as mock_help_run:
        mock_help_run.return_value = 0

        # Simulate running the command
        exit_code = run(["create-sparc-py", "help", "init"])

        mock_help_run.assert_called_once()
        called_args = mock_help_run.call_args[0][0]
        assert called_args.command == "init"

        assert exit_code == 0


def test_run_wizard_command_stub(capsys):
    """
    Test that the wizard command stub is called correctly.
    """
    with patch("create_sparc_py.cli.commands.wizard_command") as mock_wizard_run:
        mock_wizard_run.return_value = 0

        exit_code = run(["create-sparc-py", "wizard"])

        mock_wizard_run.assert_called_once()
        assert exit_code == 0


def test_run_configure_mcp_command_stub(capsys):
    """
    Test that the configure-mcp command stub is called correctly.
    """
    with patch("create_sparc_py.cli.commands.configure_mcp_command") as mock_mcp_run:
        mock_mcp_run.return_value = 0

        exit_code = run(["create-sparc-py", "configure-mcp"])

        mock_mcp_run.assert_called_once()
        assert exit_code == 0


def test_run_aigi_command_stub(capsys):
    """
    Test that the aigi command stub is called correctly and outputs simulated AI integration.
    """
    with patch("create_sparc_py.cli.commands.aigi_command") as mock_aigi_run:
        mock_aigi_run.return_value = 0

        exit_code = run(["create-sparc-py", "aigi", "generate a model"])

        mock_aigi_run.assert_called_once()
        called_args = mock_aigi_run.call_args[0][0]
        assert called_args.prompt == "generate a model"

        assert exit_code == 0

    # Now test the actual implementation (not just the patch)
    from create_sparc_py.cli.commands import aigi_command as real_aigi_run

    class Args:
        prompt = "generate a model"

    capsys.readouterr()  # Clear any previous output
    result = real_aigi_run(Args())
    captured = capsys.readouterr()
    assert result == 0
    assert "[AIGI] Using provider: openai" in captured.out
    assert "[AIGI] Prompt: generate a model" in captured.out
    assert "# AI-generated code for prompt: 'generate a model'" in captured.out
    assert "print('Hello from AI!')" in captured.out


def test_run_minimal_command_stub(capsys):
    """
    Test that the minimal command stub is called correctly.
    """
    with patch("create_sparc_py.cli.commands.minimal_command") as mock_minimal_run:
        mock_minimal_run.return_value = 0

        exit_code = run(["create-sparc-py", "minimal", "test_project"])

        mock_minimal_run.assert_called_once()
        called_args = mock_minimal_run.call_args[0][0]
        assert called_args.name == "test_project"
        assert called_args.directory is None

        assert exit_code == 0


def test_help_command_lists_commands(capsys):
    """
    Test that 'help' with no argument prints the main help (list of commands).
    """
    from create_sparc_py.cli.commands import help_command

    class Args:
        command = None

    exit_code = help_command(Args())
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "commands:" in captured.out or "Commands to run" in captured.out
    assert "init" in captured.out
    assert "add" in captured.out
    assert "help" in captured.out


def test_help_command_specific_command(capsys):
    """
    Test that 'help <command>' prints the help for that command.
    """
    from create_sparc_py.cli.commands import help_command

    class Args:
        command = "init"

    exit_code = help_command(Args())
    captured = capsys.readouterr()
    assert exit_code == 0
    # Check for the markdown help title
    assert "# create-sparc-py init" in captured.out
    assert "Create a new SPARC project" in captured.out


def test_help_command_unknown_command(capsys):
    """
    Test that 'help unknown' prints an error message.
    """
    from create_sparc_py.cli.commands import help_command

    class Args:
        command = "unknown"

    exit_code = help_command(Args())
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Unknown command" in captured.out


def test_cli_command_help_flag(capsys):
    """
    Test that '--help' flag on a command prints its help.
    """
    from create_sparc_py.cli import run
    import pytest

    with pytest.raises(SystemExit) as e:
        run(["create-sparc-py", "init", "--help"])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out
    assert "init" in captured.out


def test_wizard_command_functional(tmp_path, capsys):
    """
    Functional test for the wizard command: list, add, remove server using click.
    """
    import json
    import importlib
    from click.testing import CliRunner

    wizard_mod = importlib.import_module("create_sparc_py.cli.commands.wizard_command")
    runner = CliRunner()
    config_path = tmp_path / ".roo" / "mcp.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    # Patch CONFIG_PATH in the module
    wizard_mod.CONFIG_PATH = config_path

    # Add server
    result = runner.invoke(wizard_mod.wizard, ["add"], input="test1\nnpx\nfoo,bar\nread,write\n")
    assert result.exit_code == 0
    assert "Added/updated server: test1" in result.output

    # List servers
    result = runner.invoke(wizard_mod.wizard, ["list"])
    assert result.exit_code == 0
    assert "Configured MCP Servers:" in result.output
    assert "test1" in result.output

    # Remove server
    result = runner.invoke(wizard_mod.wizard, ["remove", "--server-id", "test1"])
    assert result.exit_code == 0
    assert "Removed server: test1" in result.output

    # Check config file is empty again
    if config_path.exists():
        config = json.loads(config_path.read_text())
    else:
        config = {}
    print("DEBUG CONFIG AFTER WIZARD:", config)
    assert config == {} or config == {"mcpServers": {}}
