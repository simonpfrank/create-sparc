# create-sparc-py add

Add a component to an existing SPARC project.

## Usage

```bash
# Add a component to a project
poetry run create-sparc-py add <component> <name>
```

## Options

- `<component>` - The type of component to add (e.g., api, database, service)
- `<name>` - The name of the component
- `-d, --directory <path>` - Directory to add the component to (default: current directory)

## Examples

```bash
# Add an API component named "users"
poetry run create-sparc-py add api users

# Add a database component named "main-db" to a specific directory
poetry run create-sparc-py add database main-db --directory ./backend
``` 