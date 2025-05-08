"""
create-sparc-py: Python port of create-sparc for scaffolding Python projects with SPARC methodology.

This package provides tools to scaffold new Python projects following the SPARC
methodology structure. It includes templates for standard SPARC projects,
AI-guided implementation (AIGI), and minimal Roo mode frameworks.

This project is a Python port of the original create-sparc Node.js tool created by
Reuven Cohen (https://github.com/ruvnet). The original project can be found at:
https://github.com/ruvnet/rUv-dev.
"""

__version__ = "0.1.0"

# Re-export main functions for easier imports
from create_sparc_py.cli import run
from create_sparc_py.core.project_generator import project_generator, ProjectGenerator

# These will be uncommented once these modules are implemented
# from create_sparc_py.core.project_generator import create_project, add_component
