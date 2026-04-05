#!/usr/bin/env python3
"""
Template utilities for Claude Code Project Helper

Provides functions for processing templates and generating project files.
"""

import os
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
import json


def substitute_template_variables(template_content: str, variables: Dict[str, Any]) -> str:
    """
    Replace template variables with actual values.

    Args:
        template_content: Template content with {{VARIABLE}} placeholders
        variables: Dictionary of variable names and values

    Returns:
        Processed content with variables substituted
    """
    content = template_content

    # Replace all variables in the format {{VARIABLE_NAME}}
    for var_name, var_value in variables.items():
        placeholder = f"{{{{{var_name}}}}}"
        content = content.replace(placeholder, str(var_value))

    return content


def get_default_variables(project_name: str, project_description: str = "",
                         author_name: str = "", author_email: str = "") -> Dict[str, Any]:
    """
    Generate default template variables.

    Args:
        project_name: Name of the project
        project_description: Description of the project
        author_name: Author's name
        author_email: Author's email

    Returns:
        Dictionary of template variables
    """
    return {
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": project_description or f"A new project named {project_name}",
        "AUTHOR_NAME": author_name or "Project Author",
        "AUTHOR_EMAIL": author_email or "author@example.com",
        "CREATION_DATE": datetime.now().isoformat(),
        "PROJECT_TYPE": "basic",
        "LICENSE_TEXT": "This project is licensed under the MIT License - see the LICENSE file for details."
    }


def copy_template_file(template_path: str, dest_path: str, variables: Dict[str, Any]) -> None:
    """
    Copy a template file to destination, processing variables.

    Args:
        template_path: Path to the template file
        dest_path: Destination path for the processed file
        variables: Template variables to substitute
    """
    # Ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    # Read template content
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Process template variables
    processed_content = substitute_template_variables(template_content, variables)

    # Write processed content to destination
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)


def copy_template_directory(template_dir: str, dest_dir: str, variables: Dict[str, Any]) -> None:
    """
    Copy entire template directory structure, processing all template files.

    Args:
        template_dir: Source template directory
        dest_dir: Destination directory
        variables: Template variables to substitute
    """
    for root, dirs, files in os.walk(template_dir):
        # Calculate relative path from template root
        rel_path = os.path.relpath(root, template_dir)

        # Calculate destination directory
        if rel_path == '.':
            dest_root = dest_dir
        else:
            dest_root = os.path.join(dest_dir, rel_path)

        # Ensure destination directory exists
        os.makedirs(dest_root, exist_ok=True)

        # Process each file
        for file in files:
            src_file_path = os.path.join(root, file)

            # Determine destination filename (remove .template extension if present)
            if file.endswith('.template'):
                dest_filename = file[:-9]  # Remove .template extension

                # Special handling for gitignore files
                if dest_filename == 'gitignore':
                    dest_filename = '.gitignore'
                # Special handling for other dotfiles
                elif dest_filename.startswith('dot_'):
                    dest_filename = '.' + dest_filename[4:]
            else:
                dest_filename = file

            dest_file_path = os.path.join(dest_root, dest_filename)

            # Process template file
            copy_template_file(src_file_path, dest_file_path, variables)


def create_directory_structure(base_path: str, directories: list) -> None:
    """
    Create directory structure.

    Args:
        base_path: Base directory path
        directories: List of directory paths to create
    """
    for directory in directories:
        full_path = os.path.join(base_path, directory)
        os.makedirs(full_path, exist_ok=True)


def save_project_config(project_path: str, variables: Dict[str, Any]) -> None:
    """
    Save project configuration to .project-config.json

    Args:
        project_path: Path to the project directory
        variables: Project variables to save
    """
    config_path = os.path.join(project_path, '.project-config.json')

    config_data = {
        "projectName": variables.get("PROJECT_NAME"),
        "projectDescription": variables.get("PROJECT_DESCRIPTION"),
        "author": {
            "name": variables.get("AUTHOR_NAME"),
            "email": variables.get("AUTHOR_EMAIL")
        },
        "createdAt": variables.get("CREATION_DATE"),
        "projectType": variables.get("PROJECT_TYPE", "basic"),
        "version": "1.0.0",
        "configuration": {
            "structure": {
                "srcDir": "src",
                "docsDir": "docs",
                "testsDir": "tests"
            },
            "tools": {
                "versionControl": "git",
                "projectHelper": "claude-code-project-helper"
            }
        },
        "metadata": {
            "generator": "claude-code-project-helper",
            "generatorVersion": "1.0.0",
            "template": "basic"
        }
    }

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2)


def validate_project_name(name: str) -> bool:
    """
    Validate project name.

    Args:
        name: Project name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name or not name.strip():
        return False

    # Check for invalid characters
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in name:
            return False

    return True


def get_gitignore_patterns(project_type: str = "basic") -> str:
    """
    Get appropriate .gitignore patterns for project type.

    Args:
        project_type: Type of project

    Returns:
        .gitignore content
    """
    base_patterns = """# General
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Temporary files
*.tmp
*.temp
*.log
*.cache

# Build artifacts
build/
dist/
*.o
*.so
*.dylib
*.dll

# Environment
.env
.env.local
.env.*.local

# Archives
*.tar.gz
*.zip
*.rar

# System
*.pid
*.seed
*.pid.lock

# Project specific
# Add your project-specific ignore patterns here
"""

    return base_patterns


if __name__ == "__main__":
    # Test the template utilities
    test_vars = get_default_variables("test-project", "A test project", "Test Author", "test@example.com")
    print("Default variables:", json.dumps(test_vars, indent=2))

    # Test template substitution
    template_text = "Project: {{PROJECT_NAME}} by {{AUTHOR_NAME}}"
    result = substitute_template_variables(template_text, test_vars)
    print("Template result:", result)