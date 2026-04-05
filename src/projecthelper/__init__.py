"""ProjectHelper: A modern project initialization tool.

A powerful, extensible project generator with rich templates and CLI interface.
Supports multiple programming languages with a focus on Rust ecosystem.
"""

__version__ = "1.0.0"
__author__ = "Claude Assistant"
__email__ = "claude@anthropic.com"

from .core.generator import ProjectGenerator
from .core.templates import TemplateManager
from .core.config import Config

__all__ = ["ProjectGenerator", "TemplateManager", "Config"]