"""Interactive REPL mode for CLI Todo Application.

This module provides an interactive command-line interface for todo app.
"""

import shlex
import sys

from src.cli import commands
from src.colors import success, error, info, warning, bold, highlight


class InteractiveREPL:
    """Interactive Read-Eval-Print Loop for CLI Todo Application."""

    def __init__(self):
        """Initialize REPL."""
        self.running = True

    def print_help(self):
        """Print help message for interactive mode."""
        print("\n" + highlight("="*60))
        print(highlight("📝  CLI Todo Application - Interactive Mode"))
        print(highlight("="*60) + "\n")
        print(bold("Commands:"))
        print(f"  {info('add')} <title> {bold('--description')} <desc>  - Add a new task")
        print(f"  {info('list')}                              - List all tasks")
        print(f"  {info('update')} <id> {bold('--title')} <title>       - Update a task")
        print(f"             {bold('--description')} <desc>")
        print(f"  {info('complete')} <id>                       - Mark task as complete")
        print(f"  {info('incomplete')} <id>                     - Mark task as incomplete")
        print(f"  {info('delete')} <id>                         - Delete a task")
        print(f"  {info('help')}                                - Show this help")
        print(f"  {warning('exit')} / {warning('quit')}                        - Exit\n")

    def execute_add(self, args: list):
        """Execute add command.

        Args:
            args: List of arguments.
        """
        if len(args) == 0:
            print(error("✗ Error: Title is required for add command"))
            print(info("Usage: add <title> --description <desc>"))
            return

        title = args[0]

        # Check for --description flag
        description = ''
        if "--description" in args:
            idx = args.index("--description")
            if idx + 1 < len(args):
                description = ' '.join(args[idx + 1:])

        return commands.handle_add(title, description)

    def execute_list(self, args: list):
        """Execute list command.

        Args:
            args: List of arguments (ignored).
        """
        return commands.handle_list()

    def execute_update(self, args: list):
        """Execute update command.

        Args:
            args: List of arguments.
        """
        if len(args) == 0:
            print(error("✗ Error: Task ID is required for update command"))
            print(info("Usage: update <id> --title <title> --description <desc>"))
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(error(f"✗ Error: Invalid task ID: {args[0]}"))
            return

        # Check for --title flag
        title = None
        if "--title" in args:
            idx = args.index("--title")
            if idx + 1 < len(args):
                title = args[idx + 1]

        # Check for --description flag
        description = None
        if "--description" in args:
            idx = args.index("--description")
            if idx + 1 < len(args):
                description = args[idx + 1]

        if title is None and description is None:
            print(error("✗ Error: At least one of --title or --description must be provided"))
            return

        return commands.handle_update(task_id, title, description)

    def execute_complete(self, args: list):
        """Execute complete command.

        Args:
            args: List of arguments [id].
        """
        if len(args) == 0:
            print(error("✗ Error: Task ID is required for complete command"))
            print(info("Usage: complete <id>"))
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(error(f"✗ Error: Invalid task ID: {args[0]}"))
            return

        return commands.handle_complete(task_id)

    def execute_incomplete(self, args: list):
        """Execute incomplete command.

        Args:
            args: List of arguments [id].
        """
        if len(args) == 0:
            print(error("✗ Error: Task ID is required for incomplete command"))
            print(info("Usage: incomplete <id>"))
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(error(f"✗ Error: Invalid task ID: {args[0]}"))
            return

        return commands.handle_incomplete(task_id)

    def execute_delete(self, args: list):
        """Execute delete command.

        Args:
            args: List of arguments [id].
        """
        if len(args) == 0:
            print(error("✗ Error: Task ID is required for delete command"))
            print(info("Usage: delete <id>"))
            return

        try:
            task_id = int(args[0])
        except ValueError:
            print(error(f"✗ Error: Invalid task ID: {args[0]}"))
            return

        return commands.handle_delete(task_id)

    def process_input(self, input_str: str):
        """Process a single user input.

        Args:
            input_str: Raw user input string.
        """
        # Remove leading/trailing whitespace
        input_str = input_str.strip()

        if not input_str:
            return

        # Use shlex to handle quoted strings properly
        parts = shlex.split(input_str)

        if not parts:
            return

        # First part is command
        command = parts[0].lower()
        args = parts[1:]

        # Handle exit commands
        if command in ('exit', 'quit', 'q'):
            print(success("\n👋 Goodbye!"))
            self.running = False
            return

        # Handle help command
        if command == 'help':
            self.print_help()
            return

        # Route to appropriate command
        if command == 'add':
            self.execute_add(args)
        elif command == 'list':
            self.execute_list(args)
        elif command == 'update':
            self.execute_update(args)
        elif command == 'complete':
            self.execute_complete(args)
        elif command == 'incomplete':
            self.execute_incomplete(args)
        elif command == 'delete':
            self.execute_delete(args)
        else:
            print(error(f"✗ Error: Unknown command '{command}'"))
            print(info("Type 'help' for available commands"))

    def run(self):
        """Run to interactive REPL loop."""
        self.print_help()

        while self.running:
            try:
                user_input = input("\n> ").strip()

                if not user_input:
                    continue

                self.process_input(user_input)

            except KeyboardInterrupt:
                print(warning("\n\n⚠ Interrupted. Type 'exit' to quit or press Ctrl+C again."))
            except EOFError:
                print(success("\n\n👋 Goodbye!"))
                self.running = False
            except Exception as e:
                print(error(f"\n✗ Unexpected error: {e}"))
                print(info("Type 'help' for available commands"))


def main():
    """Main entry point for REPL mode."""
    repl = InteractiveREPL()
    repl.run()


if __name__ == "__main__":
    main()
