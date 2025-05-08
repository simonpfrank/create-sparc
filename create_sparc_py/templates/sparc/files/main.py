#!/usr/bin/env python
"""
{{project_name}}

{{project_description}}

Author: {{author}}
License: {{license}}
"""

# This import will work once the project is set up
# For now, we provide a fallback if the module doesn't exist yet
try:
    from src.{{project_name}} import main as app_main
    
    def main():
        """
        Main entry point for the application.
        """
        print(f"Welcome to {{project_name}}!")
        print("This project follows the SPARC methodology:")
        print("  - Specification")
        print("  - Pseudocode")
        print("  - Architecture")
        print("  - Refinement")
        print("  - Completion")
        
        # Call the actual application code
        app_main()
except ImportError:
    def main():
        """
        Main entry point for the application.
        """
        print(f"Welcome to {{project_name}}!")
        print("This project follows the SPARC methodology:")
        print("  - Specification")
        print("  - Pseudocode")
        print("  - Architecture")
        print("  - Refinement")
        print("  - Completion")
        
        print("\nTo get started:")
        print("1. Edit the docs/PRD.md file to define your project requirements")
        print("2. Edit the docs/TDD.md file to design your technical solution")
        print("3. Implement your solution in the src/{{project_name}} package")


if __name__ == "__main__":
    main() 