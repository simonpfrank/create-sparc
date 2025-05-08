# Create SPARC Py

A Python port of the [create-sparc](https://github.com/ruvnet/rUv-dev) Node.js tool, designed to scaffold Python projects following the SPARC methodology.

## What is SPARC?

SPARC is a software development methodology created by Reuven Cohen that focuses on a structured approach to building applications:

- **S**pecification: Define the requirements and specifications clearly
- **P**seudocode: Create a logical outline of the implementation
- **A**rchitecture: Design the high-level architecture of the system
- **R**efinement: Refine the implementation through iterations
- **C**ompletion: Complete the implementation and add final touches

## Features

- Create new Python projects with a structured SPARC methodology
- Choose from different templates for various project types
- Generate comprehensive documentation templates (PRD, TDD, tracker)
- Establish best practices for Python project structure

## Installation

```bash
# Install using pip
# not yet published - pip install create-sparc-py 

# Or install from source
git clone https://github.com/yourusername/create-sparc-py.git
cd create-sparc-py
pip install -e .
```

## Usage

```bash
# Create a new project using the default template
create-sparc-py init my-project

# Create a new project using a specific template
create-sparc-py init my-project --template sparc

# Create a new project in a specific directory
create-sparc-py init my-project --directory /path/to/directory
```

## Available Templates

- `default`: A minimal Python project template
- `sparc`: A comprehensive Python project template following the SPARC methodology

## Project Structure

The generated project (using the `sparc` template) follows this structure:

```
/
├── docs/               # Documentation
│   ├── PRD.md          # Product Requirements Document
│   ├── TDD.md          # Technical Design Document
│   └── tracker.md      # Progress tracking
├── src/                # Source code
│   └── project_name/   # Main package
├── tests/              # Tests
├── main.py             # Entry point
├── setup.py            # Package setup
└── requirements.txt    # Dependencies
```

## Development Status

- [x] Core utilities implementation
  - [x] Logger
  - [x] Error Handler
  - [x] FS Utils
  - [x] Path Utils
- [x] Template management
  - [x] Template loading
  - [x] Template validation
  - [x] Template application
- [x] Configuration management
  - [x] Config loading/saving
  - [x] Default configuration
- [x] Project generation
  - [x] Project scaffolding
  - [x] Template-based generation
- [x] CLI interface
  - [x] Command structure
  - [x] Init command
- [ ] Additional templates
  - [x] Default template
  - [x] SPARC template
  - [ ] AIGI template
  - [ ] Roo template

## Attribution

This project is a Python port of the original create-sparc Node.js tool created by Reuven Cohen ([@ruvnet](https://github.com/ruvnet)). The original project can be found at: https://github.com/ruvnet/rUv-dev.

## Contributing

Contributions to `create-sparc-py` are welcome! Whether you're fixing bugs, improving documentation, or proposing new features, your help is appreciated.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT 