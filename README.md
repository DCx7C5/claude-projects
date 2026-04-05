# ProjectHelper

🚀 **A modern, extensible project initialization tool with rich templates and professional CLI interface**

ProjectHelper streamlines project creation with intelligent templates, focusing on the Rust ecosystem while supporting multiple programming languages through an extensible plugin architecture.

[![PyPI version](https://badge.fury.io/py/projecthelper.svg)](https://badge.fury.io/py/projecthelper)
[![Python Support](https://img.shields.io/pypi/pyversions/projecthelper.svg)](https://pypi.org/project/projecthelper/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

🦀 **Rust-Focused**: Comprehensive templates for Rust projects (CLI tools, libraries, web services)  
🎯 **Professional CLI**: Beautiful, type-safe interface built with Typer and Rich  
🔌 **Plugin Architecture**: Extensible system for adding custom templates and languages  
⚙️ **Smart Configuration**: User preferences, template customization, and project metadata  
🔄 **Git Integration**: Automatic repository initialization and structured commits  
📚 **Rich Documentation**: Generated documentation with examples and best practices  

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI
pip install projecthelper

# Or install development version
pip install git+https://github.com/claude-assistant/projecthelper.git
```

### Create Your First Project

```bash
# Rust CLI application
projecthelper init my-rust-cli --template rust-binary

# Rust library
projecthelper init my-rust-lib --template rust-library

# General project
projecthelper init my-project --template basic

# Interactive mode
projecthelper init my-project --interactive
```

## 📋 Available Templates

| Template | Description | Language | Use Case |
|----------|-------------|----------|----------|
| `rust-binary` | CLI application with clap | Rust | Command-line tools |
| `rust-library` | Library crate with docs | Rust | Reusable libraries |
| `basic` | General project structure | Any | Universal starting point |

## 🛠️ Usage

### Command Reference

```bash
# Initialize new project
projecthelper init <name> [OPTIONS]

# List available templates
projecthelper list

# Manage configuration
projecthelper config [--show|--set key=value|--reset]

# Manage plugins
projecthelper plugin <list|install|remove> [name]

# Show version
projecthelper version
```

### Interactive Mode

For guided project setup with prompts:

```bash
projecthelper init my-project --interactive
```

### Configuration

ProjectHelper stores user preferences in `~/.config/projecthelper/config.yml`:

```yaml
author:
  name: "Your Name"
  email: "your@email.com"
templates:
  default: "rust-binary"
git:
  auto_init: true
  default_branch: "main"
```

## 📁 Project Structure

Generated projects follow best practices:

```
my-rust-cli/
├── Cargo.toml              # Rust project configuration
├── README.md               # Comprehensive documentation
├── .gitignore             # Smart ignore patterns
├── .projecthelper.json    # Project metadata
├── src/
│   ├── main.rs            # Application entry point
│   ├── cli.rs             # CLI utilities
│   └── commands/          # Command implementations
└── tests/                 # Test directory
```

## 🔧 Development

### Prerequisites

- Python 3.8+
- Git (for repository features)
- Rust (for Rust templates)

### Building from Source

```bash
git clone https://github.com/claude-assistant/projecthelper
cd projecthelper

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Format code
black .
isort .

# Type checking
mypy src/
```

## 🤖 Claude Code Integration

ProjectHelper can be used as a Claude Code plugin for seamless integration:

```bash
# Install the standalone tool
pip install projecthelper

# Use via Claude Code skill
/project-init my-project --template rust-binary
```

For complete documentation and examples, visit our [GitHub repository](https://github.com/claude-assistant/projecthelper).

---

**Made with 🦀 and ❤️ for the developer community**