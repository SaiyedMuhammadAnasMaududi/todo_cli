#!/usr/bin/env python3
"""CLI Todo Application - Entry Point.

A command-line todo application for managing tasks with file-based JSON persistence.
"""

import argparse
import sys
from pathlib import Path

from src.cli import commands


def main() -> int:
    """Main entry point for CLI Todo Application.

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    # Check if running interactive mode (no arguments)
    if len(sys.argv) == 1:
        # No arguments - run interactive REPL mode
        from src.repl import main as repl_main
        repl_main()
        return 0

    parser = argparse.ArgumentParser(
        prog='todo-cli',
        description='CLI Todo Application - Manage your tasks from the command line.',
        epilog='Exit codes: 0=success, 1=validation/task not found, 2=I/O error'
    )

    # Create subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        required=True
    )

    # Add command
    add_parser = subparsers.add_parser(
        'add',
        help='Add a new task'
    )
    add_parser.add_argument(
        '--title',
        required=True,
        help='Task title (required, max 200 characters)'
    )
    add_parser.add_argument(
        '--description',
        default='',
        help='Task description (optional, max 1000 characters)'
    )

    # List command
    list_parser = subparsers.add_parser(
        'list',
        help='List all tasks'
    )

    # Update command
    update_parser = subparsers.add_parser(
        'update',
        help='Update a task'
    )
    update_parser.add_argument(
        '--id',
        required=True,
        type=int,
        help='Task ID to update'
    )
    update_parser.add_argument(
        '--title',
        help='New task title'
    )
    update_parser.add_argument(
        '--description',
        help='New task description'
    )

    # Delete command
    delete_parser = subparsers.add_parser(
        'delete',
        help='Delete a task'
    )
    delete_parser.add_argument(
        '--id',
        required=True,
        type=int,
        help='Task ID to delete'
    )

    # Complete command
    complete_parser = subparsers.add_parser(
        'complete',
        help='Mark task as complete'
    )
    complete_parser.add_argument(
        '--id',
        required=True,
        type=int,
        help='Task ID to mark complete'
    )

    # Incomplete command
    incomplete_parser = subparsers.add_parser(
        'incomplete',
        help='Mark task as incomplete'
    )
    incomplete_parser.add_argument(
        '--id',
        required=True,
        type=int,
        help='Task ID to mark incomplete'
    )

    # Parse arguments
    args = parser.parse_args()

    # Route to appropriate handler
    if args.command == 'add':
        return commands.handle_add(args.title, args.description)
    elif args.command == 'list':
        return commands.handle_list()
    elif args.command == 'update':
        return commands.handle_update(args.id, args.title, args.description)
    elif args.command == 'delete':
        return commands.handle_delete(args.id)
    elif args.command == 'complete':
        return commands.handle_complete(args.id)
    elif args.command == 'incomplete':
        return commands.handle_incomplete(args.id)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
