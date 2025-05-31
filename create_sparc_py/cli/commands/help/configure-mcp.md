# create-sparc-py configure-mcp

Configure Multi-Cloud Provider (MCP) settings for your project.

## Usage

```bash
# Run the MCP configuration command
poetry run create-sparc-py configure-mcp [options]
```

## Options

- `--add <provider>` - Add a new cloud provider configuration
- `--remove <provider>` - Remove a cloud provider configuration
- `--update <provider>` - Update an existing cloud provider configuration
- `--list` - List all configured cloud providers
- `--config-path <path>` - Custom path to MCP configuration file (default: .roo/mcp.json)
- `--region <region>` - Set the region for the provider
- `--api-key <key>` - API key for the provider (use ${env:VAR_NAME} for environment variables)
- `--debug` - Enable debug output
- `--validate` - Validate the MCP configuration

## Examples

```bash
# Add a new AWS provider
poetry run create-sparc-py configure-mcp --add aws --api-key "${env:AWS_API_KEY}" --region us-east-1

# Remove a provider
poetry run create-sparc-py configure-mcp --remove aws

# List all configured providers
poetry run create-sparc-py configure-mcp --list

# Validate the MCP configuration
poetry run create-sparc-py configure-mcp --validate
``` 