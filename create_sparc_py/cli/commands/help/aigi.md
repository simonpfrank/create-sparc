# create-sparc aigi

Create and manage AIGI projects.

## Usage

### When using poetry:

```bash
poetry run create-sparc-py aigi init my-aigi-project
poetry run create-sparc-py aigi init
```

## Commands

### init [name]

Create a new AIGI project or initialize AIGI files in an existing project.

#### Options

- `-t, --template <name>` - Template to use (default: "default")
- `-f, --force` - Allow initialization in non-empty directories
- `--skip-install` - Skip dependency installation
- `--no-git` - Skip git initialization
- `--no-symlink` - Disable symlink creation

## Examples

```bash
poetry run create-sparc-py aigi init my-ts-aigi-project --template custom-template
poetry run create-sparc-py aigi init --no-git
``` 