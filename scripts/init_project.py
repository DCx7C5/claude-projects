#!/usr/bin/env python3
"""
Project initialization script for Claude Code Project Helper

This script handles the creation of new projects with proper structure,
templates, and Git initialization.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

# Add the parent directory to the path to import template_utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from template_utils import (
    get_default_variables,
    copy_template_directory,
    create_directory_structure,
    save_project_config,
    validate_project_name,
    get_gitignore_patterns
)


def run_command(command: list, cwd: str = None, capture_output: bool = True) -> tuple:
    """
    Run a shell command and return the result.

    Args:
        command: List of command parts
        cwd: Working directory for the command
        capture_output: Whether to capture command output

    Returns:
        Tuple of (success: bool, output: str, error: str)
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=False
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def init_git_repository(project_path: str) -> bool:
    """
    Initialize Git repository and create initial commit.

    Args:
        project_path: Path to the project directory

    Returns:
        True if successful, False otherwise
    """
    print("Initializing Git repository...")

    # Initialize git repository
    success, output, error = run_command(['git', 'init'], cwd=project_path)
    if not success:
        print(f"Warning: Failed to initialize git repository: {error}")
        return False

    # Add all files
    success, output, error = run_command(['git', 'add', '.'], cwd=project_path)
    if not success:
        print(f"Warning: Failed to add files to git: {error}")
        return False

    # Create initial commit
    commit_message = "Initial commit - project created with Claude Code Project Helper"
    success, output, error = run_command([
        'git', 'commit', '-m', commit_message
    ], cwd=project_path)
    if not success:
        print(f"Warning: Failed to create initial commit: {error}")
        return False

    print("✓ Git repository initialized with initial commit")
    return True


def create_project(
    project_name: str,
    project_path: str,
    project_description: str = "",
    author_name: str = "",
    author_email: str = "",
    template_type: str = "basic",
    init_git: bool = True
) -> bool:
    """
    Create a new project with the specified configuration.

    Args:
        project_name: Name of the project
        project_path: Path where the project should be created
        project_description: Description of the project
        author_name: Author's name
        author_email: Author's email
        template_type: Type of template to use
        init_git: Whether to initialize Git repository

    Returns:
        True if successful, False otherwise
    """
    # Validate project name
    if not validate_project_name(project_name):
        print(f"Error: Invalid project name '{project_name}'")
        return False

    # Check if target directory already exists
    if os.path.exists(project_path):
        print(f"Error: Directory '{project_path}' already exists")
        return False

    print(f"Creating project '{project_name}' at '{project_path}'...")

    try:
        # Create project directory
        os.makedirs(project_path, exist_ok=True)

        # Generate template variables
        variables = get_default_variables(
            project_name=project_name,
            project_description=project_description,
            author_name=author_name,
            author_email=author_email
        )

        # Find template directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        template_dir = os.path.join(project_root, 'skills', 'project-init', 'templates', template_type)

        if not os.path.exists(template_dir):
            print(f"Error: Template '{template_type}' not found at {template_dir}")
            return False

        # Copy template files
        print("Copying template files...")
        copy_template_directory(template_dir, project_path, variables)

        # Create additional directories
        additional_dirs = ['src', 'docs', 'tests']
        create_directory_structure(project_path, additional_dirs)

        # Create .gitignore if it doesn't exist from template
        gitignore_path = os.path.join(project_path, '.gitignore')
        if not os.path.exists(gitignore_path):
            gitignore_content = get_gitignore_patterns(template_type)
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)

        # Save project configuration
        save_project_config(project_path, variables)

        print("✓ Project structure created")

        # Initialize Git repository
        if init_git:
            init_git_repository(project_path)

        print(f"\\n🎉 Project '{project_name}' created successfully!")
        print(f"📁 Location: {project_path}")
        print(f"🚀 Next steps:")
        print(f"   cd {project_path}")
        print(f"   # Start developing your project!")

        return True

    except Exception as e:
        print(f"Error creating project: {e}")
        # Clean up on failure
        if os.path.exists(project_path):
            try:
                os.rmdir(project_path)
            except:
                pass
        return False


def interactive_setup() -> Dict[str, Any]:
    """
    Interactive project setup with user prompts.

    Returns:
        Dictionary with project configuration
    """
    print("🚀 Claude Code Project Helper - Interactive Setup\\n")

    # Get project name
    while True:
        project_name = input("Project name: ").strip()
        if validate_project_name(project_name):
            break
        print("Please enter a valid project name (no special characters)")

    # Get project description
    project_description = input(f"Project description (optional): ").strip()

    # Get author information
    author_name = input("Author name (optional): ").strip()
    author_email = input("Author email (optional): ").strip()

    # Get project location
    default_path = os.path.join(os.getcwd(), project_name)
    project_path = input(f"Project location [{default_path}]: ").strip()
    if not project_path:
        project_path = default_path

    # Git initialization
    init_git_input = input("Initialize Git repository? [Y/n]: ").strip().lower()
    init_git = init_git_input != 'n'

    return {
        'project_name': project_name,
        'project_path': project_path,
        'project_description': project_description,
        'author_name': author_name,
        'author_email': author_email,
        'init_git': init_git
    }


def main():
    """Main function for project initialization script."""
    parser = argparse.ArgumentParser(
        description="Initialize a new project with Claude Code Project Helper"
    )
    parser.add_argument(
        'project_name',
        nargs='?',
        help='Name of the project to create'
    )
    parser.add_argument(
        '-d', '--description',
        help='Project description'
    )
    parser.add_argument(
        '-p', '--path',
        help='Path where the project should be created'
    )
    parser.add_argument(
        '--author-name',
        help='Author name'
    )
    parser.add_argument(
        '--author-email',
        help='Author email'
    )
    parser.add_argument(
        '-t', '--template',
        default='basic',
        help='Template type to use (default: basic)'
    )
    parser.add_argument(
        '--no-git',
        action='store_true',
        help='Skip Git repository initialization'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Interactive setup mode'
    )

    args = parser.parse_args()

    # Interactive mode
    if args.interactive or not args.project_name:
        config = interactive_setup()
        success = create_project(**config)
        sys.exit(0 if success else 1)

    # Command line mode
    project_path = args.path or os.path.join(os.getcwd(), args.project_name)

    success = create_project(
        project_name=args.project_name,
        project_path=project_path,
        project_description=args.description or "",
        author_name=args.author_name or "",
        author_email=args.author_email or "",
        template_type=args.template,
        init_git=not args.no_git
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()