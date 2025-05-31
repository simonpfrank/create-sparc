# create-sparc-py aigi

Create and manage AIGI projects.

## Usage

```bash
# Create a new AIGI project with a specific name
poetry run create-sparc-py aigi init my-aigi-project

# Initialize AIGI files in the current directory
poetry run create-sparc-py aigi init
```

## Commands

### init [name]

Create a new AIGI project or initialize AIGI files in an existing project.

#### Options

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
# Create a TypeScript AIGI project
poetry run create-sparc-py aigi init my-ts-aigi-project --typescript

# Initialize AIGI files in current directory without git
poetry run create-sparc-py aigi init --no-git

# Create an AIGI project with a specific template
poetry run create-sparc-py aigi init my-aigi-project --template custom-template
``` 