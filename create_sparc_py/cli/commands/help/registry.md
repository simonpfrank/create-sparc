# create-sparc-py registry

Interact with the remote template and component registry.

## Usage

```bash
# List available templates/components
poetry run create-sparc-py registry list

# Get details for a specific template/component
poetry run create-sparc-py registry get <name>

# Publish a template/component
poetry run create-sparc-py registry post <path>

# Authenticate with the registry
poetry run create-sparc-py registry auth --token <token>
```

## Commands

- `list` - List all available templates/components in the registry
- `get <name>` - Get details for a specific template/component
- `post <path>` - Publish a template/component to the registry
- `auth --token <token>` - Authenticate with the registry using a token

## Options

- `--registry <url>` - Use a custom registry URL
- `--token <token>` - Authentication token for the registry
- `--debug` - Enable debug output

## Examples

```bash
# List all templates
poetry run create-sparc-py registry list

# Get details for a template
poetry run create-sparc-py registry get minimal_roo

# Publish a template
poetry run create-sparc-py registry post ./templates/minimal_roo

# Authenticate with a token
poetry run create-sparc-py registry auth --token my-secret-token
``` 