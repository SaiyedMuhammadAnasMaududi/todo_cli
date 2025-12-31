"""Command handlers for CLI Todo Application.

This module implements all CLI command handlers for task management.
"""

import sys
from typing import Optional

from src.services.task_service import (
    TaskService,
    TaskNotFoundError,
    ValidationError
)
from src.services.storage import CorruptedDataError, PermissionError, StorageError
from src.colors import success, error, info, warning, bold, highlight


class CommandHandler:
    """Base class for command handlers."""

    def __init__(self, service: TaskService):
        """Initialize command handler.

        Args:
            service: TaskService instance for task operations.
        """
        self.service = service

    def execute(self) -> int:
        """Execute command.

        Returns:
            int: Exit code (0=success, 1=validation/not found, 2=I/O error).
        """
        raise NotImplementedError("Subclasses must implement execute()")


def handle_add(title: Optional[str] = None,
             description: Optional[str] = None) -> int:
    """Handle 'add' command.

    Args:
        title: Task title (required).
        description: Task description (optional).

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    try:
        # Validate required title
        if title is None:
            print("Error: --title is required for add command")
            return 1

        # Validate title (non-empty, max 200 chars, no whitespace-only)
        if not title.strip():
            print("Error: Title cannot be empty or whitespace")
            return 1
        if len(title) > 200:
            print("Error: Title must be 200 characters or less")
            return 1

        # Validate description (max 1000 chars)
        if description is not None and len(description) > 1000:
            print("Error: Description must be 1000 characters or less")
            return 1

        # Create service and add task
        service = TaskService()
        task = service.add_task(title, description or "")

        # Success output
        print(success("✓ Task created successfully!"))
        print(f"{bold('ID:')} {info(str(task.id))}")
        print(f"{bold('Title:')} {task.title}")
        if task.description:
            print(f"{bold('Description:')} {task.description}")
        status_text = success("complete") if task.complete else warning("incomplete")
        print(f"{bold('Status:')} {status_text}")

        return 0

    except ValidationError as e:
        print(error(f"✗ Error: {e}"))
        return 1
    except PermissionError as e:
        print(error(f"✗ Error: {e}"))
        return 2
    except StorageError as e:
        print(error(f"✗ Error: Failed to save task: {e}"))
        return 2


def handle_list() -> int:
    """Handle 'list' command.

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    try:
        service = TaskService()
        tasks = service.list_all()

        if not tasks:
            print(info("ℹ No tasks found. Use 'add' command to create a task."))
            return 0

        print(highlight(f"\n📋 Tasks ({len(tasks)} total):\n"))

        for task in tasks:
            if task.complete:
                status = success("✓ complete")
            else:
                status = warning("⏳ incomplete")

            print(f"{bold('ID:')} {info(str(task.id))}  {status}  {task.title}")
            if task.description:
                print(f"    {bold('Description:')} {task.description}")
            print()

        return 0

    except CorruptedDataError as e:
        print(warning(f"⚠ Warning: Data file corrupted. Starting with empty task list."))
        # Continue with empty list
        return 0
    except PermissionError as e:
        print(error(f"✗ Error: {e}"))
        return 2
    except StorageError as e:
        print(error(f"✗ Error: Cannot read tasks: {e}"))
        return 2


