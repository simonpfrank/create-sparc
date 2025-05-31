# create-sparc-py init

Create a new SPARC project or initialize SPARC files in an existing project.

## Usage

```bash
# Create a new project with a specific name
poetry run create-sparc-py init my-project

# Initialize SPARC files in the current directory
poetry run create-sparc-py init
```

## Options

- `-t, --template <name>` - Template to use (default: "default")
- `-f, --force` - Allow initialization in non-empty directories
- `--skip-install` - Skip dependency installation
- `--use-npm` - Use npm as package manager
- `--use-yarn` - Use yarn as package manager
- `--use-pnpm` - Use pnpm as package manager
- `--no-git` - Skip git initialization
- `--typescript` - Use TypeScript
- `--no-symlink` - Disable symlink creation

## Examples

```bash
# Create a TypeScript project
poetry run create-sparc-py init my-ts-project --typescript

# Initialize SPARC files in current directory without git
poetry run create-sparc-py init --no-git

# Create a project with a specific template
poetry run create-sparc-py init my-project --template custom-template
``` 