# create-sparc-py minimal

Create a new minimal Roo mode framework or initialize minimal Roo mode files in an existing project.

## Usage

```bash
poetry run create-sparc-py minimal init my-project
poetry run create-sparc-py minimal init
```

## Options

- `-f, --force` - Allow initialization in non-empty directories
- `--skip-install` - Skip dependency installation
- `--no-git` - Skip git initialization
- `--no-symlink` - Disable symlink creation

## Examples

```bash
poetry run create-sparc-py minimal init my-ts-project --force
poetry run create-sparc-py minimal init --no-git
```

## What is a Minimal Roo Mode Framework?

The minimal Roo mode framework provides a lightweight foundation for creating custom Roo modes. It includes only the essential files and structure needed to get started with Roo mode development, making it ideal for developers who want to create their own custom modes without the full SPARC project structure. 