---
name: project-init
description: Initialize new projects with proper structure and configuration. Creates basic project template with README, .gitignore, Git setup, and essential project files for rapid development startup.
---

# Project Initialization Skill

Streamline project creation with automated setup, proper structure, and essential configuration files. This skill provides a foundation for new projects with best practices built-in.

## What This Skill Provides

### Automated Project Setup
- **Directory Structure**: Create organized folder hierarchy with standard directories
- **Essential Files**: Generate README.md, .gitignore, and configuration files
- **Git Integration**: Initialize repository and create initial commit
- **Template System**: Use predefined templates for common project types

### Project Components
- **Documentation**: README template with project structure and usage instructions
- **Version Control**: Git repository with appropriate .gitignore patterns
- **Source Organization**: src/ directory for source code organization
- **Documentation Structure**: docs/ directory for project documentation
- **Configuration**: Basic project configuration files

## Usage

This skill can be invoked through:
- Direct skill invocation: `/project-init`
- Agent integration: The project-helper agent can use this skill automatically
- Interactive prompts: Guided setup with customization options

## Input Parameters

**Project Name**: The name of your project (used for directories and files)
**Project Description**: Brief description for README and documentation
**Project Type**: Type of project to determine appropriate .gitignore and structure
**Author**: Your name or organization for project attribution
**Location**: Directory where the project should be created

## Output Structure

```
project-name/
├── README.md                 # Project description and setup instructions
├── .gitignore               # Appropriate ignore patterns
├── src/                     # Source code directory
├── docs/                    # Documentation directory
├── tests/                   # Testing directory (optional)
├── .project-config.json     # Project metadata
└── LICENSE                  # License file (optional)
```

## Features

### Smart .gitignore Generation
Generates appropriate .gitignore patterns based on:
- Project type detection
- Common development artifacts
- OS-specific files
- IDE and editor files

### README Template
Creates comprehensive README with:
- Project description and purpose
- Installation and setup instructions
- Usage examples and documentation links
- Contributing guidelines
- License information

### Git Integration
- Initializes Git repository
- Creates initial commit with project structure
- Sets up basic Git configuration
- Optional remote repository setup

### Project Metadata
Stores project information in .project-config.json:
- Creation date and author
- Project type and configuration
- Tool versions and dependencies
- Build and deployment settings

## Customization

The skill supports customization through:
- **Interactive Prompts**: Guided setup with user choices
- **Template Selection**: Choose from predefined project templates
- **Configuration Options**: Customize generated files and structure
- **Extension Points**: Add custom files and directories

## Best Practices

This skill implements development best practices:
- **Clean Structure**: Organized directories for maintainability
- **Documentation First**: Comprehensive README from project start
- **Version Control**: Proper Git setup and commit hygiene
- **Configuration Management**: Centralized project settings
- **Extensibility**: Structure that grows with project needs

## Integration

Works seamlessly with:
- **project-helper agent**: For conversational project guidance
- **Development tools**: Compatible with popular IDEs and editors
- **CI/CD systems**: Structure supports automated builds and deployments
- **Package managers**: Ready for dependency management setup

This skill eliminates the tedium of project setup while ensuring consistency and best practices across all your projects.