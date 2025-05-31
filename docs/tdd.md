# Technical Design Document: create-sparc-py

## 1. Introduction

### 1.1 Purpose
This document outlines the technical design for create-sparc-py, a Python port of the create-sparc Node.js tool originally created by Reuven Cohen ([@ruvnet](https://github.com/ruvnet)). It provides detailed information about the system architecture, component design, interfaces, data structures, algorithms, and testing strategies.

If there is any functional definition missing in this document refer to the javascript source in <project root>/node_version

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
- Will use click for interactive prompts and command groups (replaces inquirer)

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
- click: Interactive command-line user interfaces (replaces inquirer)
- rich: Terminal formatting, spinners - equivalent to ora
- shutil: Standard library, for file operations
- pytest: Testing framework
- sphinx: Documentation generation

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
   - click: Interactive command-line user interfaces (replaces inquirer)
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

## 15. Project Completion Plan

### 15.1 Overview

Based on the comprehensive SPARC framework methodology (as defined in [SPARC.md](https://gist.github.com/ruvnet/27ee9b1dc01eec69bc270e2861aa2c05)), this completion plan outlines the remaining work to achieve full functionality. The plan is organized into small, incremental iterations that can be developed, tested, and validated independently.

### 15.2 Current Status Assessment

**Completed Components (85% of core infrastructure):**
- ✅ Utils Module (Logger, ErrorHandler, FSUtils, PathUtils)
- ✅ Core Module (ConfigManager, TemplateManager, ProjectGenerator)
- ✅ Basic CLI infrastructure with argparse
- ✅ Two CLI commands (init, add)
- ✅ Template system foundation
- ✅ Comprehensive unit tests (66 tests, 100% pass rate)

**Missing Components:**
- ❌ 5 CLI commands (help, wizard, configure-mcp, aigi, minimal)
- ❌ SymlinkManager for advanced file operations
- ❌ RegistryClient for remote template/component management
- ❌ MCPWizard for MCP configuration
- ❌ Integration tests
- ❌ Complete template conversion
- ❌ User and developer documentation

### 15.3 Iteration Plan

#### **Iteration 1: CLI Foundation Completion** (Priority: Critical)
**Goal:** Fix current CLI issues and implement missing command stubs
**Duration:** 1-2 days
**Dependencies:** None

**Tasks:**
1. **Fix CLI Import Issues**
   - Resolve AttributeError in CLI command routing
   - Update `create_sparc_py/cli/commands/__init__.py` imports
   - Fix function reference inconsistencies

2. **Implement Command Stubs**
   - Create `help_command.py` with basic help functionality
   - Create `wizard_command.py` with placeholder implementation
   - Create `mcp_command.py` with placeholder implementation
   - Create `aigi_command.py` with placeholder implementation
   - Create `minimal_command.py` with placeholder implementation

3. **Unit Tests**
   - Add tests for new command stubs
   - Test CLI argument parsing for all commands
   - Verify command routing works correctly

**Acceptance Criteria:**
- All CLI commands can be invoked without errors
- `create-sparc-py --help` displays all available commands
- Basic functionality works: `create-sparc-py init test-project`

#### **Iteration 2: Help System Implementation** (Priority: High)
**Goal:** Complete help command with comprehensive documentation
**Duration:** 2-3 days
**Dependencies:** Iteration 1

**Tasks:**
1. **Enhanced Help Command**
   - Implement context-sensitive help
   - Add command-specific help (e.g., `create-sparc-py help init`)
   - Include examples and usage patterns
   - Support for `--help` flag on all commands

2. **Documentation Integration**
   - Link help system to markdown documentation
   - Generate help content from docstrings
   - Add interactive help navigation

3. **Unit Tests**
   - Test help command functionality
   - Verify help content accuracy
   - Test help for all commands

**Acceptance Criteria:**
- `create-sparc-py help` shows comprehensive command list
- `create-sparc-py help <command>` shows detailed command help
- All commands support `--help` flag

#### **Iteration 3: Template System Enhancement** (Priority: High)
**Goal:** Complete template conversion and add SPARC-specific templates
**Duration:** 3-4 days
**Dependencies:** Iteration 1

**Tasks:**
1. **Template Conversion**
   - Complete conversion of Node.js templates to Python
   - Add SPARC methodology-specific templates
   - Implement minimal_roo template
   - Add aiGI template structure

2. **Template Validation**
   - Enhance template validation system
   - Add template metadata validation
   - Implement template dependency checking

3. **Variable System Enhancement**
   - Expand template variable system
   - Add conditional template rendering
   - Support for nested template structures

4. **Unit Tests**
   - Test all new templates
   - Verify template variable substitution
   - Test template validation logic

**Acceptance Criteria:**
- All templates from original Node.js version are converted
- SPARC methodology templates are available
- Template validation prevents corrupted templates

#### **Iteration 4: Wizard Implementation** (Priority: High)
**Goal:** Interactive project creation wizard following SPARC methodology
**Duration:** 4-5 days
**Dependencies:** Iterations 1, 3

**Tasks:**
1. **Interactive Wizard**
   - Implement step-by-step project creation
   - Add SPARC methodology guidance
   - Support for template selection
   - Configuration option selection

2. **SPARC Integration**
   - Guide users through Specification phase
   - Collect project requirements interactively
   - Generate initial project documentation
   - Create SPARC-compliant project structure

3. **User Experience**
   - Add progress indicators
   - Implement input validation
   - Support for going back/forward in wizard
   - Save/resume wizard sessions

4. **Unit Tests**
   - Test wizard flow logic
   - Mock user input scenarios
   - Verify generated project structure

**Acceptance Criteria:**
- Wizard guides users through complete project setup
- Generated projects follow SPARC methodology
- Wizard can be interrupted and resumed

#### **Iteration 5: SymlinkManager Implementation** (Priority: Medium)
**Goal:** Advanced file operations with symbolic link support
**Duration:** 2-3 days
**Dependencies:** Iteration 1

**Tasks:**
1. **SymlinkManager Class**
   - Implement `create()` method for symlink creation
   - Implement `exists()` method for symlink detection
   - Implement `is_symlink()` method for symlink validation
   - Cross-platform compatibility (Windows/Unix)

2. **Integration with FileManager**
   - Update FileManager to use SymlinkManager
   - Add symlink support to template system
   - Handle symlink permissions and security

3. **Unit Tests**
   - Test symlink creation and detection
   - Test cross-platform compatibility
   - Test error handling for invalid symlinks

**Acceptance Criteria:**
- Symlinks work correctly on all supported platforms
- Template system can create and manage symlinks
- Proper error handling for symlink operations

#### **Iteration 6: MCP Wizard Implementation** (Priority: Medium)
**Goal:** Multi-Cloud Provider configuration wizard
**Duration:** 3-4 days
**Dependencies:** Iterations 1, 4

**Tasks:**
1. **MCPWizard Class**
   - Implement interactive MCP configuration
   - Support for multiple cloud providers
   - Generate MCP configuration files
   - Validate MCP settings

2. **Cloud Provider Support**
   - Add AWS configuration templates
   - Add Azure configuration templates
   - Add GCP configuration templates
   - Add generic cloud provider support

3. **Configuration Management**
   - Integrate with ConfigManager
   - Support for environment-specific configs
   - Secure credential handling

4. **Unit Tests**
   - Test MCP wizard flow
   - Mock cloud provider interactions
   - Verify configuration file generation

**Acceptance Criteria:**
- MCP wizard configures cloud providers correctly
- Generated configurations are valid
- Secure handling of cloud credentials

#### **Iteration 7: AIGI Command Implementation** (Priority: Medium)
**Goal:** AI-Guided Implementation command for enhanced development
**Duration:** 3-4 days
**Dependencies:** Iterations 1, 3

**Tasks:**
1. **AIGI Command**
   - Implement AI-guided project creation
   - Support for AI model integration
   - Generate AI-enhanced project templates
   - Add AI-powered code generation hints

2. **AI Integration Framework**
   - Support for multiple AI providers (OpenAI, etc.)
   - Template generation with AI assistance
   - Code scaffolding with AI suggestions
   - Documentation generation with AI

3. **Configuration**
   - AI provider configuration
   - API key management
   - Model selection and parameters
   - Cost optimization settings

4. **Unit Tests**
   - Mock AI provider interactions
   - Test AI-generated content validation
   - Verify configuration handling

**Acceptance Criteria:**
- AIGI command creates AI-enhanced projects
- Multiple AI providers are supported
- Generated code follows best practices

#### **Iteration 8: Minimal Command Implementation** (Priority: Medium)
**Goal:** Minimal Roo mode framework creation
**Duration:** 2-3 days
**Dependencies:** Iterations 1, 3

**Tasks:**
1. **Minimal Command**
   - Implement minimal project creation
   - Support for Roo mode framework
   - Lightweight project templates
   - Fast project initialization

2. **Roo Mode Integration**
   - Create Roo-specific templates
   - Implement Roo boomerang mode support
   - Add Roo-specific configuration
   - Support for Roo development workflow

3. **Performance Optimization**
   - Optimize for fast project creation
   - Minimize dependencies
   - Streamlined file operations

4. **Unit Tests**
   - Test minimal project creation
   - Verify Roo mode compatibility
   - Performance benchmarking

**Acceptance Criteria:**
- Minimal projects are created quickly
- Roo mode integration works correctly
- Projects are lightweight and functional

#### **Iteration 9: RegistryClient Implementation** (Priority: Low)
**Goal:** Remote template and component registry support
**Duration:** 4-5 days
**Dependencies:** Iteration 1

**Tasks:**
1. **RegistryClient Class**
   - Implement HTTP client for registry communication
   - Support for authentication and authorization
   - Template and component downloading
   - Registry metadata handling

2. **Registry Protocol**
   - Define registry API specification
   - Implement registry discovery
   - Support for multiple registries
   - Version management for templates

3. **Security and Validation**
   - Verify downloaded content integrity
   - Implement signature validation
   - Secure credential storage
   - Malware scanning integration

4. **Unit Tests**
   - Mock registry server interactions
   - Test authentication flows
   - Verify content validation

**Acceptance Criteria:**
- Can download templates from remote registries
- Secure handling of remote content
- Support for multiple registry sources

#### **Iteration 10: Integration Testing** (Priority: High)
**Goal:** Comprehensive end-to-end testing
**Duration:** 3-4 days
**Dependencies:** Iterations 1-9

**Tasks:**
1. **End-to-End Tests**
   - **1.a. Integration Test Environment Setup**
     - Use a temporary directory for each test run to ensure isolation.
     - All CLI commands and file operations are run in this environment.
     - Clean up after each test.
   - **1.b. CLI Command Integration Tests**
     - Test `create_sparc_py init` to create a new project with the `minimal_roo` template.
     - Test `create_sparc_py add` to add a component to an existing project.
     - Test `create_sparc_py minimal` to create a minimal Roo project.
     - Test `create_sparc_py wizard` to run the interactive wizard and verify `.roo/mcp.json` output.
     - Test `create_sparc_py configure-mcp` to configure MCP and verify config file.
     - Test `create_sparc_py aigi` to run AI-guided code generation and verify output.
   - **1.c. Template Application End-to-End**
     - Verify that templates are applied correctly, files are generated, and variables are substituted.
     - Check that the output project structure matches expectations.
   - **1.d. Error Handling and Recovery**
     - Test invalid input scenarios (e.g., missing required arguments, invalid template names).
     - Test recovery from partial failures (e.g., interrupted project creation).
   - **1.e. File System and Output Validation**
     - After each command, verify that the expected files and directories exist and contain the correct content.
     - Validate generated config files, project files, and template outputs.
   - **1.f. Clean-Up and Isolation**
     - Ensure all test artifacts are removed after each test.
     - No test should affect the real user workspace or global config.

2. **Performance Testing**
   - Benchmark project creation times
   - Memory usage optimization
   - Large project handling
   - Concurrent operation testing

3. **Error Scenario Testing**
   - Test error handling and recovery
   - Invalid input handling
   - Network failure scenarios
   - File system permission issues

4. **User Acceptance Testing**
   - Real-world usage scenarios
   - Documentation accuracy verification
   - User experience validation

**Acceptance Criteria:**
- All integration tests pass
- Performance meets requirements
- Error handling is robust and user-friendly

---

### **TDD: Integration Test List for Task 1**

- **1.a. Environment Setup**
  - Test: Temporary directory is created and cleaned up for each integration test.
- **1.b. CLI Command Integration**
  - Test: `create_sparc_py init` creates a project with `minimal_roo` and all expected files.
  - Test: `create_sparc_py add` adds a component and updates project files.
  - Test: `create_sparc_py minimal` creates a minimal Roo project with correct structure.
  - Test: `create_sparc_py wizard` creates/updates `.roo/mcp.json` and can add/list/remove servers.
  - Test: `create_sparc_py configure-mcp` updates MCP config and is reflected in `.roo/mcp.json`.
  - Test: `create_sparc_py aigi` generates code and outputs expected result.
- **1.c. Template Application**
  - Test: All template files are copied and variables replaced for `minimal_roo`.
  - Test: Output structure matches template definition.
- **1.d. Error Handling**
  - Test: CLI returns error codes and messages for invalid input (e.g., missing args, bad template).
  - Test: Partial/incomplete operations are recoverable (e.g., re-running after failure).
- **1.e. Output Validation**
  - Test: All expected files exist and contain correct content after each command.
  - Test: Config files are valid JSON and match expected schema.
- **1.f. Clean-Up**
  - Test: No files remain after test run; workspace is clean.

---

### **Integration Test Requirements & Information Needed**

- **CLI Entry Point:** `create_sparc_py` (run via subprocess in tests)
- **Template:** Use `minimal_roo` for all relevant tests
- **Platform:** macOS (current environment)
- **MCP Server Example:** Use https://actions.zapier.com/mcp/sk-ak-r4fevXJHtgrjME3q7BB5LeqWcu/sse as a sample single tool MCP server for wizard/configure-mcp tests
- **Functional Equivalence:** Tests should ensure parity with the Node.js version in all workflows and outputs

**Files/Artifacts to be Created by Tests:**
- Temporary project directories and files
- `.roo/mcp.json` and other config files
- Output files from templates and commands

**Files/Artifacts Needed from You:**
- If you want to test with a custom template or config not already in the repo, please provide those files
- If you want to test with a real registry server, please provide a test endpoint (otherwise, registry tests will be skipped or stubbed)

---

**Please review this plan and TDD list. Once approved, I will proceed to implement the integration tests as described.**

### 15.5 Risk Mitigation

**Technical Risks:**
- **CLI complexity**: Start with simple implementations, iterate
- **Cross-platform compatibility**: Test early and often
- **Template system complexity**: Use proven templating libraries

**Project Risks:**
- **Scope creep**: Stick to defined iterations
- **Integration issues**: Continuous integration testing
- **Performance issues**: Regular benchmarking

### 15.6 Success Metrics

**Functionality Metrics:**
- All CLI commands implemented and working
- 100% template conversion from Node.js version
- >95% test coverage maintained
- All SPARC methodology features supported

**Quality Metrics:**
- Zero critical bugs in release
- <2 second project creation time
- Cross-platform compatibility verified
- User documentation completeness >95%

**Adoption Metrics:**
- Successful PyPI package publication
- Documentation accessibility
- Community feedback integration

### 15.7 Timeline Summary

**Total Estimated Duration:** 8-10 weeks

**Critical Path:**
1. Iteration 1 (CLI Foundation) - Week 1
2. Iteration 2 (Help System) - Week 2
3. Iteration 3 (Templates) - Week 3
4. Iteration 4 (Wizard) - Week 4-5
5. Iteration 10 (Integration Testing) - Week 6
6. Iteration 11 (Documentation) - Week 7
7. Iteration 12 (Packaging) - Week 8

**Parallel Development:**
- Iterations 5-9 can be developed in parallel after core foundation
- Documentation can be written alongside development
- Testing can be continuous throughout

This completion plan ensures that the create-sparc-py project will fully implement the SPARC framework methodology while maintaining high code quality and comprehensive testing throughout the development process.

## 16. Completion Plan: Missing Functionality Parity

This section outlines the plan to achieve full feature parity with the Node.js version, based on the audit in `docs/missing_functionality.md`. Each iteration includes coding, unit testing, and integration testing.

---

### **Iteration 11: Help System Parity**
- **Goal:** Implement a markdown-driven, context-sensitive help system matching Node.js.
- **Tasks:**
  1. Implement markdown help file loader and renderer for each command.
  2. Integrate help system with CLI (context-sensitive, subcommands, options).
  3. Add/port all markdown help files from Node.js.
  4. Unit tests for help rendering and CLI integration.
  5. Integration tests for `help` and `--help` on all commands.

---

### **Iteration 12: Wizard Workflow & Security**
- **Goal:** Port full wizard workflow, validation, and security modules.
- **Tasks:**
  1. Port wizard-core.js, validation.js, and security.js logic to Python.
  2. Integrate workflow engine into wizard command.
  3. Implement advanced config generation and validation.
  4. Add security checks and validation steps.
  5. Unit tests for workflow, validation, and security.
  6. Integration tests for full wizard flows.

---

### **Iteration 13: Configure-MCP Parity**
- **Goal:** Implement full configure-mcp command with advanced options and validation.
- **Tasks:**
  1. Port configure-mcp.js logic and options.
  2. Implement advanced validation and integration.
  3. Unit tests for all options and validation.
  4. Integration tests for configure-mcp flows.

---

### **Iteration 14: Add Command Parity**
- **Goal:** Support all component types, options, and validation in add command.
- **Tasks:**
  1. Port add.js logic and options.
  2. Implement advanced validation and error handling.
  3. Unit tests for all add command options.
  4. Integration tests for add command scenarios.

---

### **Iteration 15: AIGI Command Parity**
- **Goal:** Implement real AI integration and workflow for aigi command.
- **Tasks:**
  1. Port aigi.js logic and AI provider integration.
  2. Implement code generation and workflow.
  3. Unit tests for AI integration and output.
  4. Integration tests for aigi command scenarios.

---

### **Iteration 16: SymlinkManager & File Operations**
- **Goal:** Implement full symlink manager and advanced file operations.
- **Tasks:**
  1. Port symlink.js and enhanced file-manager logic.
  2. Expose symlink features in CLI and core.
  3. Unit tests for symlink and file operations.
  4. Integration tests for symlink scenarios.

---

### **Iteration 17: Registry Client Parity**
- **Goal:** Implement real registry interaction, authentication, and error handling.
- **Tasks:**
  1. Port registry-client.js and models.js logic.
  2. Implement authentication and error handling.
  3. Add mock registry for testing.
  4. Unit tests for registry client.
  5. Integration tests for registry scenarios.

---

### **Iteration 18: Template System Parity**
- **Goal:** Port all templates, advanced variable substitution, and validation.
- **Tasks:**
  1. Port all templates and template files from Node.js.
  2. Implement advanced variable substitution and validation.
  3. Add template dependency resolution.
  4. Unit tests for template logic.
  5. Integration tests for template application.

---

### **Iteration 19: Utils & Error Handling Parity**
- **Goal:** Port advanced logger, error handler, and FS/Path utils.
- **Tasks:**
  1. Port logger, error handler, and FS/Path utils from Node.js.
  2. Implement advanced logging, error formatting, and file/path operations.
  3. Unit tests for all utils.
  4. Integration tests for error and edge cases.

---

### **Iteration 20: Test Coverage & Edge Cases**
- **Goal:** Achieve full test coverage and edge case handling.
- **Tasks:**
  1. Port all missing unit and integration tests from Node.js.
  2. Add tests for edge cases, error scenarios, and workflows.
  3. Ensure all tests pass and coverage targets are met.

---

### **Iteration 21: Documentation Parity**
- **Goal:** Port all in-code and markdown documentation.
- **Tasks:**
  1. Port CLI-README, SECURITY, and workflow docs.
  2. Ensure all modules and commands are documented.
  3. Add developer and user guides as in Node.js.

---

**Each iteration consists of:**
- Coding the missing functionality
- Writing unit tests
- Writing integration tests
- Ensuring all tests pass before moving to the next iteration

This completion plan ensures that the create-sparc-py project will fully implement the SPARC framework methodology while maintaining high code quality and comprehensive testing throughout the development process. 