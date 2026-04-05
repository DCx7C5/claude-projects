# Claude Code Plugin for ProjectHelper

This directory contains the Claude Code plugin integration for ProjectHelper, providing seamless access to modern project initialization within the Claude Code ecosystem.

## Components

### Skills
- **project-init**: Core project initialization skill that leverages the standalone ProjectHelper tool
- Provides template-based project generation with Rust focus
- Supports rust-binary, rust-library, and basic templates
- Automatic tool installation and dependency management

### Agents
- **project-helper**: Conversational project management agent
- Expert guidance on project structure and best practices
- Integrated with ProjectHelper tool for automated project creation
- Specializes in Rust development and modern software engineering

## Installation

### Automatic Installation (Recommended)
The plugin automatically handles ProjectHelper installation:

1. Install the Claude Code plugin (copy this directory to your plugins folder)
2. Enable in Claude Code settings
3. Use `/project-init` or chat with the project-helper agent
4. ProjectHelper will be automatically installed on first use

### Manual Installation
If you prefer to install ProjectHelper separately:

```bash
pip install projecthelper
```

## Usage

### Using the Skill
Direct project initialization:
```
/project-init my-rust-cli --template rust-binary
```

### Using the Agent
Conversational project guidance:
```
User: I want to create a command-line tool for file processing
Agent: [Provides guidance and creates project using ProjectHelper]
```

## Features

### Template Types
- **rust-binary**: CLI applications with clap argument parsing
- **rust-library**: Library crates with documentation and benchmarks  
- **basic**: Language-agnostic project structure

### Automatic Features
- Git repository initialization
- Smart .gitignore patterns
- Comprehensive documentation
- Professional project structure
- Modern Rust conventions

### Integration Benefits
- **Seamless Workflow**: No need to switch between tools
- **Conversational Interface**: Get guidance while creating projects
- **Automatic Updates**: Tool stays current with modern practices
- **Error Handling**: Helpful error messages and troubleshooting

## Configuration

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

Configure via Claude Code or directly:
```bash
projecthelper config --set author.name="Your Name"
```

## Examples

### Create Rust CLI Tool
```
Input: /project-init weather-cli --template rust-binary --description "Weather forecasting CLI"
Output: Complete Rust CLI project with clap integration and professional structure
```

### Conversational Project Setup
```
User: Help me set up a new Rust project for data analysis
Agent: I'll create a library crate with analysis-focused dependencies...
[Creates project with appropriate template and configuration]
```

### Advanced Configuration
```
User: Set up my preferences for author information
Agent: [Guides through configuration setup for consistent project metadata]
```

## Benefits Over Standalone Use

### Enhanced User Experience
- **Conversational Guidance**: Get expert advice while creating projects
- **Context Awareness**: Agent understands your development goals
- **Integrated Workflow**: No context switching between tools
- **Automatic Setup**: Handles installation and configuration

### Professional Development
- **Best Practices**: Built-in knowledge of modern conventions
- **Template Intelligence**: Smart template recommendations
- **Error Prevention**: Catches common mistakes before they happen
- **Continuous Learning**: Stays updated with ecosystem changes

## Troubleshooting

### Common Issues

**Plugin Not Loading**
- Verify plugin directory structure
- Check Claude Code plugin settings
- Restart Claude Code after installation

**ProjectHelper Installation Failed**
- Ensure Python 3.8+ is available
- Check network connectivity
- Verify pip installation permissions

**Template Generation Issues**
- Verify template name spelling
- Check target directory permissions
- Ensure Git is configured for repository features

### Getting Help

- Use the conversational agent for guided troubleshooting
- Check ProjectHelper documentation: `projecthelper --help`
- Review generated project structure and next steps

## Development

This plugin wrapper follows Claude Code plugin standards while leveraging the full power of the standalone ProjectHelper tool. The architecture ensures both flexibility for standalone users and seamless integration for Claude Code users.

The dual approach provides:
- **Broad Adoption**: Anyone can use ProjectHelper independently
- **Enhanced Experience**: Claude Code users get conversational guidance
- **Maintainability**: Single codebase with multiple interfaces
- **Extensibility**: Easy to add new templates and features

---

*This plugin brings the power of modern project initialization directly into your Claude Code workflow, combining the flexibility of a standalone tool with the intelligence of conversational AI guidance.*