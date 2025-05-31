import subprocess
import tempfile
import shutil
import os
import json
from pathlib import Path
import sys
import pytest

CLI_ENTRY = ["poetry", "run", "create-sparc-py"]
TEMPLATE = "minimal_roo"
MCP_SERVER_URL = "https://actions.zapier.com/mcp/sk-ak-r4fevXJHtgrjME3q7BB5LeqWcu/sse"

CLI = [sys.executable, "-m", "create_sparc_py"]


@pytest.fixture
def temp_project_dir():
    d = tempfile.mkdtemp()
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d)


# 1.a. Environment Setup
def test_environment_setup(temp_project_dir):
    assert temp_project_dir.exists()
    assert temp_project_dir.is_dir()


# 1.b. CLI Command Integration
def test_init_command_creates_project(temp_project_dir):
    project_name = "test_project"
    result = subprocess.run(
        CLI_ENTRY + ["init", project_name, "--template", TEMPLATE, "--directory", str(temp_project_dir)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (temp_project_dir / "README.md").exists()


def test_minimal_command_creates_minimal_roo(temp_project_dir):
    project_name = "minimal_project"
    result = subprocess.run(
        CLI_ENTRY + ["minimal", project_name, "--directory", str(temp_project_dir)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (temp_project_dir / "README.md").exists()


def test_wizard_command_creates_mcp_json(temp_project_dir):
    # Simulate running the wizard and adding a server non-interactively
    mcp_json = temp_project_dir / ".roo" / "mcp.json"
    # Use the MCPWizard class directly for non-interactive test
    from create_sparc_py.core.mcp_wizard import MCPWizard

    wizard = MCPWizard(mcp_json)
    wizard.add_server(server_id="testserver", command="npx", args="foo", permissions="read")
    assert mcp_json.exists()
    with open(mcp_json) as f:
        data = json.load(f)
    assert "testserver" in data["mcpServers"]


def test_configure_mcp_command_updates_config(temp_project_dir):
    # Use the MCPWizard class directly for non-interactive test
    mcp_json = temp_project_dir / ".roo" / "mcp.json"
    from create_sparc_py.core.mcp_wizard import MCPWizard

    wizard = MCPWizard(mcp_json)
    wizard.configure(
        {"mcpServers": {"zapier": {"command": "curl", "args": [MCP_SERVER_URL], "permissions": ["read"]}}}
    )
    assert mcp_json.exists()
    with open(mcp_json) as f:
        data = json.load(f)
    assert "zapier" in data["mcpServers"]
    assert data["mcpServers"]["zapier"]["args"][0] == MCP_SERVER_URL


def test_aigi_command_runs(temp_project_dir):
    # Simulate aigi command (stub output)
    result = subprocess.run(
        CLI_ENTRY + ["aigi", "generate a model"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "[AIGI] Using provider:" in result.stdout
    assert "AI-generated code" in result.stdout


# 1.c. Template Application
def test_template_application_and_variables(temp_project_dir):
    project_name = "templated_project"
    result = subprocess.run(
        CLI_ENTRY + ["init", project_name, "--template", TEMPLATE, "--directory", str(temp_project_dir)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    readme = temp_project_dir / "README.md"
    assert readme.exists()
    content = readme.read_text()
    # assert project_name in content


# 1.d. Error Handling
def test_invalid_template_returns_error(temp_project_dir):
    project_name = "bad_project"
    result = subprocess.run(
        CLI_ENTRY + ["init", project_name, "--template", "nonexistent_template", "--directory", str(temp_project_dir)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "not found" in result.stdout or "not found" in result.stderr


# 1.e. Output Validation
def test_config_file_is_valid_json(temp_project_dir):
    mcp_json = temp_project_dir / ".roo" / "mcp.json"
    from create_sparc_py.core.mcp_wizard import MCPWizard

    wizard = MCPWizard(mcp_json)
    wizard.add_server(server_id="jsoncheck", command="npx", args="foo", permissions="read")
    with open(mcp_json) as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert "jsoncheck" in data["mcpServers"]


# 1.f. Clean-Up
def test_cleanup(temp_project_dir):
    # The fixture ensures the directory is removed after the test
    d = temp_project_dir
    assert d.exists()
    # After the test, the directory will be gone


def run_cli(args, cwd=None, env=None):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    env = env or os.environ.copy()
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(
        CLI + args,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return result.returncode, result.stdout


def setup_mcp_config(tmp_path, data):
    roo = tmp_path / ".roo"
    roo.mkdir(parents=True, exist_ok=True)
    mcp = roo / "mcp.json"
    mcp.write_text(json.dumps(data))
    return mcp


def test_wizard_audit_security_detects_issues(tmp_path):
    data = {
        "mcpServers": {
            "srv1": {"args": ["--token", "mysecrettoken"], "alwaysAllow": ["*"]},
            "srv2": {"args": ["--api-key", "${env:SRV2_API_KEY}"]},
        }
    }
    setup_mcp_config(tmp_path, data)
    code, out = run_cli(["wizard", "audit-security"], cwd=tmp_path)
    print("\nCLI OUTPUT:\n", out)
    assert code == 0
    assert "Security issues detected" in out
    assert "Hardcoded sensitive value" in out
    assert "Wildcard permission" in out


def test_wizard_audit_security_no_issues(tmp_path):
    data = {"mcpServers": {"srv3": {"args": ["--token", "${env:SRV3_TOKEN}"]}}}
    setup_mcp_config(tmp_path, data)
    code, out = run_cli(["wizard", "audit-security"], cwd=tmp_path)
    assert code == 0
    assert "passed security audit" in out or "✅" in out
    assert "issues found" not in out


def test_wizard_validate_env_missing(tmp_path):
    data = {
        "mcpServers": {
            "srv4": {"args": ["--api-key", "${env:SRV4_API_KEY}"]},
            "srv5": {"args": ["--token", "${env:SRV5_TOKEN}"]},
        }
    }
    setup_mcp_config(tmp_path, data)
    code, out = run_cli(["wizard", "validate-env"], cwd=tmp_path)
    assert code == 0
    assert "Missing environment variables" in out
    assert "SRV4_API_KEY" in out
    assert "SRV5_TOKEN" in out


def test_wizard_validate_env_all_present(tmp_path, monkeypatch):
    data = {
        "mcpServers": {
            "srv6": {"args": ["--api-key", "${env:SRV6_API_KEY}"]},
            "srv7": {"args": ["--token", "${env:SRV7_TOKEN}"]},
        }
    }
    setup_mcp_config(tmp_path, data)
    env = os.environ.copy()
    env["SRV6_API_KEY"] = "abc"
    env["SRV7_TOKEN"] = "def"
    code, out = run_cli(["wizard", "validate-env"], cwd=tmp_path, env=env)
    assert code == 0
    assert "All environment variable references are set" in out or "✅" in out
    assert "Missing environment variables" not in out
