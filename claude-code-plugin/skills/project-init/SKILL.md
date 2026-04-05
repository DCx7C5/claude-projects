---
name: project-init
description: Modern project initialization using ProjectHelper. Creates projects with Rust-focused templates, smart configuration, and professional structure. Automatically installs and uses the standalone ProjectHelper tool.
---

# Project Initialization Skill

This skill provides modern project initialization using the ProjectHelper tool. It creates professional project structures with comprehensive templates, focusing on Rust development while supporting multiple programming languages.

## What This Skill Provides

### Automated Project Setup
- **Modern Templates**: Rust binary applications, libraries, and general-purpose projects
- **Smart Configuration**: User preferences, Git integration, and project metadata
- **Professional CLI**: Beautiful terminal interface with progress indicators
- **Documentation**: Comprehensive README files, API docs, and development guides

### Template Types Available

#### Rust Templates
- **rust-binary**: CLI applications with clap argument parsing
- **rust-library**: Library crates with documentation and benchmarks
- **basic**: Language-agnostic project structure

#### Features for All Templates
- Proper directory structure (src/, docs/, tests/)
- Git repository initialization with initial commit
- Comprehensive README with usage instructions
- Smart .gitignore patterns
- Project metadata and configuration

## Usage

This skill automatically installs and uses the standalone ProjectHelper tool, providing a seamless experience:

```python
# The skill will automatically call:
# projecthelper init <project_name> --template <template> [options]
```

## Input Parameters

When using this skill, provide:
- **Project Name**: The name of your project
- **Template**: Template type (rust-binary, rust-library, basic)
- **Description**: Brief project description (optional)
- **Author Info**: Name and email for project attribution (optional)
- **Location**: Where to create the project (optional, defaults to current directory)

## Output Structure

Generated projects follow modern best practices:

```
my-rust-project/
├── Cargo.toml               # Rust project configuration
├── README.md                # Comprehensive documentation
├── .gitignore              # Smart ignore patterns
├── .projecthelper.json     # Project metadata
├── src/
│   ├── main.rs             # Application entry point (for binaries)
│   ├── lib.rs              # Library code (for libraries)
│   ├── cli.rs              # CLI utilities
│   └── commands/           # Command implementations
└── tests/                  # Test directory
```

## Integration with Claude Code

This skill integrates seamlessly with Claude Code workflows:

1. **Automatic Tool Installation**: Installs ProjectHelper if not available
2. **Command Execution**: Runs the appropriate projecthelper command
3. **Result Processing**: Returns structured information about created projects
4. **Error Handling**: Provides helpful error messages and suggestions

## Advanced Features

### Configuration Management
- User preferences stored in `~/.config/projecthelper/config.yml`
- Customizable author information, default templates, and Git settings
- Template search paths for custom templates

### Template Customization
- Jinja2-based templating with variable substitution
- Pre/post generation hooks for additional setup
- Plugin architecture for extending functionality

### Git Integration
- Automatic repository initialization
- Smart initial commit with project metadata
- Configurable default branch (main/master)

## Examples

### Create a Rust CLI Application
```
Input: Project name "weather-cli", template "rust-binary"
Output: Full Rust CLI project with clap integration, proper Cargo.toml, and example commands
```

### Create a Rust Library
```
Input: Project name "math-utils", template "rust-library"  
Output: Library crate with documentation, benchmarks, and proper module structure
```

### Create a General Project
```
Input: Project name "my-project", template "basic"
Output: Language-agnostic project with documentation and development structure
```

## Dependencies

This skill requires:
- Python 3.8+ (for running ProjectHelper)
- Git (for repository initialization)
- Rust toolchain (for Rust-specific templates)

The skill automatically handles ProjectHelper installation and dependency management.

## Troubleshooting

### Common Issues

**ProjectHelper Installation Failed**
- Ensure Python 3.8+ is available
- Check network connectivity for pip installation
- Verify write permissions to Python site-packages

**Template Generation Failed**
- Verify template name is correct (use 'list' command to see available templates)
- Check target directory permissions
- Ensure Git is configured if using Git integration

**Rust-Specific Issues**
- Install Rust toolchain from https://rustup.rs/
- Verify cargo is in PATH
- Check Rust edition compatibility (defaults to 2021)

## Related Skills

- `update-config` - Configure Claude Code settings
- `simplify` - Code optimization and cleanup
- Development workflow skills for specific languages

This skill transforms project initialization from a manual, error-prone process into a professional, automated workflow that follows modern development best practices.