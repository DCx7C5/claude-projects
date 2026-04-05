"""Modern CLI interface for ProjectHelper using Typer framework."""

import typer
from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm

from .core.generator import ProjectGenerator
from .core.templates import TemplateManager
from .core.config import Config

# Initialize CLI app and console
app = typer.Typer(
    name="projecthelper",
    help="🚀 Modern project initialization tool with rich templates",
    rich_markup_mode="rich",
    no_args_is_help=True,
)
console = Console()

# Initialize core components
template_manager = TemplateManager()
config = Config()


@app.command()
def init(
    name: str = typer.Argument(
        ...,
        help="Project name",
        metavar="NAME"
    ),
    template: str = typer.Option(
        "basic",
        "--template",
        "-t",
        help="Template to use for project generation",
        metavar="TEMPLATE"
    ),
    path: Optional[Path] = typer.Option(
        None,
        "--path",
        "-p",
        help="Target directory (defaults to current directory + project name)",
        metavar="PATH"
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Interactive mode with guided setup"
    ),
    no_git: bool = typer.Option(
        False,
        "--no-git",
        help="Skip Git repository initialization"
    ),
    author_name: Optional[str] = typer.Option(
        None,
        "--author-name",
        help="Author name for project metadata"
    ),
    author_email: Optional[str] = typer.Option(
        None,
        "--author-email",
        help="Author email for project metadata"
    ),
    description: Optional[str] = typer.Option(
        None,
        "--description",
        "-d",
        help="Project description"
    ),
):
    """
    Initialize a new project from a template.

    Creates a new project with the specified name using the chosen template.
    Supports interactive mode for guided setup.
    """
    console.print(f"🚀 [bold green]Creating project:[/bold green] [cyan]{name}[/cyan]")

    # Use interactive mode if requested
    if interactive:
        project_config = interactive_setup(name, template, path)
    else:
        # Determine target path
        target_path = path or Path.cwd() / name

        # Get config values with fallbacks
        project_config = {
            "name": name,
            "description": description or f"A new {template} project",
            "template": template,
            "path": target_path,
            "author_name": author_name or config.get("author.name", "Project Author"),
            "author_email": author_email or config.get("author.email", "author@example.com"),
            "init_git": not no_git,
        }

    try:
        generator = ProjectGenerator(template_manager)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Generate project
            progress.add_task("Generating project structure...", total=None)
            generator.generate_project(**project_config)

        console.print("\n✅ [bold green]Project created successfully![/bold green]")
        console.print(f"📁 [dim]Location:[/dim] {project_config['path']}")
        console.print(f"🎯 [dim]Template:[/dim] {project_config['template']}")

        # Show next steps
        console.print("\n🚀 [bold]Next steps:[/bold]")
        console.print(f"   cd {project_config['path']}")
        if project_config.get('init_git', True):
            console.print("   git status")
        console.print("   # Start developing! 🎉")

    except Exception as e:
        console.print(f"❌ [bold red]Error creating project:[/bold red] {e}")
        raise typer.Exit(1)


@app.command("list")
def list_templates():
    """List available project templates."""
    console.print("📋 [bold]Available Templates[/bold]\n")

    templates = template_manager.get_available_templates()

    if not templates:
        console.print("⚠️ [yellow]No templates found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Name", style="green", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Language", style="blue")
    table.add_column("Type", style="magenta")

    for template in templates:
        table.add_row(
            template.name,
            template.description,
            template.language or "General",
            template.project_type or "General"
        )

    console.print(table)
    console.print(f"\n💡 [dim]Use[/dim] [cyan]projecthelper init myproject --template TEMPLATE_NAME[/cyan] [dim]to create a project[/dim]")


@app.command()
def config_cmd(
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
    set_key: Optional[str] = typer.Option(None, "--set", help="Set a configuration key (format: key=value)"),
    reset: bool = typer.Option(False, "--reset", help="Reset configuration to defaults"),
):
    """Manage ProjectHelper configuration."""
    if reset:
        if Confirm.ask("Are you sure you want to reset configuration to defaults?"):
            config.reset_to_defaults()
            console.print("✅ [green]Configuration reset to defaults[/green]")
        return

    if set_key:
        try:
            key, value = set_key.split("=", 1)
            config.set(key.strip(), value.strip())
            console.print(f"✅ [green]Set {key} = {value}[/green]")
        except ValueError:
            console.print("❌ [red]Invalid format. Use: key=value[/red]")
            raise typer.Exit(1)
        return

    if show or (not set_key and not reset):
        console.print("⚙️ [bold]Current Configuration[/bold]\n")
        config_data = config.get_all()

        if not config_data:
            console.print("📝 [dim]No configuration found. Using defaults.[/dim]")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="green")
        table.add_column("Value", style="white")

        for key, value in config_data.items():
            table.add_row(key, str(value))

        console.print(table)
        console.print(f"\n💡 [dim]Use[/dim] [cyan]projecthelper config --set key=value[/cyan] [dim]to change settings[/dim]")