def handle_update(task_id: Optional[int] = None,
                  title: Optional[str] = None,
                  description: Optional[str] = None) -> int:
    """Handle 'update' command.

    Args:
        task_id: Task ID to update (required).
        title: New title (optional).
        description: New description (optional).

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    try:
        # Validate required task_id
        if task_id is None:
            print("Error: --id is required for update command")
            return 1

        # Validate at least one field to update
        if title is None and description is None:
            print("Error: At least one of --title or --description must be provided")
            return 1

        # Validate title if provided
        if title is not None:
            if not title.strip():
                print("Error: Title cannot be empty or whitespace")
                return 1
            if len(title) > 200:
                print("Error: Title must be 200 characters or less")
                return 1

        # Validate description if provided
        if description is not None and len(description) > 1000:
            print("Error: Description must be 1000 characters or less")
            return 1

        # Create service and update task
        service = TaskService()
        task = service.update_task(task_id, title, description)

        # Success output
        print(success("✓ Task updated successfully!"))
        print(f"{bold('ID:')} {info(str(task.id))}")
        print(f"{bold('Title:')} {task.title}")
        if task.description:
            print(f"{bold('Description:')} {task.description}")
        status_text = success("complete") if task.complete else warning("incomplete")
        print(f"{bold('Status:')} {status_text}")

        return 0

    except TaskNotFoundError as e:
        # Get valid IDs for helpful error message
        valid_ids = service.get_valid_ids() if 'service' in locals() else []
        if valid_ids:
            print(error(f"✗ Error: {e}. Valid IDs: {', '.join(map(str, valid_ids))}"))
        else:
            print(error(f"✗ Error: {e}"))
        return 1
    except ValidationError as e:
        print(error(f"✗ Error: {e}"))
        return 1
    except PermissionError as e:
        print(error(f"✗ Error: {e}"))
        return 2
    except StorageError as e:
        print(error(f"✗ Error: Cannot update task. {e}"))
        return 2


def handle_complete(task_id: Optional[int] = None) -> int:
    """Handle 'complete' command.

    Args:
        task_id: Task ID to mark complete (required).

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    try:
        # Validate required task_id
        if task_id is None:
            print("Error: --id is required for complete command")
            return 1

        # Create service and mark task complete
        service = TaskService()
        task = service.toggle_complete(task_id, True)

        # Success output
        print(success("✓ Task marked as complete!"))
        print(f"{bold('ID:')} {info(str(task.id))}")
        print(f"{bold('Title:')} {task.title}")

        return 0

    except TaskNotFoundError as e:
        # Get valid IDs for helpful error message
        valid_ids = service.get_valid_ids() if 'service' in locals() else []
        if valid_ids:
            print(error(f"✗ Error: {e}. Valid IDs: {', '.join(map(str, valid_ids))}"))
        else:
            print(error(f"✗ Error: {e}"))
        return 1
    except ValidationError as e:
        print(error(f"✗ Error: {e}"))
        return 1
    except PermissionError as e:
        print(error(f"✗ Error: {e}"))
        return 2
    except StorageError as e:
        print(error(f"✗ Error: Cannot update task. {e}"))
        return 2


def handle_incomplete(task_id: Optional[int] = None) -> int:
    """Handle 'incomplete' command.

    Args:
        task_id: Task ID to mark incomplete (required).

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    try:
        # Validate required task_id
        if task_id is None:
            print(error("✗ Error: --id is required for incomplete command"))
            return 1

        # Create service and mark task incomplete
        service = TaskService()
        task = service.toggle_complete(task_id, False)

        # Success output
        print(success("✓ Task marked as incomplete!"))
        print(f"{bold('ID:')} {info(str(task.id))}")
        print(f"{bold('Title:')} {task.title}")

        return 0

    except TaskNotFoundError as e:
        # Get valid IDs for helpful error message
        valid_ids = service.get_valid_ids() if 'service' in locals() else []
        if valid_ids:
            print(error(f"✗ Error: {e}. Valid IDs: {', '.join(map(str, valid_ids))}"))
        else:
            print(error(f"✗ Error: {e}"))
        return 1
    except ValidationError as e:
        print(error(f"✗ Error: {e}"))
        return 1
    except PermissionError as e:
        print(error(f"✗ Error: {e}"))
        return 2
    except StorageError as e:
        print(error(f"✗ Error: Cannot update task. {e}"))
        return 2


def handle_delete(task_id: Optional[int] = None) -> int:
    """Handle 'delete' command.

    Args:
        task_id: Task ID to delete (required).

    Returns:
        int: Exit code (0=success, 1=validation/not found, 2=I/O error).
    """
    try:
        # Validate required task_id
        if task_id is None:
            print(error("✗ Error: --id is required for delete command"))
            return 1

        # Create service and delete task
        service = TaskService()
        task = service.delete_task(task_id)

        # Success output
        print(success("✓ Task deleted successfully!"))
        print(f"{bold('ID:')} {info(str(task.id))}")
        print(f"{bold('Title:')} {task.title}")

        return 0

    except TaskNotFoundError as e:
        # Get valid IDs for helpful error message
        valid_ids = service.get_valid_ids() if 'service' in locals() else []
        if valid_ids:
            print(error(f"✗ Error: {e}. Valid IDs: {', '.join(map(str, valid_ids))}"))
        else:
            print(error(f"✗ Error: {e}"))
        return 1
    except ValidationError as e:
        print(error(f"✗ Error: {e}"))
        return 1
    except PermissionError as e:
        print(error(f"✗ Error: {e}"))
        return 2
    except StorageError as e:
        print(error(f"✗ Error: Cannot delete task. {e}"))
        return 2
