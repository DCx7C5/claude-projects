"""Template management system for ProjectHelper."""

import yaml
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader, Template
import importlib.metadata


@dataclass
class TemplateInfo:
    """Information about a project template."""
    name: str
    description: str
    path: Path
    language: Optional[str] = None
    project_type: Optional[str] = None
    version: str = "1.0.0"
    author: Optional[str] = None
    variables: Dict[str, Any] = None
    pre_hooks: List[str] = None
    post_hooks: List[str] = None

    def __post_init__(self):
        if self.variables is None:
            self.variables = {}
        if self.pre_hooks is None:
            self.pre_hooks = []
        if self.post_hooks is None:
            self.post_hooks = []


class TemplateManager:
    """Manages project templates and template rendering."""

    def __init__(self):
        self._templates: Dict[str, TemplateInfo] = {}
        self._load_templates()

    def _load_templates(self):
        """Load all available templates from built-in and plugin sources."""
        # Load built-in templates
        builtin_path = Path(__file__).parent.parent / "templates"
        if builtin_path.exists():
            self._load_templates_from_path(builtin_path)

        # Load templates from plugins
        self._load_plugin_templates()

    def _load_templates_from_path(self, base_path: Path):
        """Load templates from a directory path."""
        if not base_path.exists():
            return

        for template_dir in base_path.iterdir():
            if template_dir.is_dir():
                template_info = self._load_template_info(template_dir)
                if template_info:
                    self._templates[template_info.name] = template_info

    def _load_template_info(self, template_path: Path) -> Optional[TemplateInfo]:
        """Load template information from a template directory."""
        config_file = template_path / "template.yml"
        if not config_file.exists():
            # Try fallback to JSON
            config_file = template_path / "template.json"
            if not config_file.exists():
                # Create basic template info from directory name
                return TemplateInfo(
                    name=template_path.name,
                    description=f"Template for {template_path.name} projects",
                    path=template_path
                )

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix == '.yml':
                    config_data = yaml.safe_load(f) or {}
                else:
                    config_data = json.load(f)

            return TemplateInfo(
                name=config_data.get('name', template_path.name),
                description=config_data.get('description', f'Template for {template_path.name} projects'),
                path=template_path,
                language=config_data.get('language'),
                project_type=config_data.get('project_type'),
                version=config_data.get('version', '1.0.0'),
                author=config_data.get('author'),
                variables=config_data.get('variables', {}),
                pre_hooks=config_data.get('pre_hooks', []),
                post_hooks=config_data.get('post_hooks', [])
            )
        except Exception as e:
            print(f"Warning: Failed to load template config from {config_file}: {e}")
            return None

    def _load_plugin_templates(self):
        """Load templates from installed plugins."""
        try:
            for entry_point in importlib.metadata.entry_points(group='projecthelper.plugins'):
                try:
                    plugin_class = entry_point.load()
                    plugin_instance = plugin_class()

                    # Get templates from plugin
                    if hasattr(plugin_instance, 'get_templates'):
                        plugin_templates = plugin_instance.get_templates()
                        for template in plugin_templates:
                            self._templates[template.name] = template
                except Exception as e:
                    print(f"Warning: Failed to load plugin {entry_point.name}: {e}")
        except Exception:
            # Entry points not available or no plugins installed
            pass

    def get_available_templates(self) -> List[TemplateInfo]:
        """Get list of all available templates."""
        return list(self._templates.values())

    def get_template(self, name: str) -> Optional[TemplateInfo]:
        """Get a specific template by name."""
        return self._templates.get(name)

    def get_plugins(self) -> Dict[str, Dict[str, Any]]:
        """Get information about loaded plugins."""
        plugins = {}
        try:
            for entry_point in importlib.metadata.entry_points(group='projecthelper.plugins'):
                try:
                    plugin_class = entry_point.load()
                    plugin_instance = plugin_class()

                    plugins[entry_point.name] = {
                        'name': entry_point.name,
                        'description': getattr(plugin_instance, 'description', 'No description'),
                        'version': getattr(plugin_instance, 'version', 'unknown'),
                        'templates': [t.name for t in getattr(plugin_instance, 'get_templates', lambda: [])()]
                    }
                except Exception as e:
                    plugins[entry_point.name] = {
                        'name': entry_point.name,
                        'description': f'Failed to load: {e}',
                        'version': 'error',
                        'templates': []
                    }
        except Exception:
            pass

        return plugins

    def render_template_file(self, template_path: Path, output_path: Path, context: Dict[str, Any]):
        """Render a single template file."""
        # Set up Jinja2 environment
        template_dir = template_path.parent
        env = Environment(
            loader=FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )

        # Load and render template
        template_name = template_path.name
        template = env.get_template(template_name)
        rendered_content = template.render(**context)

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write rendered content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

    def render_template_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render a template string with the given context."""
        template = Template(template_string)
        return template.render(**context)

    def get_template_variables(self, template_name: str) -> Dict[str, Any]:
        """Get the variables defined for a template."""
        template = self.get_template(template_name)
        if template:
            return template.variables.copy()
        return {}

    def validate_template(self, template_name: str) -> bool:
        """Validate that a template exists and is properly configured."""
        template = self.get_template(template_name)
        if not template:
            return False

        # Check that template directory exists
        if not template.path.exists():
            return False

        # Check for required template files
        has_template_files = any(
            f.suffix in ['.j2', '.jinja', '.template'] or f.name.endswith('.template')
            for f in template.path.rglob('*')
            if f.is_file()
        )

        return has_template_files

    def refresh_templates(self):
        """Refresh the template cache by reloading all templates."""
        self._templates.clear()
        self._load_templates()