@app.command()
def plugin(
    action: str = typer.Argument(
        ...,
        help="Plugin action: list, install, remove",
        metavar="ACTION"
    ),
    name: Optional[str] = typer.Argument(
        None,
        help="Plugin name (for install/remove actions)",
        metavar="NAME"
    ),
):
    """Manage plugins for extended functionality."""
    if action == "list":
        console.print("🔌 [bold]Available Plugins[/bold]\n")
        plugins = template_manager.get_plugins()

        if not plugins:
            console.print("📦 [dim]No plugins loaded[/dim]")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="green")
        table.add_column("Version", style="blue")
        table.add_column("Description", style="white")
        table.add_column("Templates", style="magenta")

        for plugin_name, plugin_info in plugins.items():
            template_count = len(plugin_info.get("templates", []))
            table.add_row(
                plugin_name,
                plugin_info.get("version", "unknown"),
                plugin_info.get("description", "No description"),
                str(template_count)
            )

        console.print(table)

    elif action == "install":
        if not name:
            console.print("❌ [red]Plugin name required for install action[/red]")
            raise typer.Exit(1)
        console.print(f"🔧 Installing plugin: {name}")
        console.print("⚠️ [yellow]Plugin installation not yet implemented[/yellow]")

    elif action == "remove":
        if not name:
            console.print("❌ [red]Plugin name required for remove action[/red]")
            raise typer.Exit(1)
        console.print(f"🗑️ Removing plugin: {name}")
        console.print("⚠️ [yellow]Plugin removal not yet implemented[/yellow]")

    else:
        console.print(f"❌ [red]Unknown action: {action}[/red]")
        console.print("💡 Available actions: list, install, remove")
        raise typer.Exit(1)


@app.command()
def version():
    """Show ProjectHelper version information."""
    from . import __version__

    console.print(Panel.fit(
        f"[bold cyan]ProjectHelper[/bold cyan] v{__version__}\n"
        f"Modern project initialization tool\n"
        f"🦀 Rust-focused templates with extensible architecture",
        title="📦 Version Info",
        border_style="cyan"
    ))


def interactive_setup(name: str, default_template: str = "basic", default_path: Optional[Path] = None) -> dict:
    """Interactive project setup with guided prompts."""
    console.print("\n🎯 [bold cyan]Interactive Project Setup[/bold cyan]\n")

    # Project details
    project_name = Prompt.ask(
        "📝 Project name",
        default=name
    )

    description = Prompt.ask(
        "📄 Project description",
        default=f"A new {default_template} project"
    )

    # Template selection
    available_templates = [t.name for t in template_manager.get_available_templates()]
    if available_templates:
        template = Prompt.ask(
            "📋 Template",
            choices=available_templates,
            default=default_template if default_template in available_templates else available_templates[0]
        )
    else:
        template = default_template

    # Project location
    default_target = default_path or Path.cwd() / project_name
    path_input = Prompt.ask(
        "📁 Project location",
        default=str(default_target)
    )
    target_path = Path(path_input)

    # Author information
    author_name = Prompt.ask(
        "👤 Author name",
        default=config.get("author.name", "Project Author")
    )

    author_email = Prompt.ask(
        "📧 Author email",
        default=config.get("author.email", "author@example.com")
    )

    # Git initialization
    init_git = Confirm.ask(
        "🔄 Initialize Git repository?",
        default=True
    )

    return {
        "name": project_name,
        "description": description,
        "template": template,
        "path": target_path,
        "author_name": author_name,
        "author_email": author_email,
        "init_git": init_git,
    }


def main():
    """Entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()