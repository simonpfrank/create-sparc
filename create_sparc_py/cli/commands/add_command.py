import typer
from ...core.project_generator import ProjectGenerator
from ...core.config_manager import ConfigManager
from ...utils import Logger

logger = Logger()


def add_command(app: typer.Typer):
    @app.command("add")
    def add(
        component: str = typer.Argument(..., help="Component type"),
        name: str = typer.Option(None, "-n", "--name", help="Component name"),
        type_: str = typer.Option("component", "-t", "--type", help="Component type"),
        path: str = typer.Option(None, "-p", "--path", help="Custom path for component"),
    ):
        try:
            # Validate component type
            if not component:
                logger.error("Component type is required")
                typer.echo("See --help for usage information.")
                raise typer.Exit(1)

            # Find project configuration
            config_manager = ConfigManager()
            project_config = config_manager.find_project_config()
            if not project_config:
                logger.error("Not in a SPARC project directory")
                logger.info(
                    "Run this command from within a SPARC project or use the init command to create a new project."
                )
                raise typer.Exit(1)

            logger.info(f"Adding {component} to project")

            # Create component configuration
            component_config = {
                "name": name or component,
                "type": type_,
                "path": path,
                "project_config": project_config,
            }

            # Add component to project
            project_generator = ProjectGenerator()
            project_generator.add_component(component_config)

            logger.success(f"Component {component_config['name']} added successfully!")
        except Exception as error:
            logger.error(f"Failed to add component: {str(error)}")
            import os

            if os.getenv("DEBUG"):
                import traceback

                traceback.print_exc()
            raise typer.Exit(1)


def run(args):
    try:
        component = getattr(args, "component", None)
        name = getattr(args, "name", None)
        type_ = getattr(args, "type", "component")
        path = getattr(args, "directory", None)

        if not component:
            logger.error("Component type is required")
            print("See --help for usage information.")
            return 1

        config_manager = ConfigManager()
        project_config = config_manager.find_project_config()
        if not project_config:
            logger.error("Not in a SPARC project directory")
            logger.info(
                "Run this command from within a SPARC project or use the init command to create a new project."
            )
            return 1

        logger.info(f"Adding {component} to project")

        component_config = {
            "name": name or component,
            "type": type_,
            "path": path,
            "project_config": project_config,
        }

        project_generator = ProjectGenerator()
        project_generator.add_component(component_config)

        logger.success(f"Component {component_config['name']} added successfully!")
        return 0
    except Exception as error:
        logger.error(f"Failed to add component: {str(error)}")
        import os

        if os.getenv("DEBUG"):
            import traceback

            traceback.print_exc()
        return 1
