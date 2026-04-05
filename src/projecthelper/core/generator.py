"""Core project generation logic for ProjectHelper."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from .templates import TemplateManager, TemplateInfo
from .config import Config


class ProjectGenerationError(Exception):
    """Exception raised when project generation fails."""
    pass


class ProjectGenerator:
    """Handles the generation of new projects from templates."""

    def __init__(self, template_manager: TemplateManager, config: Optional[Config] = None):
        self.template_manager = template_manager
        self.config = config or Config()

    def generate_project(
        self,
        name: str,
        template: str,
        path: Path,
        description: Optional[str] = None,
        author_name: Optional[str] = None,
        author_email: Optional[str] = None,
        init_git: bool = True,
        **extra_vars
    ) -> bool:
        """
        Generate a new project from a template.

        Args:
            name: Project name
            template: Template name to use
            path: Target path for the project
            description: Project description
            author_name: Author name
            author_email: Author email
            init_git: Whether to initialize Git repository
            **extra_vars: Additional template variables

        Returns:
            True if successful, False otherwise

        Raises:
            ProjectGenerationError: If generation fails
        """
        # Validate inputs
        if not self._validate_project_name(name):
            raise ProjectGenerationError(f"Invalid project name: {name}")

        if path.exists():
            raise ProjectGenerationError(f"Target directory already exists: {path}")

        # Get template info
        template_info = self.template_manager.get_template(template)
        if not template_info:
            raise ProjectGenerationError(f"Template not found: {template}")

        if not self.template_manager.validate_template(template):
            raise ProjectGenerationError(f"Invalid template: {template}")

        try:
            # Create project directory
            path.mkdir(parents=True, exist_ok=True)

            # Prepare template context
            context = self._prepare_template_context(
                name=name,
                description=description or f"A new {template} project",
                author_name=author_name or self.config.get("author.name", "Project Author"),
                author_email=author_email or self.config.get("author.email", "author@example.com"),
                template_info=template_info,
                **extra_vars
            )

            # Run pre-hooks
            self._run_hooks(template_info.pre_hooks, path, context, "pre")

            # Generate project structure
            self._generate_project_structure(template_info, path, context)

            # Initialize Git repository if requested
            if init_git and self.config.get("git.auto_init", True):
                self._init_git_repository(path, context)

            # Run post-hooks
            self._run_hooks(template_info.post_hooks, path, context, "post")

            # Save project metadata
            self._save_project_metadata(path, context, template_info)

            return True

        except Exception as e:
            # Clean up on failure
            if path.exists():
                try:
                    shutil.rmtree(path)
                except Exception:
                    pass
            raise ProjectGenerationError(f"Failed to generate project: {e}") from e

    def _validate_project_name(self, name: str) -> bool:
        """Validate project name."""
        if not name or not name.strip():
            return False

        # Check for invalid characters
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in name:
                return False

        return True

    def _prepare_template_context(
        self,
        name: str,
        description: str,
        author_name: str,
        author_email: str,
        template_info: TemplateInfo,
        **extra_vars
    ) -> Dict[str, Any]:
        """Prepare the template rendering context."""
        context = {
            # Project information
            "project_name": name,
            "project_description": description,
            "project_type": template_info.project_type or "general",

            # Author information
            "author_name": author_name,
            "author_email": author_email,

            # Metadata
            "creation_date": datetime.now().isoformat(),
            "generator": "projecthelper",
            "generator_version": "1.0.0",
            "template_name": template_info.name,
            "template_version": template_info.version,

            # Common template variables
            "PROJECT_NAME": name,
            "PROJECT_DESCRIPTION": description,
            "AUTHOR_NAME": author_name,
            "AUTHOR_EMAIL": author_email,
            "CREATION_DATE": datetime.now().isoformat(),
            "PROJECT_TYPE": template_info.project_type or "general",
        }

        # Add template-specific variables
        context.update(template_info.variables)

        # Add extra variables
        context.update(extra_vars)

        return context

    def _generate_project_structure(
        self,
        template_info: TemplateInfo,
        target_path: Path,
        context: Dict[str, Any]
    ):
        """Generate the project structure from the template."""
        template_path = template_info.path

        for root, dirs, files in os.walk(template_path):
            # Skip template configuration files
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

            rel_root = Path(root).relative_to(template_path)
            target_dir = target_path / rel_root

            # Create directories
            if rel_root != Path('.'):
                target_dir.mkdir(parents=True, exist_ok=True)

            # Process files
            for file in files:
                # Skip configuration and hidden files
                if file.startswith('.') or file.endswith(('.yml', '.yaml', '.json')) and file.startswith('template'):
                    continue

                source_file = Path(root) / file
                target_file = target_dir / self._process_filename(file, context)

                self._process_template_file(source_file, target_file, context)

    def _process_filename(self, filename: str, context: Dict[str, Any]) -> str:
        """Process template variables in filenames."""
        # Handle template extensions
        if filename.endswith('.template'):
            filename = filename[:-9]
        elif filename.endswith('.j2'):
            filename = filename[:-3]
        elif filename.endswith('.jinja'):
            filename = filename[:-6]

        # Handle special cases for dotfiles
        if filename == 'gitignore':
            filename = '.gitignore'
        elif filename.startswith('dot_'):
            filename = '.' + filename[4:]

        # Render template variables in filename
        return self.template_manager.render_template_string(filename, context)

    def _process_template_file(self, source_path: Path, target_path: Path, context: Dict[str, Any]):
        """Process a single template file."""
        # Check if this is a template file that needs rendering
        is_template = (
            source_path.suffix in ['.template', '.j2', '.jinja'] or
            source_path.name.endswith('.template')
        )

        if is_template:
            # Render template file
            self.template_manager.render_template_file(source_path, target_path, context)
        else:
            # Copy file as-is
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)

    def _run_hooks(self, hooks: List[str], project_path: Path, context: Dict[str, Any], hook_type: str):
        """Run pre or post generation hooks."""
        if not hooks:
            return

        for hook in hooks:
            try:
                # Render hook command with context
                command = self.template_manager.render_template_string(hook, context)

                # Execute hook
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:
                    print(f"Warning: {hook_type}-hook failed: {result.stderr}")

            except Exception as e:
                print(f"Warning: Failed to run {hook_type}-hook '{hook}': {e}")

    def _init_git_repository(self, project_path: Path, context: Dict[str, Any]):
        """Initialize Git repository in the project."""
        try:
            # Initialize git repository
            subprocess.run(['git', 'init'], cwd=project_path, check=True, capture_output=True)

            # Set default branch if configured
            default_branch = self.config.get("git.default_branch", "main")
            if default_branch != "master":
                subprocess.run(
                    ['git', 'branch', '-m', default_branch],
                    cwd=project_path,
                    check=True,
                    capture_output=True
                )

            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=project_path, check=True, capture_output=True)

            # Create initial commit
            commit_message = f"Initial commit - {context['project_name']} created with ProjectHelper"
            subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=project_path,
                check=True,
                capture_output=True
            )

        except subprocess.CalledProcessError as e:
            print(f"Warning: Git initialization failed: {e}")
        except FileNotFoundError:
            print("Warning: Git not found, skipping repository initialization")

    def _save_project_metadata(self, project_path: Path, context: Dict[str, Any], template_info: TemplateInfo):
        """Save project metadata to a file."""
        metadata = {
            "name": context["project_name"],
            "description": context["project_description"],
            "template": {
                "name": template_info.name,
                "version": template_info.version,
            },
            "author": {
                "name": context["author_name"],
                "email": context["author_email"],
            },
            "created_at": context["creation_date"],
            "generator": {
                "name": context["generator"],
                "version": context["generator_version"],
            }
        }

        metadata_file = project_path / ".projecthelper.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, sort_keys=True)