import pytest
import tempfile
import shutil
from pathlib import Path
import json
from create_sparc_py.core.mcp_wizard import MCPWizard
from create_sparc_py.core.mcp_wizard_workflow import MCPWizardWorkflow


def test_mcp_wizard_methods_exist(tmp_path):
    config_path = tmp_path / "mcp.json"
    wizard = MCPWizard(config_path)
    # Should not raise
    wizard.run  # callable
    wizard.configure  # callable
    wizard.generate_config  # callable


def test_add_and_list_server(tmp_path, capsys):
    config_path = tmp_path / "mcp.json"
    wizard = MCPWizard(config_path)
    wizard.add_server(server_id="srv1", command="npx", args="foo,bar", permissions="read,write")
    captured = capsys.readouterr()
    assert "Added/updated server: srv1" in captured.out
    # List servers
    wizard.list_servers()
    captured = capsys.readouterr()
    assert "srv1" in captured.out
    # Config file should exist
    assert config_path.exists()
    with open(config_path) as f:
        data = json.load(f)
    assert "srv1" in data["mcpServers"]


def test_remove_server(tmp_path, capsys):
    config_path = tmp_path / "mcp.json"
    wizard = MCPWizard(config_path)
    wizard.add_server(server_id="srv2", command="npx", args="a", permissions="b")
    wizard.remove_server(server_id="srv2")
    captured = capsys.readouterr()
    assert "Removed server: srv2" in captured.out
    # Should be removed from config
    with open(config_path) as f:
        data = json.load(f)
    assert "srv2" not in data["mcpServers"]


def test_configure_and_generate_config(tmp_path):
    config_path = tmp_path / "mcp.json"
    wizard = MCPWizard(config_path)
    options = {"mcpServers": {"srv3": {"command": "npx", "args": ["x"], "permissions": ["y"]}}}
    wizard.configure(options)
    with open(config_path) as f:
        data = json.load(f)
    assert "srv3" in data["mcpServers"]
    # generate_config
    new_config = {"mcpServers": {"srv4": {"command": "cmd", "args": ["a"], "permissions": ["b"]}}}
    wizard.generate_config(new_config)
    with open(config_path) as f:
        data = json.load(f)
    assert "srv4" in data["mcpServers"]
    assert "srv3" not in data["mcpServers"]


def test_workflow_list_configured_servers_empty(tmp_path):
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    # No config file yet
    result = workflow.list_configured_servers()
    assert result["success"] is True
    assert result["servers"] == []


def test_workflow_list_configured_servers_with_servers(tmp_path):
    mcp_config = tmp_path / ".roo" / "mcp.json"
    mcp_config.parent.mkdir(parents=True, exist_ok=True)
    data = {"mcpServers": {"srvA": {"command": "npx", "args": ["foo"], "permissions": ["bar"]}}}
    mcp_config.write_text(json.dumps(data))
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    result = workflow.list_configured_servers()
    assert result["success"] is True
    assert "srvA" in result["servers"]
    assert result["details"]["srvA"]["command"] == "npx"


def test_workflow_validate_configuration_valid(tmp_path):
    mcp_config = tmp_path / ".roo" / "mcp.json"
    mcp_config.parent.mkdir(parents=True, exist_ok=True)
    data = {"mcpServers": {"srvB": {"command": "npx", "args": ["foo"], "permissions": ["bar"]}}}
    mcp_config.write_text(json.dumps(data))
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    result = workflow.validate_configuration()
    assert result["success"] is True
    assert result["errors"] == []


def test_workflow_validate_configuration_missing_file(tmp_path):
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    result = workflow.validate_configuration()
    assert result["success"] is False
    assert "Config file does not exist." in result["errors"][0]


def test_workflow_validate_configuration_invalid(tmp_path):
    mcp_config = tmp_path / ".roo" / "mcp.json"
    mcp_config.parent.mkdir(parents=True, exist_ok=True)
    # Missing required fields in server
    data = {"mcpServers": {"srvC": {"args": ["foo"]}}}
    mcp_config.write_text(json.dumps(data))
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    result = workflow.validate_configuration()
    assert result["success"] is False
    assert any("missing required field" in e for e in result["errors"])


