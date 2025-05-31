# create-sparc-py init

Create a new SPARC project or initialize SPARC files in an existing project.

## Usage

```bash
poetry run create-sparc-py init my-project
poetry run create-sparc-py init
```

## Options

- `-t, --template <name>` - Template to use (default: "default")
- `-f, --force` - Allow initialization in non-empty directories
- `--skip-install` - Skip dependency installation
- `--no-git` - Skip git initialization
- `--no-symlink` - Disable symlink creation

## Examples

```bash
poetry run create-sparc-py init my-ts-project --template custom-template
poetry run create-sparc-py init --no-git
``` 