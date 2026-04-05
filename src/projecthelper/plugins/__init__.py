"""Plugin architecture for ProjectHelper."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..core.templates import TemplateInfo


class ProjectHelperPlugin(ABC):
    """Base class for ProjectHelper plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Plugin version."""
        pass

    @abstractmethod
    def get_templates(self) -> List[TemplateInfo]:
        """Return list of templates provided by this plugin."""
        pass

    def pre_generate_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pre-generation hook. Called before project generation.

        Args:
            context: Template context dictionary

        Returns:
            Modified context dictionary
        """
        return context

    def post_generate_hook(self, project_path: str, context: Dict[str, Any]) -> None:
        """
        Post-generation hook. Called after project generation.

        Args:
            project_path: Path to the generated project
            context: Template context dictionary
        """
        pass


class BasicPlugin(ProjectHelperPlugin):
    """Built-in basic template plugin."""

    @property
    def name(self) -> str:
        return "basic"

    @property
    def description(self) -> str:
        return "Basic project templates for general use"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_templates(self) -> List[TemplateInfo]:
        """Return basic templates."""
        from pathlib import Path

        # Get the basic template directory
        template_dir = Path(__file__).parent.parent / "templates" / "basic"

        return [
            TemplateInfo(
                name="basic",
                description="Basic project template with essential files",
                path=template_dir,
                language="general",
                project_type="general",
                version="1.0.0",
                variables={
                    "license": "MIT"
                }
            )
        ]


class RustPlugin(ProjectHelperPlugin):
    """Built-in Rust template plugin."""

    @property
    def name(self) -> str:
        return "rust"

    @property
    def description(self) -> str:
        return "Rust project templates for various project types"

    @property
    def version(self) -> str:
        return "1.0.0"

    def get_templates(self) -> List[TemplateInfo]:
        """Return Rust templates."""
        from pathlib import Path

        base_dir = Path(__file__).parent.parent / "templates"

        return [
            TemplateInfo(
                name="rust-binary",
                description="Rust CLI application template with clap",
                path=base_dir / "rust-binary",
                language="rust",
                project_type="binary",
                version="1.0.0",
                variables={
                    "rust_edition": "2021",
                    "clap_version": "4.0",
                    "license": "MIT OR Apache-2.0"
                }
            ),
            TemplateInfo(
                name="rust-library",
                description="Rust library crate template with documentation",
                path=base_dir / "rust-library",
                language="rust",
                project_type="library",
                version="1.0.0",
                variables={
                    "rust_edition": "2021",
                    "license": "MIT OR Apache-2.0"
                }
            )
        ]