def test_workflow_backup_and_restore(tmp_path):
    # Setup: create config files
    roo_dir = tmp_path / ".roo"
    roo_dir.mkdir(parents=True, exist_ok=True)
    mcp_config = roo_dir / "mcp.json"
    roomodes = tmp_path / ".roomodes"
    mcp_data = {"mcpServers": {"srvD": {"command": "npx", "args": ["foo"], "permissions": ["bar"]}}}
    mcp_config.write_text(json.dumps(mcp_data))
    roomodes.write_text("testmode")
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    # Backup
    backup_result = workflow.backup_configuration()
    assert backup_result["success"] is True
    backup_paths = backup_result["backupPaths"]
    assert "mcp.json" in backup_paths
    assert ".roomodes" in backup_paths
    # Overwrite files
    mcp_config.write_text(json.dumps({"mcpServers": {}}))
    roomodes.write_text("corrupted")
    # Restore
    restore_result = workflow.restore_configuration(backup_paths)
    assert restore_result["success"] is True
    # Check restored content
    with open(mcp_config) as f:
        restored = json.load(f)
    assert restored == mcp_data
    assert roomodes.read_text() == "testmode"


def test_workflow_backup_no_files(tmp_path):
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    result = workflow.backup_configuration()
    assert result["success"] is False
    assert "No config files to backup" in result["error"]


def test_workflow_restore_invalid(tmp_path):
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    # Provide empty backup_paths
    result = workflow.restore_configuration({})
    assert result["success"] is False
    assert "No valid backup paths" in result["error"]


def test_workflow_audit_security(tmp_path):
    mcp_config = tmp_path / ".roo" / "mcp.json"
    mcp_config.parent.mkdir(parents=True, exist_ok=True)
    # Hardcoded secret and wildcard permission
    data = {
        "mcpServers": {
            "srvE": {"args": ["--token", "mysecrettoken"], "alwaysAllow": ["*"]},
            "srvF": {"args": ["--api-key", "${env:SRVF_API_KEY}"]},
        }
    }
    mcp_config.write_text(json.dumps(data))
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    result = workflow.audit_security()
    assert result["success"] is True
    assert result["secure"] is False
    assert any("Hardcoded sensitive value" in i["message"] for i in result["issues"])
    assert any("Wildcard permission" in i["message"] for i in result["issues"])
    # If no issues, recommendations should be present
    mcp_config.write_text(json.dumps({"mcpServers": {"srvG": {"args": ["--token", "${env:SRVG_TOKEN}"]}}}))
    result2 = workflow.audit_security()
    assert result2["success"] is True
    assert result2["secure"] is True
    assert result2["issues"] == []
    assert result2["recommendations"]


def test_workflow_validate_env_var_references(tmp_path, monkeypatch):
    mcp_config = tmp_path / ".roo" / "mcp.json"
    mcp_config.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "mcpServers": {
            "srvH": {"args": ["--api-key", "${env:SRVH_API_KEY}"]},
            "srvI": {"args": ["--token", "${env:SRVI_TOKEN}", "--other", "nonsensitive"]},
        }
    }
    mcp_config.write_text(json.dumps(data))
    workflow = MCPWizardWorkflow(project_path=tmp_path)
    # No env vars set
    result = workflow.validate_env_var_references()
    assert result["success"] is True
    assert result["valid"] is False
    assert "SRVH_API_KEY" in result["missingVariables"]
    assert "SRVI_TOKEN" in result["missingVariables"]
    # Set one env var
    monkeypatch.setenv("SRVH_API_KEY", "abc123")
    result2 = workflow.validate_env_var_references()
    assert result2["success"] is True
    assert result2["valid"] is False
    assert "SRVI_TOKEN" in result2["missingVariables"]
    assert "SRVH_API_KEY" not in result2["missingVariables"]
    # Set both env vars
    monkeypatch.setenv("SRVI_TOKEN", "def456")
    result3 = workflow.validate_env_var_references()
    assert result3["success"] is True
    assert result3["valid"] is True
    assert result3["missingVariables"] == []
