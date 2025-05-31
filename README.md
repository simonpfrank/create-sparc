# Create SPARC Py

A Python port of the [create-sparc](https://github.com/ruvnet/rUv-dev) Node.js tool by Reuven Cohen, designed to scaffold Python projects instead of JS/TypeScript following the SPARC methodology.

## Caveats/Explanation
- I'm no rUv
- I am not a Software Engineer, I code but I'm not a born and bred developer, I was a late starter. The list of what I have to learn is bigger than the things I know.
- This project is an ongoing experiment in using ChoT/Vibe approaches in Cursor and Roo, very much inspired by the instructional posts by Reuven Cohen (rUv) https://www.linkedin.com/in/reuvencohen/, https://github.com/ruvnet. If you don't follow him (he is also on reddit) you should. He is generous with his techniques and code, which I admire as LinkedIn is full of the opposite.
- The experiment was to expose the original in Cursor, generate a PRD and then a design document and let Cursor loose until it finished
- my goals are simple: 
  - to learn everything I can about agentic subjects by building a low effort agentic framework from scratch (on the third iteration, as I filter complexity vs. robustness)
  - Use this framework to achieve the highest possible productivity on a personal budget
  - if it's any good, it's all rUv's design this was originally to see how much Cursor can do without attendance

# Original README

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
git clone https://github.com/simonpfrank/create-sparc-py.git
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
│   ├── prd.md          # Product Requirements Document
│   ├── tdd.md          # Technical Design Document
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

Contributions to `create-sparc-py` are very welcome! As you can see I have stuff to learn, so davice and guidance or issues are welcome.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT 