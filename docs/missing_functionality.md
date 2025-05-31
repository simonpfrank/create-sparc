# Missing or Incomplete Functionality: create_sparc_py vs node_version

This report documents all missing or incomplete functionality in the Python port (`create_sparc_py`) compared to the original Node.js version (`node_version`). It is grouped by module and includes missing files, commands, features, and major differences in user experience or extensibility.

---

## 1. CLI Module

### 1.1 Command Coverage
- **Help System**: The Node.js version has a rich help system with markdown files for each command (e.g., `help/aigi.md`, `help/wizard.md`). The Python version has only a basic help command and lacks context-sensitive, markdown-driven help.
- **Wizard Command**: The Node.js wizard is a full-featured, multi-step interactive workflow with advanced validation, security, and workflow logic. The Python version's wizard is a basic click-based prompt and does not support the full workflow, validation, or security features.
- **Configure-MCP Command**: The Node.js version has a large, feature-rich `configure-mcp.js` (807 lines) with advanced options, validation, and integration. The Python version is a stub with minimal logic.
- **Add Command**: The Node.js version supports more component types, options, and validation. The Python version is basic and lacks advanced options.
- **AIGI Command**: The Node.js version supports real AI integration and workflow. The Python version is a stub with simulated output.
- **Minimal Command**: The Node.js version supports more options and validation. The Python version is basic.
- **SymlinkManager**: The Node.js CLI supports symlink creation and management. The Python CLI does not expose this functionality.

### 1.2 User Experience
- **Interactive Prompts**: Node.js uses inquirer and custom flows; Python uses click, but only for basic prompts.
- **Command Aliases/Shortcuts**: Node.js supports more aliases and flexible command invocation.
- **Error Messages**: Node.js version has more detailed, context-aware error messages.

---

## 2. Core Module

### 2.1 MCP Wizard
- **Workflow**: Node.js has a full workflow engine (`wizard-core.js`, `validation.js`, `security.js`). Python version is a stub and lacks workflow, validation, and security logic.
- **Security**: Node.js has a dedicated security module for MCP wizard. Python version has no equivalent.
- **Config Generation**: Node.js supports advanced config generation and validation. Python version is basic.

### 2.2 Config Manager
- **Schema Validation**: Node.js uses JSON schema for config validation. Python version does not.
- **Advanced Merging**: Node.js supports deep merging and environment-specific configs. Python version is basic.

### 2.3 File Manager
- **Enhanced File Operations**: Node.js version supports advanced file operations, symlinks, and error recovery. Python version is basic.
- **Symlink Support**: Node.js has a full symlink manager. Python version has a stub.

### 2.4 Project Generator
- **Template Dependency Resolution**: Node.js supports template dependencies and advanced variable resolution. Python version is basic.
- **Post-Processing**: Node.js supports post-processing hooks and dependency installation. Python version is stubbed.

### 2.5 Registry Client
- **Remote Registry**: Node.js supports real registry interaction, authentication, and error handling. Python version is a stub.
- **Mock Registry**: Node.js has a mock registry for testing. Python version does not.

---

## 3. Utils Module

- **Logger**: Node.js logger supports more levels, formatting, and output options.
- **ErrorHandler**: Node.js error handler is more advanced and context-aware.
- **FSUtils/PathUtils**: Node.js supports more file and path operations, including cross-platform quirks.

---

## 4. Templates

- **Template Coverage**: Node.js version has more templates and more complete template files (e.g., `minimal-roo` has more rules, code guidelines, and richer README).
- **Template Variables**: Node.js templates use more variables and support more advanced substitution.
- **Template Validation**: Node.js validates templates more thoroughly.

---

## 5. Help System

- **Markdown Help Files**: Node.js version has a full set of markdown help files for each command. Python version does not use or render these.
- **Context-Sensitive Help**: Node.js help system is context-sensitive and can show help for subcommands and options. Python version is basic.

---

## 6. Testing

- **Test Coverage**: Node.js version has more unit and integration tests, covering more edge cases, workflows, and error scenarios.
- **Mocking/Registry Tests**: Node.js has mock registry and workflow tests. Python version does not.
- **Symlink and File System Tests**: Node.js tests symlink and advanced file operations. Python version does not.

---

## 7. Other Architectural Differences

- **Extensibility**: Node.js version is more modular and supports plugin-like extensions (e.g., for registry, templates, workflows).
- **Security**: Node.js version has dedicated security modules and validation for MCP workflows.
- **Documentation**: Node.js version has richer in-code and markdown documentation, including CLI-README, SECURITY, and workflow docs.

---

# Summary Table

| Area                | Node.js Version         | Python Version         |
|---------------------|------------------------|-----------------------|
| CLI Commands        | Full, rich, validated  | Basic, some stubs     |
| Help System         | Markdown, context      | Basic, not markdown   |
| Wizard              | Workflow, security     | Basic, no workflow    |
| Registry            | Real, mock, auth       | Stub only             |
| Symlink             | Full support           | Stub only             |
| Templates           | Rich, validated        | Basic, some missing   |
| Testing             | Extensive, edge cases  | Basic, main flows     |
| Documentation       | Rich, CLI/SECURITY     | Basic, partial        |

---

**This audit is based on directory and file listings, and a review of the main modules and templates. For a full port, the Python version will need to implement the missing features, files, and architectural patterns described above.** 