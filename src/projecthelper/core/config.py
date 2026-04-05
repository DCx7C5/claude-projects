"""Configuration management for ProjectHelper."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class AuthorConfig(BaseModel):
    """Author configuration."""
    name: str = "Project Author"
    email: str = "author@example.com"


class TemplateConfig(BaseModel):
    """Template configuration."""
    default: str = "basic"
    search_paths: list[str] = Field(default_factory=list)


class GitConfig(BaseModel):
    """Git configuration."""
    auto_init: bool = True
    default_branch: str = "main"


class ProjectHelperConfig(BaseModel):
    """Main ProjectHelper configuration."""
    author: AuthorConfig = Field(default_factory=AuthorConfig)
    templates: TemplateConfig = Field(default_factory=TemplateConfig)
    git: GitConfig = Field(default_factory=GitConfig)


class Config:
    """Configuration manager for ProjectHelper."""

    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.yml"
        self._config = self._load_config()

    def _get_config_dir(self) -> Path:
        """Get the configuration directory."""
        if os.name == "nt":  # Windows
            base_dir = Path(os.environ.get("APPDATA", Path.home()))
            config_dir = base_dir / "ProjectHelper"
        else:  # Unix-like systems
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config_home:
                base_dir = Path(xdg_config_home)
            else:
                base_dir = Path.home() / ".config"
            config_dir = base_dir / "projecthelper"

        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir

    def _load_config(self) -> ProjectHelperConfig:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f) or {}
                return ProjectHelperConfig(**config_data)
            except Exception:
                # If config is corrupted, fall back to defaults
                return ProjectHelperConfig()
        else:
            # Create default config file
            config = ProjectHelperConfig()
            self._save_config(config)
            return config

    def _save_config(self, config: ProjectHelperConfig):
        """Save configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config.model_dump(), f, default_flow_style=False, sort_keys=False)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key.split('.')
        value = self._config.model_dump()

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """Set a configuration value using dot notation."""
        keys = key.split('.')
        config_dict = self._config.model_dump()

        # Navigate to the parent of the target key
        current = config_dict
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        # Set the value
        current[keys[-1]] = value

        # Recreate and save config
        self._config = ProjectHelperConfig(**config_dict)
        self._save_config(self._config)

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as a flat dictionary."""
        config_dict = self._config.model_dump()
        flat_dict = {}

        def flatten(d: dict, prefix: str = ""):
            for key, value in d.items():
                new_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, dict):
                    flatten(value, new_key)
                else:
                    flat_dict[new_key] = value

        flatten(config_dict)
        return flat_dict

    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self._config = ProjectHelperConfig()
        self._save_config(self._config)

    @property
    def config_path(self) -> Path:
        """Get the path to the configuration file."""
        return self.config_file

    @property
    def template_paths(self) -> list[Path]:
        """Get list of template search paths."""
        paths = [
            # Built-in templates
            Path(__file__).parent.parent / "templates",
            # User custom templates
            self.config_dir / "templates",
        ]

        # Add configured search paths
        for path_str in self._config.templates.search_paths:
            path = Path(path_str).expanduser()
            if path.exists():
                paths.append(path)

        return paths