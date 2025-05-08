# Technical Design Document: create-sparc-py

## 1. Introduction

### 1.1 Purpose
This document outlines the technical design for create-sparc-py, a Python port of the create-sparc Node.js tool originally created by Reuven Cohen ([@ruvnet](https://github.com/ruvnet)). It provides detailed information about the system architecture, component design, interfaces, data structures, algorithms, and testing strategies.

### 1.2 Scope
The document covers the complete technical design of the create-sparc-py tool, including all components, modules, and interfaces. It serves as a blueprint for development and a reference for maintenance.

### 1.3 Definitions and Acronyms
- **SPARC**: Structure, Process, Architecture, Requirements, Compliance
- **CLI**: Command-Line Interface
- **MCP**: Multi-Cloud Provider
- **aiGI**: AI-Guided Implementation
- **TDD**: Test-Driven Development

## 2. System Architecture

### 2.1 High-Level Architecture

The create-sparc-py tool follows a modular architecture with these main components:

1. **CLI Module** - Handles command-line interaction, argument parsing, and command routing
2. **Core Module** - Contains the core business logic of the application
3. **Utils Module** - Provides utility functions used across the application
4. **Templates** - Contains project templates and boilerplate code
5. **Tests** - Contains unit and integration tests

```
create-sparc-py/
├── create_sparc_py/           # Main package
│   ├── cli/                   # CLI components
│   │   ├── commands/          # Individual command implementations
│   │   │   ├── help/          # Help command resources
│   │   │   ├── add.py         # Add command implementation
│   │   │   ├── aigi.py        # AIGI command implementation
│   │   │   ├── configure_mcp.py # MCP configuration command
│   │   │   ├── help.py        # Help command implementation
│   │   │   ├── init.py        # Init command implementation
│   │   │   ├── minimal.py     # Minimal command implementation
│   │   │   └── wizard.py      # Wizard command implementation
│   │   └── __init__.py        # CLI entry point
│   ├── core/                  # Core functionality
│   │   ├── config_manager/    # Configuration management
│   │   ├── file_manager/      # File management
│   │   ├── mcp_wizard/        # MCP wizard functionality
│   │   ├── project_generator/ # Project generation
│   │   ├── registry_client/   # Registry client
│   │   └── __init__.py        # Core module initialization
│   ├── utils/                 # Utility functions
│   │   └── __init__.py        # Utils module initialization
│   ├── templates/             # Project templates
│   │   └── minimal_roo/       # Minimal Roo template
│   ├── __init__.py            # Package initialization
│   └── __main__.py            # Entry point for execution
├── tests/                     # Test suite
│   ├── integration/           # Integration tests
│   ├── unit/                  # Unit tests
│   └── utils/                 # Test utilities
├── docs/                      # Documentation
│   ├── _build/                # Built documentation
│   ├── conf.py                # Sphinx configuration
│   ├── index.rst              # Documentation index
│   ├── prd.md                 # Product Requirements Document
│   └── tdd.md                 # Technical Design Document (this document)
├── pyproject.toml             # Poetry configuration
├── README.md                  # Project readme
└── .gitignore                 # Git ignore file
```

### 2.2 Component Interaction

The components interact as follows:

1. The CLI module receives user commands and parses them into a structured format.
2. The parsed commands are routed to the appropriate command handler in the CLI commands module.
3. The command handlers use the Core module to execute the requested operation.
4. Core modules interact with the Utils module for common functionality.
5. File operations, template rendering, and configuration management are handled by their respective modules.

## 3. Detailed Component Design

### 3.1 CLI Module

#### 3.1.1 Main CLI (`__init__.py`)

The main CLI module is responsible for:
- Parsing command-line arguments using argparse
- Routing commands to appropriate handlers
- Error handling and reporting
- Displaying help information

Key functions:
- `run(args)`: Entry point for CLI processing
- `parse_args(args)`: Parse command-line arguments into a structured format

Implementation notes:
- Will use argparse with both short and long parameter names
- Will parse arguments into a dictionary called script_args
- Will include a hook system for pre and post-command actions

#### 3.1.2 Command Handlers

Each command (init, add, help, etc.) will be implemented as a separate module in the `cli/commands/` directory. Each command module will have:

- A main function that implements the command
- Argument parsing specific to the command
- Calls to core components to execute functionality

Example for init command:
```python
def init_command(subparsers):
    """Add init command to argument parser."""
    parser = subparsers.add_parser('init', help='Create a new SPARC project')
    parser.add_argument('-N','name', help='Project name')
    parser.add_argument('-T', '--template', help='Template to use')
    parser.set_defaults(func=execute_init)

def execute_init(args):
    """Execute the init command."""
    # Implementation
    pass
```

### 3.2 Core Module

#### 3.2.1 Config Manager

Responsible for loading, saving, and managing configuration files.

Key classes:
- `ConfigManager`: Manages configuration files
  - `load(path)`: Load configuration from file
  - `save(config, path)`: Save configuration to file
  - `merge(base, override)`: Merge configurations

#### 3.2.2 File Manager

Handles file operations including reading, writing, copying, and template rendering.

Key classes:
- `FileManager`: Core file operations
  - `copy(src, dest)`: Copy file or directory
  - `template(src, dest, context)`: Render template
  - `mkdir(path)`: Create directory
  - `exists(path)`: Check if path exists
  - `is_dir(path)`: Check if path is directory
  - `is_file(path)`: Check if path is file
  - `read(path)`: Read file contents
  - `write(path, content)`: Write content to file

- `SymlinkManager`: Handle symbolic links
  - `create(target, link_name)`: Create symlink
  - `exists(link_name)`: Check if symlink exists
  - `is_symlink(path)`: Check if path is symlink

#### 3.2.3 Project Generator

Generates project structure based on templates and configuration.

Key classes:
- `ProjectGenerator`: Generate project structure
  - `generate(project_name, template, output_dir)`: Generate project
  - `post_process(output_dir)`: Post-processing tasks

#### 3.2.4 Registry Client

Communicates with remote registries.

Key classes:
- `RegistryClient`: Client for registry interaction
  - `get(path)`: Get resource from registry
  - `post(path, data)`: Send data to registry
  - `authenticate(credentials)`: Authenticate with registry

#### 3.2.5 MCP Wizard

Implements the MCP configuration wizard.

Key classes:
- `MCPWizard`: Interactive MCP configuration
  - `run()`: Run the wizard
  - `configure(options)`: Configure MCP with options
  - `generate_config()`: Generate configuration files

### 3.3 Utils Module

Provides utility functions used across the application.

Key functions and classes:
- `Logger`: Logging functionality
  - `debug(message)`: Log debug message
  - `info(message)`: Log info message
  - `warning(message)`: Log warning message
  - `error(message)`: Log error message
  - `success(message)`: Log success message
  - `set_level(level)`: Set logging level

- `ErrorHandler`: Error handling utilities
  - `categorize(error)`: Categorize error
  - `format(error, verbose)`: Format error message

- `FSUtils`: File system utilities
  - `exists(path)`: Check if path exists
  - `is_directory(path)`: Check if path is directory
  - `is_file(path)`: Check if path is file
  - `read_file(path)`: Read file contents
  - `write_file(path, content)`: Write content to file
  - `copy_file(src, dest)`: Copy a file
  - `copy_dir(src, dest)`: Copy a directory recursively

- `PathUtils`: Path manipulation utilities
  - `resolve(*paths)`: Resolve path
  - `join(*paths)`: Join path segments
  - `is_absolute(path)`: Check if path is absolute
  - `get_relative_path(path, base)`: Get path relative to base

## 4. Data Design

### 4.1 Configuration Files
Configuration files will use YAML format for compatibility and readability.

Example configuration:
```yaml
project:
  name: my-project
  version: 0.1.0
  description: My SPARC project
templates:
  base: minimal
components:
  - name: api
    type: module
  - name: database
    type: service
```

### 4.2 Template Structure
Templates will be organized as follows:
```
templates/
├── minimal_roo/            # Minimal Roo template
│   ├── structure/          # Project structure templates
│   │   ├── src/            # Source code templates
│   │   └── tests/          # Test templates
│   ├── config/             # Configuration templates
│   └── template.yaml       # Template metadata
```

### 4.3 In-Memory Data Structures
Key data structures:
- Command arguments dictionary (script_args)
- Project configuration object
- Template context dictionary

## 5. Interface Design

### 5.1 Command-Line Interface
The tool will provide a command-line interface with the following commands:

- `create-sparc-py init [name]`: Create a new project
- `create-sparc-py add [component]`: Add a component to an existing project
- `create-sparc-py help [command]`: Show help information
- `create-sparc-py wizard`: Run the interactive project setup wizard
- `create-sparc-py configure-mcp`: Configure MCP components
- `create-sparc-py aigi init [name]`: Create a new AIGI project
- `create-sparc-py minimal init [name]`: Create a new minimal Roo mode framework

Each command will support both short and long parameter names.

### 5.2 API Interface
The tool will provide a Python API for programmatic usage:

```python
from create_sparc_py import create_project, add_component

# Create a new project
create_project("my-project", template="minimal")

# Add a component to an existing project
add_component("my-project", "api", type="module")
```

## 6. Error Handling and Logging

### 6.1 Error Handling
Errors will be handled using Python's exception mechanism with custom exception classes for specific error types:

- `CreateSparcError`: Base exception class
- `ConfigError`: Configuration-related errors
- `FileError`: File operation errors
- `TemplateError`: Template rendering errors
- `RegistryError`: Registry communication errors

Each error will include a descriptive message and contextual information to help with debugging.

### 6.2 Logging
The tool will use a custom logger that:
- Supports different log levels (debug, info, warning, error)
- Provides colored output for better readability
- Can be configured to output to file or console
- Includes contextual information in log messages

## 7. Testing Strategy

### 7.1 Unit Testing
Unit tests will be implemented using pytest and will cover:
- Individual functions and methods
- Edge cases and error conditions
- Configuration parsing and validation
- Command parsing and routing

Mocking will be used to isolate components for testing.

### 7.2 Integration Testing
Integration tests will verify:
- End-to-end command execution
- Interaction between components
- File generation and template rendering
- Configuration loading and saving

### 7.3 Test Coverage
Test coverage targets:
- 90% code coverage for core modules
- 80% coverage for utility functions
- 95% coverage for critical path functionality

### 7.4 Testing Tools
- pytest for test runner
- pytest-cov for coverage reporting
- pytest-mock for mocking
- temporary directories for file operation testing

## 8. Dependencies

### 8.1 External Dependencies
- argparse: Command-line argument parsing (part of standard library for Python 3.12+)
- colorama: Terminal color output
- jinja2: Template rendering
- pyyaml: YAML file handling
- pathlib: Path manipulation (part of standard library, prioritized for file operations)
- pytest: Testing framework
- sphinx: Documentation generation
- inquirer: Interactive command-line user interfaces

### 8.2 Internal Dependencies
Component dependencies:
- CLI depends on Core
- Core depends on Utils
- Commands depend on their respective Core components

## 9. Development and Deployment

### 9.1 Development Environment
- Python 3.12+
- Poetry for dependency management
- Git for version control
- Pytest for testing
- Sphinx for documentation

### 9.2 Deployment
The package will be deployed as:
- A Python package installable via pip/poetry
- A command-line executable
- Potentially a Docker container for isolated execution

### 9.3 Build Process
Poetry will be used to build the package:
```
poetry build
```

## 10. Documentation

### 10.1 Code Documentation
- Google-style docstrings will be used for all modules, classes, and functions
- Each Python file will include a module-level docstring
- Type hints will be used throughout the codebase

Example docstring:
```python
def function_name(param1: str, param2: int) -> bool:
    """Short description of function.
    
    Longer description of function that can span multiple lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: If param1 is empty
    """
```

### 10.2 User Documentation
Will be generated using Sphinx and include:
- Installation guide
- Quick start
- Command reference
- Template customization guide
- Troubleshooting

### 10.3 Developer Documentation
Will include:
- Architecture overview
- Component documentation
- API reference
- Development setup guide
- Contribution guidelines

## 11. Required Python Packages

The project will use the following Python packages:

1. **Core Dependencies**
   - argparse (standard library)
   - colorama==0.4.6
   - jinja2==3.1.2
   - pyyaml==6.0.1
   - pathlib (standard library, prioritized for file operations)
   - inquirer==3.1.3 (Python equivalent for inquirer)
   - rich==13.5.2 (for terminal formatting, spinners - equivalent to ora)
   - shutil (standard library, for file operations)

2. **Development Dependencies**
   - poetry==1.6.1
   - pytest==7.4.0
   - pytest-cov==4.1.0
   - pytest-mock==3.11.1
   - black==23.7.0
   - isort==5.12.0
   - mypy==1.5.1
   - sphinx==7.2.5
   - sphinx-rtd-theme==1.3.0
   - typer==0.9.0 (for CLI in development tools)

## 12. Security Considerations

Security measures will include:
- Input validation to prevent command injection
- Safe handling of template rendering to prevent template injection
- Verification of downloaded resources
- Secure storage of credentials
- Validation of template content before rendering

## 13. Performance Considerations

Performance optimizations:
- Lazy loading of components
- Caching of template parsing
- Efficient file operations
- Parallelization of independent tasks
- Minimizing unnecessary file operations

## 14. Appendix

### 14.1 References
- Original create-sparc Node.js package by Reuven Cohen: [https://github.com/ruvnet/rUv-dev](https://github.com/ruvnet/rUv-dev)
- Python best practices and standards
- argparse documentation
- Sphinx documentation
- Poetry documentation
- pathlib documentation

### 14.2 Revision History
- Initial draft

### 14.3 Attribution
This technical design is based on the original create-sparc project by Reuven Cohen ([@ruvnet](https://github.com/ruvnet)) in the [rUv-dev](https://github.com/ruvnet/rUv-dev) repository. The Python port adapts the concepts and architecture of the original work to Python best practices and ecosystem. 